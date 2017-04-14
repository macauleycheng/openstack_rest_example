import json

def getUserId(conn, token, who='admin'):
  reply = conn.listUsers(token)
  if not (reply.status_code == 200 or reply.status_code==203):
    print "line 6, status code %d"%reply.status_code
    return None

  reply_content = json.loads(reply.content)
  all_users=reply_content['users']

  for i in range(len(all_users)):
  	user = all_users[i]

  	if user['username'] in who:
  		return user['id']

def getRoleId(conn, token, who = 'admin'):
    reply = conn.listRoles(token)

    if not (reply.status_code == 200 or reply.status_code==203):
      print "line 22, status code %d"%reply.status_code
      return None

    reply_content = json.loads(reply.content)
    all_roles=reply_content['roles']

    for i in range(len(all_roles)):
      role = all_roles[i]

      if role['name'] in who:
        return role['id']

