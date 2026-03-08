#training
batch_size = 64
buffer_size = 1000
seq_len = 10
epochs = 20

#generation
min_length = 100
max_length = 200
first_word_temp = 1.2
temp = 0.8
saved_models_path = "model/"
current_model = "lstm_10_20"