import database
import objects
import random
import time
import locations
import os
import math
from message_sending import send_message
from commands.challenges import Challenge


distractions = {
    "A flock of ducks flies overhead, conspiring to distract the cats!":
        ["{} gazes at the majestic flying animals!",
        "{} only looks at the ducks for a second, and attacks {}!"],
    "Suddenly, a volcano erupts on a nearby island, presumably killing all inhabitants!":
        ["{} stares at the eruption, hoping no cats were harmed!",
        "{} quickly accepts that life is ephemeral, and attacks {}!"],
    "Dear me! The president of the United States appears and asks for a handshake from the cats, claiming that his handshakes are the best!":
        ["{} shakes the president's hand, but the president won't let go!",
        "{0} doesn't like humans, and the president is no exception! {0} attacks {1}!"],
    "What's this? The royal family of Catland has been spotted in the audience!":
        ["{} can't help but try to get the attention of the princess!",
        "But {0} doesn't care! {2} attacks {1}!"],
    "Oh no! I've just received word that the local government has been taken over by lizards!":
        ["{0} kneels down and swears that {2} will get revenge on the lizards!",
        "{} spends exactly 0 seconds caring, then attacks {}!"],
    "Gee willikers! Both cats' socks just came untied!":
        ["{} looks down and searches for socks to tie for some time!",
        "{} realizes that I'm messing with them, and attacks {}!"],
    "Golly! A kraken has risen up out of the sea to attack the cats!":
        ["{} attempts to fight the kraken!",
        "{0} watches while {1} fights the kraken, and waits for the perfect moment to deliver a blow!"],
    "Hey! Santa Claus just came to town!":
        ["{} spends some time trying to believe that Santa isn't real!",
        "{} quickly grabs a present from Santa, then runs back to the arena and punches {} in the face!"],
    "A flock of pigs flies overhead, conspiring to distract the cats!":
        ["{} spends some time wondering why there are pigs in the sky!",
        "{0} quickly realizes {2} is hallucinating, laughs it off, then attacks {1}!"],
    "My goodness! Both cats have suddenly dropped dead!":
        ["{} mumbles \"Aw shoot, I died,\" and sits down.",
        "{} realizes I'm trying to distract them, and attacks {}!"]
}


try:
    bot_name = os.getenv("GROUPME_BOT_NAME").split()[0]
except:
    bot_name = "johnson"


