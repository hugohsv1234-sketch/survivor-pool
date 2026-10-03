# So startest du Survivor Pool

Eine vollständige lokale NFL-Survivor-App mit persönlichen Accounts, gemeinsamer
SQLite-Datenbank, serverseitigen Regeln und vorbereiteter PWA-Installation.

## 1. Entpacken und starten

Du benötigst **Python 3.10 oder neuer**. Für die lokale App sind keine zusätzlichen
Python-Pakete, kein Node.js und kein npm-Install nötig.

1. Das ZIP vollständig entpacken.
2. Ein Terminal im Ordner `survivor-pool` öffnen.
3. Den Server starten:

   ```bash
   python3 server.py
   ```

   Unter Windows:

   ```powershell
   py -3 server.py
   ```

4. **http://localhost:8000** im Browser öffnen.
5. Pool-Passwort: **NURDERHSV**.
6. Unter „Demo-Accounts“ auf **Max** klicken oder einen eigenen Account erstellen.

Unter Windows kannst du auch `Start-Windows.bat` doppelklicken. Auf macOS ist
`Start-macOS.command` eine Alternative; falls macOS den Start blockiert, verwende
den Terminal-Befehl oben. Das Terminal muss während der Nutzung geöffnet bleiben.
Beenden: **Strg+C**.

`index.html` im Hauptordner zeigt dieselbe kurze Starthilfe. Die App selbst wird
vom lokalen Server ausgeliefert. Ein Doppelklick auf HTML allein kann keine
serverseitigen Accounts, Sessions oder Regelprüfungen starten.

Falls Port 8000 belegt ist: `python3 server.py --port 8080`, dann
http://localhost:8080 öffnen.

## 2. Die Demo ausprobieren

| Benutzername | Persönliches Passwort | Rolle |
|---|---|---|
| max | Survivor2026! | Administrator |
| lea, tim, nina, finn, ben | Survivor2026! | Spieler |

Die Demo startet in **Week 5**. Der erste Kickoff liegt beim ersten Start ungefähr
zwei Stunden in der Zukunft. Es gibt 32 Teams, 301 fiktive Begegnungen, 22 Spieltage
inklusive Playoffs und Super Bowl sowie bereits ausgewertete Tipps aus Weeks 1–4.
**Spielpläne, Zeiten und Ergebnisse sind ausdrücklich keine echten NFL-Daten.**

Ein schneller Rundgang:

1. Als **Max** auf dem Dashboard die **Ravens** auswählen.
2. Den Bestätigungsdialog abbrechen und danach erneut öffnen und bestätigen.
3. Auf dem Spieltag vor Kickoff auf die **Bengals** wechseln: es bleibt genau ein Tipp.
4. Die **Chiefs** anklicken: bereits verwendet, rot markiert.
5. Die **Dolphins** anklicken: blockiert, weil Max schon dreimal gegen die Patriots
   getippt hat. Die **Patriots selbst** bleiben auswählbar; orange markiert das
   ausgeschöpfte Gegen-Tipp-Kontingent.
6. Unter **Mein Profil → Demo steuern** ein Spiel auswählen und „Kickoff simulieren“.
   Die Demo-Uhr springt zum Kickoff. Ein Tippwechsel ist jetzt auch serverseitig
   gesperrt, selbst zu späteren Spielen. Andere Begegnungen mit demselben Kickoff
   gelten ebenfalls als gestartet.
7. „Spiel beenden“ simuliert einen Sieg, eine Niederlage oder einen Tie. Dashboard,
   Saisonübersicht, Statistik und Bestenliste werden sofort neu ausgewertet.
8. „Nächste Week öffnen“ beendet alle noch offenen Spiele mit 24 : 17 für das
   Auswärtsteam und öffnet den nächsten Spieltag. Es erscheint eine Bestätigung.

Ergebnisse lassen sich während der aktuellen Demo-Week erneut setzen. Ein
abgeschlossener Spieltag wird über die Oberfläche nicht zurückgesetzt.

## 3. Was gespeichert wird

Beim ersten Start entsteht `data/demo.sqlite3`. Alle Accounts, Tipps, Regeln,
Sessions und Demo-Änderungen bleiben bei Neustarts erhalten. Die Session gilt bis
zu 30 Tage; „Abmelden“ beendet sie sofort und schließt auch den Pool-Zugang.

Für eine **frische Demo**: Server beenden, den Ordner `data` umbenennen (z. B.
`data-backup`) und erneut starten. So bleiben deine bisherigen Daten als Kopie
erhalten. Zum Sichern den Server stoppen und den ganzen Datenordner kopieren.

## 4. Regeln

