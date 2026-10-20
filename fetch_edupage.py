import json
import os
from edupage_api import Edupage

# === DÔLEŽITÉ: VYPLŇ SVOJE ÚDAJE ===
EDUPAGE_SUBDOMAIN = "spseke"  # iba časť pred .edupage.org (napr. spseke)
USERNAME = "DavidLukac48"
PASSWORD = "Davidko369*"

def main():
    try:
        # Prihlásenie na EduPage
        edupage = Edupage()
        edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
        print("Prihlásenie na EduPage bolo úspešné!")

        # Stiahnutie suplovania
        substitutions = edupage.get_substitutions()

        changes = []
        if substitutions:
            for sub in substitutions:
                # Načítame detaily suplovania
                period = getattr(sub, 'period', '?')
                subject = getattr(sub, 'subject', 'Zmena')
                room = getattr(sub, 'room', '')
                note = getattr(sub, 'comment', 'Suplovanie')

                changes.append({
                    "period": period,
                    "subject": str(subject),
                    "room": str(room) if room else "",
                    "note": str(note)
                })

        # Príprava dát pre Dashboard
        output_data = {
            "has_changes": len(changes) > 0,
            "changes": changes
        }

        # Uloženie do súboru suplovanie.json
        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Súbor suplovanie.json bol uložený. Nádených zmien: {len(changes)}")

    except Exception as e:
        print(f"Chyba pri sťahovaní z EduPage: {e}")
        # V prípade chyby vytvoríme prázdny súbor, aby dashboard nepadol
        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump({"has_changes": False, "changes": []}, f)

if __name__ == "__main__":
    main()
