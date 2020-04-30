#!powershell

#Requires -Module Ansible.ModuleUtils.CommandUtil
#Requires -Module Ansible.ModuleUtils.Legacy

$ErrorActionPreference = "Stop"

$result = New-Object psobject @{
    vmware_workstation_clone = New-Object psobject
    changed = $false
}

$params = Parse-Args -arguments $args -supports_check_mode $true
  
$user =  Get-AnsibleParam -obj $params -name "user" -type "str" -failifempty $true
$pass = Get-AnsibleParam -obj $params -name "pass" -type "str" -failifempty $true
$targetVM = Get-AnsibleParam -obj $params -name "targetVM" -type "str" -failifempty $true
$newname = Get-AnsibleParam -obj $params -name "newname" -type "str" -failifempty $true
$apiurl = Get-AnsibleParam -obj $params -name "apiurl" -type "str" -failifempty $true

$pair = "${user}:${pass}"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)
$basicAuthValue = "Basic $base64"

$headers = @{
    'Authorization' =  $basicAuthValue;
    'Content-Type' =  'application/vnd.vmware.vmw.rest-v1+json';
    'Accept' = 'application/vnd.vmware.vmw.rest-v1+json';
}

$body = @{
    "name" = $newname;
    "parentId" = $targetVM
}

$requestbody = ($body | ConvertTo-Json)

try {
    $clonerequest = Invoke-RestMethod -Uri $apiurl -Headers $headers -method 'Post' -Body $requestbody
    $result.changed = $true;
}
catch {
        Fail-Json $result "Request failed, please check your configuration"
}

Exit-Json $result;