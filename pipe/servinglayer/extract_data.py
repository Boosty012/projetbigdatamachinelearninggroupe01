from elasticsearch import Elasticsearch
import configs.config as config
import pandas as pd
import os

# Connexion à Elasticsearch
es = Elasticsearch(config.ES_HOST)

# Requête pour récupérer les données
query = {
    "size": 10000,
    "query": {
        "match_all": {}
    }
}

def extract_data_to_csv():
    try:
        # Exécution de la requête
        results = es.search(config.ES_INDEX, body=query)

        # Extraction des documents
        docs = [hit['_source'] for hit in results['hits']['hits']]

        # Conversion en DataFrame
        df = pd.DataFrame(docs)

        # Chemin du fichier CSV
        csv_path = "../data/data_from_elasticsearch.csv"

        # Si le fichier existe, on lit et on concatène
        if os.path.exists(csv_path):
            old_df = pd.read_csv(csv_path)
            df = pd.concat([old_df, df], ignore_index=True)
            # Optionnel : supprimer les doublons
            df = df.drop_duplicates()

        # Affiche les premières lignes
        print("Aperçu des données extraites :")
        print(df.head())

        # Sauvegarde en CSV
        df.to_csv(csv_path, index=False)
        print("Données enregistrées dans data_from_elasticsearch.csv")
        return True
    except Exception as e:
        print("[Extraction EN CSV] Exception:", e)
        return False
