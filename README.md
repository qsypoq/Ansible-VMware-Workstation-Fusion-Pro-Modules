<div align="center">

<img src="https://magnier.io/content/images/2020/05/vmware_workstation_fusion_api_ansible.png">

<h2 align="center">Ansible modules interacting with VMware Workstation/Fusion Pro's REST API <br/><br/>
<img src="https://img.shields.io/badge/size-75KiB-brightgreen"> <img src="https://img.shields.io/badge/license-MIT-green"> <a href="https://twitter.com/qsypoq"><img src="https://img.shields.io/badge/twitter-@qsypoq-blue"></img></a> <br/>
</h2>

<p align="center"><b>Introduction: <a href="https://magnier.io/developing-vmware-workstation-pro-ansible-module">How I ended up developing a VMware Workstation/Fusion Pro Ansible module</a></b></p>

</div>
<hr/>

## Getting Started

### Get vmrest up and running
Set up your credentials:
- On Windows, change directories to the Workstation Pro installation folder, and run ```vmrest.exe -C```.
- On Unix, run ```vmrest -C```.

Then run vmrest:
- On Windows, change directories to the Workstation Pro installation folder, and run ```vmrest.exe``` command.
- On Unix, run ```vmrest```.

More informations on VMware REST API's docs: <a href="https://docs.vmware.com/en/VMware-Workstation-Pro/15.0/com.vmware.ws.using.doc/GUID-C3361DF5-A4C1-432E-850C-8F60D83E5E2B.html">Workstation Pro</a> | <a href="https://docs.vmware.com/en/VMware-Fusion/11/com.vmware.fusion.using.doc/GUID-5F89D1FE-A95D-4C3C-894F-0084027CF66F.html">Fusion Pro</a>

### Install the modules

#### Install from ansible-galaxy:
`ansible-galaxy collection install qsypoq.vmware_desktop`

#### Manual installation:

Put the content of `plugins/modules` to `~/.ansible/plugins/modules/` or in a `library` folder next to your playbooks.

## Informations
### Info retriving
For the modules with infos retriving only purposes you must set your ansible command with verbose flag, like:

 `ansible-playbook -i hosts.yml playbook.yml -vvv`
 
 Native use/exploitation of returned infos is WIP.

### Common variables
This 4 variables can/must to used with all the modules:
```
    username: "api-username"
    password: "api-password"
    api_url: "http://127.0.0.1"
    api_port: "8697"
    validate_certs: no
```
If you are using defaults vmrest url settings then you don't have to use `api_url` and `api_port`, as their defaults values are set to vmrest's defaults.

If you are using HTTPS you might want to use `validate_certs`, default is set to `no`.

Each time you can use `target_vm` you can also use `target_vm_name` instead, which require the display name of your VM. (The one you see on your GUI).

### Documentation
Here you will found basic examples. If you need more details you can find a file named `$module.py` available for both windows & unix version in the `modules` folder.

## Modules examples
This example are for windows's modules (Workstation Pro on Windows) but are the same for unix (Workstation Pro on Linux or Fusion Pro on macOS), you just need to replace `win` with `unix`.


### Create your first playbook
Specify the collection `qsypoq.vmware_desktop`

Playbook's host should be the machine hosting the API:

```
- hosts: vmware-workstation-host
  gather_facts: no
  collections:
    - qsypoq.vmware_desktop
  tasks:

  - name: "List all VMs"
    win_vmware_desktop_vminfos:
      username: "api-username"
      password: "api-password"
```

### win_vmware_desktop_vminfos
- Returns a list of VM IDs and paths for all VMs
```
- name: "Get infos"
  win_vmware_desktop_vminfos:
    username: "api-username"
    password: "api-password"
```
- Returns the VM setting information of a VM
```
- name: "Retrieve CPU & RAM from VM with ID 42"
  win_vmware_desktop_vminfos:
    target_vm: "42"
    username: "api-username"
    password: "api-password"
```
- Retrieve the VM restrictions
```
- name: "Get restrictions"
  win_vmware_desktop_vminfos:
    target_vm_name: "Windows 10"
    restrictions: True
    username: "api-username"
    password: "api-password"
```
- Retrieve specific VMX param
```
- name: "Get extendedConfigFile from VM ID 42"
  win_vmware_desktop_vminfos:
    target_vm: "42"
    param: "extendedConfigFile"
    username: "api-username"
    password: "api-password"
```
### win_vmware_desktop_vmmgmt
- Updates a VM CPU/RAM allocation
```
- name: "Change VM with ID 42's RAM allocation to 2048 & 2 vCPU"
  win_vmware_desktop_vmmgmt:
    target_vm: "42"
    action: update
    num_cpus: 2
    memory_mb: 2048
    username: "api-username"
    password: "api-password"
```
- Clone a VM
```
- name: "Clone VM with ID 42 as KMS-Server-Clone "
  win_vmware_desktop_vmmgmt:
    target_vm: "42"
    action: clone
    name: "KMS-Server-Clone"
    username: "api-username"
    password: "api-password"
```
- Deletes a VM
```
- name: "Delete VM ID 42"
  win_vmware_desktop_vmmgmt:
    target_vm: "42"
    action: delete
    username: "api-username"
    password: "api-password"
```
- Register a VM
```
- name: "Register VM with name ansible_test2"
  win_vmware_desktop_vmmgmt:
    name: "ansible_test2"
    action: register
    vmx_path: 'C:\Users\Qsypoq\Documents\Virtual Machines\ansible_test2\svc_pfSense.vmx'
    username: "api-username"
    password: "api-password"
```
- Update specific VMX param (NOT WORKING ATM)
```
- name: "Update displayName param"
    win_vmware_desktop_vmmgmt:
    target_vm_name: "pfsense"
    action: update
    param: displayName
    value: pfsense_OLD
    username: "api-username"
    password: "api-password"
```

