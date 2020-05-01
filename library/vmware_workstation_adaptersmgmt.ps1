#!powershell

#Requires -Module Ansible.ModuleUtils.CommandUtil
#Requires -Module Ansible.ModuleUtils.Legacy

$ErrorActionPreference = "Stop"

$result = New-Object psobject @{
    changed = $false
}

$params = Parse-Args -arguments $args -supports_check_mode $true

$user =  Get-AnsibleParam -obj $params -name "user" -type "str" -failifempty $true
$pass = Get-AnsibleParam -obj $params -name "pass" -type "str" -failifempty $true
$targetVM = Get-AnsibleParam -obj $params -name "targetVM" -type "str" -failifempty $true
$action = Get-AnsibleParam -obj $params -name "action" -type "str" -failifempty $true 
$apiurl = Get-AnsibleParam -obj $params -name "apiurl" -type "str" -default "http://127.0.0.1" -failifempty $false 
$apiport = Get-AnsibleParam -obj $params -name "apiport" -type "int" -default "8697" -failifempty $false

if (($action -eq 'list' ) -Or ($action -eq 'create')) { 
    $requesturl = "${apiurl}:${apiport}/api/vms/${targetVM}/nic"
}
if ($action -eq 'getip' ) { 
    $requesturl = "${apiurl}:${apiport}/api/vms/${targetVM}/ip"
}
if (($action -eq 'update' ) -Or ($action -eq 'create')) {
    $targetType = Get-AnsibleParam -obj $params -name "targetType" -type "str" -failifempty $true 
}
if ($targetType -eq 'custom' ) {
    $targetVMnet = Get-AnsibleParam -obj $params -name "targetVMnet" -type "str" -failifempty $true
}
if (($action -eq 'update' ) -Or ($action -eq 'delete')) { 
    $targetIndex = Get-AnsibleParam -obj $params -name "targetIndex" -type "int" -failifempty $true 
    $requesturl = "${apiurl}:${apiport}/api/vms/${targetVM}/nic/${targetIndex}"
}

$pair = "${user}:${pass}"
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
        "type" = $targetType;
        "vmnet" = $targetVMnet
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