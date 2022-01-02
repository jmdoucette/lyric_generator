import requests
from bs4 import BeautifulSoup

with open('genius_api_token', 'r') as file:
  GENIUS_API_TOKEN = file.read()
with open('artist_ids') as file:
  artist_ids = file.read().splitlines()
raw_lyrics_file = open('lyrics/raw_lyrics', 'w')

# getting the urls for the deisred lyrics
lyric_urls = []
for artist_id in artist_ids:
  #getting the urls of the lyric pages
  base_url = 'http://genius.com'
  songs_url = 'http://api.genius.com/artists/' + artist_id + '/songs'
  headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
  params = {'page': None}
  next_page = 1

  while next_page:
    params['page'] = next_page
    response = requests.get(songs_url, headers=headers, params=params)
    songs = response.json()['response']['songs']
    next_page = response.json()['response']['next_page']

    for song in songs:
      if song['lyrics_state'] == 'complete' and song['primary_artist']['api_path'] == '/artists/' + artist_id:
        lyric_urls.append(base_url + song['path'])


#getting the lyrics from the urls
headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
regex = re.compile('.*Lyrics__Container.*')
count = 0
for lyric_url in lyric_urls:
    print(lyric_url)
    response = requests.get(lyric_url, headers=headers)
    test.write(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics_section = soup.find('div', {'class': regex })
    if lyrics_section:
      lyrics = 'songstart \n' + lyrics_section.get_text(separator='\n') + '\nsongend \n'
      raw_lyrics_file.write(lyrics)
      count += 1

print(f"got {count} lyrics from {len(lyric_urls)} urls")
raw_lyrics_file.close()

