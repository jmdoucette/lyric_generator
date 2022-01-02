import config
import json
import re

with open('lyrics/data/raw_lyrics', 'r') as file:
  cleaned_lyrics = file.read()
  

#replacing unicode with ascii version
cleaned_lyrics = cleaned_lyrics.replace('\u2005', ' ')
cleaned_lyrics = cleaned_lyrics.replace('\u205f', ' ')
cleaned_lyrics = cleaned_lyrics.replace('\u200a', ' ')
cleaned_lyrics = cleaned_lyrics.replace('\u200b', ' ')

cleaned_lyrics = cleaned_lyrics.replace('\u201a', ' , ')
cleaned_lyrics = cleaned_lyrics.replace('\u2013', ' - ')
cleaned_lyrics = cleaned_lyrics.replace('\u2014', ' - ')
cleaned_lyrics = cleaned_lyrics.replace('\u2019', '\'')
cleaned_lyrics = cleaned_lyrics.replace('\u2018', '\'')
cleaned_lyrics = cleaned_lyrics.replace('\u00b4', '\'')
cleaned_lyrics = cleaned_lyrics.replace('\u0092', '\'')
cleaned_lyrics = cleaned_lyrics.replace('\u00e0', 'a')
cleaned_lyrics = cleaned_lyrics.replace('\u0435', 'e')
cleaned_lyrics = cleaned_lyrics.replace('\u00e8', 'e')
cleaned_lyrics = cleaned_lyrics.replace('\u00e9', 'e')
cleaned_lyrics = cleaned_lyrics.replace('\u00f3', 'o')
cleaned_lyrics = cleaned_lyrics.replace('\u00f1', 'n')
cleaned_lyrics = cleaned_lyrics.replace('\u2028', '\n')
cleaned_lyrics = cleaned_lyrics.replace('\u201d', '\"')
cleaned_lyrics = cleaned_lyrics.replace('\u201c', '\"')
cleaned_lyrics = cleaned_lyrics.replace('\ufb01', 'fi')



#cleaning lyrics
cleaned_lyrics = cleaned_lyrics.replace('\n', ' newline ')

#commas between numbers
cleaned_lyrics = re.sub('(?<=\\d),(?=\\d)', '', cleaned_lyrics)
cleaned_lyrics = cleaned_lyrics.replace('b.b.', 'b_b_')

chars_to_remove = [',', ':', '.', '\"', '/', '?', '!', '-', '\t', '\u2026', '\u00e2', '\u20ac', '\u009d', '\u00bd', '\ufffc', '~']
for char in chars_to_remove:
    cleaned_lyrics = cleaned_lyrics.replace(char, ' ')
cleaned_lyrics = cleaned_lyrics.lower()

#simplies intro, verse, chorus, bridge
cleaned_lyrics = re.sub('\[[^\]]*?intro[^\]]*?\]', '{intro}', cleaned_lyrics, flags=re.IGNORECASE)
cleaned_lyrics = re.sub('\[[^\]]*?chorus[^\]]*?\]', '{chorus}', cleaned_lyrics, flags=re.IGNORECASE)
cleaned_lyrics = re.sub('\[[^\]]*?verse[^\]]*?\]', '{verse}', cleaned_lyrics, flags=re.IGNORECASE)
cleaned_lyrics = re.sub('\[[^\]]*?bridge[^\]]*?\]', '{bridge}', cleaned_lyrics, flags=re.IGNORECASE)
cleaned_lyrics = re.sub('\[[^\]]*?instrumental[^\]]*?\]', '{instrumental}', cleaned_lyrics, flags=re.IGNORECASE)



#removes other text within parens or brackets to decrease complexity
cleaned_lyrics = re.sub('[\(\[].*?[\)\]]', ' ', cleaned_lyrics)
cleaned_lyrics = cleaned_lyrics.replace('{', '[')
cleaned_lyrics = cleaned_lyrics.replace('}', ']')

cleaned_lyrics = cleaned_lyrics.replace(' t n t ', ' tnt ')
cleaned_lyrics = cleaned_lyrics.replace(' v e n o m ', ' venom ')
cleaned_lyrics = cleaned_lyrics.replace(' l o v e ', ' love ')
cleaned_lyrics = cleaned_lyrics.replace(' f b i ', ' fbi ')
cleaned_lyrics = cleaned_lyrics.replace(' f i n e ', ' fine ')
cleaned_lyrics = cleaned_lyrics.replace(' m a n ', ' man ')


#converting all versions of yeah to same
cleaned_lyrics = re.sub(' a+h+ ', ' ah ', cleaned_lyrics)

#changing abbreviations to make words have same meanings
cleaned_lyrics = cleaned_lyrics.replace(' rock n roll', ' rock and roll')
cleaned_lyrics = cleaned_lyrics.replace(' \'round ', ' around ')
and_versions = [' an\' ', ' \'n ', '\'n\'', ' & ']
for and_version in and_versions:
    cleaned_lyrics = cleaned_lyrics.replace(and_version, ' and ')
