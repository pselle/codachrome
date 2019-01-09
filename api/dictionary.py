from __future__ import print_function
from __future__ import division
from collections import Counter
import math
import random
from numpy.random import choice
import operator
"""

this class handles the combination of dictionaries of suggestions

"""

#### SORTING ####

# given a list of tuples, returns its items sorted descending by score
def sort_descending(d):
	return list(reversed(sorted(d.items(),key=operator.itemgetter(1))))

# given a list of tuples, returns its items sorted ascending by score
def sort_ascending(d):
	return sorted(d.items(),key=operator.itemgetter(1))

#### LISTING ####

# returns the subset of d that is on the whitelist
def whitelist(d, WL):
	return {k: v for k, v in d.items() if k in WL}

# returns the subset of d that is not on the blacklist
def blacklist(d, BL):
	return {k: v for k, v in d.items() if k not in BL}


######## SET LOGIC ########

# combines several dictionaries into one, adding scores that share the same key
def union(dicts):
	copy = list(dicts)
	union = copy.pop()
	while len(copy) > 0:
		union = dict(Counter(union) + Counter(copy.pop()))
	return union

# union that combines scores according to associated weights
def weighted_union(dicts, weights):
	weighted_dictionaries = [{k: v*weights[i] for k, v in dicts[i].items()} for i in range(len(dicts))]
	return union(weighted_dictionaries)

# returns a single combined dictionary with only keys common to all dicts
def intersect(dicts):
	return whitelist(union(dicts), WL=set.intersection(*[set(d.keys()) for d in dicts]))

# intersection that combines scores according to associated weights
def weighted_intersect(dicts, weights):
	return whitelist(weighted_union(dicts, weights), WL=set.intersection(*[set(d.keys()) for d in dicts]))

# returns the keys in the base with the keys in the addition added, if they're in the base
def augment(base, addition, base_wt, add_wt):
	return whitelist(weighted_union(dicts=[base, addition], weights=[base_wt, add_wt]), WL=base.keys())

def normalize(d):
	total = sum(d.values())
	return {k: v/total for k, v in d.items()}

#### REGRESSION ####

def delta(signal, baseline):
	return {k: signal[k]/baseline[k] for k in signal if k in baseline}


#### PRUNING ####

# returns list of top n scores in d
def top_n(d, n):
	return sort_descending(d)[:n]

# returns list of scores in the top nth percentile
def up_to_threshold(d, threshold):
	sorted_and_normed = sort_descending(normalize(d))
	index = 0
	total = 0
	for key, rate in sorted_and_normed:
		total += rate
		index += 1
		if total > threshold:
			return sorted_and_normed[:index]
	return sorted_and_normed


### CHOICE ####


def random_choice(d):
	return random.choice(d.items())


def stochastic_choice(d):
	total = sum(d.values())
	threshold = total * random.uniform(0,1)
	cumulative = 0
	for k, v in d.items():
		cumulative += v
		if cumulative > threshold:
			return (k, v)
	print("Error: did not reach threshold")
	return None


def random_choose_n(d, n):
	return choice(d.keys(), n)

def stochastic_choose_n(d, n):
	candidates = d.keys()
	total = sum(d.values())
	weights = [v/total for v in d.values()]
	return choice(candidates, n, p=weights, replace=False).tolist()



### ENTROPY MEASURES ###

# entropy of a given decision tree
def entropy(tree):
	return -1 * sum([tree[option] * math.log(tree[option]) for option in tree])

### TESTS ###

def basic_test():
	d1 = {'a': 10, 'b': 15, 'c': 43}
	d2 = {'a': 4, 'y': 21, 'c': 9}

	print(augment(d1,d2,1,1))
	print(union([d1,d2]))
	print(intersect([d1,d2]))
	print(weighted_intersect([d1,d2],[1,5]))
	print(normalize(d1))






def inspect_loop(d):

	while True:
		term = raw_input('Input term >\n')
		print(d[term][:20])

def loops(fdict, max_steps=10):

	loops = {}

	nexts = {k: sort_descending(v)[0][0] for k, v in fdict.items()}

	for k in fdict:
		l = loop(nexts, k)
		order = str(len(l))
		if order in loops:
			loops[order].append(" ".join(l))
		else:
			loops[order] = [" ".join(l)]

def loop(nexts, k, max_steps=10):
	print(nexts)
	history = []
	steps = 0
	current = k
	while steps < max_steps:
		history.append(current)
		current = nexts[current]
		if current == k:
			return history
		steps += 1
	return history



def reversibles(fdict):
	to_return = []
	for w1 in fdict:
		try:
			w2 = sort_descending(fdict[w1])[0][0]
			if sort_descending(fdict.get(w2))[0][0] == w1:
				to_return.append(w1 + " " + w2)
		except:
			print(w1, w2)

	return to_return


if __name__ == '__main__':

	#google_test()
	#entropy_test()
	sa = specific_after()
	#sb = specific_before()
	#print(reversibles(sa, sb))
	#print(reversibles(sa))
	#fdict = sequential.forward_dict('/Users/jbrew/Desktop/github/hitmachine/voices/google/count_2w.txt',n=100000)
	#loops(fdict)
	#print(reversibles(fdict))
	inspect_loop(sa)
	#inspect_loop(sb)


def stochastic_test():
	import time
	options = {'a': 10, 'b': 5, 'c': 0.1}
	while True:
		print(stochastic_choose_n(options, 2))
		time.sleep(0.01)




	