# Changelog

All notable changes to this project will be documented in this file.

## 0.1.0
### 20 May 2021
Dynamic inventory POC

## 0.0.2
### 24 April 2021
New API endpoints implemented

## 0.0.1
### 20 Sept 2020
Converted as collection, 0.0.1 release :tada:

A huge thanks to the contributors who have helped for this release, Markus (@vMarkusK) & Marc (@Daghis) :trophy:
### 06 Sept 2020
When `fetch_url()` fails (`req is None`), use Ansible's `fail_json()` to return the information to the caller.
### 05 Sept 2020
Fix credential encoding, working for python2 & python3
### 19 Aug 2020
Fix `target_vm_name` python3 compatibility
### 14 May 2020
Allow disabling cert validation for HTTPS connections using ```validate_certs```.
### 09 May 2020
You can now use the `target_vm_name` parameter instead of `target_vm` if you want.

This parameter use the display name of your VM instead of this ID.
### 06 May 2020
Now fully compatible with VMware Workstation Pro Linux & VMware Fusion Pro on macOS
### 02 May 2020
100% API working - VMware Workstation Pro Windows
### 30 April 2020
First working POC - VMware Workstation Pro Windows