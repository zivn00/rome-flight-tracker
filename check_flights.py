import requests
import os

def send_telegram_msg(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    if not token or not chat_id:
        print("Missing Telegram credentials!")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def check_flights():
    url = "https://data.gov.il/api/3/action/datastore_search"
    resource_id = "e83f7627-746a-43d0-a0f9-c18927011404"
    
    db_file = "seen_flights.txt"
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            seen_flights = set(f.read().splitlines())
    else:
        seen_flights = set()

    params = {
        'resource_id': resource_id,
        'q': 'ROME',
        'limit': 500 
    }

    try:
        response = requests.get(url, params=params)
        records = response.json().get('result', {}).get('records', [])
        
        new_found = False
        for flight in records:
            city_en = flight.get('CHLOC1EN', '').upper()
            status = flight.get('CHRMINE', '')
            
            if 'ROME' not in city_en or "מבוטלת" in status:
                continue

            flight_id = f"{flight.get('CHOPER','')}{flight.get('CHFLNR','')}_{flight.get('CHSTOL','')}"
            
            if flight_id not in seen_flights:
                airline = flight.get('CHOPER', '')
                flight_num = flight.get('CHFLNR', '')
                arrival_time = flight.get('CHSTOL', '').replace('T', ' ')
                
                msg = (f"🚨 *טיסה חדשה מרומא אותרה!* 🚨\n\n"
                       f"✈️ *חברה:* {airline}\n"
                       f"🔢 *מספר טיסה:* {flight_num}\n"
                       f"⏰ *נחיתה:* {arrival_time}\n"
                       f"📍 *סטטוס:* {status}\n\n"
                       f"בדוק עכשיו באתר החברה!")
                
                send_telegram_msg(msg)
                seen_flights.add(flight_id)
                new_found = True

        if new_found:
            with open(db_file, "w") as f:
                f.write("\n".join(seen_flights))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_flights()
