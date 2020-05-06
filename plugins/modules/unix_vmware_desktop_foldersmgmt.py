#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: unix_vmware_desktop_foldersmgmt

short_description: Implement the Shared Folders Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Pro Shared Folders"

options:
    target_vm:
        description:
            - This is the target VM to interact with
        required: true

    action: infos || create || delete || update
        description:
            - This is the action we want to do.
        required: true   

    folder_name: "myFolderName"
        description:
            - Name of the shared folder
        required: Only for create & update & delete

    folder_path: C:\Users\qsypoq\Desktop\odbg110
        description:
            - Path of shared folder
        required: Only for create & update, the folder need to be reachable

    access: r || rw
    description:
        - Choose which kind of access the VM have to the folder
    required: false, default is read-only, you only need to use this when access needed is rw
    
    username "workstation-api-username"
        description:
            - Your workstation API username
        required: true

    password: "workstation-api-password"
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

author:
    - Adam Magnier (@qsypoq)  
'''

EXAMPLES = r'''
### List all shared folders mounted on VM ID 42
- name: "List shared folders"
  unix_vmware_desktop_foldersmgmt:
    target_vm: "42"
    action: "infos"
    username "workstation-api-username"
    password: "workstation-api-password"

### Create shared folder named ODBG110 on VM ID 42
- name: "Create shared folder"
  unix_vmware_desktop_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    folder_path: C:\Users\qsypoq\Desktop\odbg110
    access: "rw"
    action: "create"
    username "workstation-api-username"
    password: "workstation-api-password"

### Update shared folder named ODBG110 with new path and access rights
- name: "Update ODBG110"
  unix_vmware_desktop_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    folder_path: C:\Users\qsypoq\Desktop
    access: "r"
    action: "update"
    username "workstation-api-username"
    password: "workstation-api-password"

### Delete shared folder named ODBG110 on VM ID 42
- name: "Delete shared folder named ODBG110 on VM ID 42"
  unix_vmware_desktop_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    action: "delete"
    username "workstation-api-username"
    password: "workstation-api-password"
'''

RETURN = r'''
### List all shared folders mounted on VM ID 42
{
    "Count": 1, "value": [
        {
            "flags": 0,
            "folder_id": "ODBG110",
            "host_path": "C:\\Users\\qsypoq\\Desktop"
        }
    ]
}

### Create shared folder named ODBG110 on VM ID 42
{
    "Count": 1, "value": [
        {
            "flags": 4,
            "folder_id": "ODBG110",
            "host_path": "C:\\Users\\qsypoq\\Desktop\\odbg110"
        }
    ]
}

### Update shared folder named ODBG110 with new path and access rights
{
    "Count": 1, "value": [
        {
            "flags": 0,
            "folder_id": "ODBG110",
            "host_path": "C:\\Users\\qsypoq\\Desktop"
        }
    ]
}

### Delete shared folder named ODBG110 on VM ID 42
empty
'''
from base64 import b64encode
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        target_vm=dict(type='str', required=True),
        action=dict(type='str', required=True),
        folder_name=dict(type='str', required=False),
        folder_path=dict(type='str', required=False),
        access=dict(type='str', required=False),
        api_url=dict(type='str', default='http://127.0.0.1'),
        api_port=dict(type='str', default='8697'),
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
    request_creds = b64encode(creds)
    request_server = module.params['api_url']
    request_port = module.params['api_port']
    headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + request_creds}

    target_vm = module.params['target_vm']
    action = module.params['action']
    folder_name = module.params['folder_name']
    folder_path = module.params['folder_path']
    access = module.params['access']

    if access == "rw":
        flags = 4
    else:
        flags = 0

    if action == "infos":
        method = "Get"
        body = {}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/sharedfolders'

    if action == "create":
        method = "Post"
        body = {"folder_id": folder_name, "host_path": folder_path, "flags": flags}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/sharedfolders'

    if action == "update":
        method = "Put"
        body = {"host_path": folder_path, "flags": flags}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/sharedfolders/' + folder_name

    if action == "delete":
        method = "DELETE"
        body = {"id": target_vm}
        request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/sharedfolders/' + folder_name 
    
    bodyjson = json.dumps(body)

    r, info = fetch_url(module, request_url, data=bodyjson, headers=headers, method=method)

    if action == "delete":
        result['msg'] = info

    if action != "delete":
        result['msg'] = info
    
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
