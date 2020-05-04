#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_foldersmgmt

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
  vmware_workstation_foldersmgmt:
    target_vm: "42"
    action: "infos"
    username "workstation-api-username"
    password: "workstation-api-password"

### Create shared folder named ODBG110 on VM ID 42
- name: "Create shared folder"
  vmware_workstation_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    folder_path: C:\Users\qsypoq\Desktop\odbg110
    access: "rw"
    action: "create"
    username "workstation-api-username"
    password: "workstation-api-password"

### Update shared folder named ODBG110 with new path and access rights
- name: "Update ODBG110"
  vmware_workstation_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    folder_path: C:\Users\qsypoq\Desktop
    access: "r"
    action: "update"
    username "workstation-api-username"
    password: "workstation-api-password"

### Delete shared folder named ODBG110 on VM ID 42
- name: "Delete shared folder named ODBG110 on VM ID 42"
  vmware_workstation_foldersmgmt:
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