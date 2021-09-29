import numpy as np
import tensorflow as tf
import config
from model_class import LyricGenerationModel

with open('lyrics/cleaned_lyrics', 'r') as file:
   word_list = file.read().split()

vocab = sorted(set(word_list))
vocab_size = len(vocab)

word_to_id = {word:i for i,word in enumerate(vocab)}
id_to_word = {i:word for i,word in enumerate(vocab)}

id_list = np.array([word_to_id[word] for word in word_list])


examples_per_epoch = len(id_list)//(config.seq_len + 1)
id_dataset = tf.data.Dataset.from_tensor_slices(id_list)

word_sequences = id_dataset.batch(config.seq_len + 1, drop_remainder=True)

def split_input_target(chunk): 
  input_text = chunk[:-1]
  target_text = chunk[1:]
  return input_text, target_text

dataset = word_sequences.map(split_input_target)
dataset = dataset.shuffle(config.buffer_size).batch(config.batch_size, drop_remainder=True)


model = LyricGenerationModel()
model.fit(dataset, vocab_size, id_to_word, word_to_id)
model.save(config.current_model)

