#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_power

short_description: Change VMware Workstation Pro VM PowerState

version_added: "2.4"

description:
    - "Change VMware Workstation Pro VM PowerState"

options:
    targetVM:
        description:
            - This is the target VM to interact with
        required: true

    targetState: on || off || shutdown || suspend || pause || unpause
        description:
            - This is the power state we want, if not set, module will return actual VM power state
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

EXAMPLES = r'''
### Boot the VM with ID 42 
- name: "Start VM"
  vmware_workstation_power:
    targetVM: "42"
    stargetState: "on"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    apiurl: "http://127.0.0.1"
    apiport: "8697"

### Get power state of the VM with ID 42 
- name: "Get power state"
  vmware_workstation_power:
    targetVM: "42"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    apiurl: "http://127.0.0.1"
    apiport: "8697"    
'''

RETURN = r'''
'''