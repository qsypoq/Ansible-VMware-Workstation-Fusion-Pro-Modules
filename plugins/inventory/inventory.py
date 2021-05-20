#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import base64
import json
import sys
import re
from ansible.plugins.inventory import BaseInventoryPlugin
from distutils.version import LooseVersion
from ansible.errors import AnsibleError

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

try:
    import requests
    if LooseVersion(requests.__version__) < LooseVersion('1.1.0'):
        raise ImportError
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class InventoryModule(BaseInventoryPlugin):

    NAME = 'inventory'
       
    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('vmware_desktop.yaml', 'vmware_desktop.yml')):
                valid = True
            else:
                self.display.vvv('Skipping due to inventory source not ending in "vmware_desktop.yaml" nor "vmware_desktop.yml"')
        return valid

    def parse(self, inventory, loader, path, cache=False):
        if not HAS_REQUESTS:
            raise AnsibleError('This module requires Python Requests 1.1.0 or higher: '
                               'https://github.com/psf/requests.')

        super(InventoryModule, self).parse(inventory, loader, path)

        self.conf = self._read_config_data(path)

        self.api_url = self.conf['url']
        self.api_port = self.conf['port']
        self.api_username = self.conf['user']
        self.api_password = self.conf['password']

        creds = self.api_username + ':' + self.api_password
        if PY3:
            encodedBytes = base64.b64encode(creds.encode("utf-8"))
            request_creds = str(encodedBytes, "utf-8")
        else:
            encodedBytes = base64.b64encode(creds)
            request_creds = str(encodedBytes).encode("utf-8")
        self.headers = {'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + request_creds}
        self._populate()

    def get_vm_list(self):
        self.request_url = 'http://' + self.api_url + ':' + self.api_port + '/api/vms'
        self.resp = requests.get(self.request_url, headers=self.headers, verify=False, timeout=15)
        return json.loads(self.resp.content)

    def get_vm_name(self, vm_id):
        self.request_url = 'http://' + self.api_url + ':' + self.api_port + '/api/vms/' + vm_id + '/params/' + 'displayName'
        self.resp = requests.get(self.request_url, headers=self.headers, verify=False, timeout=15)
        self.jsonresp = json.loads(self.resp.content)
        if self.jsonresp['name']:
            return self.jsonresp['value']
        else:
            self.request_url = 'http://' + self.api_url + ':' + self.api_port + '/api/vms/' + vm_id + '/params/' + 'displayname'
            self.resp = requests.get(self.request_url, headers=self.headers, verify=False, timeout=15)
            self.jsonresp = json.loads(self.resp.content)
            if self.jsonresp['name']:
                return self.jsonresp['value']

    def to_safe(self, word):
        regex = r"[^A-Za-z0-9\.]"
        return re.sub(regex, "-", word.replace(" - ", "-"))

    def _populate(self):
       
        for vm in self.get_vm_list():
            vm_id = vm['id']
            vm_name = self.to_safe(self.get_vm_name(vm_id))
            #vm_os = vm_name.split('.')[-2]
            #self.inventory.add_group(vm_os)
            self.inventory.add_host(vm_name)
            self.inventory.set_variable(vm_name, 'vm_id', vm_id)
            #self.inventory.add_child(vm_os, vm_name)