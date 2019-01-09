import mido
from mido import Message
from mido import MidiFile



def lyrics_tracks(mid):
	return [track for track in mid.tracks if has_lyrics(track)]

def lyrics(mid):
	lyrics_track = lyrics_tracks(mid)[0] # first track with lyrics (should be only track with lyrics)
	#print(len(lyrics_track))
	syllables = [msg.text for msg in lyrics_track if msg.is_meta and msg.type == 'lyrics']
	syllables = [syl.replace('\r', '') for syl in syllables]
	return syllables

# returns all notes in the vocal track of the midi file
def voice_notes(mid):
	lyrics_track = lyrics_tracks(mid)[0]
	print(mid.length)
	current_time = 0
	notes = []
	for msg in lyrics_track:
		current_time += msg.time
		note = Note(msg, current_time)
		notes.append(note)
	return notes

def has_lyrics(track):
	for msg in track:
		if msg.is_meta and msg.type == 'lyrics':
			return True
	return False

class Note(object):

	def __init__(self, msg, time):

		self.timecode = time
		self.type = msg.type
		self.midicode = ''
		self.velocity = ''
		self.text = ''

		if not msg.is_meta:
			if msg.type == 'control_change':
				self.text = str(msg.value)
			elif msg.type == 'program_change':
				self.text = str(msg.channel)
			elif msg.type == 'note_on':
				self.midicode = msg.note
				self.velocity = msg.velocity
				if self.velocity == 0:
					self.type = 'note_off'
			elif msg.type == 'note_off':
				self.midicode = msg.note
				self.velocity = msg.velocity
		elif msg.is_meta:
			if msg.type == 'midi_port':
				self.text = str(msg.port)
			elif msg.type == 'track_name':
				self.text = msg.name
			elif msg.type == 'lyrics':
				self.text = msg.text
			elif msg.type == 'end_of_track':
				self.text = 'END OF TRACK'
		"""
		if msg.is_meta:
			if msg.type == 'lyrics':
				self.text = msg.text
				self.velocity = None
				self.time = msg.time
			else:
				pass
		else:
			self.time = msg.time
			self.velocity = msg.velocity
			self.text = None
		"""

	def __str__(self):
		return " ".join([str(self.timecode), self.type, str(self.midicode), str(self.velocity), self.text])


if __name__ == '__main__':
	mid = MidiFile('midifiles/girl.mid')
	print([str(n) for n in voice_notes(mid)[:100]])
