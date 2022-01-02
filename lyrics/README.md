The first step was gathering the artist_ids on genius of the artist whos lyrics I wanted to train my model on. I don't think this task is possible to automate, because genius does not allow to restrict searches to perfect matches. 

The get_lyrics.py script uses the artist ids to get all of the lyrics from these artists. 

The clean_lyrics.py script cleans the lyrics.