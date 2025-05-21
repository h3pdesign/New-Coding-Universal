
# PowerShell script to configure SharePoint Server 2016 SE with various services

# Variables
$databaseServer = "SQLServerName"
$farmPassphrase = ConvertTo-SecureString "YourPassphrase" -AsPlainText -Force
$farmCredentials = Get-Credential
$applicationPool = "SharePoint Service App Pool"
$oosServerName = "oos.contoso.com"

# 1. Create a new SharePoint farm
New-SPConfigurationDatabase -DatabaseName "SP_Config" -DatabaseServer $databaseServer -AdministrationContentDatabaseName "SP_AdminContent" -Passphrase $farmPassphrase -FarmCredentials $farmCredentials

# 2. Power Automate Integration
# Set up a Data Gateway and register SharePoint 2016 site in Power Automate (manual steps)

# 3. Managed Metadata Service (MMS)
New-SPManagedMetadataServiceApplication -Name "Managed Metadata Service" -ApplicationPool $applicationPool -DatabaseName "SP_MMS_DB"
New-SPManagedMetadataServiceApplicationProxy -Name "Managed Metadata Service Proxy" -ServiceApplication "Managed Metadata Service"

# 4. Search Service Application
New-SPEnterpriseSearchServiceApplication -Name "Search Service" -ApplicationPool $applicationPool -DatabaseName "Search_DB"
New-SPEnterpriseSearchServiceApplicationProxy -Name "Search Proxy" -ServiceApplication "Search Service"

# 5. User Profile Service (UPS)
New-SPProfileServiceApplication -Name "User Profile Service" -ApplicationPool $applicationPool -ProfileDBName "Profile_DB" -SocialDBName "Social_DB" -ProfileSyncDBName "Sync_DB"

# 6. Office Online Server (OOS) Integration
New-SPWOPIBinding -ServerName $oosServerName
Set-SPWOPIZone -Zone "internal-http"

# 7. Secure Store Service
New-SPSecureStoreServiceApplication -Name "Secure Store Service" -ApplicationPool $applicationPool -DatabaseName "SecureStore_DB"
New-SPSecureStoreServiceApplicationProxy -Name "Secure Store Proxy" -ServiceApplication "Secure Store Service"

# 8. IIS Configuration
Import-Module WebAdministration
Set-ItemProperty "IIS:\Sites\SharePoint - 80" -Name bindings -Value @{protocol="http";bindingInformation="*:80:"}
