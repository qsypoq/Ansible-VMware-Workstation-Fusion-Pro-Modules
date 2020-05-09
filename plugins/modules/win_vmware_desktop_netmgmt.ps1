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
$api_url = Get-AnsibleParam -obj $params -name "api_url" -type "str" -default "http://127.0.0.1" -failifempty $false 
$api_port = Get-AnsibleParam -obj $params -name "api_port" -type "int" -default "8697" -failifempty $false

$action = Get-AnsibleParam -obj $params -name "action" -type "str" -failifempty $true
$vmnet = Get-AnsibleParam -obj $params -name "vmnet" -type "str" -failifempty $false

if ($action -eq 'create') {
    $type = Get-AnsibleParam -obj $params -name "type" -type "str" -failifempty $true
    $requesturl = "${api_url}:${api_port}/api/vmnets"
}

if ($action -eq 'update_pf') {
    $guest_ip_address = Get-AnsibleParam -obj $params -name "guest_ip_address" -type "str" -failifempty $true
    $guest_port = Get-AnsibleParam -obj $params -name "guest_port" -type "int" -failifempty $true
    $guest_description = Get-AnsibleParam -obj $params -name "guest_description" -type "str" -failifempty $false
}

if (($action -eq 'delete') -Or ($action -eq 'update_pf')) {
    $protocol = Get-AnsibleParam -obj $params -name "protocol" -type "str" -failifempty $true
    $port = Get-AnsibleParam -obj $params -name "port" -type "int" -failifempty $true
}

$setting = Get-AnsibleParam -obj $params -name "setting" -type "str" -failifempty $false

if ($action -eq 'infos') { 
    if (-not ([string]::IsNullOrEmpty($setting))) { 
        $requesturl = "${api_url}:${api_port}/api/vmnet/${vmnet}/${setting}"
    }else {
        $requesturl = "${api_url}:${api_port}/api/vmnet"
    }
} 
if ($action -eq 'update_mti') {
    $ip_address = Get-AnsibleParam -obj $params -name "ip_address" -type "str" -failifempty $false
    $mac_address = Get-AnsibleParam -obj $params -name "mac_address" -type "str" -failifempty $true
    $encodedMAC = [System.Web.HttpUtility]::UrlEncode($mac_address) 
    $requesturl = "${api_url}:${api_port}/api/vmnet/${vmnet}/mactoip/${encodedMAC}"
}
if (($action -eq 'delete') -Or ($action -eq 'update_pf')) {
    $requesturl = "${api_url}:${api_port}/api/vmnet/${vmnet}/portforward/${protocol}/${port}"
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

if ($action -eq 'create' ) { 
    $body = @{
        "name" = $vmnet;
        "type" = $type;
        "subnet" = $ip_address;
    }      
}
if ($action -eq 'update_pf' ) { 
    $body = @{
        "guestIp" = $guest_ip_address;
        "guestPort" = $guest_port;
        "desc" = $guest_description;
    }      
}
if ($action -eq 'update_mti' ) { 
    $body = @{
        "IP" = $ip_address;
    }      
}
$requestbody = ($body | ConvertTo-Json)

if ($action -eq 'infos' ) { 
    try {
        $netinforequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Get'
        $result.infos = $netinforequest
        $result.changed = $false;
    }
    catch {
            $error_object = $_.ErrorDetails.Message | ConvertFrom-Json
            Fail-Json $result $error_object.message
    }
}
if ($action -eq 'create' ) { 
    try {
        $netcreaterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Post' -Body $requestbody
        $result.infos = $netcreaterequest
        $result.changed = $true;
    }
    catch {
            $error_object = $_.ErrorDetails.Message | ConvertFrom-Json
            Fail-Json $result $error_object.message
    }
}
if (($action -eq 'update_mti') -Or ($action -eq 'update_pf')) { 
    try {
        $netcreaterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Put' -Body $requestbody
        $result.infos = $netcreaterequest
        $result.changed = $true;
    }
    catch {
            $error_object = $_.ErrorDetails.Message | ConvertFrom-Json
            Fail-Json $result $error_object.message
    }
}
if ($action -eq 'delete' ) { 
    try {
        $netdeleterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'DELETE'
        $result.infos = $netdeleterequest
        $result.changed = $true;
    }
    catch {
            $error_object = $_.ErrorDetails.Message | ConvertFrom-Json
            Fail-Json $result $error_object.message
    }
}

Exit-Json $result;