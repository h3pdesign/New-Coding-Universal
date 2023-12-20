USERNAME=azureuser
PASSWORD=$(openssl rand -base64 32)
az vm create \
  --name myVM \
  --resource-group [sandbox resource group name] \
  --image Win2016Datacenter \
  --size Standard_DS2_v2 \
  --location eastus \
  --admin-username $USERNAME \
  --admin-password $PASSWORDPASSWORD=$(openssl rand -base64 32)