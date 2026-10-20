import json
import os
import time
import traceback
from datetime import datetime, timedelta
from edupage_api import Edupage

# Namiesto hesla v kóde načítame z prostredia alebo použi svoje údaje
EDUPAGE_SUBDOMAIN = "spseke"  # iba časť pred .edupage.org (napr. spseke)
USERNAME = "DavidLukac48"
PASSWORD = "Davidko369*"
TARGET_CLASS = "III.A"  # Tvoja trieda tak, ako sa zobrazuje na EduPage

def main():
    edupage = Edupage()
    edupage.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    logged_in = False
    for attempt in range(1, 4):
        try:
            print(f"Pokus o prihlásenie č. {attempt}...")
            edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
            logged_in = True
            print("Prihlásenie bolo úspešné!")
            break
        except Exception as e:
            print(f"Pokus {attempt} zlyhal: {e}")
            time.sleep(10)

    if not logged_in:
        print("Pripojenie zlyhalo. Ponechávam predchádzajúci súbor suplovanie.json bez prepísania.")
        return

    now = datetime.now()
    target_date = now.date()
    if now.hour >= 15:
        target_date = now.date() + timedelta(days=1)

    print(f"Načítavam suplovanie pre dátum: {target_date}")
    changes_data = edupage.get_timetable_changes(target_date)

    changes = []
    if changes_data:
        for item in changes_data:
            item_str = str(item)
            if not TARGET_CLASS or TARGET_CLASS in item_str or "všetky" in item_str.lower():
                period = getattr(item, 'period', '?')
                subject = getattr(item, 'subject', 'Zmena')
                room = getattr(item, 'room', '')
                note = getattr(item, 'comment', item_str)
                
                if hasattr(subject, 'name'):
                    subject = subject.name
                if hasattr(room, 'name'):
                    room = room.name

                changes.append({
                    "period": str(period),
                    "subject": str(subject),
                    "room": str(room) if room else "",
                    "note": str(note)
                })

    output_data = {
        "has_changes": len(changes) > 0,
        "date": target_date.strftime("%d.%m.%Y"),
        "changes": changes
    }

    with open("suplovanie.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Súbor uloženie dokončené pre dátum {target_date}. Nájdených zmien: {len(changes)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Chyba: {e}")
