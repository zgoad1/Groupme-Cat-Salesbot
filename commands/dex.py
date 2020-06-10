import pokedex
from commands.command import Command


class Dex(Command):
	def respond(self):
		super().respond()

		# Check usage
		if len(self.args) == 0:
			return self.usage()

		desc = pokedex.generateDescription(self.args[0])

		if desc == None:
			return "'{}' is not a real Pokémon you fake gamer.".format(self.args[0])
		return desc
