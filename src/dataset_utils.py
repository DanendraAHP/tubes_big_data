import pandas as pd
import tensorflow as tf
from config.config import TRAIN_CONFIG, TEST_CONFIG
import re
import pickle
from src.text_vectorizer import Vectorizer

AUTOTUNE = tf.data.AUTOTUNE

class Dataset:
    def __init__(self, train=True):
        """
        asumsi file train dan validation digabung jadi dilakukan split manual
        """
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
        label = tf.one_hot(label, 3)
        label = label[tf.newaxis, :]
        return text, label
    def remove_emojis(self,data):
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                        "]+", re.UNICODE)
        return re.sub(emoj, '', data)
    def prepare_training_data(self):
        """
        prepare data sebelum masuk ke model tensorflow
        """
        #remove emoji bajingan
        self.df[self.x_col] = self.df[self.x_col].apply(self.remove_emojis)
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
        self.df = tf.data.Dataset.from_tensor_slices(self.df[self.x_col].astype('str'))
        #load the vectorizer
        vec = Vectorizer()
        self.vectorizer = vec.load_vectorizer()
        #pre-process tf dataset
        self.df = self.df.map(self.make_inference_data)