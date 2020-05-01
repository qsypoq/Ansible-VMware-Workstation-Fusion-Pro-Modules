#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: vmware_workstation_vminfos

short_description: Get VMware Workstation VM infos

version_added: "2.4"

description:
    - "Get VMware Workstation VM infos"

options:
    targetVM:
        description:
            - This is the target VM to interact with, if not set, will get infos about all VMs
        required: false

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
# Get infos about all the VMs
- name: "Start VM ID 42"
  vmware_workstation_clone:
    user: "workstation-api-user"
    pass: "workstation-api-password"

# Get infos about VM with ID 42
- name: "Get infos about VM ID 42"
  vmware_workstation_vminfos:
    targetVM: "42"
    user: "workstation-api-user"
    pass: "workstation-api-password"
'''

RETURN = '''
'''