cleaned_lyrics = cleaned_lyrics.replace('in\' ', 'ing ')
cleaned_lyrics = cleaned_lyrics.replace(' workn\' ', ' working ')
cleaned_lyrics = cleaned_lyrics.replace(' c\'mon ', ' come on ')
cleaned_lyrics = cleaned_lyrics.replace(' ya\'all ', ' y\'all ')
yeah_versions = [' yee ', ' yea ', ' ya ', ' ya\' ', ' yah ', ' yeh ', ' yeah\' ', ' yeahh ', ' yeahh\' ', ' yeah\' ', ' \'yeah\' ']
for yeah_version in yeah_versions:
    cleaned_lyrics = cleaned_lyrics.replace(yeah_version, ' yeah ')
oh_versions = [' ohh ', ' ohhh ', ' ohhhh ', ' oi ', ' oo ', ' ooh ', ' ooo ', ' oooh ', ' ooooh ', ' oooooh ', ' ooooooo ', ' ooow ', ' ow ', ' oww ', ' oww ', ' aw ', ' aww ', ' woah ', ' wo ', ' woh ', ' whoa ']
for oh_version in oh_versions:
    cleaned_lyrics = cleaned_lyrics.replace(oh_version, ' oh ')
ay_versions = [' ayy ', ' aye ']
for ay_version in ay_versions:
    cleaned_lyrics = cleaned_lyrics.replace(ay_version, ' ay ')
mm_versions = [' mmm ', ' mmmm ']
for mm_version in mm_versions:
    cleaned_lyrics = cleaned_lyrics.replace(mm_version, ' mm ')
cleaned_lyrics = cleaned_lyrics.replace(' \'ain\'t ', ' ain\'t' )
cleaned_lyrics = cleaned_lyrics.replace(' \'bout ', ' about ')
cleaned_lyrics = cleaned_lyrics.replace(' \'cause ', ' because ')
cleaned_lyrics = cleaned_lyrics.replace(' \'come ', ' come ')
cleaned_lyrics = cleaned_lyrics.replace(' \'cos ', ' because ')
cleaned_lyrics = cleaned_lyrics.replace(' \'cross ', ' across ')
cleaned_lyrics = cleaned_lyrics.replace(' \'cuz ', ' because ')
cleaned_lyrics = cleaned_lyrics.replace(' \'em ', ' them ')
cleaned_lyrics = cleaned_lyrics.replace(' \'fore ', ' before ')
cleaned_lyrics = cleaned_lyrics.replace(' \'go ', ' go ')
cleaned_lyrics = cleaned_lyrics.replace(' \'i ', ' i ')
cleaned_lyrics = cleaned_lyrics.replace(' \'low ', ' follow ')
cleaned_lyrics = cleaned_lyrics.replace(' \'n ', ' and ')
cleaned_lyrics = cleaned_lyrics.replace(' \'neath ', ' beneath ')
cleaned_lyrics = cleaned_lyrics.replace(' \'rever ', ' forever ')
cleaned_lyrics = cleaned_lyrics.replace(' \'scuse ', ' excuse ')
cleaned_lyrics = cleaned_lyrics.replace(' \'til ', ' until  ')
cleaned_lyrics = cleaned_lyrics.replace(' \'till ', ' until ')
cleaned_lyrics = cleaned_lyrics.replace(' \'twas ', ' it was ')
cleaned_lyrics = cleaned_lyrics.replace(' \'tween ', ' between ')
cleaned_lyrics = cleaned_lyrics.replace(' \'yeah ', ' yeah ')
cleaned_lyrics = cleaned_lyrics.replace(' \'yeah \'', ' yeah ')
cleaned_lyrics = cleaned_lyrics.replace(' a\'coming ', ' coming ')
cleaned_lyrics = cleaned_lyrics.replace(' wha ', ' what ')
cleaned_lyrics = cleaned_lyrics.replace(' \'s ', ' is ')
cleaned_lyrics = cleaned_lyrics.replace(' ho__me ', ' home ')
cleaned_lyrics = cleaned_lyrics.replace(' allright ', ' alright ')

cleaned_lyrics = cleaned_lyrics.replace('\'', '')

#filtering out songs without [verse]/[chorus] tagss
songs = cleaned_lyrics.split('songstart')
songs = [song for song in songs if '[verse]' in song]
cleaned_lyrics = ' songstart '.join(songs)

word_list = cleaned_lyrics.split(' ')
word_list = [word for word in word_list if word] 
#removing repeated newlines
word_list = [word_list[i] for i in range(len(word_list)) if word_list[i] != 'newline' or (i > 0 and word_list[i-1] != 'newline')]
map(str.strip, word_list)


word_counts = {}
for word in word_list:
  word_counts[word] = word_counts.get(word, 0) + 1

amount = 0
count = 0
for word in word_counts:
    if word_counts[word] < config.necessary_count:
        amount += 1
        count += word_counts[word]
print(f'{amount} words out of {len(word_counts)} have less than {config.necessary_count} occurances.\nthere are {count} total out of {len(word_list)}')

word_counts['unknown_token'] = 0
for (i, word) in enumerate(word_list):
    if word_counts[word] < config.necessary_count:
        word_list[i] = 'unknown_token'

cleaned_lyrics = ' '.join(word_list)
with open('lyrics/data/cleaned_lyrics', 'w') as file:
  file.write(cleaned_lyrics)

word_counts = { word:count for (word,count) in sorted(word_counts.items(), key=lambda item: -1 * item[1]) if count >= config.necessary_count}
with open('lyrics/data/word_counts.json', 'w') as file:
  json.dump(word_counts, file)