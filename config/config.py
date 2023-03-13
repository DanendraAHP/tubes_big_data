TRAIN_CONFIG = {
    'MAX_VOCAB' : 50000,
    'PAD_LENGTH' : 100,
    'BATCH_SIZE' : 32,
    'EPOCHS' : 10,
    'VERBOSE':1,
    'ES_PATIENCE':5,
    'MODEL_FOLDER':'model/lstm_model',
    'TRAIN_FILENAME' : 'data/dataset_test.csv',
    'X_COL' : 'tweet',
    'Y_COL' : 'hasil',
    'EMBEDDING_DIM' : 100,
    'VECTORIZER_FILE' : 'model/vectorizer.pkl'
}

TEST_CONFIG = {
    'TEST_FILENAME':'data/test.csv',
    'X_COL':'tweet'
}