az vm create \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --image Win2016Datacenter \
>   --size Standard_DS2_v2 \
>   --location eastus \
>   --admin-username $USERNAME \
>   --admin-password $PASSWORD

az vm get-instance-view \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --output table


az vm extension set \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --vm-name myVM \
>   --name CustomScriptExtension \
>   --publisher Microsoft.Compute \
>   --settings "{'fileUris':['https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-iis.ps1']}" \
>   --protected-settings "{'commandToExecute': 'powershell -ExecutionPolicy Unrestricted -File configure-iis.ps1'}"

az vm open-port \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --port 80

az vm show \
>   --name myVM \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --show-details \
>   --query [publicIps] \
>   --output tsv

az vm resize \
>   --resource-group 79f5746e-09c1-40f0-a3f2-586af5a80a50 \
>   --name myVM \
>   --size Standard_DS3_v2

#------------------------------------------------------------------------------------------
## Other VM

New-AzVm `
    -ResourceGroupName "myResourceGroupVM" `
    -Name "myVM" `
    -Location "EastUS" `
    -VirtualNetworkName "myVnet" `
    -SubnetName "mySubnet" `
    -SecurityGroupName "myNetworkSecurityGroup" `
    -PublicIpAddressName "myPublicIpAddress" `
    -Credential $cred

New-AzVm `
    -ResourceGroupName "myResourceGroup" `
    -Name "myVM" `
    -Location "East US" `
    -VirtualNetworkName "myVnet" `
    -SubnetName "mySubnet" `
    -SecurityGroupName "myNetworkSecurityGroup" `
    -PublicIpAddressName "myPublicIpAddress" `
    -OpenPorts 80, 3389