def battle(chall):
    # Update the challenge to be in progress
    database.query("""
        UPDATE challenges
        SET in_progress = 'True'
        WHERE index = {};
        """.format(chall.index))

    # cats = {cat: {"points": point total, "stats": [stats]}}
    cats = {
        objects.Cat(*(database.query("""
            SELECT *
            FROM cats
            WHERE name = '{}';
            """.format(chall.challenger))[0])):
        {"points": 0,
         "owner": chall.get_challenger_owner()},
        objects.Cat(*(database.query("""
            SELECT *
            FROM cats
            WHERE name = '{}';
            """.format(chall.challengee))[0])):
        {"points": 0,
         "owner": chall.get_challengee_owner()}}

    for key in cats.keys():
        cats[key].update({"stats": key.stats()})

    # Intro
    send_message(
"""Hi. I'm {} the Robot Boy and I'm coming to you from {}, where today's cat battle is being held.
Without further ado, let's release the cats!""".format(bot_name, locations.get_location()))

    # Get faster cat via slight randomness
    cat_list = list(cats.keys())
    speed0 = cat_list[0].stat_score(cats[cat_list[0]]["stats"][0] + random.randrange(-20, 20))
    speed1 = cat_list[1].stat_score(cats[cat_list[1]]["stats"][0] + random.randrange(-20, 20))
    if speed0 > speed1:
        order = [0, 1]
    else:
        order = [1, 0]

    # First 2 attacks (Speed round)
    send_message(get_attack_round_message(cat_list[order[0]], cat_list[order[1]],
        cats, "{} delivers the first blow!\n"))

    time.sleep(5)

    # Choose a distraction, determine who overcomes it
    dist = random.choice(list(distractions.keys()))
    was_dist = []
    not_dist = []
    for cat in cat_list:
        if random.random() < cat.stat_score(cats[cat]["stats"][2]):
            not_dist.append(cat)
        else:
            was_dist.append(cat)
    message = dist + '\n'

    # Next 2 attacks (Intel round)
    if len(was_dist) == 2:
        message += "Both cats were distracted!\n"
        send_message(message)
    elif len(not_dist) == 2:
        message += "But nary a cat cared!\n"
        send_message(message + get_attack_round_message(cat_list[order[0]], cat_list[order[1]], cats))
    else:
        message += distractions[dist][0].format(was_dist[0].name, not_dist[0].name,
            was_dist[0].pronouns()[0], not_dist[0].pronouns()[0]) + '\n'
        message += distractions[dist][1].format(not_dist[0].name, was_dist[0].name,
            not_dist[0].pronouns()[0], was_dist[0].pronouns()[0]) + '\n'
        message += attack(not_dist[0], was_dist[0], cats)
        send_message(message)

    time.sleep(5)

    # Choose a battle scenario, determine who wins
    message = "In one last attack, {} and {}'s fists meet mid-punch!\n".format(
        cat_list[0].name, cat_list[1].name
    )
    power0 = cat_list[0].stat_score(cats[cat_list[0]]["stats"][1] + random.randrange(-20, 20))
    power1 = cat_list[1].stat_score(cats[cat_list[1]]["stats"][1] + random.randrange(-20, 20))
    if power0 > power1:
        winner = 0
    else:
        winner = 1

    # Final 1 attack (Power round)
    message += "{} is knocked back!\n".format(cat_list[1 - winner].name)
    message += attack(cat_list[winner], cat_list[1 - winner], cats)
    send_message(message)

    # Determine winner
    if cats[cat_list[0]]["points"] > cats[cat_list[1]]["points"]:
        winner = 0
    elif cats[cat_list[0]]["points"] < cats[cat_list[1]]["points"]:
        winner = 1
    else:
        winner = -1

    if winner == -1:
        message = "IT'S A DRAW!\nThere are no prizes to give out, but you can all go home knowing you saw a wonderful cat battle, and that's the real prize anyway."
        send_message(message)
    else:
        message = "{} curls up and takes a nap.\nTHE WINNER IS {}!\n".format(
            cat_list[1 - winner].name, cat_list[winner].name.upper())

        # Show each participant's money changes
        message += "{}: +${}\n{}: -${}".format(cats[cat_list[winner]]["owner"][0],
            chall.prize, cats[cat_list[1 - winner]]["owner"][0], chall.prize)
        send_message(message)
        database.query("""
            UPDATE data
            SET money = money + {}
            WHERE uid = '{}';
            """.format(chall.prize, cats[cat_list[winner]]["owner"][1]))
        database.query("""
            UPDATE data
            SET money = money - {}
            WHERE uid = '{}';
            """.format(chall.prize, cats[cat_list[1 - winner]]["owner"][1]))
        cat_list[winner].wins += 1
        cat_list[winner].battle_streak += 1
        cat_list[1 - winner].losses += 1
        cat_list[1 - winner].battle_streak = 0
        for cat in cat_list:
            cat.update_database()

        # Distribute happiness to winner
        database.set_user_data(cats[cat_list[winner]]["owner"][1], "happiness",
            database.get_user_data(cats[cat_list[winner]]["owner"][1], "happiness") + 5)

    # Distribute exp to cats based on the level of the cat they fought and if they won
    for i in range(0, len(cat_list)):
        exp = max(1, cat_list[1 - i].level - cat_list[i].level) * 10
        if winner == i:
            exp *= 2
        print("\nEXP: Giving {} exp to {}.".format(exp, cat_list[i].name))
        cat_list[i].exp += exp
        level_gain = math.floor(cat_list[i].exp / 100)
        cat_list[i].exp %= 100
        # We still need to update the database here in case they don't do it automatically by leveling up
        cat_list[i].update_database()
        for j in range(0, level_gain):
            cat_list[i].level_up()

    time.sleep(5)

    # Check if each cat deserves cuteness award
    is_cute = []
    cute = [
        cats[cat_list[winner]]["stats"][4],
        cats[cat_list[1 - winner]]["stats"][4] * 2   # losing cat effectively gets doubled cuteness
    ]
    if random.random() < cat_list[winner].stat_score(cute[0]):
        is_cute.append((cat_list[winner], get_cuteness_award(cute[0])))
    if random.random() < cat_list[1 - winner].stat_score(cute[1]):
        is_cute.append((cat_list[1 - winner], get_cuteness_award(cute[1])))
    if len(is_cute) == 0:
        message = "Incidentally, I don't think either of your cats are very cute!"
        send_message(message)
    elif len(is_cute) == 2:
        message = "I've spoken with the judges, and we've agreed that both cats deserve an extra reward because they're just so darn cute.\n{}: +${}\n{}: +${}".format(
            cats[is_cute[0][0]]["owner"][0], is_cute[0][1],
            cats[is_cute[1][0]]["owner"][0], is_cute[1][1]
        )
        send_message(message)
    else:
        message = "I've spoken with the judges, and we've agreed that {} deserves an extra reward because {}'s just so darn cute.\n{}: +${}".format(
            is_cute[0][0].name, is_cute[0][0].pronouns()[0], cats[is_cute[0][0]]["owner"][0], is_cute[0][1]
        )
        send_message(message)

    for cutie in is_cute:
        database.query("""
            UPDATE data
            SET money = money + {}
            WHERE uid = '{}';
            """.format(cutie[1], cats[cutie[0]]["owner"][1]))

    # Delete this challenge from the database
    database.query("""
        DELETE FROM challenges
        WHERE challenger = '{}';
        """.format(chall.challenger))


