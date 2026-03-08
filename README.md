##  This is a project by James Doucette to generate blues song lyrics.



#### Setup
Create a virtual envirnment and install necessary dependencies
```shell
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Test generating a blues song lyrics
```shell
py test_generate_lyrics.py
```

Start lyric generator flask webapp
```shell
flask run
```
