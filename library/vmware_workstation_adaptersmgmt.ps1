#!powershell

#Requires -Module Ansible.ModuleUtils.CommandUtil
#Requires -Module Ansible.ModuleUtils.Legacy

$ErrorActionPreference = "Stop"

$result = New-Object psobject @{
    changed = $false
}

$params = Parse-Args -arguments $args -supports_check_mode $true

$username =  Get-AnsibleParam -obj $params -name "username" -type "str" -failifempty $true
$password = Get-AnsibleParam -obj $params -name "password" -type "str" -failifempty $true
$target_vm = Get-AnsibleParam -obj $params -name "target_vm" -type "str" -failifempty $true
$action = Get-AnsibleParam -obj $params -name "action" -type "str" -failifempty $true 
$api_url = Get-AnsibleParam -obj $params -name "api_url" -type "str" -default "http://127.0.0.1" -failifempty $false 
$api_port = Get-AnsibleParam -obj $params -name "api_port" -type "int" -default "8697" -failifempty $false

if (($action -eq 'list' ) -Or ($action -eq 'create')) { 
    $requesturl = "${api_url}:${api_port}/api/vms/${target_vm}/nic"
}
if ($action -eq 'getip' ) { 
    $requesturl = "${api_url}:${api_port}/api/vms/${target_vm}/ip"
}
if (($action -eq 'update' ) -Or ($action -eq 'create')) {
    $type = Get-AnsibleParam -obj $params -name "type" -type "str" -failifempty $true 
}
if ($type -eq 'custom' ) {
    $vmnet = Get-AnsibleParam -obj $params -name "vmnet" -type "str" -failifempty $true
}
if (($action -eq 'update' ) -Or ($action -eq 'delete')) { 
    $targetIndex = Get-AnsibleParam -obj $params -name "targetIndex" -type "int" -failifempty $true 
    $requesturl = "${api_url}:${api_port}/api/vms/${target_vm}/nic/${targetIndex}"
}

$pair = "${username}:${password}"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)
$basicAuthValue = "Basic $base64"

$headers = @{
    'Authorization' =  $basicAuthValue;
    'Content-Type' =  'application/vnd.vmware.vmw.rest-v1+json';
    'Accept' = 'application/vnd.vmware.vmw.rest-v1+json';
}

if (($action -eq 'update' ) -Or ($action -eq 'create')) { 
    $body = @{
        "type" = $type;
        "vmnet" = $vmnet
    }      
}

$requestbody = ($body | ConvertTo-Json)

if (($action -eq 'list' ) -Or ($action -eq 'getip')) { 
    try {
        $listrequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Get'
        $result.infos = $listrequest
        $result.changed = $false;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

if ($action -eq 'create' ) { 
    try {
        $createrequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Post' -Body $requestbody
        $result.infos = $createrequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

if ($action -eq 'update' ) { 
    try {
        $updaterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Put' -Body $requestbody
        $result.infos = $updaterequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

if ($action -eq 'delete' ) { 
    try {
        $deleterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'DELETE'
        $result.infos = $deleterequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

Exit-Json $result;