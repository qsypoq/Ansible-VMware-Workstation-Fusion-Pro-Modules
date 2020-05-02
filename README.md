<div align="center"><img src="https://magnier.io/content/images/2020/05/repository-open-graph-template.jpg">

**Ansible modules interacting with VMware Workstation Pro's REST API** 

<img src="https://img.shields.io/badge/size-30KiB-brightgreen"> <img src="https://img.shields.io/badge/license-MIT-green">

</div>
<div align="justify">

<hr/>

**Introduction: [How I ended up developing a VMware Workstation Pro Ansible module](https://magnier.io/developing-vmware-workstation-pro-ansible-module)**

First goal of the project is to implement all the REST API requests. For the time being, following VMware's logic. Next goal may be to concatenate some of the requests to create better categories.

**This project is still in early stage developpement.**
</div>

<hr/>

## :rocket: Informations about the REST API

VMware Workstation Pro's REST API is designed as follow:

<p align="center"><img src="https://magnier.io/content/images/2020/05/vmware_workstation_api_logic.PNG"></p>

- 23 possibles requests
- Divided into 5 categories

If you want to know more about it you can access this page when the REST API is running, please refer to VMware's guide about it: <a href="https://docs.vmware.com/en/VMware-Workstation-Pro/15.0/com.vmware.ws.using.doc/GUID-C3361DF5-A4C1-432E-850C-8F60D83E5E2B.html">How to setup vmrest.exe to enable REST API</a>

## VM Management 5/5
Complete! :tada:

This section is implemented as follow:

### vmware_workstation_vminfos
- Returns a list of VM IDs and paths for all VMs

- Returns the VM setting information of a VM

### vmware_workstation_vmmgt
- Updates a VM CPU/RAM allocation

- Clone a VM

- Deletes a VM

## VM Network Adapters Management 5/5
Complete! :tada:

This section is implemented as follow:

### vmware_workstation_adaptersmgmt
- Returns all network adapters in the VM
- Updates a network adapter in the VM
- Creates a network adapter in the VM
- Deletes a VM network adapter
- Returns the IP address of a VM

Note: The last one doesn't work with all my VMs so it would need debugging.

## VM Power Management 2/2
Complete! :tada:

This section is implemented as follow:

### vmware_workstation_power
- Returns the power state of the VM

- Changes the VM power state

## VM Shared Folders Management: 4/4

Complete! :tada:

This section is implemented as follow:

### vmware_workstation_foldersmgmt

- Returns all shared folders mounted in a VM

- Updates a shared folder mounted in a VM

- Mounts a new shared folder in a VM

- Deletes a shared folder

## Host Networks Management: 5/7

### vmware_workstation_netmgmt

Implemented:
- Returns all virtual networks

- Returns all MAC-to-IP settings for DHCP service
- Returns all port forwardings

Implemented but not working yet because of admin permissions problems while interacting with vmrest.exe:
- Creates a virtual network

- Deletes port forwarding

Not implementing until admin permissions problems fixed:
- Updates the MAC-to-IP binding

- Updates port forwarding

## Todo-List / Roadmap
### Auto start vmrest.exe
- Find a way to start/stop vmrest.exe from Ansible on demand.

### Fix vmrest permission problem
- When the vmrest is run as standard user, modifications using netmgt are not authaurized.

- When vmrest is run as administrator, no API can be utilized. This problem needs more tests.

### Information gathering / Returned infos to user while running playbooks
- Make information returned by requests (like VM Id or state) easily exploitable via playbook.

- Create self explaining error info when something goes wrong instead of "Check your inputs" 

### Make API more human-usable
- Some request need non "human" values, like VM Id. Renaming a VM (from GUI) is only effective on the GUI, folder name, files names etc, don't change. So I'm searching a way to do it.

### Check user input/rationnal behaviour
- Example: Would be great if we could prevent a user to disconnect the network adapter of the VM ansible is run from. 

### Code refractor
- Many if statements can be replaced/optimised with switch when possible, or concatened togethers.

### More documentation
- One detailed example by request would be great.