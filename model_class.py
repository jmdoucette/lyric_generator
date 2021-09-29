import numpy as np
import tensorflow as tf
import json
import config


class LyricGenerationModel:
  def __init__(self):
    self.model = None


  def fit(self, dataset, vocab_size, id_to_word, word_to_id):
    self.model = tf.keras.Sequential([
    # Embed len(vocabulary) into 64 dimensions
    tf.keras.layers.Embedding(vocab_size, 64, batch_input_shape=[config.batch_size,None]),
    # LSTM RNN layers
    tf.keras.layers.LSTM(512, return_sequences=True, stateful=True),
    tf.keras.layers.LSTM(512, return_sequences=True, stateful=True),
    # Classification head
    tf.keras.layers.Dense(vocab_size)
    ])
    self.model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))
    self.model.fit(dataset, epochs=config.epochs, verbose=1)

    self.id_to_word = id_to_word
    self.word_to_id = word_to_id


  def save(self, name):
    self.model.save(config.saved_models_path + name + '/model.h5')
    with open(config.saved_models_path + name + '/id_to_word.json', 'w') as file:
        json.dump(self.id_to_word, file)
    with open(config.saved_models_path + name + '/word_to_id.json', 'w') as file:
        json.dump(self.word_to_id, file)


  def load(self, name):
    self.model = tf.keras.models.load_model(config.saved_models_path + name + '/model.h5', custom_objects={"loss":tf.losses.SparseCategoricalCrossentropy(from_logits=True)})
    with open(config.saved_models_path + name + '/id_to_word.json', 'r') as file:
        self.id_to_word = id_to_word = {int(id_string):word for (id_string,word) in json.load(file).items()}
    with open(config.saved_models_path + name + '/word_to_id.json', 'r') as file:
        self.word_to_id = {word:int(id_string) for (word, id_string) in json.load(file).items()}


  def generate_text(self):
    self.model.reset_states()

    sample = ['songstart']
    # vectorize the string
    sample_vector = [self.word_to_id[s] for s in sample]
    predicted = sample_vector
    # convert into tensor of required dimensions
    sample_tensor = tf.expand_dims(sample_vector, 0) 
    # broadcast to first dimension to 64 
    sample_tensor = tf.repeat(sample_tensor, 64, axis=0)

    temperature = 1
    for i in range(200):
        predictions = self.model(sample_tensor)
        predictions = predictions[0].numpy()/temperature
        prediction = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        while self.id_to_word[prediction] == 'unknown_token':
            prediction = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
        
        predicted.append(prediction)
        sample_tensor = predicted[-config.seq_len+1:]
        sample_tensor = tf.expand_dims([prediction],0)
        # broadcast to first dimension to 64 
        sample_tensor = tf.repeat(sample_tensor, 64, axis=0)

        if self.id_to_word[prediction] == 'songend':
            break

    return [self.id_to_word[i] for i in predicted]
