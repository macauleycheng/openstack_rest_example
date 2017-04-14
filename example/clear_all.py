import sys
import os
import simplejson as json

#This file will search all tenant and create one network and one vm on it
#the image UUId shall be prepared manually.


sys.path.append(os.path.abspath('../'))
from lib import wrap

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
    conn.destroyNetwork(token, network['id'])





if __name__ == '__main__':
  conn = wrap('192.168.200.91')
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
    delete_all_network(token, tenant['id'])

    if tenant['name'] == 'admin':
        continue

    print "destroy tenant=" + tenant['id'] + ", name="+tenant['name']
    reply = conn.destroyTenant(admin_token, tenant['id'])
    if reply.status_code != 204:
      print "Delete tenant fail, status code %d"%reply.status_code      
      os._exit(1)    

    print "Next.........."
