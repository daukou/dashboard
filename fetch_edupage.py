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

        # Ak je po 15:00, pozrieme sa na zajtrajšok, inak na dnešok
        now = datetime.now()
        target_date = now.date()
        if now.hour >= 15:
            target_date = now.date() + timedelta(days=1)

        substitutions = edupage.get_substitutions(target_date)

        changes = []
        if substitutions:
            for sub in substitutions:
                # Načítame textové údaje zo suplovania
                sub_text = str(sub)
                
                # Ak zmena obsahuje tvoju triedu alebo je všeobecná
                if not TARGET_CLASS or TARGET_CLASS in sub_text or "všetky" in sub_text.lower():
                    period = getattr(sub, 'period', '?')
                    subject = getattr(sub, 'subject', 'Zmena')
                    room = getattr(sub, 'room', '')
                    note = getattr(sub, 'comment', sub_text)

                    changes.append({
                        "period": period,
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

        print(f"Súbor uložený. Nájdených zmien: {len(changes)}")

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
