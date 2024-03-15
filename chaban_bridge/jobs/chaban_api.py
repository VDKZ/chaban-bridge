# Built-in
from datetime import date, timedelta
from typing import Any, Dict

# Third-party
import requests

CHABAN_URL = "https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=20"
DAYS = 5


def chaban_api() -> Dict[str, Any]:
    response = requests.get(CHABAN_URL)
    if response.status_code != 200:
        print(
            f"Error status {response.status_code} during call to Chaban bridge api call"
        )
        return {"status": f"error status {response.status_code}"}

    data = response.json()

    results: Dict[str, Any] = {}
    today = date.today()
    start_date = today.strftime("%Y-%m-%d")
    date_delta = date.today() + timedelta(days=DAYS)
    end_date = date_delta.strftime("%Y-%m-%d")

    if "results" not in data:
        print("Error, no data for Chaban bridge API")
        return {"status": "Error, no data for Chaban bridge API"}

    for event in data["results"]:
        open_date = event.get("date_passage", None)
        is_closed = event.get("fermeture_totale", None)
        close_start = event.get("fermeture_a_la_circulation", None)
        close_end = event.get("re_ouverture_a_la_circulation", None)

        if open_date <= end_date and open_date >= start_date and is_closed == "oui":
            closing_hours = {
                "fermeture_a_la_circulation": close_start,
                "re_ouverture_a_la_circulation": close_end,
            }
            if event["date_passage"] in results:
                results[event["date_passage"]].append(closing_hours)
            else:
                results[event["date_passage"]] = [closing_hours]

    return results
