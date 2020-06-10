import database
from helper import print_list, string_from_words, prep_name
from commands.command import Command


class Challenge:
    def __init__(self, index, challenger, challengee, type, prize, in_progress = False):
        self.index = index
        self.challenger = challenger
        self.challengee = challengee
        self.type = type
        self.prize = prize
        self.challenger_owner = None
        self.challenger_uid = None
        self.challengee_owner = None
        self.challengee_uid = None
        self.in_progress = in_progress

    def __str__(self):
        challenger_owner = self.get_challenger_owner()[0]
        challengee_owner = self.get_challengee_owner()[0]
        challenger_streak = database.query("""
            SELECT battle_streak
            FROM challenges JOIN cats ON challenger = name
            WHERE name = '{}';
            """.format(self.challenger))[0][0]
        challengee_streak = database.query("""
            SELECT battle_streak
            FROM challenges JOIN cats ON challengee = name
            WHERE name = '{}';
            """.format(self.challengee))[0][0]

        return "ID: {}\nChallenger: {}\nChallengee: {}\n{} (streak: {}) vs. {} (streak: {})\n{} for ${}".format(
            self.index, challenger_owner, challengee_owner, self.challenger,
            challenger_streak, self.challengee, challengee_streak,
            self.type.capitalize(), self.prize
        )

    def get_challenger_owner(self):
        if self.challenger_owner == None:
            self.challenger_owner, self.challenger_uid = database.query("""
                SELECT data.name, uid
                FROM challenges
                    JOIN cats ON challenger = cats.name
                    JOIN data ON owner = uid
                WHERE index = {};
                """.format(self.index))[0]
        return (self.challenger_owner, self.challenger_uid)

    def get_challengee_owner(self):
        if self.challengee_owner == None:
            self.challengee_owner, self.challengee_uid = database.query("""
                SELECT data.name, uid
                FROM challenges
                    JOIN cats ON challengee = cats.name
                    JOIN data ON owner = uid
                WHERE index = {};
                """.format(self.index))[0]
        return (self.challengee_owner, self.challengee_uid)


class Challenges(Command):
    def respond(self):
        super().respond()

        # Handle no args
        try:
            dir = self.args[0][0].lower()
            if dir != 'i' and dir != 'o':
                raise ValueError
        except:
            return self.usage()

        # Handle no user args
        try:
            user = string_from_words(self.args[1:])
        except:
            user = self.name

        # Handle nonexistent user
        try:
            uid = database.query("""
                SELECT uid
                FROM data
                WHERE LOWER(name) = '{}';
                """.format(prep_name(user)))[0][0]
        except:
            return "I could not find the human you call '{}'.".format(user)

        if dir == 'i':
            # Get challenge list (where the challengee cat belongs to us)
            challenges = [str(Challenge(*c)) for c in database.query("""
                SELECT index, challenger, challengee, type, prize
                FROM challenges JOIN cats ON challengee = name
                WHERE owner = '{}';
                """.format(uid))]

            # Handle no challenges
            if len(challenges) == 0:
                return "{} has no incoming challenge requests.".format(user)

            # Display all incoming challenges
            return print_list(challenges, "{}'s incoming challenges:".format(user))

        else:
            # Get challenge list (where the challenger cat belongs to us)
            challenges = [str(Challenge(*c)) for c in database.query("""
                SELECT index, challenger, challengee, type, prize
                FROM challenges JOIN cats ON challenger = name
                WHERE owner = '{}';
                """.format(uid))]

            # Handle no challenges
            if len(challenges) == 0:
                return "{} has no outgoing challenge requests.".format(user)

            # Display all incoming challenges
            return print_list(challenges, "{}'s outgoing challenges:".format(user))
