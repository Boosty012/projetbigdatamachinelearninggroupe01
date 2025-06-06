# main.py

import threading
from streamlayer.producteur import run_producer
from servinglayer.consumer import run_consumer

if __name__ == "__main__":
    print("Démarrage du producteur et du consommateur...")

    # lance le producteur kafka
    producer_thread = threading.Thread(target=run_producer)
    producer_thread.daemon = True
    producer_thread.start()

    # lance le consummateur ElasticSearch
    consumer_thread = threading.Thread(target=run_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()

    # Maintient le thread principal en cours
    producer_thread.join()
    consumer_thread.join()
