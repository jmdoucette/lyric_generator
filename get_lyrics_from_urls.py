import requests
from bs4 import BeautifulSoup
import re

with open('genius_api_token', 'r') as file:
  GENIUS_API_TOKEN = file.read()
headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}


with open('lyrics/lyric_urls', 'r') as file:
  lyric_urls = list(map(lambda x: x.strip(), file.readlines()))
raw_lyrics_file = open('lyrics/raw_lyrics', 'w')
test = open('request_result.html', 'w')


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

raw_lyrics_file.close()
test.close()

print(f"got {count} lyrics from {len(lyric_urls)} urls")