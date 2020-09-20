#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: win_vmware_desktop_power

short_description: Change VMware Workstation Pro VM PowerState

version_added: "2.4"

description:
    - "Change VMware Workstation Pro VM PowerState"

options:
    target_vm:
        description:
            - This is the target VM to interact with
        required: true

    state: on || off || shutdown || suspend || pause || unpause
        description:
            - This is the power state we want, if not set, module will return actual VM power state
        required: false

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

author:
    - Adam Magnier (@qsypoq)
'''

EXAMPLES = r'''
### Boot the VM with ID 42
- name: "Start VM"
  win_vmware_desktop_power:
    target_vm: "42"
    state: "on"
    username: "api-username"
    password: "api-password"
    api_url: "http://127.0.0.1"
    api_port: "8697"

### Get power state of the VM with ID 42
- name: "Get power state"
  win_vmware_desktop_power:
    target_vm: "42"
    username: "api-username"
    password: "api-password"
'''

RETURN = r'''
### Get power state of the VM with ID 42
"power_state": "poweredOff"

### Boot the VM with ID 42
"power_state": "poweredOn"
'''
