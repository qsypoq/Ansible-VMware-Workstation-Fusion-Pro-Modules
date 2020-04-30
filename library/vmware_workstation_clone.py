#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: vmware_workstation_clone

short_description: Clone VMware Workstation VM

version_added: "2.4"

description:
    - "Clone VMware Workstation VM"

options:
    targetVM:
        description:
            - This is the target VM to interact with
        required: true

    newname: "KMS-Server-Clone"
        description:
            - This is the name of the cloned VM
        required: true      

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
    newname: "KMS-Server-Clone"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    apiurl: "http://127.0.0.1"
    apiport: "8697"
'''

RETURN = '''
'''