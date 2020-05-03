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
### Return IP address of VM 42
### Doesn't work with VMs having multiple NICs
- name: "Return IP address"
  vmware_workstation_adaptersmgmt:
    targetVM: "42"
    action: "getip"
    user: "workstation-api-user"
    pass: "workstation-api-password"

### Return all network adapters in VM 42
- name: "Return network adapters"
  vmware_workstation_adaptersmgmt:
    targetVM: "42"
    action: "list"
    user: "workstation-api-user"
    pass: "workstation-api-password"

### Edit NIC N°1 of VM 42 to assign it a custom type targetting vmnet10
- name: "update NIC N°1 of VM42"
    vmware_workstation_adaptersmgmt:
    targetVM: "42"
    action: "update"
    targetIndex: 1
    targetType: custom
    targetVMnet: vmnet10

### Create NIC N°1 of VM 42 and assign it a custom type targetting vmnet10
- name: "Create NIC N°1 of VM 42"
    vmware_workstation_adaptersmgmt:
    targetVM: "42"
    action: "create"
    targetIndex: 1
    targetType: custom
    targetVMnet: vmnet10

### Delete NIC N°1 of VM 42 
- name: "Delete NIC"
    vmware_workstation_adaptersmgmt:
    targetVM: "42"
    action: "delete"
    targetIndex: 1
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

- name: "Edit NIC N°1 of VM 42 to assign it a custom type targetting vmnet10"
{
    "index": 1,
    "macAddress": "00:12:24:e7:98:4a",
    "type": "custom",
    "vmnet": "vmnet10"
}

### Returned macAddress is empty: 
### - If your VM is off then it will be generated at the next boot
### - If it's on then you can get it now by runing a "action: list"
- name: "Create NIC N°1 of VM 42 to assign it a custom type targetting vmnet10"
{
  "index": 2,
  "type": "custom",
  "vmnet": "vmnet10",
  "macAddress": ""
}

- name: "Delete NIC N°1 of VM 42"
return nothing
'''