from config.config import TRAIN_CONFIG
import tensorflow as tf
import pickle

class Vectorizer:
    def __init__(self):
        self.filepath = TRAIN_CONFIG['VECTORIZER_FILE']

    def adapt_vectorizer(self, train_df):
        """
        cuma dipanggil saat training model aja,
        baik training maupun inference manggil dari load_vectorizer
        selesai diadapt
        """
        vectorize_layer = tf.keras.layers.TextVectorization(
            standardize='lower_and_strip_punctuation',
            max_tokens=TRAIN_CONFIG['MAX_VOCAB']  ,
            output_mode='int',
            output_sequence_length=TRAIN_CONFIG['PAD_LENGTH']
        )
        vectorize_layer.adapt(train_df.map(lambda x,y:x))
        #save
        # Pickle the config and weights
        pickle.dump({'config': vectorize_layer.get_config(),
                    'weights': vectorize_layer.get_weights()}
                    , open(self.filepath, "wb"))
    def load_vectorizer(self):
        from_disk = pickle.load(open(self.filepath, "rb"))
        new_v = tf.keras.layers.TextVectorization.from_config(from_disk['config'])
        # You have to call `adapt` with some dummy data (BUG in Keras)
        new_v.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
        new_v.set_weights(from_disk['weights'])
        return new_v