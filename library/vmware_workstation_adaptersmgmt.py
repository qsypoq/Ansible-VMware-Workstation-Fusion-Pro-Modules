#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_adaptersmgmt

short_description: Implement the Network Adapters Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Pro Network Adapters "

options:
    targetVM:
        description:
            - This is the target VM to interact with
        required: true

    action: list || getip || update || create || delete
        description:
            - This is the action we want to do.
        required: true   

    targetIndex: 1
        description:
            - Index's number refering to your network adapter
        required: Only for delete & update

    targetType: custom || bridged || nat || hostonly
        description:
                - This is the target VMNET to interact with
        required: only for update & create

    targetVMnet:
        description:
                - This is the target VMNET to interact with
        required: only when targetType = custom
    
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
- name: "Return the IP adress of VM 42"
  vmware_workstation_adaptersmgmt:
    targetVM: "42"
    targetFolder: "ODBG110"
    targetPath: C:\Users\qsypoq\Desktop\odbg110
    action: "create"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    
- name: "Return all network adapters in VM 42"
  vmware_workstation_adaptersmgmt:
    targetVM: "42"
    action: "list"
    user: "workstation-api-user"
    pass: "workstation-api-password"
'''

RETURN = r'''
- name: "Return the IP adress of VM 42"
{
    "ip": "172.20.20.10"
}

- name: "Return all network adapters in VM 42"
{
    "nics": [
        {
            "index": 1,
            "macAddress": "00:46:80:23:23:59",
            "type": "custom",
            "vmnet": "vmnet0"
        },
        {
            "index": 2,
            "macAddress": "00:0c:25:50:23:67",
            "type": "custom",
            "vmnet": "vmnet10"
        }
    ],
    "num": 2
}
'''