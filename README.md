## Projektidee: Bookjournal – Deine persönliche Lesebibliothek
Viele Leserinnen und Leser möchten ihre gelesenen Bücher, Notizen und Gedanken zentral verwalten, reflektieren und jederzeit abrufen können. Informationen werden oft in verschiedenen Notizbüchern, Apps oder auf Zetteln festgehalten, was unübersichtlich ist. Die Web-App bietet eine übersichtliche, digitale Lösung, um Bücher zu katalogisieren, Lesefortschritt zu verfolgen und persönliche Notizen oder Reflexionen zu speichern.

## Ausgangslage
BookJournal ist eine Web-App, mit der, der Nutzer: Bücher erfassen und Details wie Titel, Autor und Status (gelesen, aktuell, geplant) eintragen kann.
Notizen zu Büchern hinterlegen
Lesefortschritt verfolgen
Das Problem, das gelöst wird: Zentrale Sammlung aller Leseaktivitäten und Notizen

## Ansichten der APP
Übersicht:                  Übersicht der Bücher: Buchtitel, Autor, Schnellnavigation zu Büchern
Buchdetails:                Alle Informationen zu einem Buch werden angezeigt: Titel, Autor
Journal / Notizen:          Freitext-Notizen zu Büchern oder eigenen Gedanken
Dashboard:                  Veranschaulichung Anzahl Büchern und in welchem Status

## Daten
Eingelesen: Buchdetails (Titel, Autor), Notizen, Lesestatus
Gespeichert: Datum der Einträge, Buchinformationen, Notizen
Ausgegeben: Buchübersicht, Notizen, Lesestatus

## Funktionen für den Nutzer
Bücher hinzufügen, bearbeiten, löschen
Notizen erfassen

## Umsetzung mit Flask
Backend:        Flask (Python) für Routing und Logik
Frontend:       HTML/CSS 

## Benutzerführung & Funktionen der App
Bei der erstmaligen Nutzung der App muss sich der Nutzer registrieren. Dafür gibt er einen Benutzernamen sowie ein selbst gewähltes Passwort ein. Nach erfolgreicher Registrierung kann sich der Nutzer über die Login-Seite mit seinem Benutzernamen und Passwort anmelden.

Nach erfolgreichem Login wird der Nutzer auf die Hauptseite der App weitergeleitet. Dort stehen ihm insgesamt vier Navigationspunkte zur Verfügung.

Über den Menüpunkt „Buch hinzufügen“ kann der Nutzer neue Bücher erfassen. Beim Hinzufügen eines Buches werden der Titel, der Autor sowie der Status angegeben. Der Status kann dabei zwischen „Geplantes Buch“, „Aktuelles Buch“ und „Abgeschlossenes Buch“ gewählt werden. Dieser Status kann jederzeit nachträglich geändert werden.

Unter dem Navigationspunkt „Übersicht“ erhält der Nutzer eine Liste aller erfassten Bücher und kann die aktuellen Buchtitel einsehen.

Im Bereich „Dashboard“ wird eine grafische Übersicht der Bücher angezeigt. Die Bücher werden dabei nach ihrem jeweiligen Status gruppiert und visuell dargestellt, sodass der Nutzer einen schnellen Überblick über seine Leseaktivitäten erhält.

Über die Logout-Funktion kann sich der Nutzer jederzeit aus der App abmelden und wird anschließend wieder auf die Login-Seite weitergeleitet.
