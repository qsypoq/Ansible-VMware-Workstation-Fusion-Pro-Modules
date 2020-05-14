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
$target_vm = Get-AnsibleParam -obj $params -name "target_vm" -type "str" -failifempty $false
$api_url = Get-AnsibleParam -obj $params -name "api_url" -type "str" -default "http://127.0.0.1" -failifempty $false 
$api_port = Get-AnsibleParam -obj $params -name "api_port" -type "int" -default "8697" -failifempty $false
$validate_certs = Get-AnsibleParam -obj $params -name "validate_certs" -type "bool" -default $false -failifempty $false

$pair = "${username}:${password}"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)
$basicAuthValue = "Basic $base64"

$headers = @{
    'Authorization' =  $basicAuthValue;
    'Content-Type' =  'application/vnd.vmware.vmw.rest-v1+json';
    'Accept' = 'application/vnd.vmware.vmw.rest-v1+json';
}

if ($validate_certs -eq $false ) { 
    [System.Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
if (-not ([System.Management.Automation.PSTypeName]'ServerCertificateValidationCallback').Type)
{
$certCallback = @"
    using System;
    using System.Net;
    using System.Net.Security;
    using System.Security.Cryptography.X509Certificates;
    public class ServerCertificateValidationCallback
    {
        public static void Ignore()
        {
            if(ServicePointManager.ServerCertificateValidationCallback ==null)
            {
                ServicePointManager.ServerCertificateValidationCallback += 
                    delegate
                    (
                        Object obj, 
                        X509Certificate certificate, 
                        X509Chain chain, 
                        SslPolicyErrors errors
                    )
                    {
                        return true;
                    };
            }
        }
    }
"@
    Add-Type $certCallback
 }
    [ServerCertificateValidationCallback]::Ignore()
}

$target_vm_name = Get-AnsibleParam -obj $params -name "target_vm_name" -type "str" -failifempty $false
if (-not ([string]::IsNullOrEmpty($target_vm_name))) { 
    $vmlist = @()
    $requestnamesurl = "${api_url}:${api_port}/api/vms"
    $requestvmlist = Invoke-RestMethod -Uri $requestnamesurl -Headers $headers -method 'Get'
    foreach ($vm in $requestvmlist) {
        $currentvmx = Select-String -Path $vm.path -Pattern ^displayName
        $currentname="$currentvmx".split('"')[1]
        $finalname=$currentname.ToLower() 
        $currentvmprop = @{
            id=$vm.id
            path=$vm.path
            name=$finalname
        }
        $currentvm = New-Object PSObject –Property $currentvmprop
        $vmlist = $vmlist + $currentvm
    }
    $vm_name_search = $target_vm_name.ToLower() 
    foreach ($vm in $vmlist) {
        if ($vm.name -eq $vm_name_search) { 
            $target_vm = $vm.id
        }
    }
}

if (-not ([string]::IsNullOrEmpty($target_vm))) { 
    $requesturl = "${api_url}:${api_port}/api/vms/${target_vm}"
}
else {
    $requesturl = "${api_url}:${api_port}/api/vms"
}

try {
    $vminfosrequest = Invoke-RestMethod -Uri $requesturl -Headers $headers -method 'Get'
    $result.infos = $vminfosrequest
    $result.changed = $false;
}
catch {
        #$error_object = $_.ErrorDetails.Message | ConvertFrom-Json
        Fail-Json $result $error_object.message
}

Exit-Json $result;