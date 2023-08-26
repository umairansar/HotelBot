import pickle
from sklearn.preprocessing import LabelBinarizer
import numpy as np 
import tensorflow as tf
from transformers import BertTokenizer

class IntentModel:
    def __init__(self):
        # Load the trained model from the file
        self.model = tf.keras.models.load_model('intent_predictor.h5')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        
    def predict(phrase):
        tokens = self.tokenizer.encode_plus(phrase, max_length= seq_len, truncation= True, padding= 'max_length', add_special_tokens = True, return_tensors= 'tf')
        input = {'input_ids' : tf.cast(tokens['input_ids'], tf.float64),'attention_mask' : tf.cast(tokens['attention_mask'], tf.float64)}
        prediction = self.model.predict(input)
        print(prediction)
        return LabelBinarizer().inverse_transform(prediction)[0]

