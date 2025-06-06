# Configuration pour l'API Polygon.io
API_KEY="xw6P36oWUqTKQQk8pMmdDBjY93u5Tn2W"
TICKER="AAPL"
# TICKER="X:BTCUSD"
FROM_DATE = "2024-01-01"
TO_DATE = "2025-06-03"
MULTIPLIER = 1
TIMESTAMP = "hour"  # minute, hour, day
INTERVAL=900 # 15 minutes

# Configuration pour Kafka
KAFKA_TOPIC="polygon-data"
KAFKA_BROKER="localhost:9092"
KAFKA_GROUP_ID="polygon-consumer-group"

# Configuration pour Elasticsearch
ES_HOST="http://localhost:9200"
ES_INDEX="polygon-aapl"

