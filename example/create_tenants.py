import sys
import os
import simplejson as json

#This file will search all tenant and create one network and one vm on it
#the image UUId shall be prepared manually.


sys.path.append(os.path.abspath('../'))
from lib import wrap
from lib import tools

#define how many tenant will be crated
Total_Tenant=2
#give the user which want to added into tenant
User_ID_Admin = '3fc5b034f74442378e70483a7475bc09'
Role_Admin = '806aa185fddc4b96975bf37ba0e1855c'


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

  admin_User_ID_Admin = tools.getUserId(conn, token, 'admin')
  if admin_User_ID_Admin != None:
  	User_ID_Admin = admin_User_ID_Admin

  role_admin_id = tools.getRoleId(conn, token, 'admin')
  if role_admin_id != None:
  	Role_Admin = role_admin_id
  

  for i in range(Total_Tenant):
    name = "test_demo"+ str(i)
    reply = conn.createTenant(token, name)
    if reply.status_code != 200:
        print "not normal 200 is %d"%reply.status_code
        os._exit(1)

    reply_content = json.loads(reply.content)

    print "Created Tenant UUID "+ reply_content['tenant']['id']+", name=" + name


    reply = conn.addTenantUser(token, reply_content['tenant']['id'], User_ID_Admin, Role_Admin)
    if reply.status_code != 200:
        print "line 42 +fail status code"+str(reply.status_code)
        os._exit(1)

    reply_content = json.loads(reply.content)
