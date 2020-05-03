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

    action: infos || delete || create || updatePF || update MTI
        description:
            - This is the action we want to do.
        required: true  

    targetSetting: portforward || mactoip
        description:
                - Choose what infos you want to list, portforwarding or mac-to-ip, empty = listing all vmnets
        required: no, only usefull with action = infos

    targetType: custom || bridged || nat || hostonly
        description:
                - This is the type of virtual network you want to create
        required: only for create

    targetVMnet:
        description:
                - Choose your VMnet
        required: only when targetType = custom

    targetDHCP: true || false
        description:
                - Do you want to enable dhcp on it ?
        required: only for create

    targetSubnet: 172.10.10.0
        description:
                - This is the target subnet where you want to create
        required: only for create

    targetMask: 255.255.0.0
        description:
                - This is the subnet mask for your subnet
        required: only for create

    targetProtocol: TCP || UDP
        description:
                - Your targeted protocol
        required: only for updatePF & delete

    targetPort: 1337
        description:
                - Your targeted port
        required: only for updatePF & delete

    guestIP: "172.13.13.13"
        description:
            - Your targeted IP
        required: only for updatePF

    guestPort: "1111"
        description:
            - Your targeted port
        required: only for updatePF

    desc: "itworks!"
        description:
            - PF description
        required: false, only usefull for updatePF

    targetMAC: "00:0C:29:87:4B:89"
        description:
            - Your targeted mac address
        required: only for updateMTI

    targetIP: "192.168.188.13"
        description:
            - Your targeted mac address
        required: false, only use is for updateMTI, if you do it without specifying a IP it will delete the MTI

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

### Get infos of all the configured vmnets
- name: "Get all vmnet infos"
  vmware_workstation_netmgmt:
    action: infos
    user: "workstation-api-user"
    pass: "workstation-api-password"

### Return all the Mac-to-IP settings from vmnet8
- name: "Return MTI of vmnet8"
  vmware_workstation_netmgmt:
    action: infos
    targetVMnet: "vmnet8"
    targetSetting: "mactoip"
    user: "workstation-api-user"
    pass: "workstation-api-password"

### Return all the forwarded ports settings from vmnet8
- name: "Return vmnet13 portforward"
  vmware_workstation_netmgmt:
    action: infos
    targetVMnet: "vmnet13"
    targetSetting "portforward"
    user: "workstation-api-user"
    pass: "workstation-api-password"

### Create a new vmnet as vmnet13, as host only, with dhcp, on 172.60.60.0/16
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

### Delete the forwarded 1337 tcp port from vmnet8
- name: "Delete portforwarding"   
  vmware_workstation_netmgmt:
    targetVMnet: "vmnet8"
    targetProtocol: "TCP"
    targetPort: "1337"
    action: delete
    user: "workstation-api-user"
    pass: "workstation-api-password"

### Update the forwarded 1337 tcp port from vmnet8 to 172.13.13.13:1111 with "itworks!" as description
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

### Update the MAC 00:12:29:34:4B:56 to be assigned as 192.168.188.13 on vmnet
- name: "Update Mac to IP"
  vmware_workstation_netmgmt:
    targetVMnet: "vmnet8"
    targetMAC: "00:12:29:34:4B:56"
    targetIP: "192.168.188.13"
    action: updateMTI
    user: "workstation-api-user"
    pass: "workstation-api-password"
'''

RETURN = r'''
- name: "Return all MTI settings of vmnet8"
{
    "mactoips": [
        {
            "ip": "172.60.60.60",
            "mac": "00:0c:34:3e:54:52",
            "vmnet": "vmnet8"
        },
        {
            "ip": "192.168.43.43",
            "mac": "00:0c:40:87:36:17",
            "vmnet": "vmnet8"
        }
    ]
}

- name: "Update Mac to IP"
{
    "Code": 0,
    "Message": "The operation was successful"
}
'''