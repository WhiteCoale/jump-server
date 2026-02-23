import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lade Konfiguration aus config.json
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

config = load_config()

# JIRA Webhook URL aus config.json (oder als Umgebungsvariable)
JIRA_WEBHOOK_URL = os.environ.get(
    "JIRA_WEBHOOK_URL", 
    config.get("JIRA_WEBHOOK_URL", "https://deine-domain.atlassian.net/rest/webhooks/1.0/webhook/deine-id")
)

@app.route('/trigger-webhook', methods=['GET', 'POST'])
def trigger_webhook():
    """
    Dieser Endpunkt nimmt den Request aus der Outlook-E-Mail entgegen.
    Da Outlook manchmal keine sauberen POST-Requests über einfache Links senden kann (ohne JavaScript), 
    akzeptiert dieser Endpunkt sowohl GET als auch POST.
    Anschließend wird ein POST-Request an Jira weitergeleitet.
    """
    
    # Payload zusammenstellen, die an Jira gesendet wird
    payload = {}
    
    try:
        # Abhängig vom Request-Typ (GET oder POST) die Parameter extrahieren
        if request.method == 'POST':
            if request.is_json:
                payload = request.get_json()
            else:
                payload = request.form.to_dict()
        elif request.method == 'GET':
            payload = request.args.to_dict()
            
        # Optional: Hier können feste Werte ergänzt werden, die Jira erwartet
        # payload['custom_field'] = 'Wert aus E-Mail'

        # Sende den POST-Request an den Jira Webhook
        print(f"Sende Payload an Jira: {payload}")
        
        # Falls es in firmeninternen Netzwerken zu SSL-Zertifikatfehlern kommt,
        # kann hier verify=False übergeben werden. Andernfalls verify=True.
        # Es wird empfohlen, verify=True für Produktivsysteme beizubehalten, 
        # außer es lässt sich lokal nicht anders lösen.
        response = requests.post(JIRA_WEBHOOK_URL, json=payload, verify=False)
        
        # Prüfen, ob Jira den Request erfolgreich angenommen hat
        if response.status_code in [200, 201, 202, 204]:
            # Rückgabe als HTML, da der Benutzer das in seinem Browser sieht, wenn er auf den Button in der Mail klickt
            return """
            <html>
                <head><title>Erfolg</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                    <h2 style="color: green;">Erfolg!</h2>
                    <p>Die Aktion wurde erfolgreich an Jira übermittelt.</p>
                </body>
            </html>
            """, 200
        else:
            return f"""
            <html>
                <head><title>Fehler</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                    <h2 style="color: red;">Fehler bei Jira</h2>
                    <p>Status Code: {response.status_code}</p>
                    <p>{response.text}</p>
                </body>
            </html>
            """, 500

    except Exception as e:
        return f"""
        <html>
            <head><title>Server Fehler</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                <h2 style="color: red;">Interner Server Fehler</h2>
                <p>{str(e)}</p>
            </body>
        </html>
        """, 500

if __name__ == '__main__':
    # Server starten auf Port 5000 (lokal oder auf einem echten Server)
    print("Starte Jump-Server für Outlook zu Jira Webhook...")
    print(f"JIRA_WEBHOOK_URL = {JIRA_WEBHOOK_URL}")
    app.run(host='0.0.0.0', port=5000, debug=True)
