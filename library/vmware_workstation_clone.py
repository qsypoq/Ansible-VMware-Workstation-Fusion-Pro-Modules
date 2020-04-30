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
    targetId:
        description:
            - This is the target VM to interact with
        required: true

author:
    - Adam Magnier (@qsypoq)
'''

EXAMPLES = '''
# Clone VM with ID 42
- name: "Start VM ID 42"
  vmware_workstation_clone:
    targetVM: "42"
    newname: "Hello_World"
    user: "api-user"
    pass: "api-password"
    apiurl: "http://127.0.0.1:8697/api/vms"

'''

RETURN = '''
'''