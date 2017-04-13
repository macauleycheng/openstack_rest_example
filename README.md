curl -i -g -X GET -H "X-Auth-Token:70b5ee2ddf2141d49a4fb81084fb2310" -H 'Content-Type: application/json'  http://192.168.200.71:8774/v2.1/os-hosts/cmp

curl -i -X POST http://192.168.200.71:35357/v2.0/tokens -H "Content-Type: application/json" -H "User-Agent: python-keystoneclient" -d '{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "password"}}}'
