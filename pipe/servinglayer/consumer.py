import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import configs.config as config
from .extract_data import extract_data_to_csv

# Connexion à Elasticsearch
es = Elasticsearch(config.ES_HOST)
# Le nombre de documents dans l'index
count = 0

consumer = KafkaConsumer(
    config.KAFKA_TOPIC,
    bootstrap_servers=config.KAFKA_BROKER,
    auto_offset_reset='latest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id=config.KAFKA_GROUP_ID,
    api_version=(2, 6, 0)
)

def index_to_elasticsearch(message):
    doc_id = f"{message['ticker']}_{message['timestamp']}"
    es.index(index=config.ES_INDEX, id=doc_id, document=message)
    
def extract_data():
    if count >= 1000:
        try:
            if extract_data_to_csv():
                count = 0
        except Exception as e:
            print("[Extraction] Exception:", e)

def run_consumer():
    try: 
        print("En attente de messages Kafka...")
        if not es.ping():
            print("Elasticsearch ne répond pas.")
            exit()

        for message in consumer:
            data = message.value
            print("Données reçues de Kafka :", data)
            res = index_to_elasticsearch(data)
            print("Donnée insérée dans Elasticsearch :", res['result'])
            count += 1

    except Exception as e:
        print("[Consumer] Exception:", e)
