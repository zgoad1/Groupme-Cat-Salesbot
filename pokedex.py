import requests # This works while urllib.requests.urlopen gives a 403 error
from bs4 import BeautifulSoup
from random import randint
from iri_converter import iriToUri
import string
import re


baseURL = 'https://bulbapedia.bulbagarden.net'


#
# Scrape the description of a Pokemon from Bulbapedia.
#
def getDescription(pokemon):
	url = '{}/wiki/{}_(Pokémon)'.format(baseURL, pokemon.capitalize())
	print('Attempting to open: {} '.format(url))
	try:
		html = requests.get(iriToUri(url)).text
		soup = BeautifulSoup(html)
		content = soup.find('span', {'id': 'Biology'}).parent.next_siblings
		# Return all paragraphs under the biology header
		info = []
		for tag in content:
			if tag.name == 'p':
				info.append(tag.get_text())
			if tag.name == 'h2':
				break
		return ' '.join(p for p in info)
	except:
		return None


#
# Markov Chain methods
#

# Simple method to get the sum of all values in a dictionary
def wordListSum(wordList):
	sum = 0
	for word, value in wordList.items():
		sum += value
	return sum


# Choose a random word based on its probability
def retrieveRandomWord(wordList):
	randIndex = randint(1, wordListSum(wordList))
	for word, value in wordList.items():
		randIndex -= value
		if randIndex <= 0:
			return word


# Make a Markov Chain-ready word dictionary out of some reference text
def buildWordDict(text):
	# Remove newlines and quotes
	text = text.replace('\n', ' ').replace('"', '')

	# Make sure punctuation is treated as its own words
	for symbol in string.punctuation:
		text = text.replace(symbol, ' {} '.format(symbol))

	# Convert string to list
	words = text.split()

	# Filter out empty words
	words = [word for word in words if word != '']

	wordDict = {}
	for i in range(1, len(words)):
		if words[i - 1] not in wordDict:
			# Create a new dictionary for this word
			wordDict[words[i - 1]] = {}
		if words[i] not in wordDict[words[i - 1]]:
			# This word has not been found following that word yet, add it
			wordDict[words[i - 1]][words[i]] = 1
		else:
			wordDict[words[i - 1]][words[i]] += 1
	return wordDict


# Procedurally generate a sequence of words vaguely based on the string passed
# in as reference
def markovChain(reference, length):
	dict = buildWordDict(reference)
	chain = [reference.split()[0]]
	print('Starting Markov chain with {} '.format(chain[0]))
	for i in range(0, length):
		# Get a new word based on the previous word
		newWord = retrieveRandomWord(dict[chain[-1]])
		chain.append(newWord)
	return chain


# Clean up a Markov Chain and turn it into a presentable string
def generateDescription(pokemon):
	desc = getDescription(pokemon)
	if desc == None:
		return None
	chain = markovChain(desc, randint(10, 100))
	str = ' '.join(chain)

	# Clean up the result
	# These symbols should have the space before them removed
	for symbol in ['.', ',', '!', '?', ')', ':', ';']:
		str = str.replace(' {}'.format(symbol), symbol)
	# These symbols should have the space after them removed
	for symbol in ['(']:
		str = str.replace('{} '.format(symbol), symbol)
	# These symbols should not be preceded or proceeded by a space
	for symbol in ['\'', '-']:
		str = str.replace(' {} '.format(symbol), symbol)

	# Remove characters from the end of the string until we hit a .
	# If there is no period, add one.
	if('.' not in str):
		str += '.'
	str = re.sub(r'\.((?!\.).)*$', r'.', str)

	return str


# print(generateDescription('Gyarados'))
