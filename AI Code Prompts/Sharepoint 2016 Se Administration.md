To configure and use **SharePoint Server 2016 SE** with **PowerShell**, including integration with **Power Automate**, **Managed Metadata Service (MMS)**, **Search**, **User Profile Service (UPS)**, **Office Online Server (OOS)**, **Secure Store**, and **IIS**, here's a structured guide based on best practices and Microsoft documentation [1](https://learn.microsoft.com/en-us/sharepoint/sharepoint-powershell) [2](https://www.sphammad.com/abcd-of-powershell-automating-sharepoint-2016-installation/) [3](https://answers.microsoft.com/en-us/msoffice/forum/all/connect-sharepoint-2016-with-powerapps-and-power/3b4ace2d-fda0-4c20-abb1-84b23dcfadf1):

---

### 🔧 **1. Initial Setup with PowerShell**

Start by launching the **SharePoint Management Shell** as Administrator. This shell is preloaded with SharePoint cmdlets.

#### Example: Create a new SharePoint farm

```powershell
New-SPConfigurationDatabase -DatabaseName "SP_Config" -DatabaseServer "SQLServerName" -AdministrationContentDatabaseName "SP_AdminContent" -Passphrase (ConvertTo-SecureString "YourPassphrase" -AsPlainText -Force) -FarmCredentials (Get-Credential)
### 🔧 **1. Initial Setup with PowerShell**

### 📝 **Full Deployment Script Template**

Below is a PowerShell script template to automate the setup of SharePoint 2016 SE core services. Update placeholders (e.g., server names, service accounts) as needed:

```powershell
# Variables
$DBServer = "SQLServerName"
$FarmPassphrase = ConvertTo-SecureString "YourPassphrase" -AsPlainText -Force
$FarmAccount = Get-Credential -Message "Enter Farm Account Credentials"
$AppPoolAccount = Get-Credential -Message "Enter Service App Pool Account"

# 1. Create Configuration Database and Central Admin
New-SPConfigurationDatabase -DatabaseName "SP_Config" -DatabaseServer $DBServer -AdministrationContentDatabaseName "SP_AdminContent" -Passphrase $FarmPassphrase -FarmCredentials $FarmAccount
Install-SPFarm -DatabaseServer $DBServer -DatabaseName "SP_Config" -Passphrase $FarmPassphrase -AdminContentDatabaseName "SP_AdminContent" -FarmCredentials $FarmAccount
New-SPCentralAdministration -Port 2016 -WindowsAuthProvider "NTLM"

# 2. Create Application Pool
New-SPServiceApplicationPool -Name "SharePoint Service App Pool" -Account $AppPoolAccount

# 3. Managed Metadata Service
$mms = New-SPManagedMetadataServiceApplication -Name "Managed Metadata Service" -ApplicationPool "SharePoint Service App Pool" -DatabaseName "SP_MMS_DB"
New-SPManagedMetadataServiceApplicationProxy -Name "Managed Metadata Service Proxy" -ServiceApplication $mms

# 4. Search Service Application
$search = New-SPEnterpriseSearchServiceApplication -Name "Search Service" -ApplicationPool "SharePoint Service App Pool" -DatabaseName "Search_DB"
New-SPEnterpriseSearchServiceApplicationProxy -Name "Search Proxy" -ServiceApplication $search

# 5. User Profile Service
$ups = New-SPProfileServiceApplication -Name "User Profile Service" -ApplicationPool "SharePoint Service App Pool" -ProfileDBName "Profile_DB" -SocialDBName "Social_DB" -ProfileSyncDBName "Sync_DB"

# 6. Secure Store Service
$sss = New-SPSecureStoreServiceApplication -Name "Secure Store Service" -ApplicationPool "SharePoint Service App Pool" -DatabaseName "SecureStore_DB"
New-SPSecureStoreServiceApplicationProxy -Name "Secure Store Proxy" -ServiceApplication $sss

# 7. Office Online Server (OOS) Integration
New-SPWOPIBinding -ServerName "oos.contoso.com"
Set-SPWOPIZone -Zone "internal-http"

