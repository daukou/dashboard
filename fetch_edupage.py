import json
import re
import time
import traceback
from datetime import datetime, timedelta
from edupage_api import Edupage

EDUPAGE_SUBDOMAIN = "spseke"  # iba časť pred .edupage.org (napr. spseke)
USERNAME = "DavidLukac48"
PASSWORD = "Davidko369*"
TARGET_CLASS = "III.A"  # Tvoja trieda tak, ako sa zobrazuje na EduPage

def main():
    logged_in = False
    edupage = None
    
    # Zvýšený počet pokusov na 5, pri každom vytvoríme úplne nové pripojenie
    for attempt in range(1, 6):
        try:
            print(f"Pokus o prihlásenie č. {attempt}...")
            edupage = Edupage()
            edupage.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
            logged_in = True
            print("Prihlásenie bolo úspešné!")
            break
        except Exception as e:
            print(f"Pokus {attempt} zlyhal: {e}")
            time.sleep(10) # Počkáme 10 sekúnd, kým to skúsime znova

    if not logged_in or not edupage:
        raise ConnectionError("Nepodarilo sa nadviazať spojenie s EduPage serverom ani po 5 pokusoch.")

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
                lesson_match = re.search(r"lesson_n=(\d+)", item_str)
                period = lesson_match.group(1) if lesson_match else "?"

                title_match = re.search(r"title='([^']+)'", item_str)
                title_text = title_match.group(1) if title_match else item_str

                subj_match = re.search(r"([A-Z0-9]{2,5})\s*-", title_text)
                subject = subj_match.group(1) if subj_match else "Zmena"

                changes.append({
                    "period": int(period) if period.isdigit() else period,
                    "subject": subject,
                    "info": title_text
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
        error_data = {
            "has_changes": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "changes": []
        }
        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(error_data, f, ensure_ascii=False, indent=2)
