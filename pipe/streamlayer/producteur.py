import requests
import json
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import configs.config as config


producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(2, 6, 0)
)

# Retroune tableau des valeurs historique d'un ticker
# Exemple : get_polygon_historic_data("AAPL", 1, "day", "2024-01-01", "2025-03-01")
def get_polygon_historic_data(ticker, multiplier, timespan):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=2)

    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_str}/{to_str}?adjusted=true&sort=asc&apiKey={config.API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            return data["results"]
    return None


def run_producer():
    while True:
        print(f"[Producteur] Envoi des données de Polygon.io ({config.TICKER}) vers Kafka '{config.KAFKA_TOPIC}'...")
        results = get_polygon_historic_data(config.TICKER, config.MULTIPLIER, config.TIMESTAMP)
        if results:
            for result in results:
                message = {
                    "ticker": config.TICKER,
                    "timestamp": result.get("t"),
                    "open": result.get("o"),
                    "close": result.get("c"),
                    "high": result.get("h"),
                    "low": result.get("l"),
                    "volume": result.get("v"),
                    "number_of_trades": result.get("n"),
                }
                print("Données envoyées à Kafka :", message)
                producer.send(config.KAFKA_TOPIC, value=message)
        else:
            print("Pas de résultats dans la réponse.")
        # Pause avant la prochaine requête
        time.sleep(config.INTERVAL)
