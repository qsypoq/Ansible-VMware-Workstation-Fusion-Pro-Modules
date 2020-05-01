#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_vminfos

short_description: Get VMware Workstation VM infos

version_added: "2.4"

description:
    - "Get VMware Workstation VM infos"

options:
    targetVM:
        description:
            - This is the target VM to interact with:
                When not set: return all VMs id & path
                When set: return CPU & RAM of the target VM
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
# Get infos about all the VMs
- name: "Get infos"
  vmware_workstation_vminfos:
    user: "workstation-api-user"
    pass: "workstation-api-password"

# Retrieve CPU & RAM from VM with ID 42
- name: "Get infos about VM ID 42"
  vmware_workstation_vminfos:
    targetVM: "42"
    user: "workstation-api-user"
    pass: "workstation-api-password"
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
'''