#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: vmware_workstation_netmgt

short_description: Implement the VMNet Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation VMNets"

options:
    targetVMNET:
        description:
            - This is the target NETVM to interact with
        required: false

    action: infos || delete || create
        description:
            - This is the action we want to do. Actual issue: only infos works.
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

'''

RETURN = '''
'''