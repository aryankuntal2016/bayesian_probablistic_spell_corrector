import Levenshtein
import numpy as np
from itertools import product

alphabets = 'abcdefghijklmnopqrstuvwxyz'


WORDS = []
with open("airports.txt", "r") as f:
	WORDS = [x.strip() for x in f.readlines()]

TOKENS = set([x.lower() for x in WORDS])
TOKEN_TO_WORD_MAP = {x.lower():x  for x in WORDS}

WORDS_LENGTH = len(WORDS)
ONE_WORD_PROBABLITY = 1.0/WORDS_LENGTH


def insert(word):
	tokens = set()
	for i in range(len(word) + 1):
		for alphabet in alphabets:
			tokens.add(word[:i] + alphabet + word[i:])
	return tokens

def delete(word):
	tokens = set()
	for i in range(len(word)):
		tokens.add(word[:i] + word[i+1:])
	return tokens


def substitute(word):
	tokens = set()
	for i in range(len(word)):
		for alphabet in alphabets:
			if alphabet != word[i]:
				tokens.add(word[:i] + alphabet + word[i+1:])

	return tokens


def get_likelihood(word1, word2):
	levenshtein_dist = Levenshtein.distance(word1, word2)
	likelihood = np.exp(-levenshtein_dist)
	return likelihood


def generate_possible_tokens(word, max_distance = 2):
	word = word.lower()
	current_tokens = set([word])
	tokens = set([word])

	for _ in range(max_distance):
		new_tokens = set()
		for token in current_tokens:
			new_tokens.update(insert(token))
			new_tokens.update(delete(token))
			new_tokens.update(substitute(token))
		tokens.update(new_tokens)
		current_tokens = new_tokens
	return tokens



def get_correct_word(incorrect_word, max_dist = 2):
	tokens = generate_possible_tokens(incorrect_word, max_distance)
	correct_word = ""
	best_score = -1

	for token in tokens:

		if token in TOKENS:
			likelihood = get_likelihood(incorrect_word, token)
			score = likelihood*ONE_WORD_PROBABLITY
			if score > best_score:
				best_score = score 
				correct_word = token
	
	if TOKEN_TO_WORD_MAP.get(correct_word):
		return TOKEN_TO_WORD_MAP.get(correct_word)

	return correct_word




if __name__ == "__main__":

	
	incorrect_word = "Tirupitu"
	max_distance = 2
	correct_word = get_correct_word(incorrect_word, max_distance)

	print(correct_word)



	







