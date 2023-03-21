import pandas as pd
import tensorflow as tf
from config.config import TRAIN_CONFIG, TEST_CONFIG
import re
from src.text_vectorizer import Vectorizer
from sklearn import preprocessing
import preprocessor as p

AUTOTUNE = tf.data.AUTOTUNE

class Dataset:
    def __init__(self, train=True):
        """
        asumsi file train dan validation digabung jadi dilakukan split manual
        """
        self.num_class = TRAIN_CONFIG['NUM_CLASS']
        if train:
            self.df = pd.read_csv(TRAIN_CONFIG['TRAIN_FILENAME'])
            self.x_col = TRAIN_CONFIG['X_COL']
            self.y_col = TRAIN_CONFIG['Y_COL']
        #inference
        else:
            self.df = pd.read_csv(TEST_CONFIG['TEST_FILENAME'])
            self.x_col = TEST_CONFIG['X_COL']
    def make_training_data(self, text, label):
        text = tf.expand_dims(text, -1)
        text = self.vectorizer(text)
        if self.num_class>2:
            label = tf.one_hot(label, self.num_class)
            label = label[tf.newaxis, :]
        else:
            label = tf.expand_dims(label,-1)
        return text, label
    def prepare_training_data(self):
        """
        prepare data sebelum masuk ke model tensorflow
        """
        #preprocess the data
        self.df[self.x_col] = self.df[self.x_col].apply(p.clean)
        if self.df.dtypes[self.y_col] =='O':
            le = preprocessing.LabelEncoder()
            self.df[self.y_col] = le.fit_transform(self.df[self.y_col])
        #split data to train and val
        print('splitting the dataset'.center(60,'-'))
        self.train_df = self.df.sample(frac=0.8)
        self.val_df = self.df.loc[~self.df.index.isin(self.train_df.index)]
        #make tensorflow dataset
        print('make tensorflow dataset'.center(60,'-'))
        self.train_df = tf.data.Dataset.from_tensor_slices((self.train_df[self.x_col].astype('str'), self.train_df[self.y_col].astype('int')))
        self.val_df = tf.data.Dataset.from_tensor_slices((self.val_df[self.x_col].astype('str'), self.val_df[self.y_col].astype('int')))
        #adapt the vectorizer
        print('adapting vectorizer'.center(60,'-'))
        vec = Vectorizer()
        vec.adapt_vectorizer(train_df=self.train_df)
        #preprocess the data
        #load the vectorizer
        self.vectorizer = vec.load_vectorizer()
        #map the tf dataset
        self.train_df = self.train_df.map(self.make_training_data)
        self.val_df = self.val_df.map(self.make_training_data)
        self.train_df = self.train_df.prefetch(AUTOTUNE)
        self.val_df = self.val_df.prefetch(AUTOTUNE)
    def make_inference_data(self, text):
        text = tf.expand_dims(text, -1)
        text = self.vectorizer(text)
        return text
    def prepare_inference_data(self):
        #preprocess the data
        self.df[self.x_col] = self.df[self.x_col].apply(p.clean)
        self.df = tf.data.Dataset.from_tensor_slices(self.df[self.x_col].astype('str'))
        #load the vectorizer
        vec = Vectorizer()
        self.vectorizer = vec.load_vectorizer()
        #pre-process tf dataset
        self.df = self.df.map(self.make_inference_data)
