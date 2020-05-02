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
    targetVM:
        description:
            - This is the target VM to interact with
        required: true

    action: infos || create || delete || update
        description:
            - This is the action we want to do.
        required: true   

    targetFolder: "myFolderName"
        description:
            - Name of the shared folder
        required: Only for create & update & delete

    targetPath: C:\Users\qsypoq\Desktop\odbg110
        description:
            - Path of shared folder
        required: Only for create & update

    access: r || rw
    description:
        - Choose which kind of access the VM have to the folder
    required: false, default is read-only, you only need to use this when access needed is rw
    
    user: "workstation-api-user"
        description:
            - Your workstation API username
        required: true

    pass: "workstation-api-password"
        description:
            - Your workstation API password
        required: true

    apiurl: "http://127.0.0.1"
        description:
            - Your workstation API URL
        required: false
        default: "http://127.0.0.1"

    apiport: "8697"
        description:
            - Your workstation API PORT
        required: false
        default: "8697"

author:
    - Adam Magnier (@qsypoq)  
'''

EXAMPLES = r'''
- name: "Create shared folder named ODBG110 on VM ID 42"
  vmware_workstation_foldersmgmt:
    targetVM: "42"
    targetFolder: "ODBG110"
    targetPath: C:\Users\qsypoq\Desktop\odbg110
    access: "rw"
    action: "create"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    
- name: "Delete shared folder named ODBG110 on VM ID 42"
  vmware_workstation_foldersmgmt:
    targetVM: "42"
    targetFolder: "ODBG110"
    action: "delete"
    user: "workstation-api-user"
    pass: "workstation-api-password"
'''

RETURN = r'''
- name: "Create shared folder named ODBG110 on VM ID 42"
{
    "Count": 1, "value": [
        {
            "flags": 4,
            "folder_id": "ODBG110",
            "host_path": "C:\\Users\\qsypoq\\Desktop\\odbg110"
        }
    ]
}
'''