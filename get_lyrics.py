import requests
from bs4 import BeautifulSoup

with open('genius_api_token', 'r') as file:
  GENIUS_API_TOKEN = file.read()

with open('artist_ids') as file:
  artist_ids = file.read().splitlines()

lyric_urls_file = open('lyrics/lyric_urls', 'w')
raw_lyrics_file = open('lyrics/raw_lyrics', 'w')


for artist_id in artist_ids:
  #getting the urls of the lyric pages
  base_url = 'http://genius.com'
  songs_url = 'http://api.genius.com/artists/' + artist_id + '/songs'
  headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
  params = {'page': None}
  next_page = 1

  lyric_urls = []
  while next_page:
    params['page'] = next_page
    response = requests.get(songs_url, headers=headers, params=params)
    songs = response.json()['response']['songs']
    next_page = response.json()['response']['next_page']

    for song in songs:
      #checking that lyrics are complete and the artist is actually led zeppelin (other lyrics that mention led zepelin can result from search)
      #removing song 591796 as other data is mistagged as lyrics
      if song['lyrics_state'] == 'complete' and song['primary_artist']['api_path'] == '/artists/' + artist_id and song['id'] != 591796:
        lyric_urls.append(base_url + song['path'])

  for lyric_url in lyric_urls:
    lyric_urls_file.write(lyric_url + '\n')

  '''
  #getting the lyrics and writing to a file
  for lyric_url in lyric_urls:
    response = requests.get(lyric_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics_section = soup.find('div', {'class':'Lyrics__Container-sc-1ynbvzw-7 dVtOne'})
    if lyrics_section:
      lyrics = 'songstart \n' + lyrics_section.get_text(separator='\n') + '\nsongend \n'
      raw_lyrics_file.write(lyrics)
  '''


lyric_urls_file.close()
raw_lyrics_file.close()

