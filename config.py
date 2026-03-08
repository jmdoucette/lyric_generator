#training
batch_size = 64
buffer_size = 1000
seq_len = 10
epochs = 20

#generation
min_length = 100
max_length = 200
temp = 1 # don't set this below 0.2 -- otherwise the word sampler will often get stuck on an unknown token
saved_models_path = "model/"
current_model = "lstm_10_20"