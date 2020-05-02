#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_netmgmt

short_description: Implement the VMNet Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Pro VMNets"

options:
    targetVMnet:
        description:
            - This is the target NETVM to interact with
        required: false

    action: infos || delete || create
        description:
            - This is the action we want to do. Actual issue: only infos works.
        required: true  

    targetType: custom || bridged || nat || hostonly
        description:
                - This is the type of virtual network you want to create
        required: only for create

    targetVMnet:
        description:
                - Choose your VMnet
        required: only when targetType = custom

    targetDHCP: custom || bridged || nat || hostonly
        description:
                - This is the target VMNET to interact with
        required: only for create

    targetSubnet: 172.10.10.0
        description:
                - This is the target subnet where you want to create
        required: only for create

    targetMask: 255.255.0.0
        description:
                - This is the subnet mask for your subnet
        required: only for create

    targetProtocol: 
        description:
                -
        required: only for update & delete

    targetPort: 255.255.0.0
        description:
                - 
        required: only for update & delete
        

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
- name: "Get all vmnet infos"
    vmware_workstation_netmgmt:
    action: infos
    user: "workstation-api-user"
    pass: "workstation-api-password"

- name: "Create vmnet13"   
      vmware_workstation_netmgmt:
        targetVMnet: "vmnet13"
        targetType: "hostonly"
        targetDHCP: "true"
        targetSubnet: "172.60.60.0"
        targetMask: "255.255.0.0"
        action: create
        user: "workstation-api-user"
        pass: "workstation-api-password"

- name: "Delete portforwarding"   
      vmware_workstation_netmgmt:
        targetVMnet: "vmnet8"
        targetProtocol: "TCP"
        targetPort: "1337"
        action: delete
        user: "workstation-api-user"
        pass: "workstation-api-password"

- name: "update forwarded port"
      vmware_workstation_netmgmt:
        targetVMnet: "vmnet8"
        targetProtocol: "TCP"
        targetPort: "1337"
        guestIP: "172.13.13.13"
        guestPort: "1111"
        desc: "itworks!"
        action: updatePF
        user: "workstation-api-user"
        pass: "workstation-api-password"

'''

RETURN = r'''
'''