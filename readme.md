Le projet consiste à collecter les informations financières
sur le site polygon.io et créer un modèle de prédiction.

Pipeline

Polygon.io API ──> Kafka ──> Elasticsearch 
                                 ──>  Pretraitement  ──> Stockage 
                                                            ──>  modele  ──>  prediction

Structure du projet:
    configs ──> contient le fichiers de configuration
    data ──> contient les donnees recuperer
    ml ──> contient les traitements du modele ainsi que le modele
    streamlayer ──> contient les fichiers du stream layer
    servinglayer ──> contient les fichiers du serving layer


Run kafka zookeper : bin/zookeeper-server-start.sh config/zookeeper.properties
Run kafka server : bin/kafka-server-start.sh config/server.properties

Run ElasticSearch : bin/elasticsEarch


Lister les donnees : bin/kafka-console-consumer.sh --bootstrap-server TonAdresseServeur:tonPort --topic tonTOpicKafka --from-beginning

    exemple: bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic polygon-data --from-beginning