# 8. IIS Configuration Example
Import-Module WebAdministration
Set-ItemProperty "IIS:\Sites\SharePoint - 80" -Name bindings -Value @{protocol="http";bindingInformation="*:80:"}
```

---

### 🗺️ **Visual Architecture Diagram**

Below is a conceptual diagram of the SharePoint 2016 SE environment and its integrations:

```mermaid
graph TD
    A[SharePoint 2016 SE] --> B[SQL Server]
    A --> C[Managed Metadata Service]
    A --> D[Search Service]
    A --> E[User Profile Service]
    A --> F[Secure Store Service]
    A --> G[Office Online Server]
    A --> H[Power Automate (via Data Gateway)]
    A --> I[IIS]
    H -.->|Limited Triggers/Actions| A
    G -->|WOPI Binding| A
```

> **Note:** Adjust the script and diagram to match your actual server names, accounts, and network topology.



### 🔄 **2. Power Automate Integration**

SharePoint 2016 is on-premises, so to use **Power Automate**, you need to:

- Set up a **Data Gateway** to bridge cloud services with on-premises data.
- Register your SharePoint 2016 site in **Power Automate** using the gateway.

> Note: Only limited triggers/actions are available for on-prem SharePoint in Power Automate [3](https://answers.microsoft.com/en-us/msoffice/forum/all/connect-sharepoint-2016-with-powerapps-and-power/3b4ace2d-fda0-4c20-abb1-84b23dcfadf1).



### 🧠 **3. Managed Metadata Service (MMS)**

To configure MMS via PowerShell:

```powershell
New-SPManagedMetadataServiceApplication -Name "Managed Metadata Service" -ApplicationPool "SharePoint Service App Pool" -DatabaseName "SP_MMS_DB"
New-SPManagedMetadataServiceApplicationProxy -Name "Managed Metadata Service Proxy" -ServiceApplication "Managed Metadata Service"
```



### 🔍 **4. Search Service Application**

```powershell
New-SPEnterpriseSearchServiceApplication -Name "Search Service" -ApplicationPool "SharePoint Service App Pool" -DatabaseName "Search_DB"
New-SPEnterpriseSearchServiceApplicationProxy -Name "Search Proxy" -ServiceApplication "Search Service"
```



### 👤 **5. User Profile Service (UPS)**

UPS setup is more complex and includes:

- Creating the UPS service app
- Starting the **User Profile Synchronization Service**
- Configuring synchronization connections

```powershell
New-SPProfileServiceApplication -Name "User Profile Service" -ApplicationPool "SharePoint Service App Pool" -ProfileDBName "Profile_DB" -SocialDBName "Social_DB" -ProfileSyncDBName "Sync_DB"
```


### 📝 **6. Office Online Server (OOS) Integration**

- Install and configure OOS separately.
- Use PowerShell to bind OOS to SharePoint:

```powershell
New-SPWOPIBinding -ServerName "oos.contoso.com"
Set-SPWOPIZone -Zone "internal-http"
```


### 🔐 **7. Secure Store Service**

```powershell
New-SPSecureStoreServiceApplication -Name "Secure Store Service" -ApplicationPool "SharePoint Service App Pool" -DatabaseName "SecureStore_DB"
New-SPSecureStoreServiceApplicationProxy -Name "Secure Store Proxy" -ServiceApplication "Secure Store Service"
```



### 🌐 **8. IIS Configuration**

While IIS is mostly managed via GUI, you can automate tasks like:

```powershell
Import-Module WebAdministration
Set-ItemProperty "IIS:\Sites\SharePoint - 80" -Name bindings -Value @{protocol="http";bindingInformation="*:80:"}
```

---

### ✅ **Next Steps**

### 🌐 **8. Visual Architecture**

![SharePoint 2016 SE Architecture](./SharePoint2016SE-Architecture.png)



[1](https://learn.microsoft.com/en-us/sharepoint/sharepoint-powershell): <https://learn.microsoft.com/en-us/sharepoint/sharepoint-powershell>  
[2](https://www.sphammad.com/abcd-of-powershell-automating-sharepoint-2016-installation/): <https://www.sphammad.com/abcd-of-powershell-automating-sharepoint-2016-installation/>  
[3](https://answers.microsoft.com/en-us/msoffice/forum/all/connect-sharepoint-2016-with-powerapps-and-power/3b4ace2d-fda0-4c20-abb1-84b23dcfadf1): <https://answers.microsoft.com/en-us/msoffice/forum/all/connect-sharepoint-2016-with-powerapps-and-power/3b4ace2d-fda0-4c20-abb1-84b23dcfadf1>

