import database
from commands.challenges import Challenge
from commands.command import Command


class Cancel(Command):
    def respond(self):
        super().respond()

        # Handle usage
        try:
            request_index = int(self.args[0])
        except:
            return self.usage()

        # Get all outgoing request indices
        requests = [tuple[0] for tuple in database.query("""
            SELECT index
            FROM challenges
                JOIN cats ON challenger = cats.name
                JOIN data ON owner = uid
            WHERE uid = '{}';
            """.format(self.uid))]

        # Handle no requests
        if len(requests) == 0:
            return "You have no outgoing challenge requests, {}.".format(self.name)

        # Handle bad index
        if request_index not in requests:
            return "You have no outgoing challenge request with ID {}, {}.".format(request_index, self.name)

        # Reject the request and delete its data
        cancelled = str(Challenge(*(database.query("""
            SELECT *
            FROM challenges
            WHERE index = {};
            """.format(request_index))[0])))
        database.query("""
            DELETE FROM challenges
            WHERE index = {};
            """.format(request_index))
        return "{} has cancelled the following challenge:\n\n{}".format(self.name, cancelled)
