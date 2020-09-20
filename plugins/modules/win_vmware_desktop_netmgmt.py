#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: win_vmware_desktop_netmgmt

short_description: Implement the VMNet Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Pro VMNets"

options:
    vmnet:
        description:
            - This is the target NETVM to interact with
        required: false

    action: infos || delete || create || update_pf || update_mti
        description:
            - This is the action we want to do.
        required: true

    setting: portforward || mactoip
        description:
                - Choose what infos you want to list, portforwarding or mac-to-ip, empty = listing all vmnets
        required: no, only usefull with action = infos

    type: custom || bridged || nat || hostonly
        description:
                - This is the type of virtual network you want to create
        required: only for create

    vmnet:
        description:
                - Choose your VMnet
        required: only when type = custom

    protocol: TCP || UDP
        description:
                - Your targeted protocol
        required: only for update_pf & delete

    port: 1337
        description:
                - Your targeted port
        required: only for update_pf & delete

    guest_ip_address: "192.168.188.13"
        description:
            - Your targeted IP
        required: true, only with update_pf

    guest_port: "1111"
        description:
            - Your targeted port
        required: only for update_pf

    guest_description: "itworks!"
        description:
            - PF description
        required: false, only usefull for update_pf

    mac_address: "00:0C:29:87:4B:89"
        description:
            - Your targeted mac address
        required: only for updateMTI

    ip_address: "192.168.188.13"
        description:
            - Your targeted mac address
        required: false, if you don't have a target IP it will delete the MTI

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

### Get infos of all the configured vmnets
- name: "Get all vmnet infos"
  win_vmware_desktop_netmgmt:
    action: infos
    username: "api-username"
    password: "api-password"

### Return all Mac-to-IP settings from vmnet8
- name: "Return MTI of vmnet8"
  win_vmware_desktop_netmgmt:
    action: infos
    vmnet: "vmnet8"
    setting: "mactoip"
    username: "api-username"
    password: "api-password"

### Return all the forwarded ports settings from vmnet8
- name: "Return vmnet13 portforward"
  win_vmware_desktop_netmgmt:
    action: infos
    vmnet: "vmnet13"
    setting "portforward"
    username: "api-username"
    password: "api-password"

### Create a new vmnet as vmnet13, as host only
- name: "Create vmnet13"
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet13"
    type: "hostonly"
    action: create
    username: "api-username"
    password: "api-password"

### Delete the forwarded 1337 tcp port from vmnet8
- name: "Delete portforwarding"
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet8"
    protocol: "TCP"
    port: "1337"
    action: delete
    username: "api-username"
    password: "api-password"

### Update the forwarded 1337 tcp port from vmnet8 to 172.13.13.13:1111 with "itworks!" as description
- name: "update forwarded port"
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet8"
    protocol: "TCP"
    port: "1337"
    guest_ip_address: "172.13.13.13"
    guest_port: "1111"
    guest_description: "itworks!"
    action: update_pf
    username: "api-username"
    password: "api-password"

### Update the MAC 00:12:29:34:4B:56 to be assigned as 192.168.188.13 on vmnet8
- name: "Update Mac to IP"
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet8"
    mac_address: "00:12:29:34:4B:56"
    ip_address: "192.168.188.13"
    action: update_mti
    username: "api-username"
    password: "api-password"
'''

RETURN = r'''
### Return all Mac-to-IP settings from vmnet8
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

### Update Mac to IP
{
    "Code": 0,
    "Message": "The operation was successful"
}
### Create a new vmnet as vmnet13, as host only
{
        "num": 1,
        "vmnets": [
            {
                "dhcp": "true",
                "mask": "255.255.255.0",
                "name": "vmnet13",
                "subnet": "192.168.244.0",
                "type": "hostOnly"
            }
        ]
    }
'''
