import mido
from mido import Message
from mido import MidiFile
from . import dictionary
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
	if history in ngram_dict:
		return dictionary.normalize(ngram_dict[history])
	else:
		return {}


def continuation_dictionary(note_list, n):
	ng_dict = {}

	for start in range(len(note_list)-n):
		end = start+n
		ngram = [str(note.midicode) for note in note_list[start:end]]
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

# returns a list of ngram dictionaries
def ngram_dictionaries(note_list, max_n):
	return[continuation_dictionary(note_list, n+1) for n in range(max_n)]


#### API FUNCTIONS ####

# given a sequence, return a continuation
def continuation_from_history(history, continuation_length, continuation_dictionary, max_n=2):
	continuation = history[-1*max_n:] # grab the last n members of the sequence
	for i in range(continuation_length):
		next_one = next_note(continuation[-1*max_n:], continuation_dictionary)
		continuation.append(next_one)
	return continuation[max_n-1:]

def full_continued_sequence(history, continuation_length, continuation_dictionary):
	continuation = continuation_from_history(history, continuation_length, continuation_dictionary)
	return history + continuation


def next_note(history, ng_dicts, weights=None):
	# array of strings representing all subets of the history, plus an empty list denoting no history
	sub_histories = [history[i:] for i in range(len(history))] + [[]]

	continuation_sets = []
	for sh in sub_histories:
		ng_size = len(sh)
		ng_dict = ng_dicts[ng_size]
		continuation_sets.append(possible_continuations(' '.join(str(i) for i in sh), ng_dict))

	# previous 5 lines as one-liner:
	# continuation_sets = [possible_continuations(' '.join(sh), ng_dicts[len(sh)]) for sh in sub_histories]

	if not weights: # if no weights, assign higher weights for longer ngram dicts
		weights = [0.5**n for n in range(len(ng_dicts))]

	scored_continuations = dictionary.weighted_union(continuation_sets, weights)
	return dictionary.stochastic_choice(scored_continuations)[0]

def gen_ngrams(filepath):
	mid = MidiFile(filepath)
	all_notes = notes_by_track_number(mid, 3)
	note_ons = [n for n in all_notes if n.type == 'note_on']
	return ngram_dictionaries(note_ons, 3)


if __name__ == '__main__':
	filepath = 'midifiles/BeautyAndBeast.mid'
	mid = MidiFile(filepath)
	all_notes = notes_by_track_number(mid, 3)
	#print(len(all_notes))
	note_ons = [n for n in all_notes if n.type == 'note_on']
	#print(len(note_ons))

	ndict = continuation_dictionary(note_ons, 2)

	ngram_dicts = ngram_dictionaries(note_ons, 3)
	weights = [2**n for n in range(len(ngram_dicts))]
	#print(ngram_dicts[1].keys())
	#print(ngram_dicts[0].values())
	#print(weights)

	print(continuation_from_history(['74'],5, ngram_dicts))

	print(full_continued_sequence(['60','62','63'],5,ngram_dicts))
