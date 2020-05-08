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
$state = Get-AnsibleParam -obj $params -name "state" -type "str" -failifempty $false
$api_url = Get-AnsibleParam -obj $params -name "api_url" -type "str" -default "http://127.0.0.1" -failifempty $false 
$api_port = Get-AnsibleParam -obj $params -name "api_port" -type "int" -default "8697" -failifempty $false

$requesturl = "${api_url}:${api_port}/api/vms/${target_vm}/power"

$pair = "${username}:${password}"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)
$basicAuthValue = "Basic $base64"

$headers = @{
    'Authorization' =  $basicAuthValue;
    'Content-Type' =  'application/vnd.vmware.vmw.rest-v1+json';
    'Accept' = 'application/vnd.vmware.vmw.rest-v1+json';
}

if (-not ([string]::IsNullOrEmpty($state))) { 
    try {
        $powerrequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Put' -Body $state
        $result.power_state = $powerrequest.power_state
        $result.changed = $true;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
} else {
    try {
        $powerrequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Get'
        $result.power_state = $powerrequest.power_state
        $result.changed = $false;
    }
    catch {
            Fail-Json $result "Request failed, please check your configuration"
    }
}

Exit-Json $result;