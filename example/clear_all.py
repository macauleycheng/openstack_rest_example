import sys
import os
import simplejson as json

#This file will search all tenant and create one network and one vm on it
#the image UUId shall be prepared manually.


sys.path.append(os.path.abspath('../'))
from lib import wrap
from lib import tools

def delete_all_vms(token, tenant_id):
  print "delete all VMs"
  reply = conn.listServers(token, tenant_id)
  if reply.status_code != 200:
      print reply.status_code
      os._exit(1)

  reply_content = json.loads(reply.content)  
  all_servers = reply_content['servers']

  for i in range(len(all_servers)):
      server = all_servers[i]
      print "delete VM UUID "+ server['id']
      conn.destroyServers(token, server['id'], tenant_id)
  print "finished delete all VMs"

def delete_all_network(token, tenant_id):
  print "delete all networks"
  reply = conn.listNetworks(token)
  if reply.status_code != 200:
      os._exit(1)

  reply_content = json.loads(reply.content)   
  all_networks=reply_content['networks']
  
  for i in range(len(all_networks)):
    network = all_networks[i]
    if network['tenant_id'] not in tenant_id:
        continue

    print "delete network UUID " + network['id'] + ", name=" + network['name']
    reply = conn.destroyNetwork(token, network['id'])

    if reply.status_code != 204:
      print "line 65 exist status code %d"%reply.status_code      
      os._exit(1)
      
  print "finished delete all networks"

def delete_all_routers(token, tenant_id):
  print "delete all routers"
  reply = conn.listRouters(token)
  if reply.status_code != 200:
      os._exit(1)  

  reply_content = json.loads(reply.content)     
  all_routers=reply_content['routers']  

  for i in range(len(all_routers)):
    router = all_routers[i]
    if router['tenant_id'] not in tenant_id:
        continue
    
    print "deletea all router interfaces"
    reply = conn.listPorts(token)
    if reply.status_code != 200:    
      print "list port fail, exist status code %d"%reply.status_code      
      os._exit(1)
    reply_content = json.loads(reply.content)
    all_ports = reply_content['ports']

    for i in range(len(all_ports)):
      port = all_ports[i]

      if  'network' in port['device_owner']:
          reply = conn.delRouterInterface(token, router['id'], port_uuid=port['id'])
          if reply.status_code != 200:    
            print "delete port fail, exist status code %d"%reply.status_code      
            os._exit(1)

    print "delete router UUID " + router['id'] + ", name=" + router['name']
    reply = conn.destroyRouter(token, router['id'])

    if reply.status_code != 204:
      print "delete router fail, exist status code %d"%reply.status_code      
      os._exit(1)

  print "finished delete all routers"



if __name__ == '__main__':
  ip_addr = raw_input("Input target Ip address? ")
  if tools.validateIPaddr(str(ip_addr) == False):
    print "Fail to connect to target IP"
    os_exit(1)

  conn = wrap(ip_addr)
  print "get token"
  reply = conn.getToken()
  reply_content = json.loads(reply.content)
  #print reply_content

  if reply.status_code!=200:
    os._exit(1)

  admin_token = reply_content['access']['token']['id']
  print "token = "+admin_token

  print "list tenants"
  reply = conn.listTenant(admin_token)
  reply_content = json.loads(reply.content)
  #print reply_content

  #crecord all tenant_id
  all_tenants=reply_content['tenants']
  #print all_tenants
  print "Total Tenants "+ str(len(all_tenants))
  #print all_tenants
  for i in range(len(all_tenants)):
    tenant=all_tenants[i]
    if tenant['name'] == 'services':
      continue

    print "tenant id  "+ tenant['id']

    reply = conn.getToken(tenant_uuid=tenant['id'])
    reply_content = json.loads(reply.content)
    if reply.status_code != 200:
      print "get token fail, status code %d"%reply.status_code   
      print "destroy tenant=" + tenant['id'] + ", name="+tenant['name']
      reply = conn.destroyTenant(admin_token, tenant['id'])
      if reply.status_code != 204:
          print "Delete tenant fail, status code %d"%reply.status_code
      else:
        continue
      os._exit(1)

    token = reply_content['access']['token']['id']
    print "token " + token

    delete_all_vms(token, tenant['id'])
    delete_all_routers(token, tenant['id'])
    delete_all_network(token, tenant['id'])

    if tenant['name'] == 'admin':
        continue

    print "destroy tenant=" + tenant['id'] + ", name="+tenant['name']
    reply = conn.destroyTenant(admin_token, tenant['id'])
    if reply.status_code != 204:
      print "Delete tenant fail, status code %d"%reply.status_code      
      os._exit(1)    

    print "Next.........."
