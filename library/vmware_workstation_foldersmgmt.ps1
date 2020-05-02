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
$flags = Get-AnsibleParam -obj $params -name "flags" -type "int" -default "4" -failifempty $false 
$apiurl = Get-AnsibleParam -obj $params -name "apiurl" -type "str" -default "http://127.0.0.1" -failifempty $false 
$apiport = Get-AnsibleParam -obj $params -name "apiport" -type "int" -default "8697" -failifempty $false

if (($action -eq 'infos' ) -Or ($action -eq 'create')) { 
    $requesturl = "${apiurl}:${apiport}/api/vms/${targetVM}/sharedfolders"
}
if ($action -eq 'create' ) { 
    $targetFolder = Get-AnsibleParam -obj $params -name "targetFolder" -type "str" -failifempty $true
}
if (($action -eq 'update' ) -Or ($action -eq 'create')) { 
    $targetPath = Get-AnsibleParam -obj $params -name "targetPath" -type "str" -failifempty $true
}
if (($action -eq 'delete') -Or ($action -eq 'update')) { 
    $targetFolder = Get-AnsibleParam -obj $params -name "targetFolder" -type "str" -failifempty $true
    $requesturl = "${apiurl}:${apiport}/api/vms/${targetVM}/sharedfolders/${targetFolder}"
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

if ($action -eq 'update' ) { 
    $body = @{
        "host_path" = $targetPath;
        "flags" = $flags
    }      
}
if ($action -eq 'create' ) { 
    $body = @{
        "folder_id" = $targetFolder;
        "host_path" = $targetPath;
        "flags" = $flags
    }      
}

$requestbody = ($body | ConvertTo-Json)

if ($action -eq 'infos' ) { 
    try {
        $inforequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Get'
        $result.infos = $inforequest
        $result.changed = $false;
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