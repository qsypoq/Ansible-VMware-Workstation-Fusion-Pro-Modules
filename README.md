<div align="center">

<img src="https://magnier.io/content/images/vrac/workstation-ansible-api-github.jpg">

<h2 align="center">Ansible modules interacting with VMware Workstation Pro's REST API <br/><br/>
<img src="https://img.shields.io/badge/size-32KiB-brightgreen"> <img src="https://img.shields.io/badge/license-MIT-green"> <br/>
</h2>

<p align="center"><b>Introduction: <a href="https://magnier.io/developing-vmware-workstation-pro-ansible-module">How I ended up developing a VMware Workstation Pro Ansible module</a></b></p>

<p align="center"><strike>First goal of the project is to implement all the REST API requests, for the time being, following VMware's logic. </strike><br/> Next goal is to rework some natives API functions interactions to make it's use simpler.<br/><br/>
<b>This project is still in early stage developpement.</b></p>
</div>
<hr/>

## :rocket: Informations about the REST API

VMware Workstation Pro's REST API is designed as follow:

<p align="center"><img src="https://magnier.io/content/images/2020/05/vmware_workstation_api_logic.PNG"></p>

- 23 possibles requests
- Divided into 5 categories

If you want to know more about it you can access this page when the REST API is running, please refer to VMware's guide about it: <a href="https://docs.vmware.com/en/VMware-Workstation-Pro/15.0/com.vmware.ws.using.doc/GUID-C3361DF5-A4C1-432E-850C-8F60D83E5E2B.html">How to setup vmrest.exe to enable REST API</a>

## :white_check_mark: VM Management 5/5
Complete! :tada:

This section is implemented as follow:

### vmware_workstation_vminfos
- Returns a list of VM IDs and paths for all VMs

- Returns the VM setting information of a VM

### vmware_workstation_vmmgmt
- Updates a VM CPU/RAM allocation

- Clone a VM

- Deletes a VM

## :white_check_mark: VM Network Adapters Management 5/5
Complete! :tada:

This section is implemented as follow:

### vmware_workstation_adaptersmgmt
- Returns all network adapters in the VM
- Updates a network adapter in the VM
- Creates a network adapter in the VM
- Deletes a VM network adapter
- Returns the IP address of a VM

Note: The last one doesn't work with all my VMs so it would need debugging.

## :white_check_mark: VM Power Management 2/2
Complete! :tada:

This section is implemented as follow:

### vmware_workstation_power
- Returns the power state of the VM

- Changes the VM power state

## :white_check_mark: VM Shared Folders Management: 4/4

Complete! :tada:

This section is implemented as follow:

### vmware_workstation_foldersmgmt

- Returns all shared folders mounted in a VM

- Updates a shared folder mounted in a VM

- Mounts a new shared folder in a VM

- Deletes a shared folder

## :white_check_mark: Host Networks Management: 7/7

**For this part to work you need to run your vmrest.exe in an elevated prompt !**

Complete! :tada:

This section is implemented as follow:

### vmware_workstation_netmgmt

- Returns all virtual networks
- Creates a virtual network
- Returns all MAC-to-IP settings for DHCP service
- Returns all port forwardings
- Deletes port forwarding
- Updates port forwarding
- Updates the MAC-to-IP binding

## :construction: Todo-List / Roadmap

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

### Porting to Linux / Mac (Fusion)

- As the API is the same it should be trivial to port it (powershell <=> python convertion).

- I thought that tweaking with unix's powershell package would work but I didn't successed yet.