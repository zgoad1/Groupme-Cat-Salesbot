import database
import random
import objects
from helper import prep_name, string_from_words
from commands.challenges import Challenge
from commands.command import Command


battle_bet_increm = 50	# How much to increment battle bets by for each win in a cat's win streak
challenge_announcements = [
	"{} challenges {} to a cat battle!",
	"It's time for {}'s cat to battle {}'s cat.",
	"{1} punches {0} in the face. {0} retaliates by issuing a cat battle!",
	"{} issues a challenge of cat battle to {}!",
	"{} believes their cat is better than {}'s cat.",
	"I think {0} could beat {1} in a cat battle, but I wonder if {1} thinks the same!",
	"{} and {} literally just bought my cats from me, and now they want to make them fight.",
	"Here I am minding my own business, and {} comes up to me and says,\n\"I WANT MY CAT TO FIGHT {}'S CAT RIGHT NOW.\"",
	"What if...\n{}'s cat fought {}'s cat...?\nlol jk...\nUnless...?",
	"Who is better? {} or {}? Let's find out by battling their cats!",
	"Hello, {}. You want to challenge {}? Sure, I'll make your cats fight each other.",
	"Long ago, {1}'s ancestors murdered {0}'s family. Today, {0} gets their revenge in a cat battle.",
	"{}'s strongest cat\nBattling under the sun\nAgainst {}'s cat"
	"{0}'s cat asks {0} for permission to battle {1}'s cat. {0} asks me, and I say \"Yes, you can do that.\"",
	"{} really does not like {} as a person, so they issue a challenge of cat battle!",
	"For some unknown reason, {} wants to make their cat fight {}'s cat.",
	"{} challenges {} to a cat battle, for no significant reason other than to annoy them!"]


class Battle(Command):
	def respond(self):
		super().respond()

		# Handle incorrect usage
		try:
			cats = ' '.join(arg for arg in self.args).split(' vs ')
			print("Checking if {} and {} can fight...".format(cats[0], cats[1]))
		except:
			return self.usage()

		# Check for valid cat names
		owners = []
		try:
			owners.append(database.query("""
				SELECT owner
				FROM cats
				WHERE LOWER(name) = '{}';
				""".format(prep_name(cats[0])))[0][0])
			owners.append(database.query("""
				SELECT owner
				FROM cats
				WHERE LOWER(name) = '{}';
				""".format(prep_name(cats[1])))[0][0])
		except IndexError:
			return "Hey, at least one of those is not a real cat! Check spelling!"

		# Check that this user owns exactly one of the cats
		if self.uid == owners[0] == owners[1]:
			return "You can't make your own cats fight, you monster!"
		if self.uid not in owners:
			return "You can't force other people's cats to fight, you monster!"

		# Get the challengee's UID
		for i in range(0, len(owners)):
			if owners[i] != self.uid:
				challengee = owners[i]
				break

		# Check that neither cat has a pending challenge
		all_cats = database.query("""
			SELECT challenger, challengee
			FROM challenges;
			""")
		all_challengers = [i.lower() for i, j in all_cats]
		all_challengees = [j.lower() for i, j in all_cats]
		for cat in cats:
			if cat.lower() in all_challengers or cat.lower() in all_challengees:
				return "{} already has a pending challenge request!".format(cat)

		# Get bet amount
		wins = []
		wins.append(database.query("""
			SELECT battle_streak
			FROM cats
			WHERE LOWER(name) = '{}';
			""".format(prep_name(cats[0])))[0][0])
		wins.append(database.query("""
			SELECT battle_streak
			FROM cats
			WHERE LOWER(name) = '{}';
			""".format(prep_name(cats[1])))[0][0])
		bet_amount = 0
		for streak in wins:
			bet_amount += (streak + 1) * battle_bet_increm

		# Get our index so we know which cat in the cats array is ours
		if owners[0] == self.uid:
			challenger_index = 0
			challengee_index = 1
		else:
			challenger_index = 1
			challengee_index = 0

		# Make a dictionary for easy data access
		data = {
			self.uid: [self.name,
					   self.money,
					   objects.Cat(*(database.query("""
					   		SELECT *
							FROM cats
							WHERE LOWER(name) = '{}';
						""".format(prep_name(cats[challenger_index])))[0]))],
			challengee: [database.get_user_data(challengee, "name"),
						 database.get_user_data(challengee, "money"),
  					     objects.Cat(*(database.query("""
  					   		SELECT *
  							FROM cats
  							WHERE LOWER(name) = '{}';
  						  """.format(prep_name(cats[challengee_index])))[0]))]
		}

		# Check that both users have enough money to bet
		for key in data.keys():
			if data[key][1] < bet_amount:
				return "{} cannot afford to bet ${}!".format(
					data[key][0], bet_amount
				)

		# Send battle request to the other cat's owner
		for owner in owners:
			if owner != self.uid:
				database.query("""
					INSERT INTO challenges(challenger, challengee, type, prize)
					VALUES('{}', '{}', 'battle', {});
					""".format(data[self.uid][2].name, data[challengee][2].name, bet_amount))

		# Get an object representation of the challenge
		challenge = Challenge(*(database.query("""
			SELECT *
			FROM challenges
			WHERE challenger = '{}';
			""".format(data[self.uid][2].name))[0]))

		return "{}\n\n{}\n\n{}".format(
			random.choice(challenge_announcements).format(self.name, data[challengee][0]),
			str(challenge),
			"{0}: Please respond to this request with '/accept {1}' or '/reject {1}'.".format(data[challengee][0], challenge.index))
