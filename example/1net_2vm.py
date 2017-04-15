import sys
import os
import simplejson as json

#This file will search all tenant and create one network and one vm on it
#the image UUId shall be prepared manually.


sys.path.append(os.path.abspath('../'))
from lib import wrap
from lib import tools

#user shall change this according to his openstack
image_ref = 'bb9429e5-448b-478a-bf7d-b577bf2b195b'

def patch_work(token, tenant_id):
  print "create network"
  reply = conn.createNetwork(token, tenant_id, name = 'test')
  if reply.status_code !=201:    
    os._exit(1)

  reply_content = json.loads(reply.content)
  network_uuid = reply_content['network']['id']
  print "network UUID "+ network_uuid

  print "create subnet"
  reply = conn.createSubnet(token, tenant_id, network_uuid, 4, "1.1.1.0/24")
  if reply.status_code !=201:
    os._exit(1)

  reply_content = json.loads(reply.content)
  subnet_uuid = reply_content['subnet']['id']
  print "subnet UUID "+subnet_uuid

  print "create VM1"
  reply = conn.createServer(token = token,
                            project_uuid=tenant_id,
                            name = 'vm1',
                            image_ref=image_ref,
                            network=network_uuid)

  if reply.status_code != 202:
    os._exit(1)

  reply_content = json.loads(reply.content)
  vm_uuid = reply_content['server']['id']
  print "vm UUID " + vm_uuid



  print "create VM2"
  reply = conn.createServer(token = token,
                            project_uuid=tenant_id,
                            name = 'vm2',
                            image_ref=image_ref,
                            network=network_uuid)

  if reply.status_code != 202:
    os._exit(1)

  reply_content = json.loads(reply.content)
  vm_uuid = reply_content['server']['id']
  print "vm2 UUID " + vm_uuid





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

  token = reply_content['access']['token']['id']
  print "token = "+token

  print "list tenants"
  reply = conn.listTenant(token)
  reply_content = json.loads(reply.content)
  #print reply_content

  #crecord all tenant_id
  all_tenants=reply_content['tenants']
  #print all_tenants
  print "Total Tenants "+ str(len(all_tenants))

  for i in range(len(all_tenants)):
    tenant=all_tenants[i]
    if tenant['name'] == 'services':
      continue
    print "tenant id  "+ tenant['id']
    reply = conn.getToken(tenant_uuid=tenant['id'])
    reply_content = json.loads(reply.content)
    if reply.status_code != 200:
      os._exit(1)
    token = reply_content['access']['token']['id']
    print "token " + token
    patch_work(token, tenant['id'])

