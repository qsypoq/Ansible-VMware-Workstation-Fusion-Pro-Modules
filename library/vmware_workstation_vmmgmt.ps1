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

if ($action -eq 'update' ) { 
    $targetCPU = Get-AnsibleParam -obj $params -name "targetCPU" -type "int" -failifempty $false
    $targetRAM = Get-AnsibleParam -obj $params -name "targetRAM" -type "int" -failifempty $false
}
if ($action -eq 'clone' ) { 
    $newname = Get-AnsibleParam -obj $params -name "newname" -type "str" -failifempty $true
}

$apiurl = Get-AnsibleParam -obj $params -name "apiurl" -type "str" -default "http://127.0.0.1" -failifempty $false 
$apiport = Get-AnsibleParam -obj $params -name "apiport" -type "int" -default "8697" -failifempty $false

if ($action -eq 'clone' ) { 
    $requesturl = "${apiurl}:${apiport}/api/vms"
}
if (($action -eq 'delete' ) -Or ($action -eq 'update')) { 
    $requesturl = "${apiurl}:${apiport}/api/vms/${targetVM}"
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

if ($action -eq 'clone' ) { 
    $body = @{
        "name" = $newname;
        "parentId" = $targetVM
    }
}
if ($action -eq 'delete' ) { 
    $body = @{
        "id" = $targetVM
    }
}
if ($action -eq 'update' ) { 
    $body = @{
        "processors" = $targetCPU;
        "memory" = $targetRAM
    }      
}

$requestbody = ($body | ConvertTo-Json)

if ($action -eq 'clone' ) { 
    try {
        $clonerequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Post' -Body $requestbody
        $result.infos = $clonerequest
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}
if ($action -eq 'delete' ) { 
    try {
        $deleterequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'DELETE' -Body $requestbody
        $result.infos = $deleterequest
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

Exit-Json $result;