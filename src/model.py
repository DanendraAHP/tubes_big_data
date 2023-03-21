import tensorflow as tf
from config.config import TRAIN_CONFIG
import pickle
import numpy as np
class TFModel:
    def __init__(self):
        self.num_class = TRAIN_CONFIG['NUM_CLASS']
        self.model_folder = TRAIN_CONFIG['MODEL_FOLDER']
        self.model_cp_path = f'{self.model_folder}/cp.ckpt'
        self.verbose = TRAIN_CONFIG['VERBOSE']
        self.batch_size = TRAIN_CONFIG['BATCH_SIZE']
        self.epochs = TRAIN_CONFIG['EPOCHS']
        self.es_patience = TRAIN_CONFIG['ES_PATIENCE']
        self.max_vocab = TRAIN_CONFIG['MAX_VOCAB']+1
        self.embedding = TRAIN_CONFIG['EMBEDDING_DIM']
        self.vectorizer_file = TRAIN_CONFIG['VECTORIZER_FILE']
    def create_model(self):
        self.model=tf.keras.Sequential()
        #embedding layer
        self.model.add(tf.keras.layers.Embedding(self.max_vocab, self.embedding)) 
        self.model.add(tf.keras.layers.LSTM(128,return_sequences=True,dropout=0.2))
        #Global Maxpooling
        self.model.add(tf.keras.layers.GlobalMaxPooling1D())
        #Dense Layer
        self.model.add(tf.keras.layers.Dense(64,activation='relu')) 
        if self.num_class>2:
            self.model.add(tf.keras.layers.Dense(self.num_class, activation='softmax'))
            #Add loss function, metrics, optimizer
            self.model.compile(optimizer='adam', loss='categorical_crossentropy',metrics=["acc"]) 
        else:
            self.model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
            #Add loss function, metrics, optimizer
            self.model.compile(optimizer='adam', loss='binary_crossentropy',metrics=["acc"]) 
    def train_model(self, train_data, val_data):
        print('creating the model'.center(60,'-'))
        self.create_model()
        #Adding callbacks
        es = tf.keras.callbacks.EarlyStopping(
            monitor='val_acc', mode='max', 
            verbose=self.verbose,
            patience=self.es_patience
        )  
        mc=tf.keras.callbacks.ModelCheckpoint(
            filepath = self.model_cp_path, 
            monitor='val_acc', 
            mode='max', 
            save_best_only=True,
            verbose=self.verbose,
            save_weights_only=True
        )  
        print('training the model'.center(60,'-'))
        self.model.fit(
            train_data,
            validation_data=val_data,
            epochs=self.epochs,
            verbose=self.verbose,
            callbacks=[es, mc],
            batch_size=self.batch_size
        )
    def eval_model(self, val_data):
        print('evaluating the model'.center(20,'-'))
        loss, accuracy = self.model.evaluate(val_data)
        print(accuracy)
    def train_and_eval(self, train_data, val_data):
        self.train_model(train_data, val_data)
        self.eval_model(val_data)
    def inference(self, test_data):
        self.create_model()
        self.model.load_weights(self.model_cp_path)
        y_pred = self.model.predict(test_data)
        if self.num_class>2:
            return np.argmax(y_pred, axis=1)
        else:
            return [1 if y>0.5 else 0 for y in y_pred]
