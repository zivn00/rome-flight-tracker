import requests
import os

def send_telegram_msg(message):
    token = os.getenv('8294553898:AAGzK4YrXwEbluWVdk1_ZlqbLX8hDh3l9uo')
    chat_id = os.getenv('733855231')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_flights():
    print("Step 1: Script started")
    url = "https://data.gov.il/api/3/action/datastore_search"
    resource_id = "e83f7627-746a-43d0-a0f9-c18927011404"
    
    # משוך את 500 הטיסות האחרונות בלי לסנן בשרת
    params = {'resource_id': resource_id, 'limit': 500}

    try:
        print("Step 2: Fetching all recent flights...")
        response = requests.get(url, params=params)
        records = response.json().get('result', {}).get('records', [])
        print(f"Step 3: Found {len(records)} total flights in API.")

        db_file = "seen_flights.txt"
        if os.path.exists(db_file):
            with open(db_file, "r") as f:
                seen_flights = set(f.read().splitlines())
        else:
            seen_flights = set()

        new_found = False
        for flight in records:
            # בדיקה גמישה: מחפשים את רומא באנגלית או בעברית, בכל מקום בשדות המיקום
            loc_en = str(flight.get('CHLOC1EN', '')).upper()
            loc_he = str(flight.get('CHLOC1CH', ''))
            status = str(flight.get('CHRMINE', ''))

            if ('ROME' in loc_en or 'רומא' in loc_he) and "מבוטלת" not in status:
                
                flight_id = f"{flight.get('CHOPER','')}{flight.get('CHFLNR','')}_{flight.get('CHSTOL','')}"
                
                if flight_id not in seen_flights:
                    print(f"Match found! Flight {flight_id}")
                    msg = (f"✈️ *טיסה חדשה מרומא!*\n\n"
                           f"🏢 *חברה:* {flight.get('CHOPER','')}\n"
                           f"🔢 *מספר:* {flight.get('CHFLNR','')}\n"
                           f"⏰ *נחיתה:* {flight.get('CHSTOL','').replace('T', ' ')}\n"
                           f"📍 *סטטוס:* {status}")
                    
                    send_telegram_msg(msg)
                    seen_flights.add(flight_id)
                    new_found = True

        if new_found:
            with open(db_file, "w") as f:
                f.write("\n".join(seen_flights))
        else:
            print("Step 4: No new Rome flights filtered.")

    except Exception as e:
        print(f"Step 5: Error: {e}")

if __name__ == "__main__":
    check_flights()
