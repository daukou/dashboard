import json
import traceback
import requests
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

        # 1. Skúsime vytiahnuť dáta cez rozvrh/suplovanie v knižnici
        changes = []
        
        # Zistíme dostupné metódy na objekte edupage pre kontrolu
        available_methods = [m for m in dir(edupage) if not m.startswith('_')]
        print(f"Dostupné metódy v Edupage: {available_methods}")

        # Skúsime nájsť metódu pre rozvrh alebo suplovanie
        sub_data = None
        if hasattr(edupage, 'get_timetable'):
            try:
                sub_data = edupage.get_timetable(target_date)
            except Exception as e:
                print(f"get_timetable zlyhal: {e}")

        if hasattr(edupage, 'get_missing_teachers'):
            try:
                sub_data = edupage.get_missing_teachers(target_date)
            except Exception as e:
                print(f"get_missing_teachers zlyhal: {e}")

        # 2. Ak sa nepodarilo cez metódy knižnice, stiahneme JSON endpoint priamo zo školy
        if not changes:
            date_str = target_date.strftime("%Y-%m-%d")
            url = f"https://{EDUPAGE_SUBDOMAIN}.edupage.org/gserver/substitution.r?gserver_function=getsubstitution&date={date_str}"
            
            # Použijeme session z edupage_api, ak existuje, alebo štandardný request
            session = getattr(edupage, 'session', requests.Session())
            res = session.get(url)
            
            if res.status_code == 200:
                try:
                    data = res.json()
                    # Ak EduPage vrátil zmeny v JSON formáte
                    if "rows" in data:
                        for row in data["rows"]:
                            text_row = str(row)
                            if TARGET_CLASS in text_row or not TARGET_CLASS:
                                changes.append({
                                    "period": row.get("period", "?"),
                                    "subject": row.get("header", "Zmena"),
                                    "room": row.get("classroom", ""),
                                    "note": row.get("info", "Suplovanie")
                                })
                except Exception:
                    pass

        output_data = {
            "has_changes": len(changes) > 0,
            "date": target_date.strftime("%d.%m.%Y"),
            "available_methods": available_methods,
            "changes": changes
        }

        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Súbor uloženie dokončené. Zmien: {len(changes)}")

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
