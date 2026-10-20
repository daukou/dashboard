import json
import os
from datetime import datetime, timedelta
from edupage_api import Edupage

# === DÔLEŽITÉ: VYPLŇ SVOJE ÚDAJE ===
EDUPAGE_SUBDOMAIN = "spseke"  # iba časť pred .edupage.org (napr. spseke)
USERNAME = "DavidLukac48"
PASSWORD = "Davidko369*"
TARGET_CLASS = "III.A"  # Tvoja trieda tak, ako sa zobrazuje na EduPage

def main():
    debug_log = []
    try:
        edupage = Edupage()
        edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
        debug_log.append("Prihlasenie prebehlo uspesne.")

        now = datetime.now()
        target_date = now.date()
        if now.hour >= 15:
            target_date = now.date() + timedelta(days=1)
            
        debug_log.append(f"Hladam suplovanie pre datum: {target_date}")

        substitutions = edupage.get_substitutions(target_date)
        
        raw_data = []
        if substitutions:
            for sub in substitutions:
                # Vytiahneme kompletne vsetky surova data o kazdom suplovani
                raw_data.append(str(getattr(sub, '__dict__', repr(sub))))

        # Ulozime vsetko do JSONu bez akehokolvek filtrovania
        output_data = {
            "has_changes": False,
            "debug_log": debug_log,
            "total_found": len(raw_data),
            "raw_data": raw_data,
            "changes": []
        }

        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        # Ak nastane chyba (napr. zlyhalo prihlasenie), zapiseme ju do suboru
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
