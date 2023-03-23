TRAIN_CONFIG = {
    'NUM_CLASS' : 2,
    'MAX_VOCAB' : 50000,
    'PAD_LENGTH' : 100,
    'BATCH_SIZE' : 32,
    'EPOCHS' : 10,
    'VERBOSE':1,
    'ES_PATIENCE':5,
    'MODEL_FOLDER':'model/lstm_model',
    'TRAIN_FILENAME' : 'data/Dataset-Sentimen-Analisis-Bahasa-Indonesia-master/dataset_tweet_sentiment_pilkada_DKI_2017.csv',
    'X_COL' : 'Text Tweet',
    'Y_COL' : 'Sentiment',
    'EMBEDDING_DIM' : 100,
    'VECTORIZER_FILE' : 'model/vectorizer.pkl'
}

TEST_CONFIG = {
    'TEST_FILENAME':'data/youtube-api.csv',
    'X_COL':'description'
}

PRODUCER_CONFIG = {
    'CREDENTIALS_FILE' : '../config/credential.json',
    'KEYWORD_LIST' : {
        'anies' : ['anies'],
        'prabowo' : ['prabowo'],
        'ganjar' : ['ganjar'],
        'puan' : ['puan']
    },
    'HDFS_FOLDER' : 'hdfs://localhost:9000/pilkada_raw',
    'KAFKA_TOPIC' : 'youtube-api'
}

INFERENCE_CONFIG = {
    'RAW_FOLDER'  : 'hdfs://localhost:9000/pilkada_raw',
    'RAW_CSV_FILE' : 'data/youtube-api.csv',
    'INFERENCE_FOLDER' : 'hdfs://localhost:9000/youtube_inferred/' 
}