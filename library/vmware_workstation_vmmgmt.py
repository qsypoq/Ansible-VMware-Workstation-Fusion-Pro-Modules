#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_vmmgmt

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

    username: "workstation-api-username"
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
# Change VM with ID 42's RAM allocation to 2048
- name: "Edit VM ID 42"
  vmware_workstation_vmmgmt:
    target_vm: "42"
    action: update
    memory_mb: 2048
    username: "workstation-api-username"
    password: "workstation-api-password"

# Clone VM with ID 42 as KMS-Server-Clone 
- name: "Clone VM ID 42"
  vmware_workstation_vmmgmt:
    target_vm: "42"
    action: clone
    name: "KMS-Server-Clone"
    username: "workstation-api-username"
    password: "workstation-api-password"

# Delete VM with ID 42
- name: "Delete VM ID 42"
  vmware_workstation_vmmgmt:
    target_vm: "42"
    action: delete
    username: "workstation-api-username"
    password: "workstation-api-password"
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
### Return clone's CPU/RAM/ID
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