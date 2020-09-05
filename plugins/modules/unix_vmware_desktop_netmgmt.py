#!/usr/bin/python

import base64
import json
import sys
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: unix_vmware_desktop_netmgmt

short_description: Implement the VMNet Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Pro VMNets"

options:
    vmnet:
        description:
            - This is the target NETVM to interact with
        required: false

    action: infos || delete || create || update_pf || update MTI
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

    validate_certs: "no || yes"
        description:
            - Validate Certificate it HTTPS connection
        required: false

author:
    - Adam Magnier (@qsypoq)
'''

EXAMPLES = r'''

### Get infos of all the configured vmnets
- name: "Get all vmnet infos"
  unix_vmware_desktop_netmgmt:
    action: infos
    username: "api-username"
    password: "api-password"

### Return all Mac-to-IP settings from vmnet8
- name: "Return MTI of vmnet8"
  unix_vmware_desktop_netmgmt:
    action: infos
    vmnet: "vmnet8"
    setting: "mactoip"
    username: "api-username"
    password: "api-password"

### Return all the forwarded ports settings from vmnet13
- name: "Return vmnet13 portforward"
  unix_vmware_desktop_netmgmt:
    action: infos
    vmnet: "vmnet13"
    setting "portforward"
    username: "api-username"
    password: "api-password"

### Create a new vmnet as vmnet13, as host only
- name: "Create vmnet13"   
  unix_vmware_desktop_netmgmt:
    vmnet: "vmnet13"
    type: "hostonly"
    action: create
    username: "api-username"
    password: "api-password"

### Delete the forwarded 1337 tcp port from vmnet8
- name: "Delete portforwarding"   
  unix_vmware_desktop_netmgmt:
    vmnet: "vmnet8"
    protocol: "TCP"
    port: "1337"
    action: delete
    username: "api-username"
    password: "api-password"

### Create/Update the forwarded 1337 tcp port from vmnet8 to 172.13.13.13:1111 with "itworks!" as description
- name: "forward port"
  unix_vmware_desktop_netmgmt:
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
  unix_vmware_desktop_netmgmt:
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

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        vmnet=dict(type='str', required=False),
        action=dict(type='str', required=True),
        type=dict(type='str', required=False),
        guest_ip_address=dict(type='str', required=False),
        guest_port=dict(type='int', required=False),
        guest_description=dict(type='str', required=False),
        protocol=dict(type='str', required=False),
        port=dict(type='str', required=False),
        ip_address=dict(type='str', required=False),
        mac_address=dict(type='str', required=False),
        setting=dict(type='str', required=False, default=''),
        api_url=dict(type='str', default='http://127.0.0.1'),
        api_port=dict(type='str', default='8697'),
        validate_certs=dict(type='bool', default='no'),
    )

    result = dict(
        changed=False,
        msg=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    api_username = module.params['username']
    api_password = module.params['password']
    creds = api_username + ':' + api_password
    if PY3:
        encodedBytes = base64.b64encode(creds.encode("utf-8"))
        request_creds = str(encodedBytes, "utf-8")
    else:
        encodedBytes = base64.b64encode(creds)
        request_creds = str(encodedBytes).encode("utf-8")
    request_server = module.params['api_url']
    request_port = module.params['api_port']
    headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + request_creds}

    vmnet = module.params['vmnet']
    action = module.params['action']
    typep = module.params['type']
    guest_ip_address = module.params['guest_ip_address']
    guest_port = module.params['guest_port']
    guest_description = module.params['guest_description']
    protocol = module.params['protocol']
    port = module.params['port']
    ip_address = module.params['ip_address']
    mac_address = module.params['mac_address']
    setting = module.params['setting']

    if action == "create":
        method = "Post"
        body = {"name": vmnet, "type": typep, "subnet": ip_address}
        request_url = request_server + ':' + request_port + '/api/vmnets'

    if action == "update_pf":
        method = "Put"
        body = {"guestIp": guest_ip_address, "guestPort": guest_port, "desc": guest_description}
        request_url = request_server + ':' + request_port + '/api/vmnet/' + vmnet + '/portforward/' + protocol + '/' + port

    if action == "update_mti":
        method = "Put"
        encoded_mac = mac_address.replace(":", "%3A")
        body = {"IP": ip_address}
        request_url = request_server + ':' + request_port + '/api/vmnet/' + vmnet + '/mactoip/' + encoded_mac

    if action == "delete":
        method = "delete"
        body = {}
        request_url = request_server + ':' + request_port + '/api/vmnet/' + vmnet + '/portforward/' + protocol + '/' + port

    if action == "infos":
        if setting != "":
            request_url = request_server + ':' + request_port + '/api/vmnet/' + vmnet + '/' + setting
        else:
            request_url = request_server + ':' + request_port + '/api/vmnet'
        method = "get"
        body = {}

    bodyjson = json.dumps(body)

    req, info = fetch_url(module, request_url, data=bodyjson, headers=headers, method=method)

    if action == "delete":
        result['msg'] = info

    if action != "delete":
        result['msg'] = json.loads(req.read())

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
