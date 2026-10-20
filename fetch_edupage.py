import os
import json
import urllib.request

# Nastavenia EduPage
EDUPAGE_URL = "https://TVOJA_SKOLA.edupage.org" # Uprav na URL tvojej skoly

def get_substitution():
    # Sem pride logika stiahnutia suplovania. 
    # Zatial vratime testovacie data, aby sme overili, ze automatizacia na GitHube funguje.
    sample_data = {
        "has_changes": True,
        "date": "Zajtra",
        "changes": [
            {"period": 2, "subject": "OBP", "room": "24", "note": "Supluje Mgr. Novak"},
            {"period": 4, "subject": "SJL", "room": "Odpadla", "note": "Hodina zrusena"}
        ]
    }
    return sample_data

if __name__ == "__main__":
    data = get_substitution()
    with open("suplovanie.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Suplovanie bolo uspesne ulozene do suplovanie.json")