def attack(attacker, victim, cats):
    message = ""
    # Check victim's coolness
    rand = random.random()
    score = victim.stat_score(cats[victim]["stats"][3] / 4)
    if rand < score:
        cool = True
        message += "{}'s coolness manifests around {} in the form of a shield, weakening the next attack!\n".format(
            victim.name, victim.pronouns()[1])
    else:
        cool = False

    # Check attacker's luck (accuracy), attackee's speed (evasiveness)
    if random.random() > attacker.stat_score(cats[attacker]["stats"][5] / cats[victim]["stats"][0] * 200):
        message += "But {}'s attack missed! Oh, how unfortunate!\n".format(attacker.name)
        return message

    # Get damage
    damage = int(max(1, (cats[attacker]["stats"][1]
        + random.randrange(int(-0.25 * cats[attacker]["stats"][1]), int(0.25 * cats[attacker]["stats"][1])))
        / 10))
    if cool:
        damage = max(1, int(damage / 2))
    message += "{} takes {} damage!\n".format(victim.name, damage)
    cats[attacker]["points"] += damage
    return message


def get_attack_round_message(cat0, cat1, cats, atkmsg0 = "{} attacks!\n", atkmsg1 = "{} attacks!\n"):
    message = ""
    message += atkmsg0.format(cat0.name)
    message += attack(cat0, cat1, cats)
    message += atkmsg1.format(cat1.name)
    message += attack(cat1, cat0, cats)
    return message

def get_cuteness_award(cute):
    return max(10, int(min(1000, (random.randrange(0, cute) / 50) ** 2.5)))


# scores = 0
# for i in range(0, 10000):
#     scores += get_cuteness_award(800)
#
# print("Average reward: " + str(scores / 10000) + "\nSingle reward: " + str(get_cuteness_award(800)))
