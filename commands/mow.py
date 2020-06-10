from commands.command import Command


mowing_link = "https://bit.ly/2YfgVBJ"	# MOWING


class Mow(Command):
	def respond(self):
		super().respond()
		return "ARE YOU READY FOR A TRUE GAMING EXPERIENCE, GAMER?\nCLICK >> {0}\nCLICK >> {0}\nCLICK >> {0}".format(mowing_link)
