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
    try:
        edupage = Edupage()
        edupage.login(USERNAME, PASSWORD, EDUPAGE_SUBDOMAIN)
        print("Prihlásenie na EduPage bolo úspešné!")

        # Určíme dátum pre kontrolu (ak je po 15:00, pozeráme zajtrajšok, inak dnešok)
        now = datetime.now()
        target_date = now.date()
        if now.hour >= 15:
            target_date = now.date() + timedelta(days=1)

        # Získame suplovanie pre daný dátum
        substitutions = edupage.get_substitutions(target_date)

        changes = []
        if substitutions:
            for sub in substitutions:
                # Kontrola, či sa zmena týka našej triedy alebo všetkých
                sub_class = getattr(sub, 'class_name', '') or str(getattr(sub, 'classes', ''))
                
                # Ak zmena obsahuje našu triedu alebo trieda nie je špecifikovaná (všeobecný oznam)
                if not TARGET_CLASS or TARGET_CLASS in sub_class or not sub_class:
                    period = getattr(sub, 'period', '?')
                    subject = getattr(sub, 'subject', 'Zmena')
                    room = getattr(sub, 'room', '')
                    note = getattr(sub, 'comment', 'Suplovanie')
                    group = getattr(sub, 'group', '')

                    full_note = f"{note}" if not group else f"{group}: {note}"

                    changes.append({
                        "period": period,
                        "subject": str(subject),
                        "room": str(room) if room else "",
                        "note": str(full_note)
                    })

        # Ak sa cez get_substitutions nič nenašlo, skúsim vybrať všetky aktuálne suplovania bez filtra dátumu
        if not changes:
            all_subs = edupage.get_substitutions()
            if all_subs:
                for sub in all_subs:
                    sub_class = getattr(sub, 'class_name', '') or str(getattr(sub, 'classes', ''))
                    if not TARGET_CLASS or TARGET_CLASS in sub_class:
                        changes.append({
                            "period": getattr(sub, 'period', '?'),
                            "subject": str(getattr(sub, 'subject', 'Zmena')),
                            "room": str(getattr(sub, 'room', '')),
                            "note": str(getattr(sub, 'comment', 'Suplovanie'))
                        })

        output_data = {
            "has_changes": len(changes) > 0,
            "date": target_date.strftime("%d.%m.%Y"),
            "changes": changes
        }

        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Súbor suplovanie.json bol uložený pre dátum {target_date}. Nájdených zmien: {len(changes)}")

    except Exception as e:
        print(f"Chyba pri sťahovaní z EduPage: {e}")
        with open("suplovanie.json", "w", encoding="utf-8") as f:
            json.dump({"has_changes": False, "changes": []}, f)

if __name__ == "__main__":
    main()
