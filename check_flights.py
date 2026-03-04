import requests
import os

def check_flights():
    print("Step 1: Script started") # בדיקה שהסקריפט התחיל
    url = "https://data.gov.il/api/3/action/datastore_search"
    resource_id = "e83f7627-746a-43d0-a0f9-c18927011404"
    
    params = {'resource_id': resource_id, 'q': 'ROME', 'limit': 500}

    try:
        print("Step 2: Connecting to Israel Airport Authority API...")
        response = requests.get(url, params=params)
        data = response.json()
        records = data.get('result', {}).get('records', [])
        
        print(f"Step 3: Found {len(records)} raw records in the API.") # כמה תוצאות חזרו בכלל?

        found_count = 0
        for flight in records:
            city_en = flight.get('CHLOC1EN', '').upper()
            # הדפסה קטנה כדי לראות מה עובר בסינון
            if 'ROME' in city_en:
                print(f"Checking flight: {flight.get('CHFLNR')} | Status: {flight.get('CHRMINE')}")
            
            # כאן יכולה להיות הבעיה - אולי הסטטוס בנתב"ג השתנה?
            status = flight.get('CHRMINE', '')
            if 'ROME' not in city_en or "מבוטלת" in status:
                continue
            
            found_count += 1
            # ... (כאן באה לוגיקת השליחה לטלגרם)
            
        print(f"Step 4: Processed {found_count} valid Rome flights.")

    except Exception as e:
        print(f"Step 5: Error occurred: {e}")

if __name__ == "__main__":
    check_flights()
