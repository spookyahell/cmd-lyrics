from vlc import MediaPlayer, State
from time import sleep
import re

init = False
p = MediaPlayer(r'$VLC_PLAYABLE_AUDIO_FILE_LOCATION')
f = open(r'$LRC_FILE_LOCATION', 'r', encoding = 'utf-16le')

timecodes_ms = []
texts = []
for item in f.readlines():
	m = re.fullmatch('\[(?P<mm>\d\d):(?P<ss>\d\d).(?P<msms>\d\d)\](?P<txt>[\S ]+)?', item.strip())
	if m:
		if m.group('txt') != None:
			texts.append(m.group('txt'))
		else:
			texts.append('')
			
		timecodes_ms.append( (int(m.group('mm'))*60000) + (int(m.group('ss'))*1000) + (int(m.group('msms'))))
init = False
p.play()
while p.get_state() != State.Ended and p.get_state() != State.NothingSpecial:
	if p.get_state() != State.Opening:
		if init is False:
			duration = p.get_length()
			init = True
		pos_in_ms = duration*(p.get_position())
		if len(timecodes_ms)>0:
			if pos_in_ms>timecodes_ms[0]:
				if len(texts) == 1 and texts[0] == '':
					print('\n[THE END]\n(waiting for song file to end)')
				else:
					print(texts[0])
				del texts[0]
				del timecodes_ms[0]
	else:
		continue
	continue
