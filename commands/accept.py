import database
from message_sending import send_message
from challenges.battle import battle
from commands.challenges import Challenge
from commands.command import Command


class Accept(Command):
    def respond(self):
        super().respond()

        # Handle usage
        try:
            request_index = int(self.args[0])
        except:
            return self.usage()

        # Get all incoming request indices
        requests = [tuple[0] for tuple in database.query("""
            SELECT index
            FROM challenges
                JOIN cats ON challengee = cats.name
                JOIN data ON owner = uid
            WHERE uid = '{}';
            """.format(self.uid))]

        # Handle no requests
        if len(requests) == 0:
            return "You have no incoming challenge requests, {}.".format(self.name)

        # Handle challenge already in progress
        in_progress = database.query("""
            SELECT *
            FROM challenges
            WHERE in_progress = 'True';
            """)
        if len(in_progress) > 0:
            return "Wait until the current battle is over, you impatient buffoon!"

        # Handle bad index
        if request_index not in requests:
            return "You have no incoming challenge request with ID {}, {}.".format(
                request_index, self.name)

        # Accept the request, mark it as in progress, wait until it's over to delete it
        accepted = Challenge(*(database.query("""
            SELECT *
            FROM challenges
            WHERE index = {};
            """.format(request_index))[0]))
        database.query("""
            UPDATE challenges
            SET in_progress = 'True'
            WHERE challenger = '{}';
            """.format(accepted.challenger))

        send_message("{} has accepted the following challenge:\n\n{}".format(
            self.name, accepted))

        # Start the battle
        battle(accepted)
