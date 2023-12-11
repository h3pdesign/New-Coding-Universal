Requesting a Cloud Shell.Succeeded.
Connecting terminal...

Welcome to Azure Cloud Shell

Type "az" to use Azure CLI
Type "help" to learn about Cloud Shell

hipeders@Azure:~$ USERNAME=azureuser
hipeders@Azure:~$ PASSWORD=$(openssl rand -base64 32)
hipeders@Azure:~$ az vm create \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --image Win2016Datacenter \
>   --size Standard_DS2_v2 \
>   --location eastus \
>   --admin-username $USERNAME \
>   --admin-password $PASSWORD
{
    "fqdns": "",
    "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Compute/virtualMachines/myVM",
    "location": "eastus",
    "macAddress": "00-0D-3A-1A-23-E8",
    "powerState": "VM running",
    "privateIpAddress": "10.0.0.4",
    "publicIpAddress": "40.114.78.242",
    "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
    "zones": ""
}
hipeders@Azure:~$ az vm get-instance-view \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --output table
Name    ResourceGroup                         Location    ProvisioningState    PowerState
------  ------------------------------------  ----------  ------------------ - ------------
myVM    79f5746e-09c1-40f0-a3f2-586af5a80a50  eastus      Succeeded            VM running
hipeders@Azure:~$ az vm extension set \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --vm-name myVM \
>   --name CustomScriptExtension \
>   --publisher Microsoft.Compute \
>   --settings "{'fileUris':['https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-iis.ps1']}" \
>   --protected-settings "{'commandToExecute': 'powershell -ExecutionPolicy Unrestricted -File configure-iis.ps1'}"
{
    "autoUpgradeMinorVersion": true,
    "forceUpdateTag": null,
    "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Compute/virtualMachines/myVM/extensions/CustomScriptExtension",
    "instanceView": null,
    "location": "eastus",
    "name": "CustomScriptExtension",
    "protectedSettings": null,
    "provisioningState": "Succeeded",
    "publisher": "Microsoft.Compute",
    "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
    "settings": {
        "fileUris": [
        "https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-iis.ps1"
        ]
    },
    "tags": null,
    "type": "Microsoft.Compute/virtualMachines/extensions",
    "typeHandlerVersion": "1.9",
    "virtualMachineExtensionType": "CustomScriptExtension"
}
hipeders@Azure:~$ az vm open-port \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --port 80
{
    "defaultSecurityRules": [
    {
        "access": "Allow",
        "description": "Allow inbound traffic from all VMs in VNET",
        "destinationAddressPrefix": "VirtualNetwork",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "*",
        "destinationPortRanges": [],
        "direction": "Inbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/defaultSecurityRules/AllowVnetInBound",
        "name": "AllowVnetInBound",
        "priority": 65000,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "VirtualNetwork",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
    },
    {
        "access": "Allow",
        "description": "Allow inbound traffic from azure load balancer",
        "destinationAddressPrefix": "*",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "*",
        "destinationPortRanges": [],
        "direction": "Inbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/defaultSecurityRules/AllowAzureLoadBalancerInBound",
        "name": "AllowAzureLoadBalancerInBound",
        "priority": 65001,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "AzureLoadBalancer",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
    },
    {
        "access": "Deny",
        "description": "Deny all inbound traffic",
        "destinationAddressPrefix": "*",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "*",
        "destinationPortRanges": [],
        "direction": "Inbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/defaultSecurityRules/DenyAllInBound",
        "name": "DenyAllInBound",
        "priority": 65500,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "*",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
    },
    {
        "access": "Allow",
        "description": "Allow outbound traffic from all VMs to all VMs in VNET",
        "destinationAddressPrefix": "VirtualNetwork",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "*",
        "destinationPortRanges": [],
        "direction": "Outbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/defaultSecurityRules/AllowVnetOutBound",
        "name": "AllowVnetOutBound",
        "priority": 65000,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "VirtualNetwork",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
    },
    {
        "access": "Allow",
        "description": "Allow outbound traffic from all VMs to Internet",
        "destinationAddressPrefix": "Internet",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "*",
        "destinationPortRanges": [],
        "direction": "Outbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/defaultSecurityRules/AllowInternetOutBound",
        "name": "AllowInternetOutBound",
        "priority": 65001,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "*",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
    },
    {
        "access": "Deny",
        "description": "Deny all outbound traffic",
        "destinationAddressPrefix": "*",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "*",
        "destinationPortRanges": [],
        "direction": "Outbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/defaultSecurityRules/DenyAllOutBound",
        "name": "DenyAllOutBound",
        "priority": 65500,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "*",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules"
    }
    ],
    "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
    "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG",
    "location": "eastus",
    "name": "myVMNSG",
    "networkInterfaces": [
    {
        "dnsSettings": null,
        "enableAcceleratedNetworking": null,
        "enableIpForwarding": null,
        "etag": null,
        "hostedWorkloads": null,
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkInterfaces/myVMVMNic",
        "interfaceEndpoint": null,
        "ipConfigurations": null,
        "location": null,
        "macAddress": null,
        "name": null,
        "networkSecurityGroup": null,
        "primary": null,
        "provisioningState": null,
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "resourceGuid": null,
        "tags": null,
        "tapConfigurations": null,
        "type": null,
        "virtualMachine": null
    }
    ],
    "provisioningState": "Succeeded",
    "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
    "resourceGuid": "fd04a03b-6116-413a-afaa-8500464d08c2",
    "securityRules": [
    {
        "access": "Allow",
        "description": null,
        "destinationAddressPrefix": "*",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "3389",
        "destinationPortRanges": [],
        "direction": "Inbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/securityRules/rdp",
        "name": "rdp",
        "priority": 1000,
        "protocol": "Tcp",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "*",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/securityRules"
    },
    {
        "access": "Allow",
        "description": null,
        "destinationAddressPrefix": "*",
        "destinationAddressPrefixes": [],
        "destinationApplicationSecurityGroups": null,
        "destinationPortRange": "80",
        "destinationPortRanges": [],
        "direction": "Inbound",
        "etag": "W/\"2c2d00ea-7d6d-4f09-b381-cbb8995f2baa\"",
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkSecurityGroups/myVMNSG/securityRules/open-port-80",
        "name": "open-port-80",
        "priority": 900,
        "protocol": "*",
        "provisioningState": "Succeeded",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "sourceAddressPrefix": "*",
        "sourceAddressPrefixes": [],
        "sourceApplicationSecurityGroups": null,
        "sourcePortRange": "*",
        "sourcePortRanges": [],
        "type": "Microsoft.Network/networkSecurityGroups/securityRules"
    }
    ],
    "subnets": null,
    "tags": { },
    "type": "Microsoft.Network/networkSecurityGroups"
}
hipeders@Azure:~$ az vm show \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --show-details \
>   --query [publicIps] \
>   --output tsv
40.114.78.242
hipeders@Azure:~$ az vm resize \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --name myVM \
>   --size Standard_DS3_v2
{
    "additionalCapabilities": null,
    "availabilitySet": null,
    "diagnosticsProfile": null,
    "hardwareProfile": {
        "vmSize": "Standard_DS3_v2"
    },
    "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Compute/virtualMachines/myVM",
    "identity": null,
    "instanceView": null,
    "licenseType": null,
    "location": "eastus",
    "name": "myVM",
    "networkProfile": {
        "networkInterfaces": [
        {
            "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Network/networkInterfaces/myVMVMNic",
            "primary": null,
            "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50"
        }
        ]
    },
    "osProfile": {
        "adminPassword": null,
        "adminUsername": "azureuser",
        "allowExtensionOperations": true,
        "computerName": "myVM",
        "customData": null,
        "linuxConfiguration": null,
        "requireGuestProvisionSignal": true,
        "secrets": [],
        "windowsConfiguration": {
            "additionalUnattendContent": null,
            "enableAutomaticUpdates": true,
            "provisionVmAgent": true,
            "timeZone": null,
            "winRm": null
        }
    },
    "plan": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
    "resources": [
    {
        "autoUpgradeMinorVersion": true,
        "forceUpdateTag": null,
        "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Compute/virtualMachines/myVM/extensions/CustomScriptExtension",
        "instanceView": null,
        "location": "eastus",
        "name": "CustomScriptExtension",
        "protectedSettings": null,
        "provisioningState": "Succeeded",
        "publisher": "Microsoft.Compute",
        "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
        "settings": {
            "fileUris": [
            "https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-iis.ps1"
            ]
        },
        "tags": null,
        "type": "Microsoft.Compute/virtualMachines/extensions",
        "typeHandlerVersion": "1.9",
        "virtualMachineExtensionType": "CustomScriptExtension"
    }
    ],
    "storageProfile": {
        "dataDisks": [],
        "imageReference": {
            "id": null,
            "offer": "WindowsServer",
            "publisher": "MicrosoftWindowsServer",
            "sku": "2016-Datacenter",
            "version": "latest"
        },
        "osDisk": {
            "caching": "ReadWrite",
            "createOption": "FromImage",
            "diffDiskSettings": null,
            "diskSizeGb": 127,
            "encryptionSettings": null,
            "image": null,
            "managedDisk": {
                "id": "/subscriptions/c650f239-db86-43f4-ab35-6c9823e2180a/resourceGroups/79f5746e-09c1-40f0-a3f2-586af5a80a50/providers/Microsoft.Compute/disks/myVM_OsDisk_1_0c44bdbec13047788a78838ce3dd12a2",
                "resourceGroup": "79f5746e-09c1-40f0-a3f2-586af5a80a50",
                "storageAccountType": "Premium_LRS"
            },
            "name": "myVM_OsDisk_1_0c44bdbec13047788a78838ce3dd12a2",
            "osType": "Windows",
            "vhd": null,
            "writeAcceleratorEnabled": null
        }
    },
    "tags": { },
    "type": "Microsoft.Compute/virtualMachines",
    "vmId": "6efdc8cd-9e9a-4512-a9bb-0c5308ecf5a7",
    "zones": null
}
hipeders@Azure:~$ az vm show \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --name myVM \
>   --query "hardwareProfile" \
>   --output tsv
Standard_DS3_v2
hipeders@Azure:~$