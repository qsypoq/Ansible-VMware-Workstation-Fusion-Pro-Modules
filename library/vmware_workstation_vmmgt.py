#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: vmware_workstation_vmmgt

short_description: Implement the VM Management part of the API

version_added: "2.4"

description:
    - "Clone VMware Workstation VM"

options:
    targetVM:
        description:
            - This is the target VM to interact with
        required: true

    action: clone || delete || update
        description:
            - This is the action we want to do. update CPU/RAM, clone or delete the VM
        required: true  

    newname: "KMS-Server-Clone"
        description:
            - This is the name of the cloned VM
        required: only when action = clone      

    targetCPU: 2
        description:
            - This is the new values of CPU allocated to the VM
        required: false, only usefull when action = update

    targetRAM: 2048
        description:
            - This is the new values of RAM allocated to the VM
        required: false, only usefull when action = update

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

EXAMPLES = '''
# Clone VM with ID 42 as KMS-Server-Clone using API @ http://127.0.0.1:8697
- name: "Start VM ID 42"
  vmware_workstation_clone:
    targetVM: "42"
    action: clone
    newname: "KMS-Server-Clone"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    apiurl: "http://127.0.0.1"
    apiport: "8697"

# Delete VM with ID 42
- name: "Start VM ID 42"
  vmware_workstation_clone:
    targetVM: "42"
    action: delete
    user: "workstation-api-user"
    pass: "workstation-api-password"

# Change VM with ID 42's RAM allocation to 2048
- name: "Start VM ID 42"
  vmware_workstation_clone:
    targetVM: "42"
    action: update
    targetRAM: 2048
    user: "workstation-api-user"
    pass: "workstation-api-password"
'''

RETURN = '''
'''