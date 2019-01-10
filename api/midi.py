import mido
from mido import Message
from mido import MidiFile
import dictionary
import random


def notes_by_track_number(mid, n):
	lyrics_track = mid.tracks[n]
	current_time = 0
	notes = []
	for msg in lyrics_track:
		current_time += msg.time
		note = Note(msg, current_time)
		notes.append(note)
	return notes

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
		# TODO: add duration
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


def process_midifile(filename):
	filepath = 'midifiles/%s' % filename
	mid = MidiFile(filepath)
	notes = [str(n) for n in notes_by_track_number(mid,3)]
	outpath = 'melodies/%s' % filename.split('.')[0]
	with open(outpath, 'w') as f:
		for note in notes:
			f.write(str(note)+'\n')

# return a list of likely next tokens given a context
# context is a list of Note objects that occurred in sequence
# return value is a list of tuples linking Notes to scores which represent their likelihood
def possible_continuations(history, ngram_dict):
	return dictionary.normalize(ngram_dict[history])


def next_note(history, ngram_dict):
	return dictionary.stochastic_choice(possible_continuations(history, ngram_dict))[0]

	

"""
def continuation_dictionary(note_list, n):
	ng_dict = {}

	for start in range(len(note_list)):
		end = start+n-1

		ngram = " ".join([str(note.midicode) for note in note_list[start:end+1]])

		if ngram in ng_dict:
			ng_dict[ngram] += 1
		else: # not in dictionary
			ng_dict[ngram] = 1

	return ng_dict
"""

def continuation_dictionary(note_list, n):
	ng_dict = {}

	for start in range(len(note_list)-n):
		end = start+n
		ngram = [str(note.midicode) for note in note_list[start:end]]
		if len(ngram) == 1:
			print('ALERT ', ngram)
		history = " ".join(ngram[:-1])
		continuation = ngram[-1]

		if history in ng_dict:
			if continuation in ng_dict[history]:
				ng_dict[history][continuation] += 1
			else:
				ng_dict[history][continuation] = 1
		else:
			ng_dict[history] = {continuation: 1}

	return ng_dict




def continuation_from_seed(start_note, seq_length, continuation_dictionary):
	continuation = [start_note] # initialize sequence
	for i in range(seq_length):
		continuation.append(next_note(continuation[-1], continuation_dictionary))
	return continuation[1:]

# same function, but takes a sequence
def continuation_from_sequence(seq, continuation_length, continuation_dictionary):
	return continuation_from_seed(seq[-1])

def continue_sequence(seq, continuation_length, continuation_dictionary):
	continuation = sequence_from_seed(seq[-1], continuation_length, continuation_dictionary)
	return seq + continuation



if __name__ == '__main__':
	#process_midifile('BeautyAndBeast.mid')
	filepath = 'midifiles/BeautyAndBeast.mid'
	mid = MidiFile(filepath)
	all_notes = notes_by_track_number(mid, 3)
	print(len(all_notes))
	note_ons = [n for n in all_notes if n.type == 'note_on']
	print(len(note_ons))

	ndict = continuation_dictionary(note_ons, 2)

	for i in dictionary.sort_descending(ndict):
		print(i)

	"""
	for i in range(100):
		print(next_note('74', ndict))
	"""

	print(sequence_from_seed('74',5, ndict))




	

