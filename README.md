# Ansible-VMware-Workstation-Modules

## Actual state of the modules: 7/23
VMware Workstation's REST API is designed as follow:
- 23 possibles requests
- Divided into 5 categories

<p align="center"><img src="vmware_workstation_api_logic.PNG"></p>

First goal of the project is to implement all the requests. For the time being, following VMware's logic. Next goal may be to concatenate some of the requests to create better categories

### Host Networks Management: 0/7
- Returns all virtual networks

 Not implemented yet

- Returns all MAC-to-IP settings for DHCP service

 Not implemented yet

- Returns all port forwardings

 Not implemented yet

- Updates the MAC-to-IP binding

 Not implemented yet

- Updates port forwarding

 Not implemented yet

- Creates a virtual network

 Not implemented yet

- Deletes port forwarding

 Not implemented yet


### VM Management: 5/5
Complete! :tada: This section is implemented as follow:

**vmware_workstation_vminfos**
- Returns a list of VM IDs and paths for all VMs
- Returns the VM setting information of a VM

**vmware_workstation_vmmgt**
- Updates a VM CPU/RAM allocation
- Clone a VM 
- Deletes a VM

### VM Network Adapters Management: 0/5
- Returns the IP address of a VM

Not implemented yet

- Returns all network adapters in the VM

Not implemented yet

- Updates a network adapter in the VM

Not implemented yet

- Creates a network adapter in the VM

Not implemented yet

- Deletes a VM network adapter

Not implemented yet

### VM Power Management: 2/2
Complete! :tada: This section is implemented as follow:

**vmware_workstation_power**.
- Returns the power state of the VM
- Changes the VM power state

### VM Shared Folders Management: 0/4
- Returns all shared folders mounted in the VM

Not implemented yet

- Updates a shared folder mounted in the VM

Not implemented yet

- Mounts a new shared folder in the VM

Not implemented yet

- Deletes a shared folder

Not implemented yet