### win_vmware_desktop_adaptersmgmt
- Return all network adapters in the VM
```
- name: "Return all network adapters in VM 42"
  win_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "list"
    user: "workstation-api-user"
    password: "api-password"
```
- Updates a network adapter in the VM
```
- name: "Edit NIC N°1 of VM 42 to assign it a custom type targetting vmnet10"
    win_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "update"
    index: 1
    type: custom
    vmnet: vmnet10
    user: "workstation-api-user"
    password: "api-password"
```
- Creates a network adapter in the VM
```
- name: "Create NIC N°1 of VM 42 and assign it a custom type targetting vmnet10"
    win_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "create"
    type: custom
    vmnet: vmnet10
    user: "workstation-api-user"
    password: "api-password"
```
- Deletes a VM network adapter
```
- name: "Delete NIC N°1 of VM 42 "
    win_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "delete"
    index: 1
    user: "workstation-api-user"
    password: "api-password"
```
- Returns the IP address of a VM

Doesn't work with VMs having multiple NICs
```
- name: "Return IP address of VM 42"
  win_vmware_desktop_adaptersmgmt:
    target_vm: "42"
    action: "getip"
    user: "workstation-api-user"
    password: "api-password"
```

### win_vmware_desktop_power
- Returns the power state of the VM
```
- name: "Get power state of the VM with ID 42 "
  win_vmware_desktop_power:
    target_vm: "42"
    username: "api-username"
    password: "api-password"
```
- Changes the VM power state
```
- name: "Start VM with ID 42"
  win_vmware_desktop_power:
    target_vm: "42"
    state: "on"
    username: "api-username"
    password: "api-password"
```

### win_vmware_desktop_foldersmgmt

- Returns all shared folders mounted in a VM
```
- name: "List all shared folders mounted on VM ID 42"
  win_vmware_desktop_foldersmgmt:
    target_vm: "42"
    action: "infos"
    username "api-username"
    password: "api-password"
```
- Create a shared folder mounted in a VM
```
- name: "Create shared folder named ODBG110 on VM ID 42"
  win_vmware_desktop_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    folder_path: C:\Users\qsypoq\Desktop\odbg110
    access: "rw"
    action: "create"
    username "api-username"
    password: "api-password"
```
- Update shared folder
```
- name: "Update shared folder named ODBG110 with new path and access rights"
  win_vmware_desktop_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    folder_path: C:\Users\qsypoq\Desktop
    access: "r"
    action: "update"
    username "api-username"
    password: "api-password"
```
- Deletes a shared folder
```
- name: "Delete shared folder named ODBG110 on VM ID 42"
  win_vmware_desktop_foldersmgmt:
    target_vm: "42"
    folder_name: "ODBG110"
    action: "delete"
    username "api-username"
    password: "api-password"
```
### win_vmware_desktop_netmgmt
**For this part to work you need to run vmrest with privileges.**

- Returns all virtual networks
```
- name: "Get infos of all the configured vmnets"
  win_vmware_desktop_netmgmt:
    action: infos
    username: "api-username"
    password: "api-password"
```
- Creates a virtual network
```
- name: "Create a new vmnet as vmnet13, as host only"   
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet13"
    type: "hostonly"
    action: create
    username: "api-username"
    password: "api-password"
```
- Returns all MAC-to-IP settings for DHCP service
```
- name: "Return all Mac-to-IP settings from vmnet8"
  win_vmware_desktop_netmgmt:
    action: infos
    vmnet: "vmnet8"
    setting: "mactoip"
    username: "api-username"
    password: "api-password"
```
- Returns all port forwardings
```
- name: "Return all the forwarded ports settings from vmnet8"
  win_vmware_desktop_netmgmt:
    action: infos
    vmnet: "vmnet13"
    setting "portforward"
    username: "api-username"
    password: "api-password"
```
- Deletes port forwarding
```
- name: "Delete the forwarded 1337 tcp port from vmnet8"   
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet8"
    protocol: "TCP"
    port: "1337"
    action: delete
    username: "api-username"
    password: "api-password"
```
- Updates port forwarding
```
- name: "Update the forwarded 1337 tcp port from vmnet8 to 172.13.13.13:1111 with "itworks!" as description"
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
```
- Updates the MAC-to-IP binding
```
- name: "Update the MAC 00:12:29:34:4B:56 to be assigned as 192.168.188.13 on vmnet8"
  win_vmware_desktop_netmgmt:
    vmnet: "vmnet8"
    mac_address: "00:12:29:34:4B:56"
    ip_address: "192.168.188.13"
    action: update_mti
    username: "api-username"
    password: "api-password"
```
## :construction: Todo-List / Roadmap

### Information gathering / Returned infos to user while running playbooks
- Make information returned by requests (like VM Id or state) easily exploitable via playbook.

- Create self explaining error info when something goes wrong instead of "Check your inputs" 

### Check user input/rationnal behaviour
- Example: Would be great if we could prevent a user to disconnect the network adapter of the VM ansible is run from. 

### Code refractoring
- If statements may be replaced/optimised.