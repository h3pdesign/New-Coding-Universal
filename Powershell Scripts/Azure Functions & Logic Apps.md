# Functions im Vergleich zu Logic Apps

Sowohl mit Functions als auch mit Logic Apps können komplexe Orchestrierungen erstellt werden. Eine Orchestrierung ist eine Sammlung von Funktionen oder Schritten, die zum Erledigen einer komplexen Aufgabe ausgeführt werden. Mit Azure Functions schreiben Sie Code, um jeden Schritt auszuführen. Mit Logik-Apps verwenden eine grafische Benutzeroberfläche, um die Aktionen und deren Beziehungen untereinander zu definieren.

In einer Orchestrierung können die Dienste nach Belieben miteinander kombiniert werden. Sie können also Funktionen in Logik-Apps aufrufen und umgekehrt. Nachstehend sind einige allgemeine Unterschiede aufgeführt, die es zwischen diesen beiden gibt.

- |Functions | Logic Apps |
---------|---------|----------|---------
 Zustand | Normalerweise zustandslos, aber Durable Functions bieten einen Zustand | Zustandsbehaftet
 Entwicklung | Code First (imperativ) | Designer First (deklarativ)
 Konnektivität | Etwa ein Dutzend integrierte Bindungstypen. Schreiben Sie Code für benutzerdefinierte Bindungen. | Umfangreiche Sammlung von Connectors, Enterprise Integration Pack für B2B-Szenarien, Erstellen von benutzerdefinierten Connectors.
Aktionen |Jede Aktivität ist eine Azure-Funktion. Schreiben Sie Code für Aktivitätsfunktionen.|Umfangreiche Sammlung vorgefertigter Aktionen
Überwachung|Azure Application Insights|Azure-Portal, Log Analytics
Verwaltung|REST-API, Visual Studio|Azure-Portal, REST-API, PowerShell, Visual Studio
Ausführungskontext|Kann lokal oder in der Cloud ausgeführt werden.|Kann nur in der Cloud ausgeführt werden.