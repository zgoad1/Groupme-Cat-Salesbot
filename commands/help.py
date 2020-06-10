from message_sending import send_message
from helper import split_message, print_list
from commands.command import Command
from commands.command import commands


remap = {"cat": 	"cats",
		 "gambl": 	"gambling"}


class Help(Command):
	def respond(self):
		super().respond()

		topics = set()
		printable_topics = []
		for tuple in commands.values():
			for t in tuple[3]:
				topics.add(t)

		for t in topics:
			try:
				printable_topics.append("/help " + remap[t])
			except:
				printable_topics.append("/help " + t)

		# Handle no args
		try:
			topic = self.args[0]
		except:
			return print_list(printable_topics, "There are too many commands to show all at once! Try one of these:")

		# Handle unknown topic
		topic_in_topics = False
		for t in topics:
			if t in topic:
				topic_in_topics = True
				break
		if not topic_in_topics:
			for c in commands.keys():
				if c in topic:
					topic_in_topics = True
					break
			if not topic_in_topics:
				return print_list(printable_topics, "I don't know what that word means! Try one of these:")

		# Find all commands that match the topic
		matched_commands = []
		for name, data in commands.items():
			topic_in_topics = False
			for t in data[3]:
				if t in topic.lower():
					topic_in_topics = True
					matched_commands.append("/{0}\n{1}\nUsage:\n/{0} {2}".format(name, data[0], data[1]))
					if len(data[2]) > 0:
						matched_commands[len(matched_commands) - 1] += '\n' + data[2]
					break
			if topic_in_topics:
				continue
			if name in topic.lower():
				matched_commands.append("/{0}\n{1}\nUsage:\n/{0} {2}".format(name, data[0], data[1]))
				if len(data[2]) > 0:
					matched_commands[len(matched_commands) - 1] += '\n' + data[2]

		lines = print_list(matched_commands, "Commands matching '{}':".format(topic.lower())).split('\n')
		messages = split_message(lines)
		for msg in messages:
			send_message(msg)


# 		lines = """Commands:
# {}
#
# Use a command by typing the '/' character followed by the name of the command.
# Using a command incorrectly will output the command's proper usage, which looks something like this:
# /adopt <cat #> <name>
# Arguments inside <> must be specified, while those in [] are optional. In the above example, both the cat's number and new name must be specified.
# To use this command to adopt the third cat in the shop and name it 'Green Bean', you would type:
# /adopt 3 Green Bean
#
# If you need more help, ask my dad.
# 			""".format(
# 			'\n'.join('\t' + item[0] + ' - ' + item[1][0] for item in commands.items())).split('\n')

		# msgs = split_message(lines)
		# for msg in msgs:
		# 	send_message(msg)
