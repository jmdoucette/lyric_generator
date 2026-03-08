# AI Coding Agent Instructions for Lyric Generator

## Project Overview
A Flask-based blues/rock lyric generation system using a stateful LSTM language model. The system has three phases: **data collection** → **model training** → **serving**. The model generates lyrics based on patterns learned from Genius artist datasets.

**Deployed at:** https://blues-lyric-generator.herokuapp.com (Heroku)

## Architecture & Data Flows

### 1. Data Collection Pipeline (`lyrics/`)
- **`get_lyrics.py`**: Fetches songs from Genius API using artist IDs (requires `genius_api_token` file and `artist_ids` file)
  - Outputs raw HTML lyrics → `lyrics/data/raw_lyrics`
- **`clean_lyrics.py`**: Tokenizes and normalizes:
  - Replaces unicode characters with ASCII equivalents
  - Converts lyrics to lowercase, adds `newline` tokens for line breaks
  - Standardizes section markers: `[intro]` → `{intro}`, `[chorus]` → `{chorus}` etc.
  - Outputs word sequence → `lyrics/data/cleaned_lyrics`

**Key pattern:** Text is space-delimited word tokens with special tokens: `songstart`, `songend`, `newline`, `{intro}`, `{chorus}`, `{verse}`, etc.

### 2. Model Training (`model/`)
- **`train_model.py`**: 
  - Reads `lyrics/data/cleaned_lyrics`, builds vocab
  - Creates `word_to_id` / `id_to_word` mappings (JSON dicts)
  - Builds stateful sequential dataset: sequences of `seq_len` words predict next word
  - Trains LSTM architecture and saves to `model/<model_name>/`
  
- **`model_class.py`** - `LyricGenerationModel`:
  - **Architecture:** Embedding(64d) → 2×LSTM(512) → Dense(vocab_size)
  - **Batch size:** 64 (stateful, required for deployment)
  - **Generate:** Uses temperature sampling with `config.temp` (default 0.7)
  - **Stopping:** Generates up to 200 tokens or until `songend` token

### 3. Flask Application (`app.py`)
- Single model loaded per request from `config.current_model` path
- `/`: Index form (index.html)
- `/display`: Generates and displays formatted lyrics (display.html)
- Models require both `.h5` file + vocab JSON files to load

## Configuration
**`config.py`** controls all hyperparameters and paths:
```python
seq_len = 10              # Context window for training
batch_size = 64           # Must match stateful model creation
epochs = 20               # Training iterations
temp = 0.7                # Softmax temperature for generation
current_model = "lstm_10_20"  # Active model folder name
```

Model folders: `model/<name>/` contains `model.h5`, `word_to_id.json`, `id_to_word.json`

## Development Workflows

### Running the Web App
```bash
# Development (Flask debug mode)
python app.py

# Production (Heroku-like)
gunicorn app:app
```

### Training a New Model
1. Ensure `lyrics/data/cleaned_lyrics` exists (run `clean_lyrics.py` after `get_lyrics.py`)
2. Update `config.current_model` with new name (e.g., `"lstm_15_30"`)
3. Run: `python model/train_model.py`
4. Update `config.current_model` to point to the saved model folder

### Adding New Artists
1. Get artist IDs from Genius (manual step, see `lyrics/README.md`)
2. Add IDs to `lyrics/data/artist_ids`
3. Run `lyrics/get_lyrics.py` → `lyrics/data/raw_lyrics`
4. Run `lyrics/clean_lyrics.py` → `lyrics/data/cleaned_lyrics`
5. Retrain with `model/train_model.py`

## Key Implementation Patterns

### Stateful LSTM Constraint
The model uses `stateful=True` with `batch_size=64`. This requires:
- All inputs must be batched to exactly 64 sequences
- `model.reset_states()` must be called before generating new lyrics (see `model_class.py` line 59)
- Batch dimension is hardcoded in model creation—changing batch size requires retraining

### Text Generation Process
1. Initialize with seed: `['songstart', '[intro]']`
2. For each iteration: predict next token using temperature-scaled softmax
3. Skip `unknown_token` predictions (retry sampling)
4. Stop on `songend` token or after 200 tokens
5. Post-process: add newlines after section headers, strip boundaries

### Vocab & Mapping Persistence
- `word_to_id` / `id_to_word` are JSON-serialized in model folders
- `word_to_id` keys are strings; `id_to_word` keys are integers (with string conversion during load)
- New words are not handled—all unknowns become `unknown_token` during vocab building

## Deployment Notes
- **Procfile:** `web: gunicorn app:app`
- **Dependencies:** Flask, TensorFlow (CPU), NumPy, Gunicorn
- Model files must be included in Heroku slug (no external storage)
- Single model instance per request (no caching layer)

## Common Debugging
- **Unknown tokens in output:** Usually indicates out-of-vocab words during generation—check vocab coverage
- **Model won't load:** Verify all three files exist in model folder (`.h5` + both JSON files)
- **Generation stuck in loop:** Check if `songend` token is in vocab; may need sampling threshold adjustment
- **Low quality lyrics:** Increase epochs, training dataset size, or adjust temperature
