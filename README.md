# Outlook zu Jira Jump-Server

Dieser kleine Python-Server dient als Brücke (Proxy) zwischen Outlook-E-Mails und Jira-Webhooks.
Da in Outlook aus Sicherheitsgründen kein JavaScript ausgeführt werden kann (und somit oft keine direkten POST-Requests aus Buttons in der Mail möglich sind), nimmt dieser Server einfache Klicks aus einer E-Mail (GET- oder POST-Requests) entgegen und wandelt sie in einen formatierten POST-Request für Jira um.

## 🚀 Schritt-für-Schritt Anleitung

### 1. Voraussetzungen

Du benötigst auf deinem System:
- **Python 3** (Am besten Version 3.8 oder neuer)

### 2. Projekt klonen / herunterladen

Stelle sicher, dass du dich im Ordner dieses Projekts befindest. Öffne ein Terminal (z.B. PowerShell oder Eingabeaufforderung) und navigiere in das Projektverzeichnis:
```cmd
cd c:\Users\Benni\Documents\jump-server
```

### 3. Abhängigkeiten installieren

Bevor du den Server das erste Mal starten kannst, müssen die benötigten Python-Pakete (`Flask` und `requests`) installiert werden.
Führe dazu folgenden Befehl aus:

```cmd
pip install -r requirements.txt
```

### 4. Konfiguration (URL anpassen)

In diesem Ordner findest du eine Datei namens `config.json`.
Öffne diese mit einem beliebigen Texteditor. Sie sieht ungefähr so aus:

```json
{
    "JIRA_WEBHOOK_URL": "https://deine-domain.atlassian.net/rest/webhooks/1.0/webhook/deine-id"
}
```

- Ersetze den Wert `"https://deine-domain.atlassian.net/..."` durch **deine echte Jira-Webhook URL**.
- Speichere die Datei ab.

*(Tipp: Um den Server auch ohne Neuschreiben der Datei betreiben zu können, akzeptiert der Server auch eine einfache Systemumgebungsvariable `JIRA_WEBHOOK_URL`).*

### 5. Den Server starten

Sobald die Konfiguration hinterlegt ist und die Abhängigkeiten installiert sind, kannst du den Server starten:

```cmd
python server.py
```

Wenn alles erfolgreich war, siehst du im Terminal eine Ausgabe, die dir sagt, dass der Server auf Port `5000` läuft (z. B. `* Running on http://127.0.0.1:5000`).
Lass dieses Terminalfenster offen, solange der Server erreichbar sein soll.

### 6. Testen!

Du kannst nun in deinem Browser oder in deiner Outlook-E-Mail einen Link wie den folgenden verwenden:

```
http://localhost:5000/trigger-webhook?action=approve&ticket=JIRA-123
```

Sobald du (oder ein anderer Nutzer) darauf klickt, schnappt sich dieser Jump-Server die Anfrage und sendet die Parameter (`action=approve` und `ticket=JIRA-123`) als Payload in einem POST-Request an dein Jira.
Als Antwort erhältst du im Browser eine grüne Bestätigungsseite.

---

### Fehlerbehebung

- **Server startet nicht:** Hast du Schritt 3 (`pip install -r requirements.txt`) ausgeführt?
- **Rote "Fehler bei Jira" Seite nach dem Klick:** Dein Jira hat die Anfrage abgelehnt. Hast du in der `config.json` beachtet, deine richtige URL einzutragen? Checke auch den genauen Statuscode in der Fehlermeldung (z.B. `404` wenn die URL gar nicht existiert).
- **Die Konfiguration in `config.json` wurde geändert, aber der Server nutzt immer noch die alte URL:** Der Server liest die Datei beim Starten ein. Beende den Server kurz mit `STRG + C` im Terminal und starte ihn mit `python server.py` einfach neu.
