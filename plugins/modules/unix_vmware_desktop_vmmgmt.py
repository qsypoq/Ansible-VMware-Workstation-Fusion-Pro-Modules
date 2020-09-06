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
module: unix_vmware_desktop_vmmgmt
short_description: Implement the VM Management part of the API
version_added: "2.4"
description:
    - "Manage VMware Workstation Pro VM"
options:
    target_vm:
        description:
            - This is the target VM to interact with
        required: true
    action: clone || delete || update
        description:
            - This is the action we want to do. update CPU/RAM, clone or delete the VM
        required: true  
    name: "KMS-Server-Clone"
        description:
            - This is the name of the cloned VM
        required: only when action = clone      
    num_cpus: 2
        description:
            - This is the new values of CPU allocated to the VM
        required: false, only usefull when action = update
    memory_mb: 2048
        description:
            - This is the new values (in mb) of RAM allocated to the VM
        required: false, only usefull when action = update
    username: "api-username"
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
    timeout: 
        description:
            - Specifies a timeout in seconds for communicating with vmrest
        required: false
        default: 30

author:
    - Adam Magnier (@qsypoq)
'''

EXAMPLES = r'''
# Change VM with ID 42's RAM allocation to 2048
- name: "Edit VM ID 42"
  unix_vmware_desktop_vmmgmt:
    target_vm: "42"
    action: update
    memory_mb: 2048
    username: "api-username"
    password: "api-password"
# Clone VM with ID 42 as KMS-Server-Clone 
- name: "Clone VM ID 42"
  unix_vmware_desktop_vmmgmt:
    target_vm: "42"
    action: clone
    name: "KMS-Server-Clone"
    username: "api-username"
    password: "api-password"
# Delete VM with ID 42
- name: "Delete VM ID 42"
  unix_vmware_desktop_vmmgmt:
    target_vm: "42"
    action: delete
    username: "api-username"
    password: "api-password"
'''

RETURN = r'''
### Change VM with ID 42's RAM allocation to 2048
### Return VM's CPU/RAM/ID
{
    "cpu": {
        "processors": 1
    },
    "id": "42",
    "memory": 2048
}
### Clone VM with ID 42 as KMS-Server-Clone
{
    "cpu": {
        "processors": 1
    },
    "id": "50",
    "memory": 768
}
# Delete VM with ID 42
return nothing
'''

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        target_vm=dict(type='str', required=False),
        target_vm_name=dict(type='str', required=False, default=''),
        action=dict(type='str', required=True),
        name=dict(type='str', required=False),
        num_cpus=dict(type='int', required=False),
        memory_mb=dict(type='int', required=False),
        api_url=dict(type='str', default='http://127.0.0.1'),
        api_port=dict(type='str', default='8697'),
        validate_certs=dict(type='bool', default='no'),
        timeout=dict(type='int', required=False, default=30)
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
    request_creds = str(encodedBytes).encode("utf-8")
    request_server = module.params['api_url']
    request_port = module.params['api_port']
    headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json',
               'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json',
               'Authorization': 'Basic ' + request_creds}
    timeout = module.params['timeout']

    target_vm = module.params['target_vm']
    action = module.params['action']
    num_cpus = module.params['num_cpus']
    memory_mb = module.params['memory_mb']
    name = module.params['name']

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

    if action == "clone":
        method = "Post"
        body = {"name": name, "parentId": target_vm}
        request_url = request_server + ':' + request_port + '/api/vms'

    if action == "delete":
        method = "DELETE"
        body = {"id": target_vm}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm

    if action == "update":
        method = "Put"
        body = {"processors": num_cpus, "memory": memory_mb}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm

    bodyjson = json.dumps(body)

    req, info = fetch_url(module, request_url, data=bodyjson, headers=headers,
                          method=method, timeout=timeout)

    if req is None:
        module.fail_json(msg=info['msg'])

    result["changed"] = True

    if action == "delete":
        result['msg'] = info

    if action != "delete":
        result['msg'] = json.loads(req.read())

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
