import sys
import os
import simplejson as json

#This file will search all tenant and create one network and one vm on it
#the image UUId shall be prepared manually.


sys.path.append(os.path.abspath('../'))
from lib import wrap

#user shall change this according to his openstack
image_ref = 'bb9429e5-448b-478a-bf7d-b577bf2b195b'

def patch_work(token, tenant_id):
  print "create network1"
  reply = conn.createNetwork(token, tenant_id, name = 'test')
  if reply.status_code !=201:    
    os._exit(1)

  reply_content = json.loads(reply.content)
  network1_uuid = reply_content['network']['id']
  print "network UUID "+ network1_uuid

  print "create subnet1"
  reply = conn.createSubnet(token, tenant_id, network1_uuid, 4, "1.1.1.0/24")
  if reply.status_code !=201:
    os._exit(1)

  reply_content = json.loads(reply.content)
  subnet1_uuid = reply_content['subnet']['id']
  print "subnet UUID "+subnet1_uuid

  print "create VM1"
  reply = conn.createServer(token = token,
                            project_uuid=tenant_id,
                            name = 'vm1',
                            image_ref=image_ref,
                            network=network1_uuid)

  if reply.status_code != 202:
    os._exit(1)

  reply_content = json.loads(reply.content)
  vm_uuid = reply_content['server']['id']
  print "vm UUID " + vm_uuid

  print "create network2"
  reply = conn.createNetwork(token, tenant_id, name = 'test')
  if reply.status_code !=201:    
    os._exit(1)

  reply_content = json.loads(reply.content)
  network2_uuid = reply_content['network']['id']
  print "network UUID "+ network2_uuid

  print "create subnet2"
  reply = conn.createSubnet(token, tenant_id, network2_uuid, 4, "2.2.2.0/24")
  if reply.status_code !=201:
    os._exit(1)

  reply_content = json.loads(reply.content)
  subnet2_uuid = reply_content['subnet']['id']
  print "subnet UUID "+subnet2_uuid

  print "create VM2"
  reply = conn.createServer(token = token,
                            project_uuid=tenant_id,
                            name = 'vm2',
                            image_ref=image_ref,
                            network=network2_uuid)

  if reply.status_code != 202:
    os._exit(1)

  reply_content = json.loads(reply.content)
  vm_uuid = reply_content['server']['id']
  print "vm2 UUID " + vm_uuid

  print "Create Router and connect to two network"
  reply = conn.createRouter(token, tenant_id)
  if reply.status_code !=201:
    print "line 83, exit status code %d"%reply.status_code    
    os._exit(1)
  reply_content = json.loads(reply.content)
  r_uuid = reply_content['router']['id']

  reply = conn.addRouterInterface(token, r_uuid, subnet1_uuid)
  if reply.status_code !=200:
    print "line 90, exit status code %d"%reply.status_code
    os._exit(1)

  reply = conn.addRouterInterface(token, r_uuid, subnet2_uuid)
  if reply.status_code !=200:
    print "line 95, exit status code %d"%reply.status_code
    os._exit(1)






if __name__ == '__main__':
  conn = wrap('192.168.200.91')
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

