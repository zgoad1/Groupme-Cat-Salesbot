#
# Join words from a list into a string with each word separated by a space
#
def string_from_words(words):
	if len(words) == 0:
		raise IndexError("Tried to make a string from an empty list.")
	return ''.join(w + ' ' for w in words).strip()


#
# Convert a word to an integer representing money
#
def money_from_word(word):
	return int(word.replace('$', ''))


#
# Like str.split() but can take multiple splitter arguments.
# Replaces all the occurrences of each argument with '\`' because I can't
# think of anywhere that character is actually used, then splits the string
# by that character.
#
def multi_split(str, char_list):
	if str is None:
		return None

	new_str = str
	for char in char_list:
		new_str = new_str.replace(char, '\`')
	return new_str.split('\`')


#
# Return a presentable string of each element in a list, separated by nice lines.
# Assumes your list elements don't end in \n.
#
def print_list(_list, header = ""):
	_list = list(_list)

	if len(_list) == 0:
		return

	result = header
	if len(header) > 0:
		result += '\n\n'

	result += _list.pop(0) + '\n'
	for s in _list:
		result += '= ' * 12 + '\n'
		result += s + '\n'

	return result


#
# Prepare to use a cat name, which may contain ' characters, in a query.
#
def prep_name(name):
	return name.lower().replace("’", "'").replace("'", "''")


#
# Split a message into parts that are short enough to legally send.
# lines - an array of lines of a message.
#
def split_message(lines):
	messages = [""]
	while(len(lines) > 0):
		if len(messages[len(messages) - 1]) + len(lines[0]) + 1 > 450:
			messages.append("")
		messages[len(messages) - 1] += lines.pop(0) + '\n'
	return messages

	# msg = ""
	# while(len(lines) > 0):
	# 	if len(msg) + len(lines[0]) + 1 > 450:
	# 		send_message(msg)
	# 		msg = ""
	# 	msg += lines.pop(0) + '\n'
	# if len(msg) > 0:
	# 	send_message(msg)
	# return messages
