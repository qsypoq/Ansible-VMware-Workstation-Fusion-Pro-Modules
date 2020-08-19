#!/usr/bin/python

import base64
import json
import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: unix_vmware_desktop_adaptersmgmt

short_description: Implement the Network Adapters Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Pro Network Adapters "

options:
    target_vm:
        description:
            - This is the target VM to interact with
        required: true

    action: list || getip || update || create || delete
        description:
            - This is the action we want to do.
        required: true   

    targetIndex: 1
        description:
            - Index's number refering to your network adapter
        required: Only for delete & update

    type: custom || bridged || nat || hostonly
        description:
                - This is the target VMNET to interact with
        required: only for update & create

    vmnet:
        description:
                - This is the target VMNET to interact with
        required: only when type = custom
    
    user: "workstation-api-user"
        description:
            - Your workstation API username
        required: true

    password: "api-password"
        description:
            - Your workstation API password
        required: true

    api_url: "http://127.0.0.1"
        description:
            - Your workstation API URL
        required: false
        default: "http://127.0.0.1"

    api_port: "8697"
        description:
            - Your workstation API PORT
        required: false
        default: "8697"

    validate_certs: "no || yes"
        description:
            - Validate Certificate it HTTPS connection
        required: false

author:
    - Adam Magnier (@qsypoq)  
'''

EXAMPLES = r'''
### Return IP address of VM 42
### API doesn't work with all the NICs setups, need debugging to find the reasons
- name: "Return IP address"
  unix_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "getip"
    user: "workstation-api-user"
    password: "api-password"

### Return all network adapters in VM 42
- name: "Return network adapters"
  unix_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "list"
    user: "workstation-api-user"
    password: "api-password"

### Edit NIC N°1 of VM 42 to assign it a custom type targetting vmnet10
- name: "update NIC N°1 of VM42"
    unix_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "update"
    index: "1"
    type: custom
    vmnet: vmnet10
    user: "workstation-api-user"
    password: "api-password"

### Create NIC N°1 of VM 42 and assign it a custom type targetting vmnet10
- name: "Create NIC N°1 of VM 42"
    unix_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "create"
    type: custom
    vmnet: vmnet10
    user: "workstation-api-user"
    password: "api-password"

### Delete NIC N°1 of VM 42 
- name: "Delete NIC"
    unix_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "delete"
    index: "1"
    user: "workstation-api-user"
    password: "api-password"
'''

RETURN = r'''
### Return the IP adress of VM 42
{
    "ip": "172.20.20.10"
}

### Return all network adapters in VM 42
{
    "nics": [
        {
            "index": 1,
            "macAddress": "00:46:80:23:23:59",
            "type": "custom",
            "vmnet": "vmnet0"
        },
        {
            "index": 2,
            "macAddress": "00:0c:25:50:23:67",
            "type": "custom",
            "vmnet": "vmnet10"
        }
    ],
    "num": 2
}

### Edit NIC N°1 of VM 42 to assign it a custom type targetting vmnet10
{
    "index": 1,
    "macAddress": "00:12:24:e7:98:4a",
    "type": "custom",
    "vmnet": "vmnet10"
}

### Create NIC N°1 of VM 42 to assign it a custom type targetting vmnet10
### Returned macAddress is empty: 
### - If your VM is off then it will be generated at the next boot
### - If it's on then you can get it now by runing a "action: list"
{
  "index": 2,
  "type": "custom",
  "vmnet": "vmnet10",
  "macAddress": ""
}

### Delete NIC N°1 of VM 42
return nothing
'''

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        target_vm=dict(type='str', required=False),
        target_vm_name=dict(type='str', required=False, default=''),
        action=dict(type='str', required=True),
        type=dict(type='str', required=False),
        vmnet=dict(type='str', required=False),
        index=dict(type='str', required=False),
        api_url=dict(type='str', default='http://127.0.0.1'),
        api_port=dict(type='str', default='8697'),
        validate_certs=dict(type='bool', default='no'),
    )

    result = dict(
        changed=False,
        msg=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    api_username = module.params['username']
    api_password = module.params['password']
    creds = api_username + ':' + api_password
    encodedBytes = base64.b64encode(creds.encode("utf-8"))
    request_creds = str(encodedBytes, "utf-8")
    request_server = module.params['api_url']
    request_port = module.params['api_port']
    headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + request_creds}

    target_vm = module.params['target_vm']
    action = module.params['action']
    typep = module.params['type']
    vmnet = module.params['vmnet']
    index = module.params['index']

    target_vm_name = module.params['target_vm_name']
    vmlist = []
    if target_vm_name != "":
        requestnamesurl = request_server + ':' + request_port + '/api/vms'
        reqname, infoname = fetch_url(module, requestnamesurl, headers=headers, method="Get")
        responsename = json.loads(reqname.read())

        for vm in responsename:
            currentvmx = vm['path']
            with open(currentvmx, 'r') as vmx:
                for line in vmx:
                    if re.search(r'^displayName', line):
                        currentname = line.split('"')[1]
            finalname = currentname.lower() 
            vm.update({'name': finalname})
            vmlist.append(vm)

        vm_name_search = target_vm_name.lower() 
        for vm in vmlist:
            if vm['name'] == vm_name_search:
                target_vm = vm['id']

    if action == "list":
        method = "get"
        body = {}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/nic'

    if action == "getip":
        method = "get"
        body = {}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/ip'

    if action == "delete":
        method = "DELETE"
        body = {}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/nic/' + index

    if action == "update":
        method = "Put"
        body = {"type": typep, "vmnet": vmnet}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/nic/' + index

    if action == "create":
        method = "Post"
        body = {"type": typep, "vmnet": vmnet}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/nic'

    bodyjson = json.dumps(body)

    req, info = fetch_url(module, request_url, data=bodyjson, headers=headers, method=method)

    if action == "delete":
        result['msg'] = info

    if action != "delete":
        result['msg'] = json.loads(req.read())

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
