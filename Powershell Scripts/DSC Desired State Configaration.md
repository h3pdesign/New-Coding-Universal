# Desired State Configuration (DSC): Grundlagen und Funktionsweise

PowerShell 4.0 führte eine dekla­rative Erwei­terung zur Konfi­guration von System­ein­stel­lun­gen ein. Damit lassen sich nicht nur Windows und Linux, sondern auch Anwen­dungen wie SQL Server oder Share­Point an­passen. DSC kann GPOs und an­dere Deploy­ment-Tools ersetzen.
Für verschiedene Deployment-Szenarien hat es sich eingebürgert, dass Admins ein so genanntes Golden Image erstellen, das bereits alle Rollen und Features für bestimmte Aufgaben enthält. Beispiele wären etwa der Einsatz von Windows Server als Web-Server oder Hyper-V-Host. Ein solcherart angepasstes Systemabbild wird dann auf die Zielrechner verteilt.

## Dynamische Anpassung des OS

Darauf kann man beim Einsatz von DSC verzichten, weil  sie in der Lage ist, die notwendige Funktionalität während der Laufzeit hinzu­zufügen. Als Ausgangspunkt reicht ihr somit eine Standard­installation des OS von einer unmodi­fizierten ISO oder WIM.
Neben dem dynamischen Aktivieren oder Entfernen von Komponenten konfiguriert DSC alle möglichen Einstellungen. Diese Aufgabe kommt traditionell den Gruppen­richtlinien zu, die GPOs in regel­mäßigen Intervallen auf Änderungen prüfen und sie auf ein laufendes System anwenden.
Das DSC-Gegenstück zu den Client Side Extensions der Gruppen­richtlinien ist der so genannte Local Configuration Manager, der eine Konfiguration auf dem Zielrechner implementiert und überwacht. Im Unterschied zu den Group Policies lässt er sich über Push- und Pull-Mechanismen füttern.

## Konfiguration über das Web verteilen

Für wenige Rechner reicht es aus, wenn man eine Konfiguration auf die Ziel-PCs kopiert und dort mit dem Cmdlet Start-DscConfiguration anwendet.

![Powershell DSC Pull/Push](https://www.windowspro.de/sites/windowspro.de/files/imagepicker/3/powershell-dsc-pull-push.png)

Für größere Umgebungen richtet man dagegen einen Pull-Server ein, von dem die betreffenden Systeme ihre Konfiguration regelmäßig abrufen. Dafür benötigt man auf der einen Seite einen spezifisch angepassten Web-Server, während man auf dem Client die DSC auf den Pull-Server ausrichten muss.
Bedeutungsverlust für AD DS und GPOs
Im Unterschied zu den Gruppen­richtlinien hängt die Desired State Configuration nicht von Domänen­diensten des Active Directory ab. Sie greifen somit auch auf Workgroup-Rechnern oder Nicht-Microsoft-Systemen wie Linux und lassen sich über die Cloud an jeden beliebigen Standort verteilen.
Die Weichenstellung von Microsoft in Richtung DSC kann man am Beispiel Nano Server erkennen. Diese superschlanke Installations­variante unterstützt keine Gruppen­richtlinien mehr. Wer dort die exportierten lokalen Richtlinien eines Rechners nicht manuell auf einen anderen übertragen möchte, sollte zu den DSC greifen.

## Konfiguration erstellen

Mit DSC erhielt PowerShell das neue Keyword configuration. Im Prinzip handelt es sich dabei um eine spezielle function, die wie gewohnt durch Ausführen des Scripts geladen wird. Wenn man sie anschließend aufruft, dann schreibt sie die im Script enthaltene Konfiguration in eine so genannte MOF-Datei. Diese wird dann auf die Zielsysteme übertragen.

Innerhalb des configuration-Abschnitts legt man die gewünschten Einstellungen durch Einträge in der Form von `Name = Wert` fest. Damit man überhaupt weiß, welche Einstellungen und Werte man beispielsweise für das Einrichten lokaler Benutzer­konten oder das Schreiben von Registry-Einträgen verwenden kann, stellt DSC diese Informationen über so genannte Resources zur Verfügung.
Wenn man so möchte, handelt es sich bei den Resources um das Gegenstück zu den ADMX-Dateien der Gruppen­richtlinien. Sie liegen aber nicht als XML-Dateien vor, sondern als PowerShell-Module. Deshalb lassen sich die Namen der Einstellungen in der PowerShell_ISE auch über IntelliSense automatisch vervollständigen.

Zum Lieferumfang von Windows gehören nur ein paar Ressourcen, die man durch den Aufruf von `Get-DscResource` anzeigen kann. Möchte man den Inhalt einer bestimmten Ressource ausgeben, um die verfügbaren Einstellungen, ihren Datentyp und mögliche Werte zu ermitteln, gibt man im Fall von User
`Get-DscResource -Name "User" | Select-Object -ExpandProperty Properties`
ein.

Die meisten Ressourcen stehen online zur Verfügung und lassen sich über die OneGet-Funktionen auflisten, herunterladen und installieren. Wenn man mit
`Find-Module -Tag DSCResourceKit`
das erste Mal nach Einträgen im Resource Kit sucht, dann muss man auf Nachfrage von PowerShell einen eigenen Provider für diesen Zweck installieren. Ein weiteres Repository findet man auf Github.

![Repository](https://www.windowspro.de/sites/windowspro.de/files/imagepicker/3/powershell-dsc-resource-kit.png)

Um etwa das Modul für Windows Defender zu installieren, würde man anschließend
`Install-Module -Name xDefender`
aufrufen und mit
`Get-DscResource -Name xMpPreference  | Select-Object -ExpandProperty Properties`
die darin enthaltenen Einstellungen anzeigen. Im Unterschied zu den integrierten Modulen muss man die selbst hinzu­gefügten Ressourcen mittels`Import-DscResource explizit` hinzufügen.

* [Desired State Configuration: Zielsysteme festlegen mit ConfigurationData](https://www.windowspro.de/script/desired-state-configuration-zielsysteme-festlegen-configurationdata)
* [Desired State Configuration: Nodes und configuration mit Parametern anpassen](https://www.windowspro.de/script/desired-state-configuration-nodes-configuration-parametern-anpassen)
* [Test-DscConfiguration, DSCEA: Konfiguration von PCs remote überprüfen](https://www.windowspro.de/wolfgang-sommergut/test-dscconfiguration-dscea-konfiguration-pcs-remote-ueberpruefen)
* [Anleitung: SMB v1 mit Desired State Configuration deinstallieren oder deaktivieren](https://www.windowspro.de/script/anleitung-desired-state-configuration-fuer-smb1-erstellen-anwenden)
* [New-SelfSignedCertificate: Selbstsignierte Zertifikate ausstellen mit PowerShell](https://www.windowspro.de/script/new-selfsignedcertificate-selbstsignierte-zertifikate-ausstellen-powershell)