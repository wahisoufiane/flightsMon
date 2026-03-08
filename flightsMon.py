import serpapi
import requests
import os

SERPAPI_KEY = os.getenv("API_KEY")
TELEGRAM_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
params = {
  "api_key": SERPAPI_KEY,
  "engine": "google_flights",
  "hl": "en",
  "gl": "us",
  "departure_id": "MED,JED",
  "arrival_id": "SAW,IST,CAI,FCO",
  "outbound_date": "2026-03-19",
  "currency": "USD",
  "type": "2",
  "travel_class": "1",
  "show_hidden": "true",
  "deep_search": "true",
  "sort_by": "2",
  "adults": "1",
  "exclude_conns": "BAH,AMM,KWI,DOH,MCT,BEY,LHR,AUH,DXB,RKT,SHJ",
  "max_price": "400"
}

params2 = {
  "api_key": SERPAPI_KEY,
  "engine": "google_flights",
  "hl": "en",
  "gl": "us",
  "departure_id": "JED,MED",
  "arrival_id": "CMN",
  "outbound_date": "2026-03-19",
  "currency": "USD",
  "type": "2",
  "travel_class": "1",
  "show_hidden": "true",
  "deep_search": "true",
  "sort_by": "2",
  "adults": "1",
  "exclude_conns": "BAH,AMM,KWI,DOH,MCT,BEY,LHR,AUH,DXB,RKT,SHJ",
  "max_price": "600"
}

data = serpapi.search(params)

results = []

for i, option in enumerate(data.get("other_flights", []), start=1):

    flights = option["flights"]

    departure_airport = flights[0]["departure_airport"]["id"]
    arrival_airport = flights[-1]["arrival_airport"]["id"]

    duration = option.get("total_duration")

    layovers = ", ".join([l["id"] for l in option.get("layovers", [])])

    arrival_time = flights[-1]["arrival_airport"]["time"]

    price = option.get("price", "N/A")

    msg = (
        f"Option {i}: {departure_airport} to {arrival_airport} "
        f"- Price {price} - Duration {duration} "
        f"- Layover {layovers} - Arrival time {arrival_time}"
    )

    if price != "N/A":
        results.append(msg)


results.append("-----------------------")

data2 = serpapi.search(params2)

for i, option in enumerate(data2.get("other_flights", []), start=1):

    flights = option["flights"]

    departure_airport = flights[0]["departure_airport"]["id"]
    arrival_airport = flights[-1]["arrival_airport"]["id"]

    duration = option.get("total_duration")

    layovers = ", ".join([l["id"] for l in option.get("layovers", [])])

    arrival_time = flights[-1]["arrival_airport"]["time"]

    price = option.get("price", "N/A")

    msg = (
        f"Option {i}: {departure_airport} to {arrival_airport} "
        f"- Price {price} - Duration {duration} "
        f"- Layover {layovers} - Arrival time {arrival_time}"
    )

    if price != "N/A":
        results.append(msg)

text = "\n".join(results)
print(text)

TOKEN=TELEGRAM_TOKEN
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
)