- Genau ein Team pro Benutzer, Saison und Spieltag.
- Jedes gewählte Team höchstens einmal bis einschließlich Super Bowl.
- Höchstens drei Tipps gegen dasselbe Team.
- Ein ungesperrter Tipp darf ersetzt werden. Der alte Tipp wird bei der Prüfung
  von Teamverbrauch und Gegner-Limit ausgenommen.
- Ab dem Kickoff **des bisher ausgewählten Spiels** bleibt der Tipp gesperrt.
  Serverzeit, Spielstatus und persistierte Sperre sind maßgeblich, nicht die
  Uhr oder veränderte Schaltflächen im Browser.
- Ein Sieg zählt richtig, eine Niederlage falsch. Nur abgeschlossene Spiele
  mit zwei gültigen Ergebnissen werden ausgewertet.
- Standard: Ein Tie zählt falsch. Max kann im Profil auf **neutral** umstellen.
  Ein neutraler Tie zählt weder als Sieg noch als Niederlage; das Team bleibt
  verbraucht. Die Erfolgsquote ist Siege / (Siege + Niederlagen).
- Survivor-Status: Die erste Niederlage führt zum Ausscheiden. Standardmäßig
  dürfen ausgeschiedene Spieler für die Bestenliste weiter tippen.
- Standardmäßig führt ein verpasster Spieltag zum Ausscheiden, sobald alle
  nicht abgesagten Spiele begonnen haben. Das gilt erst ab dem Beitrittsspieltag.
- Diese drei Pool-Regeln sind für Administratoren im Profil konfigurierbar.
  Änderungen werten vorhandene Tipps neu aus.
- Bestenliste: richtige Tipps absteigend, danach Anzeigename alphabetisch,
  bei Namensgleichheit Benutzername. Anzahl falscher Tipps ist kein Tiebreaker.
- Tipps anderer Spieler werden erst zu ihrem Kickoff sichtbar.

## 5. App installieren und offline nutzen

Manifest, 192-/512-Pixel-Icons, maskierbares Icon, Startfarbe und Service Worker
sind enthalten. „App installieren“ startet den Browserdialog, sobald dieser
verfügbar ist. Ansonsten zeigt der Button passende Installationshinweise.

- Desktop/Android: Browser-Menü → „App installieren“.
- iPhone/iPad: Safari → Teilen → „Zum Home-Bildschirm“.
- Installation benötigt **localhost oder HTTPS**. Eine einfache HTTP-Adresse
  im WLAN reicht dafür normalerweise nicht.
- Nach dem ersten Laden wird die öffentliche App-Hülle offline verfügbar.
  Bereits auf dem Bildschirm geladene Daten bleiben bei einem Verbindungsabbruch
  sichtbar. Nach einem Offline-Neuladen wird nur der geschützte Eingang gezeigt.
- Private API-Daten und Sessions werden nicht im Service-Worker-Cache gespeichert.
  Offline-Tipps sind gesperrt und werden nicht nachträglich ungeprüft gesendet.

## 6. Auf dem Smartphone lokal testen

PC und Smartphone müssen im selben vertrauenswürdigen WLAN sein. Starte den
Server auf dem PC für die eigene Netzwerk-Adresse. Beispiel, **192.168.1.20
durch die tatsächliche IP ersetzen**:

macOS/Linux:

```bash
POOL_ORIGIN=http://192.168.1.20:8000,http://localhost:8000 python3 server.py --host 0.0.0.0
```

Windows PowerShell:

```powershell
$env:POOL_ORIGIN = "http://192.168.1.20:8000,http://localhost:8000"
py -3 server.py --host 0.0.0.0
```

Auf dem Smartphone `http://192.168.1.20:8000` aufrufen. Alle Geräte nutzen dieselbe
Datenbank auf dem PC. Der lokale HTTP-Server ist zum Testen gedacht. Verwende
für einen öffentlich erreichbaren Pool den dokumentierten HTTPS-Betrieb.

## 7. Tests und Weiterentwicklung

Backend und Regeln testen:

```bash
python3 -m unittest discover -s tests -v
```

Zusätzliche Oberflächenlogik-Tests, optional mit Node.js 20+:

```bash
python3 tests/export_snapshot.py
node tests/test_frontend.cjs
```

Dokumentation:

- [Architektur, Sicherheit und späteres Hosting](docs/ARCHITEKTUR.md)
- [NFL-Feed und Schnittstellen](docs/API.md)
- [Testbericht und Browser-Checkliste](docs/TESTS.md)

Die App nutzt eigene Kürzel-Kacheln statt offizieller Teamlogos. Lizenzierte
Logos können später über `teams.logo` und Dateien in `public/assets/teams/`
ergänzt werden. Externe Schriftarten, Tracking und CDNs sind nicht erforderlich.

Ein privates Fanprojekt; keine offizielle NFL-Anwendung.
