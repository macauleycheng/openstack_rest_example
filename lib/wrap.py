#!/usr/bin/python
import requests
import json
import urllib2

headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
patchheaders = {'Conent-Type':'application/json-patch+json'}

class wrap():
    httpSuccessCodes = [200, 201, 202, 204]
    def  __init__ (self, ip, timeout=10):
        self.ip = ip
        self.timeout = timeout
        self.keystone = 'http://%s:%s/'%(ip,str(35357))
        self.networks = 'http://%s:%s/'%(ip, str(9696))
        self.nova = 'http://%s:%s/v2/'%(ip, str(8774))

    def getToken(self, tenant_uuid=None, tenant_name="admin", user_name="admin", password="admin"):

        if tenant_uuid == None:
            obj = {
                  "auth":{
                      "tenantName":tenant_name,
                      "passwordCredentials":{
                                             "username":user_name,
                                             "password":password
                                            }
                         }
                  }
        else:
            obj = {
                  "auth":{
                      "tenantId":tenant_uuid,
                      "passwordCredentials":{
                                             "username":user_name,
                                             "password":password
                                            }
                         }
                  }

        reqUrl =  self.keystone + 'v2.0/tokens'
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)

        return r

    #normal response is 200
    def createTenant(self, token, name, description="", enabled=True):
        obj = {
               "tenant": {
                          "name": name,
                          "description": description,
                          "enabled": enabled
                         }
        }      

        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/tenants'
        r = requests.post(reqUrl, data=json.dumps(obj),headers=headers, timeout=self.timeout)
        
        return r

    #normal response is 204
    def destroyTenant(self, token, project_uuid):

        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/tenants/'+ project_uuid
        r = requests.delete(reqUrl,headers=headers, timeout=self.timeout)
        
        return r 

    def addTenantUser(self, token, project_uuid, user_uuid, role_uuid):
        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/tenants/'+ project_uuid+"/users/"+user_uuid+'/roles/OS-KSADM/'+role_uuid
        r = requests.put(reqUrl,headers=headers, timeout=self.timeout)

        return r

    def listTenant(self, token):
        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/tenants'
        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)

        return r

    #Normal response codes: 201
    def createUser(self, token, project_uuid, user_name='demo', password="password", email="new-user@example.com"):
        obj={
                "user": {
                    "email": email,
                    "password": password,
                    "enabled": True,
                    "name": user_name,
                    "tenantId": project_uuid
                }
            }
        
        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)

        return r

    def listUsers(self, token):
        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/users'
        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)

        return r      

    def listRoles(self, token):
        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/OS-KSADM/roles'

        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)

        return r      
    #Normal response codes: 201
    def createRouter(self, token, project_uuid, name="r1", ext_net_uuid=None, ext_ip='', ext_subnet_uuid=''):
        if ext_net_uuid == None:
          obj = {
                "router": {
                    "name": name,
                    "tenant_id": project_uuid,
                    #"project_id": project_uuid,
                    "admin_state_up": True
                          }
                }
        else:
          obj = {
                "router": {
                    "name": name,
                    "tenant_id": project_uuid,
                    #"project_id": project_uuid,                    
                    "external_gateway_info": {
                        "network_id": ext_net_uuid,
                        "enable_snat": True,
                        "external_fixed_ips": [
                            {
                                "ip_address": ext_ip,
                                "subnet_id": ext_subnet_uuid
                            }
                        ]
                    },
                    "admin_state_up": True
                }
            }            
        reqUrl =  self.networks+ 'v2.0/routers'
        headers['X-Auth-Token']=token

        r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        return r

    #Normal response codes: 204
    def destroyRouter(self, token, r_uuid):
        reqUrl =  self.networks+ 'v2.0/routers/'+r_uuid
        headers['X-Auth-Token']=token

        r = requests.delete(reqUrl, headers=headers, timeout=self.timeout)
        return r      

    #Normal response codes: 200
    def addRouterInterface(self, token, r_uuid, subnet_uuid=None, port_uuid=None):
        if subnet_uuid != None:
          obj = {
                "subnet_id": subnet_uuid
                }
        else:
          obj ={
                "port_id": port_uuid
               }

        reqUrl =  self.networks+ 'v2.0/routers/'+r_uuid+"/add_router_interface"
        headers['X-Auth-Token']=token

        r = requests.put(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        return r

    #Normal response codes: 200
    def delRouterInterface(self, token, r_uuid, subnet_uuid=None, port_uuid=None):
        if subnet_uuid != None:
          obj = {
                "subnet_id": subnet_uuid
                }
        else:
          obj ={
                "port_id": port_uuid
               }

        reqUrl =  self.networks+ 'v2.0/routers/'+r_uuid+"/remove_router_interface"
        headers['X-Auth-Token']=token
        print obj
        r = requests.put(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        return r

    def listRouters(self, token):
        reqUrl =  self.networks+ 'v2.0/routers'
        headers['X-Auth-Token']=token

        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)
        return r

    def listPorts(self, token, filter=None):
        if filter == None:
          reqUrl =  self.networks+ 'v2.0/ports'
        else:
          reqUrl = self.networks + 'v2.0/ports?'+filter

        headers['X-Auth-Token']=token

        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)
        return r        


    #https://developer.openstack.org/api-ref/networking/v2/index.html?expanded=create-network-detail,create-segment-detail,create-subnet-detail#networks
    def createNetwork(self, token, project_uuid, name, spec=None):
        obj = { 
              "network": {
                         "tenant_id": project_uuid,
                         #"project_id": project_uuid,                         
                         "name": name,
                         "admin_state_up": True
                         }

              }
        reqUrl =  self.networks+ 'v2.0/networks'
        headers['X-Auth-Token']=token

        if spec is None:
            r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        else:
            r = requests.post(reqUrl, data=json.dumps(spec), headers=headers, timeout=self.timeout)

        return r

    def destroyNetwork(self, token, network_uuid):
        reqUrl =  self.networks+ 'v2.0/networks/'+network_uuid
        headers['X-Auth-Token']=token

        r = requests.delete(reqUrl, headers=headers, timeout=self.timeout)

        return r        

    def listNetworks(self, token):
        reqUrl =  self.networks+ 'v2.0/networks'
        headers['X-Auth-Token']=token

        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)
        return r

    def createSubnet(self, token, project_uuid, network_uuid, version, cidr, spec=None):
        obj = {
              "subnet": {
                         #"project_id": project_uuid,
                         "tenant_id": project_uuid,
                         "network_id": network_uuid,
                         "ip_version": version,
                         "cidr": cidr,
                         "enable_dhcp": True
                        }
             } 
        headers['X-Auth-Token']=token
        reqUrl =  self.networks+ '/v2.0/subnets'
        if spec is None:
            r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        else:
            r = requests.post(reqUrl, data=json.dumps(spec), headers=headers, timeout=self.timeout)

        return r

    #https://developer.openstack.org/api-ref/compute/?expanded=create-server-detail,add-network-detail
    def createServer(self, token, project_uuid, image_ref, name="default", flavor='1', network='auto', spec=None):
        obj = {
              "server": {
                        "name": name,
                        "imageRef": image_ref,
                        "flavorRef": flavor,
                        "networks": [{"uuid": network}
                                    ]
                        }
             }
        headers['X-Auth-Token']=token
        reqUrl =  self.nova + project_uuid + '/servers'

        if spec is None:
            r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        else:
            r = requests.post(reqUrl, data=json.dumps(spec), headers=headers, timeout=self.timeout)

        return r


    def destroyServers(self, token, server_uuid, project_uuid):
        headers['X-Auth-Token']=token
        reqUrl =  self.nova + project_uuid + '/servers/'+ server_uuid        

        r = requests.delete(reqUrl, headers=headers, timeout=self.timeout)

        return r

    def listServers(self, token, project_uuid):
        reqUrl =  self.nova + project_uuid + '/servers'
        headers['X-Auth-Token']=token

        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)
        return r        
