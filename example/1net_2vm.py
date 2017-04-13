import sys
import os
import simplejson as json

sys.path.append(os.path.abspath('../'))
from lib import wrap

def patch_work(token, tenant_id):
  print "create network"
  reply = conn.createNetwork(token, tenant_id, name = 'test')
  if reply.status_code !=201:
    print "exit, status code " + str(reply.status_code)
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

  print "create VM"
  reply = conn.createServer(token = token,
                            project_uuid=tenant_id,
                            image_ref='bb9429e5-448b-478a-bf7d-b577bf2b195b',
                            network=network_uuid)
  print reply.status_code
  if reply.status_code != 202:
    print reply.content
    os._exit(1)

  reply_content = json.loads(reply.content)
  vm_uuid = reply_content['server']['id']
  print "vm UUID " + vm_uuid


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
  #os._exit(1)
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

