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

if ($action -eq 'update' ) { 
    $num_cpus = Get-AnsibleParam -obj $params -name "num_cpus" -type "int" -failifempty $false
    $memory_mb = Get-AnsibleParam -obj $params -name "memory_mb" -type "int" -failifempty $false
}
if ($action -eq 'clone' ) { 
    $name = Get-AnsibleParam -obj $params -name "name" -type "str" -failifempty $true
}

$api_url = Get-AnsibleParam -obj $params -name "api_url" -type "str" -default "http://127.0.0.1" -failifempty $false 
$api_port = Get-AnsibleParam -obj $params -name "api_port" -type "int" -default "8697" -failifempty $false

if ($action -eq 'clone' ) { 
    $requesturl = "${api_url}:${api_port}/api/vms"
}
if (($action -eq 'delete' ) -Or ($action -eq 'update')) { 
    $requesturl = "${api_url}:${api_port}/api/vms/${target_vm}"
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

if ($action -eq 'clone' ) { 
    $body = @{
        "name" = $name;
        "parentId" = $target_vm
    }
}
if ($action -eq 'delete' ) { 
    $body = @{
        "id" = $target_vm
    }
}
if ($action -eq 'update' ) { 
    $body = @{
        "processors" = $num_cpus;
        "memory" = $memory_mb
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