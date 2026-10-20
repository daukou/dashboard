import json
import traceback
from datetime import datetime, timedelta
from edupage_api import Edupage

# === DÔLEŽITÉ: VYPLŇ SVOJE ÚDAJE ===
EDUPAGE_SUBDOMAIN = "spseke"  # iba časť pred .edupage.org (napr. spseke)
USERNAME = "DavidLukac48"
PASSWORD = "Davidko369*"
TARGET_CLASS = "III.A"  # Tvoja trieda tak, ako sa zobrazuje na EduPage

def main():
    try:
        edupage = Edupage()
        edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
        print("Prihlásenie na EduPage bolo úspešné!")

        now = datetime.now()
        target_date = now.date()
        if now.hour >= 15:
            target_date = now.date() + timedelta(days=1)

        # Načítanie zmien v rozvrhu (suplovania) pre cieľový dátum
        changes_data = edupage.get_timetable_changes(target_date)

        changes = []
        if changes_data:
            for item in changes_data:
                item_str = str(item)
                
                # Kontrola, či sa zmena týka III.A alebo je všeobecná
                if not TARGET_CLASS or TARGET_CLASS in item_str or "všetky" in item_str.lower():
                    period = getattr(item, 'period', '?')
                    subject = getattr(item, 'subject', 'Zmena')
                    room = getattr(item, 'room', '')
                    note = getattr(item, 'comment', item_str)
                    
                    # Ak je predmet/skupina v kódovom objekte, prevedieme na string
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

        print(f"Súbor uloženie dokončené pre dátum {target_date}. Našlo sa zmien: {len(changes)}")

    except Exception as e:
        print(f"Chyba: {e}")
        error_data = {
            "has_changes": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "changes": []
        }
        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(error_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
