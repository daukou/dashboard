import json
import time
import traceback
from datetime import datetime, timedelta
from edupage_api import Edupage

EDUPAGE_SUBDOMAIN = "spseke"  # iba časť pred .edupage.org (napr. spseke)
USERNAME = "DavidLukac48"
PASSWORD = "Davidko369*"
TARGET_CLASS = "III.A"  # Tvoja trieda tak, ako sa zobrazuje na EduPage

def main():
    edupage = Edupage()
    edupage.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    logged_in = False
    for attempt in range(1, 4):
        try:
            edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
            logged_in = True
            break
        except Exception:
            time.sleep(3)

    if not logged_in:
        raise ConnectionError("Spojenie zlyhalo.")

    now = datetime.now()
    target_date = now.date()
    if now.hour >= 15:
        target_date = now.date() + timedelta(days=1)

    changes_data = edupage.get_timetable_changes(target_date)

    raw_changes = []
    if changes_data:
        for item in changes_data:
            item_str = str(item)
            if not TARGET_CLASS or TARGET_CLASS in item_str or "všetky" in item_str.lower():
                raw_changes.append(item_str)

    output_data = {
        "has_changes": len(raw_changes) > 0,
        "date": target_date.strftime("%d.%m.%Y"),
        "raw_changes": raw_changes
    }

    with open("suplovanie.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_data = {
            "has_changes": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "raw_changes": []
        }
        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(error_data, f, ensure_ascii=False, indent=2)
