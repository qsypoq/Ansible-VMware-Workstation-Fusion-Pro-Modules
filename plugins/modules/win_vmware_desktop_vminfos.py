#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: win_vmware_desktop_vminfos

short_description: Get VMware Workstation Pro VM infos

version_added: "2.4"

description:
    - "Get VMware Workstation Pro VM infos"

options:
    target_vm:
        description:
            - This is the target VM to interact with:
                When not set: return all VMs id & path
                When set: return CPU & RAM of the target VM
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
# Get infos about all the VMs
- name: "Get infos"
  win_vmware_desktop_vminfos:
    username: "api-username"
    password: "api-password"

# Retrieve CPU & RAM from VM with ID 42
- name: "Get infos about VM ID 42"
  win_vmware_desktop_vminfos:
    target_vm: "42"
    username: "api-username"
    password: "api-password"

# Retrieve restrictions from VM with name "Windows 10"
- name: "Get restrictions"
  win_vmware_desktop_vminfos:
    target_vm_name: "Windows 10"
    restrictions: True
    username: "api-username"
    password: "api-password"

# Retrieve extendedConfigFile from VM with ID 42
- name: "Get infos about VM ID 42"
  win_vmware_desktop_vminfos:
    target_vm: "42"
    param: "extendedConfigFile"
    username: "api-username"
    password: "api-password"
'''

RETURN = r'''
# Get infos about all the VMs
[{
  "id": "0J319913PHLM1304J1P6EPLADAM",
  "path": "G:\\VMs\\ESXi\\ESXi.vmx"},
{
  "id": "19915KM24UQ0J0OADAMH69H16T125LOL",
  "path": "G:\\VMs\\pfsense\\pfsense.vmx"
}]

# Retrieve CPU & RAM from VM with ID 42
{
  "cpu": {"processors": 1},
  "id": "42",
  "memory": 2048
}
# Retrieve restrictions from VM with name "pfsense"
{
    "changed": false,
    "infos": {
        "applianceView": {
            "author": "",
            "port": "",
            "showAtPowerOn": "",
            "version": ""
        },
        "cddvdList": {
            "devices": [],
            "num": 0
        },
        "cpu": {
            "processors": 1
        },
        "firewareType": 0,
        "floppyList": {
            "devices": [],
            "num": 0
        },
        "groupID": "",
        "guestIsolation": {
            "copyDisabled": false,
            "dndDisabled": false,
            "hgfsDisabled": true,
            "pasteDisabled": false
        },
        "id": "R33IRMF281FGQ584LH7FSVA58L4LN76N",
        "integrityConstraint": "",
        "memory": 1024,
        "nicList": {
            "nics": [
                {
                    "index": 1,
                    "macAddress": "00:0C:29:5B:FD:35",
                    "type": "custom",
                    "vmnet": "vmnet2"
                },
                {
                    "index": 2,
                    "macAddress": "00:0C:29:5B:FD:3F",
                    "type": "custom",
                    "vmnet": "vmnet10"
                },
                {
                    "index": 4,
                    "macAddress": "00:0C:29:5B:FD:53",
                    "type": "custom",
                    "vmnet": "vmnet4"
                }
            ],
            "num": 3
        },
        "orgDisplayName": "",
        "parallelPortList": {
            "devices": [],
            "num": 0
        },
        "remoteVNC": {
            "VNCEnabled": false,
            "VNCPort": 5900
        },
        "serialPortList": {
            "devices": [],
            "num": 0
        },
        "usbList": {
            "num": 2,
            "usbDevices": [
                {
                    "BackingType": 8,
                    "backingInfo": "",
                    "connected": false,
                    "index": 0
                },
                {
                    "BackingType": 2,
                    "backingInfo": "",
                    "connected": false,
                    "index": 1
                }
            ]
        }
    }
}
# Retrieve extendedConfigFile from VM with ID 42
{
  "name": "extendedConfigFile",
  "value": "pfsense.vmxf"
}
'''
