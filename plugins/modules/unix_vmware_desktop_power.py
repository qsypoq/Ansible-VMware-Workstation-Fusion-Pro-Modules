#!/usr/bin/python

from base64 import b64encode
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: unix_vmware_desktop_power

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

    username: "workstation-api-username"
        description:
            - Your workstation API username
        required: true

    password: "workstation-api-password"
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
  unix_vmware_desktop_power:
    target_vm: "42"
    state: "on"
    username: "workstation-api-username"
    password: "workstation-api-password"
    api_url: "http://127.0.0.1"
    api_port: "8697"

### Get power state of the VM with ID 42 
- name: "Get power state"
  unix_vmware_desktop_power:
    target_vm: "42"
    username: "workstation-api-username"
    password: "workstation-api-password"
'''

RETURN = r'''
### Get power state of the VM with ID 42 
"power_state": "poweredOff"

### Boot the VM with ID 42 
"power_state": "poweredOn"
'''

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        target_vm=dict(type='str', required=True),
        state=dict(type='str', required=False, default=''),
        api_url=dict(type='str', default='http://127.0.0.1'),
        api_port=dict(type='str', default='8697'),
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
    request_creds = b64encode(creds)
    request_server = module.params['api_url']
    request_port = module.params['api_port']
    headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + request_creds}

    target_vm = module.params['target_vm']
    state = module.params['state']
    request_url = request_server + ':' + request_port + '/api/vms/' + target_vm +"/power"

    if state != "":
        method = "Put"
        r, info = fetch_url(module, request_url, data=state, headers=headers, method=method)
    else:
        method = "Get"
        r, info = fetch_url(module, request_url, headers=headers, method=method)

    result['msg'] = json.loads(r.read())
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
