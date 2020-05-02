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
$apiurl = Get-AnsibleParam -obj $params -name "apiurl" -type "str" -default "http://127.0.0.1" -failifempty $false 
$apiport = Get-AnsibleParam -obj $params -name "apiport" -type "int" -default "8697" -failifempty $false


$action = Get-AnsibleParam -obj $params -name "action" -type "str" -failifempty $true
$targetVMnet = Get-AnsibleParam -obj $params -name "targetVMnet" -type "str" -failifempty $false

if ($action -eq 'create') {
    $targetType = Get-AnsibleParam -obj $params -name "targetType" -type "str" -failifempty $true
    $targetDHCP = Get-AnsibleParam -obj $params -name "targetDHCP" -type "str" -failifempty $true
    $targetSubnet = Get-AnsibleParam -obj $params -name "targetSubnet" -type "str" -failifempty $true
    $targetMask = Get-AnsibleParam -obj $params -name "targetMask" -type "str" -failifempty $true
}

if ($action -eq 'updatePF') {
    $guestIP = Get-AnsibleParam -obj $params -name "guestIP" -type "str" -failifempty $true
    $guestPort = Get-AnsibleParam -obj $params -name "guestPort" -type "int" -failifempty $true
    $desc = Get-AnsibleParam -obj $params -name "desc" -type "str" -failifempty $false
}

if (($action -eq 'delete') -Or ($action -eq 'updatePF')) {
    $targetProtocol = Get-AnsibleParam -obj $params -name "targetProtocol" -type "str" -failifempty $true
    $targetPort = Get-AnsibleParam -obj $params -name "targetPort" -type "int" -failifempty $true
}

$targetSetting = Get-AnsibleParam -obj $params -name "targetSetting" -type "str" -failifempty $false

if ($action -eq 'infos') { 
    if (-not ([string]::IsNullOrEmpty($targetSetting))) { 
        $requesturl = "${apiurl}:${apiport}/api/vmnet/${targetVMnet}/${targetSetting}"
    }else {
        $requesturl = "${apiurl}:${apiport}/api/vmnet"
    }
} 

if ($action -eq 'create') {
    $requesturl = "${apiurl}:${apiport}/api/vmnets"
}

if ($action -eq 'updateMTI') {
    $targetMTI = Get-AnsibleParam -obj $params -name "targetMTI" -type "str" -failifempty $false
    $targetMAC = Get-AnsibleParam -obj $params -name "targetMAC" -type "str" -failifempty $true
    $requesturl = "${apiurl}:${apiport}/api/vmnets/${targetVMnet}/mactoip/${targetMAC}"
}

if (($action -eq 'delete') -Or ($action -eq 'updatePF')) {
    $requesturl = "${apiurl}:${apiport}/api/vmnet/${targetVMnet}/portforward/${targetProtocol}/${targetPort}"
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

if ($action -eq 'create' ) { 
    $body = @{
        "name" = $targetVMnet;
        "type" = $targetType;
        "dhcp" = $targetDHCP;
        "subnet" = $targetSubnet;
        "mask" = $targetMask
    }      
}

if ($action -eq 'updatePF' ) { 
    $body = @{
        "guestIp" = $guestIP;
        "guestPort" = $guestPort;
        "desc" = $desc;
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
            Fail-Json $result "Request failed, please check your configuration"
    }
}

if ($action -eq 'create' ) { 
    try {
        $netcreaterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Post' -Body $requestbody
        $result.infos = $netcreaterequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

if (($action -eq 'updateMTI') -Or ($action -eq 'updatePF')) { 
    try {
        $netcreaterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Put' -Body $requestbody
        $result.infos = $netcreaterequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

if ($action -eq 'delete' ) { 
    try {
        $result.test = $requesturl
        $netdeleterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'DELETE'
        $result.infos = $netdeleterequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

Exit-Json $result;