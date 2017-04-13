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



    def listTenant(self, token, tenantName="admin"):
        headers['X-Auth-Token']=token
        reqUrl =  self.keystone + 'v2.0/tenants'
        r = requests.get(reqUrl, headers=headers, timeout=self.timeout)

        return r

    #https://developer.openstack.org/api-ref/networking/v2/index.html?expanded=create-network-detail,create-segment-detail,create-subnet-detail#networks
    def createNetwork(self, token, project_uuid, name, spec=None):
        obj = { 
              "network": {
                         "project_id": project_uuid,
                         "tenant_id": project_uuid,
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

    def createSubnet(self, token, project_uuid, network_uuid, version, cidr, spec=None):
        obj = {
              "subnet": {
                         "project_id": project_uuid,
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
        print reqUrl
        if spec is None:
            r = requests.post(reqUrl, data=json.dumps(obj), headers=headers, timeout=self.timeout)
        else:
            r = requests.post(reqUrl, data=json.dumps(spec), headers=headers, timeout=self.timeout)

        return r


