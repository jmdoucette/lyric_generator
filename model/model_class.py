import numpy as np
import tensorflow as tf
import json
import config


class LyricGenerationModel:
    def __init__(self, model, id_to_word, word_to_id):
        self.model = model
        self.id_to_word = id_to_word
        self.word_to_id = word_to_id

    @classmethod
    def fit(cls, dataset, vocab_size, id_to_word, word_to_id):
        model = tf.keras.Sequential([
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

        return cls(model, id_to_word, word_to_id)


    @classmethod
    def load(cls, name):
        model = tf.keras.models.load_model(config.saved_models_path + name + '/model.h5', custom_objects={"loss":tf.losses.SparseCategoricalCrossentropy(from_logits=True)})
        with open(config.saved_models_path + name + '/id_to_word.json', 'r') as file:
            id_to_word = id_to_word = {int(id_string):word for (id_string,word) in json.load(file).items()}
        with open(config.saved_models_path + name + '/word_to_id.json', 'r') as file:
            word_to_id = {word:int(id_string) for (word, id_string) in json.load(file).items()}

        return cls(model, id_to_word, word_to_id)


    def save(self, name):
        self.model.save(config.saved_models_path + name + '/model.h5')
        with open(config.saved_models_path + name + '/id_to_word.json', 'w') as file:
            json.dump(self.id_to_word, file)
        with open(config.saved_models_path + name + '/word_to_id.json', 'w') as file:
            json.dump(self.word_to_id, file)


    def generate_text(self):
        words = self.generate_words()
        #adding spaces after section headers if not already theres
        new_words = []
        for word in words:
            new_words.append(word)
            if word in ['[chorus]', '[verse]', '[bridge]', '[intro]', '[instrumental]']:
                new_words.append('newline')
            words = new_words

        #removing leading, trailing and repeated newlines
        words = [word for word in words if word != 'songstart' and word != 'songend']
        first_non_newline = 0
        for i,word in enumerate(words):
            if word != 'newline':
                first_non_newline = i
                break
        last_non_newline = len(words)
        for i,word in reversed(list(enumerate(words))):
            if word != 'newline':
                last_non_newline = i
                break

        words = words[first_non_newline:last_non_newline+1]
        words = [words[i] for i in range(len(words)) if words[i] != 'newline' or (i > 0 and words[i-1] != 'newline')]

        #prettifying
        text = ' '.join(words)
        text = text.replace('songstart', '')
        text = text.replace('songend', '')
        text = text.replace('newline', '<br>')
        text = text.replace('[chorus]', '<br> [chorus]')
        text = text.replace('[verse]', '<br> [verse]')
        text = text.replace('[bridge]', '<br> [bridge]')
        text = text.replace('[intro]', '<br> [intro]')
        text = text.replace('[instrumental]', '<br> [instrumental]')
        return text


    def generate_words(self):
        self.model.reset_states()

        initial_words = ['songstart', '[intro]']
        generation = [self.word_to_id[s] for s in initial_words]

        for num_generated in range(config.max_length):                
            context = generation[-config.seq_len+1:]
            input_tensor = self.convert_context_to_input_tensor(context)
            
            # allowing a separate temperature for the first word to increase variety
            # without this the first word was only ever a few values, usually unlock
            if (num_generated == 0):
                temp = config.first_word_temp
            else:
                temp = config.temp

            prediction = self.generate_next_word(input_tensor, temp, num_generated)
            generation.append(prediction)

            if self.id_to_word[prediction] == 'songend':
                break

        return [self.id_to_word[i] for i in generation]


    def generate_next_word(self, input_tensor, temperature, num_generated):
        tokens_to_skip = self.get_tokens_to_skip(num_generated)

        predictions = self.model(input_tensor)
        predictions = predictions[0]
        predictions = predictions[-1] / temperature

        predictions = predictions.numpy()
        for token in tokens_to_skip:
            predictions[token] = -1e9

        prediction = tf.random.categorical([predictions], 1)[0,0].numpy()
        return prediction


    def get_tokens_to_skip(self, num_generated):
        tokens_to_skip = [
            self.word_to_id['unknown_token']
        ]
        if num_generated < config.min_length:
            tokens_to_skip.append(self.word_to_id['songend'])
        return tokens_to_skip


    def convert_context_to_input_tensor(self, context):
        # convert into tensor of required dimensions
        expanded = tf.expand_dims(context, 0) 
        # broadcast to first dimension to 64 
        return tf.repeat(expanded, 64, axis=0)