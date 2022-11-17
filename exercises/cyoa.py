"""An RPG in a choose-your-own-adventure style."""

__author__ = "930605992"


import time
from random import randint, uniform
# import msvcrt


points: int = 0
gold: int = 50
user_name: str = ""
player: str = ""
max_health: int = 30
health: int = 30
speed: int = 10
room_id: str = "tutorial"
met_jester: bool = False
enemy_distracted: bool = False
upgrades: list[str] = list()
temp_item_buffs_ADS: list[int] = [0, 0, 0]  # attack buff, defense buff, shield active or not
hp_potions: int = 5
arrows_ready: int = 4
arrows_quiver: int = 30
poisoned_arrow_bunch: int = 0
using_poisoned_arrows: bool = False
poison_left: list[int] = [0, 0, 0, 0, 0, 0, 0, 0]
attack_up_scroll: int = 0
defense_up_ointment: int = 0
ItemPrice = tuple[str, int, str]  # Name, Price, Extra space if needed
EnemyStats = tuple[str, int, int, int, int, int, int]  # Name, Health, Attack, Defense, Speed (inverse to Accuracy Window if have reaction attack upgrade), G on kill, points on win
enemy_current_health: list[int] = list()
who_alive: list[bool] = [True]

U_PLAYR: str = "\U0000265F"
U_BOX_G: str = "\U0001F7E9"
U_BOX_Y: str = "\U0001F7E8"
U_BOX_R: str = "\U0001F7E5"


def main() -> None:
    """Entrypoint of program."""
    greet()
    global health
    health = max_health
    still_playing: bool = True
    while still_playing:
        global room_id
        draw_map(room_id)
        path: str = room_dialogue(room_id)
        if path == "fight":
            room_id = room_fight(room_id)
        else:
            room_id = path
        

def greet() -> None:
    """Begin the game with instructions and lore, and input names."""
    global points
    global player
    input("(When lines of text not requiring input appear, press the ENTER key to progress after reading.)")
    print("(Good. Now, when input is required, options such as [FIGHT] or [TALK] will be included")
    choice: str = input("  and you should type one of them (minus the brackets) (not case sensitive), [OKAY]?) ").lower()
    # while choice != "okay":
    #     choice = input("(So if the option you want to select is [OKAY], you can type \"okay\", [OKAY]?) ").lower()
    if choice == "okay":
        input("(Great! Thank you for listening.)")
        points += 10
    else:
        choice = input("(So if the option you want to select is [OKAY], you can type \"okay\", [OKAY]?) ").lower()
        if choice == "okay":
            input("(Nice! Thanks for listening.)")
            points += 5
        else:
            input("(Um... that's not exactly an \"okay\", but it'll do for now.)")
    input("(Sometimes, though, a hidden option you might have used in the past can be available, even if not listed, so type wisely...)")
    input("(And now that the controls have been introduced...)")
    input("(On with the show.)")
    points += 5
    input("Greetings, and welcome to \"After Check!\"")
    input("In this adventure, the Great Board has just concluded a fearsome battle, ending in a devastating checkmate, the White Side triumphing.")
    input("(In case you couldn't tell, this is chess.)")
    input("((Just, y'know, making sure you got it...))")
    input("(((and that you're paying attention)))")
    input("((((Okay, okay, sorry; I'll get back to narrating, jeez...))))")
    input("Though while the White Side emerged victorious, the Black Side's remaining members harbored an intense emnity after having been defeated.")
    input("Eventually, several minutes later, one such pawn embarked on a monumental quest of revenge...")
    player = input("Now... What's that daring hero's name? ")
    while not player:
        player = input("(Please don't just spam enter. Name the hero.) ")
    input("...Interesting...")
    input(f"And the hero's name... was {player}.")
    print(f"Welcome, {player}!")
    global user_name
    print("But what of the user?")
    user_name = input("What is your name? ")
    while not user_name:
        user_name = input("(Really? Don't detract from the experience. What is your real name?) ")
    input("Ah, very good. Well then, it is time to begin your journey.")
    input(f"Good luck, {user_name}.\n")
    input(f"And so, {player} set off, seeking vengeance.")
    input("However, they lacked training, and decided to start by stopping by to see an impartial (and rather eccentric) character for some training: the jester.")
    points += 5


def draw_map(room: str) -> None:
    """Draw rooms that the player enters using emojis."""
    global U_PLAYR
    U_BWALL: str = "\U00002B1B"
    U_FLOOR: str = "\U00002B1C"
    U_JOKER: str = "\U0001F0CF"
    U_WPAWN: str = "\U00002659"
    U_KNGHT: str = "\U00002658"
    U_BSHOP: str = "\U00002657"
    U_WROOK: str = "\U00002656"
    U_QUEEN: str = "\U00002655"
    U_WKING_ROTATED: str = "\U0001FA09"
    u_current_enemy: str = ""
    if room == "pawn":
        u_current_enemy = U_WPAWN
    elif room == "knight":
        u_current_enemy = U_KNGHT
    elif room == "bishop":
        u_current_enemy = U_BSHOP
    elif room == "rook":
        u_current_enemy = U_WROOK
    elif room == "queen":
        u_current_enemy = U_QUEEN
    else:
        u_current_enemy = U_FLOOR

    if room == "tutorial":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_JOKER}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "tutorial_intersection":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "shop_intersection":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "shop":
        U_BUILD: str = "\U0001F7EB"
        U_SLOTS: str = "\U0001F3B0"
        U_GSIGN: str = "\U00002733"
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BUILD}{U_BUILD}{U_BUILD}{U_BUILD}{U_BUILD}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_BUILD}{U_FLOOR}{U_GSIGN}{U_FLOOR}{U_BUILD}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BUILD}{U_FLOOR}{U_SLOTS}{U_FLOOR}{U_BUILD}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "pawn_legion":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_WPAWN}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_WPAWN}{U_WPAWN}{U_WPAWN}{U_WPAWN}{U_WPAWN}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_WPAWN}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_WPAWN}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "king" or room == "king_spared":
        U_WKING: str = "\U00002654"
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_WKING}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "king_dead":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_WKING_ROTATED}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "king_dead_joker":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_WKING_ROTATED}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_JOKER}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    elif room == "empty_normal":
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')
    else:
        print(f'''
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{u_current_enemy}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_PLAYR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}
        {U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_FLOOR}{U_BWALL}{U_BWALL}{U_BWALL}{U_BWALL}
        ''')


def room_dialogue(room: str) -> str:
    """Interact with characters depending on the room the player enters."""
    choice: str = ""
    global points
    if room == "tutorial":
        print(f"{player} arrives near the entrance to the White Castle, colloquially referred to as \"The Guantlet\" because of its")
        input("oddly linear path and progression of difficulty leading straight to the castle, which strikes most as strategically inept.")
        input(f"Ahead of {player} is the local jester - a neutral party and a bit of a wild card, but more than happy to spar.")
        input("Some training might be useful before wagering your life in a series of disadventageous battles. And who knows? They could offer a reward for beating them.")
        choice = input("Would you like to [TALK], skip them and go [RIGHT] to the Guantlet, or [QUIT] here? ").lower()
        while choice != "talk" and choice != "right":
            if choice == "quit":
                quit_game()
            choice = input("[TALK] to the jester, go [RIGHT], or [QUIT] the game? ").lower()
        if choice == "right":
            return "tutorial_intersection"
        else:
            global met_jester 
            met_jester = True
            points += 15
            input("JESTER: \"Uee hee hee! You want to learn to keep yourself out of a garbage bin?")
            input("         You'll be glad you came to me! I'll teach you how to win, win, win!")
            input("         Go right for a fight, but you pay for that fray...")
            input("         But not with me; this brawl is free!\"")
            return "fight"
    elif room == "tutorial_intersection":
        choice = input(f"{player} braces themself as they prepare to advance through the Guantlet. There's nothing else to do now but continue [UP] or [QUIT]. ").lower()
        if choice == "quit":
            quit_game()
        i: int = 0
        while choice != "up":
            if choice == "quit":
                quit_game()
            if i == 0:
                choice = input("There's literally nothing to do here. Go [UP]. ").lower()
            elif i == 1:
                choice = input("Seriously. Stop it. [UP]. Now. ").lower()
            elif i == 2:
                choice = input("Really? Quit stalling. Go on, you can do it: [UP]. ").lower()
            elif i == 3:
                choice = input("Oh come on; it's just two letters! [UP] isn't hard to type! ").lower()
            elif i == 4:
                choice = input("Ugh, okay, fine, just take some adventure points and leave [UP].").lower()
                points += 20
            else:
                choice = input("Proceed [UP]. ").lower()
            i += 1
        return "pawn"
    elif room == "pawn":
        print(f"Before {player}, the intrepid pawn, stands a fellow pawn, yet of the opposite side. This shall be the true beginning of your vengeful spree.")
        choice = input(f"There is no turning back. Not for {player}. {player}, at least right now, only wants to [FIGHT]. Now, as a courtesy, what will you do? [QUIT]? Or [FIGHT]? ").lower()
        while choice != "fight" and choice != "talk":
            if choice == "quit":
                quit_game()
            choice = input(f"{player} is too blinded by fury to do anything but [FIGHT]... at least for now. ").lower()
        input("PAWN: \"Oh? A survivor? Go back home and sulk, you miserable wretch. Your side's been beaten!\"")
        input("      \"Really? You're gonna face me head-on? Bring it! I'm due for a promotion soon anyway!\"")
        points += 5
        return "fight"
    elif room == "knight":
        choice = input(f"In this section of the Guantlet, {player} encounters a fearsome knight atop their horse. Will you [TALK], [FIGHT], or [QUIT]? ").lower()
        while choice != "fight" and choice != "talk":
            if choice == "quit":
                quit_game()
            choice = input("Your only choices here are [TALK] and [FIGHT], and given the look of disgust on the knight's face, they'll do the same thing... ").lower()
        if choice == "talk":
            points += 15
            input("KNIGHT: \"Um.\"")
            input("        \"What are you doing here? We already destroyed you lot.\"")
            input("        \"Leave before I make you leave, knave.\"")
            choice = input("Well, it was worth a shot. [FIGHT]. ").lower()
            while choice != "fight":
                if choice == "quit":
                    quit_game()
                choice = input("Proceed to the [FIGHT]. ").lower()
        print("        \"Alright, that's it. I'm gonna fry your liver. You can try to put up a fight and make it challenging, I guess.")
        input("        \"Catch me if you can!\"")
        input("        \"Spoiler alert: you can't!\"")
        return "fight"
    elif room == "pawn_legion":
        choice = input(f"As {player} advances, they come across a whole platoon of pawns! They seem angry about something. [TALK], [FIGHT], or [QUIT]? ").lower()
        while choice != "fight" and choice != "talk":
            if choice == "quit":
                quit_game()
            choice = input("I'm... not sure you have much choice here. You can immediately [FIGHT] them, or you could attempt to [TALK] to them. ").lower()
        if choice == "talk":
            points += 15
            input("PAWN 1: \"Hey, what the-")
            input("         What's a black pawn doing all the way over-\"")
            input("PAWN 4: \"Hold up. That's the little snot that merc'd Gary!\"")
            input("PAWN 6: \"WHAT???\"")
            input("PAWN 3: \"Let's get'im!")
            input("They're out for blood. I'm sensing a pattern with trying to talk to these guys before fighting them... At least you get some adventure points out of it.")
            while choice != "fight":
                choice = input("Well, time to [FIGHT]. ").lower()
                if choice == "quit":
                    quit_game()
        input("PAWN 7: \"We've got you surrounded, at least from this side!\"")
        input("PAWN 5: \"You're outnumbered. Just give up now!\"")
        input("PAWN 2: \"Can't dodge all of us forever. Let's get this over with.\"")
        input("PAWN 1: \"Square up.\"")
        return "fight"
    elif room == "shop_intersection":
        choice = input(f"{player} comes across a branch in the path. Do you [QUIT], investigate [RIGHT], or continue [UP]? You won't be able to return if you proceed upwards. ").lower()
        while choice != "up" and choice != "right":
            if choice == "quit":
                quit_game()
            choice = input("Deviate and go [RIGHT] or continue fighting [UP] without resting.").lower()
        if choice == "right":
            return "shop"
        else:
            return "bishop"
    elif room == "shop":
        points += 15
        input(f"{player} comes across a wooden structure with a sign advertising \"shop\", with a flashy, unfamiliar shopkeep seated inside.")
        choice = input("[TALK] to them, go back [LEFT], or [QUIT]? ").lower()
        while choice != "talk" and choice != "left":
            if choice == "quit":
                quit_game()
            choice = input("There isn't much to do here other than [TALK] to the merchant, so do so or retrn [LEFT]. ")
        if choice == "left":
            input("           Hm. How rude. You've already decided you don't require my services without speaking to me or perusing the options? Fine, but you might just regret it later.")
            return "shop_intersection"
        else:
            choice = input("SHOPKEEP: \"Welcome, traveler, warrior, whatever you might be... Could I interest you in a deal of some sort? I have many wares available... for a price, of course. ").lower()
            if choice == "no":
                input("           Hm. How rude. You've already decided you don't require my services before perusing the options? Suit yourself. You might just regret it later.")
                points += 5
            else:
                if shop_menu():
                    input("SHOPKEEP: \"You have my gratitude. Thank you for your patronage. Luck be upon you on the rest of your journey, and may fortune smile upon your quest.\"")
                    points += 50
                else:
                    input("SHOPKEEP: \"Seen enough? Thank you for browsing, in any case. Luck be upon you; without making a purchase, I'd wager you'll need it.\"")
                    points += 10
            return "shop_intersection"
    elif room == "bishop":
        input(f"After a bit more traveling, {player} finds themself entering fancier and fancier terrain, and comes across a haughty-looking bishop with a pointy hat.")
        input("The bishop seems to notice you quite quickly, glaring out of the corner of their eye, but not saying anything as of yet.")
        choice = input("What course of action would you like to pursue? Attempt to [TALK] and reason with them, [FIGHT] right away, or [QUIT]? ").lower()
        while choice != "fight" and choice != "talk":
            if choice == "quit":
                quit_game()
            choice = input("I don't think you can really do anything to circumvent the bishop. [TALK] with them or jump straight to the [FIGHT]. ").lower()
        if choice == "talk":
            points += 15
            choice = input("BISHOP: \"Oh. Now it tries to talk to me. What do you want, peasant?\" ").lower()
            if "kill" in choice or "fight" in choice or "destroy" in choice:
                input("        \"My. How uncivilized.")
                if "kill me" not in choice and "destroy me" not in choice:
                    input("         I highly doubt you can significantly harm me. How about I dispose of you, instead?\"")
                points += 15
            print("        \"Eugh; I'm glad we're enemies.\"")
            choice = input("The bishop's disdain for you is evident. It seems you'll have to [FIGHT] them. ").lower()
            while choice != "fight":
                if choice == "quit":
                    quit_game()
                elif choice == "talk":
                    choice == input("The bishop doesn't seem much for conversation. ").lower()
                else:
                    choice == input("This bishop's ego with be their downfall; they're a bit overconfident in their ability to [FIGHT]. ").lower()
        deity: str = "Chess"
        if randint(0, 3) == 3:
            global user_name
            deity = user_name
        input(f"BISHOP: \"Now then, let us begin. The power of {deity} compels you! Begone, pawn!")
        return "fight"
    elif room == "rook":
        input(f"{player} comes upon the next obstacle to overcome: a well-armored bastion of a rook. Their expresson is stern, and their arms are crossed.")
        choice = input("What do you want to do? [TALK] to them and try to reason your way by, [FIGHT] them right away, or [QUIT]? ").lower()
        while choice != "fight" and choice != "talk":
            if choice == "quit":
                quit_game()
            choice = input("This rook is not moving. Looks like you'll have to [TALK] to them or even just plain [FIGHT]. ").lower()
        if choice == "talk":
            points += 20
            input("ROOK: \"Halt! None shall pass this. I have strict orders to not let anyone by.")
            print("       Though if you are a pawn or even simply a civilian, you are advised to take shelter.\"")
            input("      \"There have been reports of a deranged madpiece sent by the defeated enemy slaughtering our troops, working their way through the ranks...\"")
            input("      \"...\"")
            input("      \"...Wait...\"")
            print("      \"You're a pawn of the black side, right?\"")
            while choice != "yes" and choice != "no":
                choice = input("[YES] or [NO]? ").lower()
                if choice == "quit":
                    quit_game()
            if choice == "yes":
                print("ROOK: \"Ah, I thought so! You must be sympathetic towards our side, though, if you're this close to the Castle.")
                input("       If you see the rampaging one, could you ask them to stop, please? Comrade to comrade?\"")
                input("      \"...\"")
            else:
                input("ROOK: \"Oh. Hm. Sorry for assuming.\"")
                input("      \"...\"")
                input("      \"...No, wait... You definitely are... But why would you lie to me like that?\"")
            input("      \"WAIT OH NO THAT'S YOU!!!\"")
            choice = input("Darn; they've seen through your ruse. Oh well. Here you go [FIGHT]ing again. ").lower()
            while choice != "fight":
                choice = input("The rook has seen through your attempts at deceit and is now on guard. You'll have to [FIGHT]. ").lower()
                if choice == "quit":
                    quit_game()
        else:
            input("ROOK: \"What the heck? What are you doing? Halt!\"")
        input(f"{player} approaches the rook.")
        input("ROOK: \"So we must clash? In that case, I shall strike you down!\"")
        return "fight"
    elif room == "queen":
        input(f"As they near the end of the Guantlet, {player}'s path is suddenly blocked by an incredibly intimidating presence...")
        input(f"The Queen appears! Their regal form towers above you. A flash of regret passes through {player} as they glare down at them.")
        choice = input("What will you do? What can you do, though? [TALK]? [FIGHT]? [QUIT]? ").lower()
        while choice != "talk" and choice != "fight":
            if choice == "quit":
                quit_game()
            choice = input("There's no turning back now... You must proceed. [TALK] or [FIGHT]. ").lower()
        if choice == "talk":
            points += 20
            input("QUEEN: \"Lowly pawn... How dare thee intrude upon our Castle Grounds?\"")
            input("       \"We will enlighten thee about defiling our Royal Realm!\"")
            input("       \"Ah, and we will claim vengeance for our fallen subjects.\"")
            choice = input(f"The Queen and {player} glare at each other... Looks like [FIGHT]ing is your only option. ").lower()
            tried_talking: bool = False
            while choice != "fight":
                if choice == "quit":
                    quit_game()
                elif choice == "talk" and not tried_talking:
                    print("QUEEN: \"Don't bother trying to deceive us with your talk of justice. We're not as soft as the King.\"")
                    points += 10
                    tried_talking = True
                choice = input("Proceed. [FIGHT]. ").lower()
        input("QUEEN: \"You dare to resist us? Have at thee, villainous cur! Off with thy head!\"")
        return "fight"
    elif room == "king":
        input(f"Finally, after a difficult journey plagued with trials, {player} arrives at the throne room: the pinnacle of the Guantlet.")
        input("The enemy King sits before you upon their throne. They raise their gaze, settling upon {player}. Their face bears an expression of weariness.")
        choice = input("This is it. [TALK]. [FIGHT]. [QUIT]. In any case, this is where it ends. ").lower()
        i = 0
        while choice != "talk" and choice != "fight":
            if choice == "quit":
                quit_game()
            if i == 0:
                choice = input("You cannot evade fate, at least for now... Perhaps once you've sufficiently weakened the King? No matter. At the moment, you must [TALK] or [FIGHT]. ").lower()
            else:
                choice = input("[TALK]. [FIGHT]. In whatever you choose, proceed. ").lower()
            i += 1
        if choice == "talk":
            points += 25
            input("KING: \"Greetings, young one.\"")
            input("      \"I want so badly to offer you refreshments of some sort... but I suppose I cannot do that.\"")
            input("      \"It was never my intention to go to war... nor to instill such a burning hatred for your kind within my subjects.\"")
            input("      \"I never wanted for so much blood to be shed. Please, if you have it within you, forgive me for this.\"")
            input("      \"I wholly understand if that is an impossibility, though.\"")
            input("      \"It was nice to meet you, little pawn. Truly.\"")
            input("The King rises from their seat, their face having assumed a visage of resigned determination.")
            input("They are sparing you from having to make the choice one final time, initiating the fight themself.")
        print("KING: \"I'm sorry.\"")
        time.sleep(1)
        print(f"     \"Farewell, {player}.\"")
        time.sleep(1)
        input("The King attacks.")
        return "fight"
    elif room == "king_spared":
        points += 100
        input("KING: \"You... You're sparing me? After all I've done?\"")
        input("      \"From the bottom of my heart... you have my gratitude.\"")
        input("      \"Come... let us put an end to this senseless hatred.\"")
        print(f"      \"We shall foster a new era of piece between our peoples. {player}, would you speak on behalf of your people and bridge the gap between our nations?")
        choice = input("[YES] or [NO]? ").lower()
        while choice != "yes" and choice != "no":
            choice = input("Will you become the ambassador of the Black Side? ")
        if choice == "yes":
            points += 15
            input(f"KING: \"Excellent. Thank you, {player}. Now, let us begin. This will be... a long process...")
        else:
            points += 5
            input(f"KING: \"Ah... That is alright. I cannot force you to do anything. In any case, I must now start to reform my kingdom. I will call an escort to see you back home. Goodbye, {player}.")
        input(f"And so, {player}'s quest has come to a close, ending in peace after a trail of bloodshed...")
        quit_game()
        return "tutorial"
    elif room == "king_dead":
        points += 100
        input(f"And so... it is done. {player} has defeated the White Side and taken revenge for the slaughtering of their forces.")
        input(f"A creeping sense of cold emptiness begins to engulf {player} as the finality of what they've done sets in...")
        input(f"But then a strangely familiar voice calls out from behind {player}...")
        input("? ? ? : \"So then... you've succeeded.\"")
        input("        \"Exactly as I planned, exactly as I needed.\"")
        choice = input(". . . [ T U R N ]   a r o u n d . . .").lower()
        while choice != "turn":
            if choice == "quit":
                input("You cannot quit now.")
            print("? ? ? : \"Face me. Then you'll see.\"")
            choice = input("[TURN] AROUND. ")
        input("You turn around to see the Jester from outside the entrance grinning broadly, casting a shadow in the light from the doorway.")
        draw_map("king_dead_joker")
        input("JESTER: \"Thanks to your continued assistance, in getting here, I've met no resistance!\"")
        input("        \"You've paved a path for me to get my way; if you don't mind I'll fill this power vacuum...")
        input("         So at the end of the day, it's MY seeds of power that'll bloom!\"")
        input("        \"But wait, if we tussle now I'll surely fail,")
        input("         unless I find a way to somehow end the tale...\"")
        input(f"        \"After all, {player}, you're but a puppet on strings.")
        input("         Winning over and over until I die once would sting.\"")
        input(f"        \"So goodbye, {user_name}. Perhaps our meeting was fated...")
        print("        It's been fun, but now-\"-")
        time.sleep(1)
        print("<<Error: Connection Terminated>>")
        time.sleep(3)
        quit_game()
        return "tutorial"
    else:
        input("The room dialogue being called for does not exist. Sorry! You've somehow broken the game.")
        return "tutorial"


def room_fight(room: str) -> str:
    """Begin a fight with the proper character."""
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    input("FIGHT!")
    choice: str = ""
    turn: int = 1
    HEALTH_UPGRADE_HEALTH: int = 60
    global max_health
    global who_alive
    who_alive = [True]
    enemy: EnemyStats
    STATS_JESTER: EnemyStats = ("Jester", 30, 15, 20, 99, 30, 50)
    STATS_PAWN: EnemyStats = ("Pawn", 15, 10, 20, 10, 5, 15)
    STATS_KNIGHT: EnemyStats = ("Knight", 40, 25, 25, 80, 50, 30)
    STATS_BISHOP: EnemyStats = ("Bishop", 20, 75, 5, 50, 75, 50)
    STATS_ROOK: EnemyStats = ("Rook", 50, 25, 80, 15, 50, 75)
    STATS_QUEEN: EnemyStats = ("Queen", 75, 80, 60, 90, 300, 100)
    STATS_KING: EnemyStats = ("King", 300, 50, 20, 20, 100, 85)
    if room == "tutorial":
        enemy = STATS_JESTER
    elif room == STATS_PAWN[0].lower():
        enemy = STATS_PAWN
    elif room == STATS_KNIGHT[0].lower():
        enemy = STATS_KNIGHT
    elif room == "pawn_legion":
        enemy = STATS_PAWN
        who_alive = [True, True, True, True, True, True, True, True]
    elif room == STATS_BISHOP[0].lower():
        enemy = STATS_BISHOP
    elif room == STATS_ROOK[0].lower():
        enemy = STATS_ROOK
    elif room == STATS_QUEEN[0].lower():
        enemy = STATS_QUEEN
    elif room == STATS_KING[0].lower():
        enemy = STATS_KING
    global enemy_current_health
    enemy_current_health.append(enemy[1])
    if room == "pawn_legion":
        i: int = 1
        while i < 8:
            enemy_current_health.append(enemy[1])
            i += i
    global health
    while True in who_alive and health > 0:
        if room == "queen":
            enemy_turn(room, enemy, who_alive)
        else:
            player_turn(room, enemy, turn, who_alive)
        if room != "queen":
            enemy_turn(room, enemy, who_alive)
        else:
            player_turn(room, enemy, turn, who_alive)
        turn += 1
    if health > 0:
        global upgrades
        global points
        global gold
        points += enemy[5]
        gold += enemy[6]
        if room != "pawn_legion":
            input(f"Congratulations! You've defeated the {enemy[0]}!")
        else:
            input("Congratulations! You've defeated the legion of pawns!")
        input(f"You earned {enemy[6]}G!")
        if room == "tutorial":
            upgrades.append("iron shield")
            input("You received the Iron Shield! Much sturdier than your wooden shield. Can reduce incoming damage for 3 turns instead of 2!")
            return "tutorial_intersection"
        elif room == "pawn":
            upgrades.append("pawn soul")  # en passant (reactionary attacks)
            input("You've collected the soul of the enemy pawn. It increases your Pawn Power, and through the power of En Passant, your attacks now rely on Reaction Speed!")
            return "knight"
        elif room == "knight":
            upgrades.append("knight soul")  # widens window of reactionary attack (not actuall necessary bc of linear progression) and ability to choose RNG or reactionary
            print("You've collected the knight's soul. It increases your accuracy window during Reactionary Attacks, and ")
            input(" it grants you the ability to choose whether to use them or to rely on RNG attacks.")
            return "pawn_legion"
        elif room == "pawn_legion":
            upgrades.append("legion souls")
            input(f"You've obtained the souls of enough pawns that your maximum health has increased from {max_health} to {HEALTH_UPGRADE_HEALTH}! You'll need it if you want to survive the stronger opponants ahead.")
            max_health = HEALTH_UPGRADE_HEALTH
            return "shop_intersection"
        elif room == "bishop":
            upgrades.append("bishop soul")
            input("You've collected the bishop's soul. It sharpens your weapons, increasing your damage output.")
            return "rook"
        elif room == "rook":
            upgrades.append("rook soul")
            input("You've collected the rook's soul. It strengthens your armor, providing you with higher defense from incoming attacks.")
            return "queen"
        elif room == "queen":
            upgrades.append("queen soul")
            input("You've collected the Queen's soul. It drastically improves your attack, defense, and speed.")
            input("With this, you should be ready to take on the King.")
            return "king"
        elif room == "king":
            while choice != "talk" and choice != "fight" and choice != "spare" and choice != "kill":
                choice = input("[TALK] or [FIGHT]. [SPARE] or [KILL]. ").lower()
            if choice == "talk" or choice == "spare":
                return "king_spared"
            else:
                upgrades.append("king soul")
                input("You've collected the King's soul.")
                return "king_dead"
        else:
            return "tutorial"
    else:
        input("Y O U   D I E D .")
        choice = input("[RETRY] or [QUIT]? Keep in mind, only health is reset if you [RETRY]. If you want a better run, [QUIT] and start over. ").lower()
        while choice != "retry":
            if choice == "quit":
                input("That's understandable. Good try.")
                quit_game()
            choice = input("[RETRY] or [QUIT]? ").lower()
        health = max_health
        return room


def player_turn(room: str, enemy: EnemyStats, turn: int, alive: list[bool]) -> None:
    """During a fight, determine player's action each turn."""
    global player
    global upgrades
    choice: str = ""
    i: int = 0
    fight_flavor_text(room, turn, alive)
    input(f"--{player}'s turn.--")
    print_stats()
    print("What will you do?")
    while choice != "fight" and choice != "act" and choice != "item":
        choice = input("[FIGHT], [ACT], [ITEM], [QUIT]? ").lower()
        if choice == "quit":
            quit_game()
    which: int = 1
    if choice == "fight":
        which = choose_enemy(alive)
        weapon: str = ""
        print("What weapon would you like to use?")
        while weapon != "sword" and weapon != "dagger" and weapon != "bow" and weapon != "knife" and weapon != "cancel":
            weapon = input("[SWORD], [DAGGER], [BOW], or [CANCEL]? ").lower()
            if weapon == "quit":
                quit_game()
            elif weapon == "cancel" or weapon == "back":
                return player_turn(room, enemy, turn, alive)
        if weapon == "knife":
            weapon = "dagger"
        use_reactionary_attack: bool = False
        if "pawn soul" in upgrades and "knight soul" in upgrades:
            choice = input("Would you like to use a [SPEED]-based attack or [RNG]-based attack? ").lower()
            while choice != "speed" and choice != "rng":
                if choice == "quit":
                    quit_game()
                choice = input("[SPEED]-based attack, where damage relies on your reflexes, or [RNG]-based attack, where appropriately-balanced random number generators decide damage? ").lower()
            if choice == "speed":
                use_reactionary_attack = True
        elif "pawn soul" in upgrades and "knight soul" not in upgrades:
            use_reactionary_attack = True
        if use_reactionary_attack:
            speed_attack(weapon, enemy, which, room, turn, alive)
        else:
            rng_attack(weapon, enemy, which, room, turn, alive)
    elif choice == "act":
        which = choose_enemy(alive)
        print("What would you like to do?")
        global enemy_distracted
        if room != "king":
            while choice != "check" and choice != "pay" and choice != "apologize" and choice != "compliment" and choice != "mystify" and choice != "trick" and choice != "insult" and choice != "flirt" and choice != "dance" and choice != "cancel":
                print("[CHECK], ", end="", flush=True)
                if room == "queen":
                    print("[PAY] to distract, ", end="", flush=True)
                elif room == "rook":
                    print("[APOLOGIZE]", end="", flush=True)
                choice = input("[COMPLIMENT], [MYSTIFY], [TRICK], [INSULT], [FLIRT], [DANCE], or [CANCEL]? ").lower()
                if choice == "quit":
                    quit_game()
                elif choice == "cancel" or choice == "back":
                    return player_turn(room, enemy, turn, alive)
                    choice = "cancel"
                if room != "queen" and choice == "pay":
                    choice = ""
                    input("This enemy isn't greedy enough to be distracted by money, nor disloyal enough to take a bribe.")
                elif room == "queen" and choice == "pay":
                    global gold
                    payment = randint(5, 20)
                    if gold < payment:
                        payment = gold
                    if gold > 0:
                        gold -= payment
                        input("You toss {payment}G on the ground! The Queen's greed blinds them! They will be distracted (easier to hit and does less damage) next turn. {gold}G left!")
                        enemy_distracted = True
                    else:
                        input("You don't have enough gold! You've run out!")
                        choice = ""
                        enemy_distracted = False
                elif room == "queen" and choice != "pay":
                    enemy_distracted = False
                if room != "rook" and choice == "apologize":
                    choice = ""
                    input("The enemy doesn't listen and doesn't care when you try to apologize.")
                    enemy_distracted = False
                elif room == "rook" and choice == "apologize":
                    input("The rook hesitates for a moment, touched by your words. They consider the possibility you could change and stop killing people on a rampage of revenge.")
                    input("They will be distracted (easier to hit and does less damage) until next turn.")
                    enemy_distracted = True
                elif room == "rook" and choice != "apologize":
                    if enemy_distracted:
                        input("The rook resolves themself. They are no longer distracted!")
                    enemy_distracted = False
            if choice == "check":
                act_check_info(room, enemy, which)
            elif choice == "compliment":
                enemy_distracted = act_compliment(room, enemy, which)
            elif choice == "mystify":
                enemy_distracted = act_mystify(room, enemy)
            elif choice == "trick":
                act_trick(room, enemy, which)
            elif choice == "insult":
                act_insult(room, enemy, which)
            elif choice == "flirt":
                act_flirt(room, enemy, which)
            elif choice == "dance":
                act_dance(room, enemy, which)
            else:
                input("(I don't even know what you're trying to do...)")
                input("(So I guess you don't do anything.)")
        else:
            while choice != "check" and choice != "talk":
                choice = input("[CHECK], [TALK], or [CANCEL]. ").lower()
                if choice == "cancel" or choice == "back":
                    return player_turn(room, enemy, turn, alive)
            if choice == "check":
                act_check_info(room, enemy, which)
            elif choice == "talk":
                talk_king: list[str] = list()
                talk_king.append("You try to apologize to the King. They thank you sincerely, but do not stop fighting.")
                talk_king.append("You tell the King what you've done. They nod sadly.")
                talk_king.append("You try to think of something to say, but couldn't think of any conversation topics. After all, you're in a battle.")
                talk_king.append("You compliment the King, but they act like they don't hear you.")
                talk_king.append("You ask the King why they murdered so many of your people. Their expression of grief deepens, but they keep attacking.")
                i = randint(0, len(talk_king) - 1)
                input(talk_king[i])
    elif choice == "item":
        global temp_item_buffs_ADS
        while choice != "shield" and choice != "hp pot" and choice != "quiver" and choice != "poisoned arrows" and choice != "atk scroll" and choice != "def ointment" and choice != "cancel":
            choice = input("What item would you like to use? [SHIELD], [HP POT], [QUIVER], [POISONED ARROWS], [ATK SCROLL], [DEF OINTMENT], or [CANCEL]? ").lower()
            if choice == "cancel" or choice == "back":
                return player_turn(room, enemy, turn, alive)
        global arrows_ready
        global using_poisoned_arrows
        if choice == "shield":
            if "iron shield" in upgrades:
                temp_item_buffs_ADS[2] = 3
            else:
                temp_item_buffs_ADS[2] = 2
            input("You ready your shield.")
            input(f"Damage will be reduced for the next {temp_item_buffs_ADS[2]} turns.")
        elif choice == "hp pot":
            global max_health
            global health
            global hp_potions
            if hp_potions <= 0:
                return player_turn(room, enemy, turn, alive)
            input("You drink a health potion.")
            i = randint(12, 40)
            healing: int = int((i * 0.01) * max_health)
            input(f"{healing} health regained!")
            if i > 35:
                input("Critical healing!")
            if i > 30:
                input("It's ambrosial.")
            elif i <= 20:
                input("The enemy startled you, and you dropped the potion mid-chug!")
            elif i > 20 and i <= 25:
                input("A bit bitter...")
            elif i > 25 and i <= 30:
                input("The potion tastes... decent. But it's the effect that matters!")
                input("The effect is also just okay.")
            health += healing
            if health >= max_health:
                health = max_health
                i = randint(0, 2)
                print("HP fully restored.")
                if i == 0:
                    input("Good as new!")
                elif i == 1:
                    input("You're all healed up!")
                else:
                    input("You feel refreshed!")
            hp_potions -= 1
        elif choice == "quiver":
            global arrows_quiver
            if arrows_quiver == 0:
                input("You don't have any arrows left to draw!")
                return player_turn(room, enemy, turn, alive)
            arrows_transferred: int = 4 - arrows_ready
            if arrows_quiver < 4:
                arrows_transferred = arrows_quiver
            arrows_quiver -= arrows_transferred
            arrows_ready += arrows_transferred
            input(f"You draw {arrows_transferred} arrows out of your quiver.")
            using_poisoned_arrows = False
        elif choice == "poisoned arrows":
            global poisoned_arrow_bunch
            if poisoned_arrow_bunch <= 0:
                input("You don't have any poisoned arrows!")
                return player_turn(room, enemy, turn, alive)
            arrows_ready = 4
            using_poisoned_arrows = True
            poisoned_arrow_bunch -= 1
        elif choice == "atk scroll":
            global attack_up_scroll
            if attack_up_scroll <= 0:
                input("You don't have any attack-up scrolls!")
                return player_turn(room, enemy, turn, alive)
            attack_up_scroll -= 1
            temp_item_buffs_ADS[0] = 3
        elif choice == "def ointment":
            global defense_up_ointment
            if defense_up_ointment <= 0:
                input("You don't have any defense-up ointments!")
                return player_turn(room, enemy, turn, alive)
            attack_up_scroll -= 1
            temp_item_buffs_ADS[1] = 3


def act_check_info(room: str, enemy: EnemyStats, which: int = 1) -> None:
    """During battle, access information about the enemies and display it."""
    global player
    global points
    global enemy_current_health
    input("You examine the enemy.")
    print(f"{enemy[0]}", end="", flush=True)
    if room == "pawn_legion":
        print(f" {which}. ", end="", flush=True)
    else:
        print(". ", end="", flush=True)
    input(f"HP: {enemy_current_health[which - 1]}/{enemy[1]}. Attack: {enemy[2]}. Defense: {enemy[3]}. Speed: {enemy[4]}.")
    if room == "tutorial":
        input("An eccentric yet experienced wild card. Has a great sense of humor, but also only speaks in rhymes.")
        input("They seem to just be a nice person, willing to train whoever asks nicely. How nice of them to help you practice! They seem like a fairly normal person.")
        input("They have a... broadsword. (Wow, that's... a bit more extreme than I expected.)")
        input("...And a dagger. (Wow, they're almost as armed as you!)")
        input("It also appears...")
        input("They have some magic?!")
        input("Okay, so maybe not such a normal person. Still nice, though.")
        input("Oh, and they're attacking you now.")
    elif room == "pawn":
        input("A standard troop of the White Side. They usually rely on strength in numbers, but this one is confident in themself.")
        input("They're looking forward to hopefully getting a promotion soon.")
        input("They seem unsure of how to actually fight effectively, though...")
        input(f"All of this might be true, but only one thing matters to {player} right now...")
        input("They're an enemy. And they're in your way.")
    elif room == "knight":
        input("A mobile flanker of the White Side that excels in limiting their opponent's options in a variety of directions from horseback.")
        input("Also somewhat arrogant, looking down on less nimble classes, especially pawns.")
        input("They're darting around you, landing sneaky blows; it's hard to return them. They seem to be changing up their attack style every hit.")
    elif room == "pawn_legion":
        if which == 1:
            input("This pawn seems quite serious. Their face is set with a determined glint in their eye and a furrowed brow.")
        if which == 2:
            input("Seems bored. They hold their weapon loosely and their eyes wander. Even if their thrusts are half-hearted, though, they're still stabbing at you.")
        if which == 3:
            input("Vibrating on the spot. They look eager to fight you and gleefully violent. A wide grin is plastered on their face.")
        if which == 4:
            input("Quietly observing you, but their eyes are filled with hatred. They're out for revenge, but they're being methodical about it, collecting information between attacks.")
        if which == 5:
            input("Looks a bit conflicted, an expression of resignation on their face. They kind of want to reason with you, to talk it out, but knows they can't. They know they must fight.")
        if which == 6:
            input("This one is being incredibly loud. They look somehow both surprised and furious, attacking with wild, reckless abandon.")
        if which == 7:
            input("An absolute idiot. Just a complete and utter imbecile. Looks like they enjoy fighting. Tries to act like how they think a stereotypical soldier might act.")
        if which == 8:
            input("Quiet. Reserved. Who knows what they're thinking?")
            input("(Me. I do. I'm the narrator, and what I say is law, but YOU don't get to know. The secrets of the universe that I made up just now will remain a mystery to you!)")
    elif room == "bishop":
        input("A haughty elite member of the White Side. This religious leader looks down on pieces of lower classes as well as on all who oppose the White Side.")
        input("Capable of devastating, pinpoint attacks, but extremely fragile due to a weak constitution and not having had to do much of anything all their life.")
    elif room == "rook":
        input("A steadfast guard for the White Side. Actually quite compassionate. Not the most perceptive sometimes, but dead set on protecting those they care about.")
        input("Their sturdy stance and style plus their tough armor give them a hefty advantage in terms of defending, but they suffer for it in speed.")
        input("Loyal to their side and acts heroic if needed. Their strong sense of justice could be used to your advantage.")
    elif room == "queen":
        input("A monarch of the White Side. Incredibly intimidating, standing tall and proud. Confident in their ability to crush you.")
        input("A multifaceted powerhouse, they excel in all areas, proving to be a vicious foe.")
        input("Also quite greedy. You can use that to your advantage if she's proving too tough.")
    elif room == "king":
        input("The leader of the White Side.")
        input("Majestic, calm, and tired. They can take a lot of damage, but usually doesn't have to. They can deal some damage, but usually doesn't want to.")
        input("They don't want to have to fight you. They never wanted war.")
        i: int = randint(0, 2)
        if i == 0:
            global user_name
            input(f"But something has brought you two together. Call it fate. Call it {user_name}. And now, the fight continues.")
        input("Perhaps there is a way to end this... differently. Perhaps... once you have sufficiently weakened him.")
        input("It won't take long. After claiming the Queen's soul, your power has increased significantly.")


def act_compliment(room: str, enemy: EnemyStats, which: int = 1) -> bool:
    """During battle, an option for the player to use to interact with the enemy by complimenting them."""
    print("You praise and flatter ", end="", flush=True)
    if room == "pawn_legion":
        input(f"{enemy[0]} {which}.")
    else:
        input(f"the {enemy[0]}.")
    if room == "queen":
        input("The Queen sneers and reassures you that they're aware of their own perfection. Looks like compliments don't work on them.")
        return False
    i: int = randint(0, 3)
    if i == 0 and room != "bishop" and room != "rook":
        input("Sadly, it has no effect this time; the enemy seems unfazed.")
        return False
    elif i > 0 and i < 3:
        input("The compliment somehow lands. They thank you, a bit puzzled.")
        input("Confused and hesitant, they accidentally give you the opportunity to land an extra blow!")
        attack_of_opportunity("player", enemy[2], enemy[3], which)
        return False
    elif i == 3:
        input("The enemy is pleasantly stunned! They're temporarily distracted.")
        return True
    elif room == "bishop":
        input("The bishop's ego is somehow inflated even more.")
        return True
    elif room == "rook":
        input("The rook smiles awkwardly and thanks you while continuing to fight. No hesitation this time.")
        return False
    else:
        input("Oh... wow... Yeah, no, that didn't work.")
        return False


def act_flirt(room: str, enemy: EnemyStats, which: int = 1) -> bool:
    """During battle, an option for the player to use to interact with the enemy by flirting with them."""
    if room == "rook":
        input("The rook confusedly turns you down. Seems like they aren't really susceptible to flirting.")
    i: int = randint(0, 2)
    if i == 0:
        input("You botch the delivery of the worst, most overused pick-up line I've ever heard.")
        input("You awkward clown, you can't smoothtalk!")
        input("Distracted, you let the enemy land an extra hit, you flustered mess!")
        attack_of_opportunity("enemy", enemy[2], enemy[3], which)
        return False
    elif i == 1:
        input(f"The {enemy[0].lower()} blinks. They thank you. They seem thrown a bit off-balance. You have time to sneak an extra hit in.")
        attack_of_opportunity("enemy", enemy[2], enemy[3], which)
        return False
    else:
        input(f"...Oh no... You overdid it. The {enemy[0].lower()} is smitten and momentarily distracted. You're sick, you know that?")
        return True


def act_mystify(room: str, enemy: EnemyStats) -> bool:
    """During battle, an option for the player to use to interact with the enemy by mystifying them."""
    i: int = randint(0, 2)
    if i == 0:
        input("You do something...   m y s t e r i o u s !")
        input("(So mysterious, even you don't know what it is!)")
    elif i == 1:
        input("You do a magic trick in hopes of dazzling the enemy.")
    elif i == 2:
        input("You engage the enemy in a philosophical discussion about the mysteries of life and death.")
    if room == "bishop":
        input("The bishop gasps.")
        input("BISHOP: \"HERESY!!!\"")
        input("They seem too rage-filled to concentrate fully on attacking you for the moment.")
        return True
    else:
        i = randint(0, 3)
        if i == 0:
            input(f"The {enemy[0].lower()} remains unimpressed.")
            return False
        elif i == 1:
            input(f"The {enemy[0].lower()} is impressed!")
            input("But not enough to stop.")
            return False
        elif i == 2:
            input(f"The {enemy[0].lower()} is filled with wonder!")
            input(" /existential terror!")
            input("They are temporarily distracted.")
            return True
        else:
            input(f"Your stunt has caused this {enemy[0].lower()} to achieve temporary transcendance!")
            input("...Good job.")
            input("How in the world did you manage that?")
            input("It's safe to say they're a bit distracted.")
            return True
    

def act_insult(room: str, enemy: EnemyStats, which: int = 1) -> bool:
    """During battle, an option for the player to use to interact with the enemy by complimenting them."""
    if room != "legion":
        input(f"You insult the {enemy[0].lower()}.")
    else:
        input(f"You insult {enemy[0].lower()} {which}.")
    i: int = randint(0, 2)
    if i == 0:
        input("They look at you weirdly, laugh, and fire a witty comeback at you.")
        input("Ouch.")
        input(f"You are distracted by getting absolutely destroyed, and the {enemy[0].lower()} gets in a cheap shot.")
        attack_of_opportunity("enemy", enemy[2], enemy[3], which)
        return False
    if i == 1:
        input("They seem hurt and taken aback.")
        input("They're off their game, and you take the opportunity to strike out quickly. Even after that, they'll probably be a bit distracted for a minute.")
        attack_of_opportunity("player", enemy[2], enemy[3], which)
        return True
    else:
        input("Looks like you hit a nerve!")
        input(f"The {enemy[0].lower()} lashes out recklessly, infuriated.")
        i = randint(0, 1)
        if i == 0:
            input("They strike at you viciously, fuelled by rage!")
            attack_of_opportunity("enemy", enemy[2], enemy[3], which)
        else:
            input("They lunge at you, but they miss and hurt themself in the process!")
            i = randint(1, 4)
            input(f"{i} damage!")
            global enemy_current_health
            enemy_current_health[which - 1] -= i
        input("They will still be a bit distracted as they calm down.")
        return True


def act_trick(room: str, enemy: EnemyStats, which: int = 1) -> bool:
    """During battle, an option for the player to use to interact with the enemy by lying to them."""
    i: int = 0
    if enemy[4] > 50:
        i = randint(0, 4)
    else:
        i = randint(0, 2)
        if room == "rook" and i == 1:
            i = 0
    if i == 0:
        input(f"You tell a clever lie to the {enemy[0].lower()}. For a split second, they seem to believe you.")
        input("It's long enough for you to get a cheap shot in.")
        attack_of_opportunity("player", enemy[2], enemy[3], which)
        return False
    else:
        input(f"You tell the {enemy[0].lower()} an elaborate lie, and they almost believe you!")
        input("However, they realize that you're trying to deceive them before you get the chance to strike.")
        return False


def act_dance(room: str, enemy: EnemyStats, which: int = 1) -> bool:
    """During battle, an option for the player to use to interact with the enemy by dancing."""
    i: int = randint(0, 2)
    if i == 0:
        input("You strike a dramatic pose!")
    elif i == 1:
        input("You start dancing energetically.")
    else:
        input("You begin breakdancing.")
    i = randint(0, 2)
    if i == 0:
        input(f"The {enemy[0].lower()} is not amused. Preoccupied, you can't react fast enough as they attempt a quick attack of opportunity.")
        attack_of_opportunity("enemy", enemy[2], enemy[3], which)
        return False
    elif i == 1:
        if room != "legion":
            input(f"The {enemy[0].lower()} is just... confused as to why you're dancing during a battle.")
        else:
            input(f"{enemy[0]} {str(which)} is just... confused as to why you're dancing during a battle.")
        return False
    else:
        input(f"The {enemy[0].lower()} joins you! They'll be a bit distracted by dancing temporarily.")
        return True
    

def choose_enemy(alive: list[bool]) -> int:
    """During a battle with multiple enemies, this allows the player to choose which enemy to target."""
    i: int = 1
    which: str = "1"
    enemy_valid: bool = True
    if len(alive) > 1:
        print("Which one? ", end="", flush=True)
        i = 1
        while i <= len(alive):
            if alive[i]:
                print(f"[{i}]", end="", flush=True)
            if i < len(alive):
                print(", ", end="", flush=True)
        which = input("? ")
        enemy_valid = False
        while not enemy_valid:
            try:
                int(which)
                i = 1
                while i <= len(alive):
                    if alive[i]:
                        enemy_valid = True
            except ValueError:
                which = input("That's not even a number. Which? ").lower()
            if not enemy_valid:
                which = input("Which? ").lower()
    return int(which)


def speed_attack(weapon: str, enemy: EnemyStats, which: int, room: str, turn: int, alive: list[bool]) -> None:
    """Allows the player to perform an attack on the enemy that relies on quick reflexes."""
    lowest_dmg: int = 0
    highest_dmg: int = 10
    delay: list[float] = [3, 0.5, 1]  # Before, crit window, miss threshold
    if weapon == "sword":
        input("Get ready to swing your sword!")
        lowest_dmg = 4
        highest_dmg = 9
        delay[0] = uniform(3, 4)
        delay[2] += (1 - enemy[4] * 0.01) + 2.2
    elif weapon == "dagger":
        input("You ready your dagger!")
        lowest_dmg = 1
        highest_dmg = 12
        delay[0] = uniform(1, 2)
        delay[2] += (1 - enemy[4] * 0.01) + 1.2
    elif weapon == "bow":
        global arrows_ready
        global arrows_quiver
        global using_poisoned_arrows
        global poison_left
        delay[0] = uniform(2, 3)
        delay[2] += (1 - enemy[4] * 0.01) + 4
        if arrows_ready == 0 and arrows_quiver == 0:
            input("You don't have any arrows left!")
            return player_turn(room, enemy, turn, alive)
        elif arrows_ready == 0:
            input("You need to draw more arrows!")
            return player_turn(room, enemy, turn, alive)
        else:
            input("You nock an arrow and draw your bow!")
            if using_poisoned_arrows:
                poison_left[which - 1] = 3
        arrows_ready -= 1
        lowest_dmg = -2
        highest_dmg = 15
    input(f"To land a critical hit, you must react below {int(delay[1] * 100) / 100}s, and a miss is guaranteed after {int(delay[2] * 100) / 100}s.")
    delay[1] = (1 - enemy[4] * 0.01) + 0.2
    damage: int = 0
    key_to_be_pressed: str = chr(randint(97, 122))
    input("Type the letter as prompted and hit enter as soon as you see the letter in brackets!")
    print("Get ready...")
    time.sleep(delay[0])
    # while msvcrt.kbhit():
    #     if msvcrt.getch():
    #         print("Don't hit anything early!")
    #         time.sleep(delay[0])
    time_start: float = time.time()
    choice: str = ""
    while choice != key_to_be_pressed:
        choice = input(f"[{key_to_be_pressed}]! ").lower()
    time_end: float = time.time()
    time_delta: float = time_end - time_start
    input(f"Reaction time: {int(time_delta * 1000) / 1000}s!")
    if time_delta < 0:
        input("Cheating isn't nice.")
        time_delta = 60
    if time_delta <= delay[1]:
        damage = highest_dmg
        input("Critical hit!")
    elif time_delta > delay[1] and time_delta <= delay[2]:
        time_standardized: float = (delay[2] - time_delta) / delay[2]
        damage_highest_zeroed: int = highest_dmg - lowest_dmg
        damage = int(damage_highest_zeroed * time_standardized + lowest_dmg + 1)
    else:
        damage = 0
    global enemy_distracted
    if enemy_distracted:
        damage += 2
    if weapon == "bow" and enemy[4] >= 50:
        damage -= 1
    global temp_item_buffs_ADS
    global upgrades
    if temp_item_buffs_ADS[0] > 0:
        damage += randint(3, 8)
        temp_item_buffs_ADS[0] -= 1
    if "bishop soul" in upgrades:
        damage += 2
    if "queen soul" in upgrades:
        damage += 104
    if weapon == "bow" and damage < 5:
        damage = 0
    if enemy[3] >= 50:
        damage -= 3
    elif enemy[3] >= 25:
        damage -= 2
    elif enemy[3] >= 10:
        damage -= 1
    if damage < 0:
        damage = 0
    input(f"{damage} damage!")
    if damage == 0:
        input("Miss!")
    global enemy_current_health
    enemy_current_health[which - 1] -= damage
    if enemy_current_health[which - 1] <= 0:
        enemy_current_health[which - 1] = 0
        global who_alive
        who_alive[which - 1] = False


def rng_attack(weapon: str, enemy: EnemyStats, which: int, room: str, turn: int, alive: list[bool]) -> None:
    """Allows the player to perform an attack on the enemy that relies on random number generators."""
    lowest_dmg: int = 0
    highest_dmg: int = 10
    if weapon == "sword":
        input("You swing your sword!")
        lowest_dmg = 4
        highest_dmg = 9
    elif weapon == "dagger":
        input("You slash your dagger!")
        lowest_dmg = 1
        highest_dmg = 12
    elif weapon == "bow":
        global arrows_ready
        global arrows_quiver
        global using_poisoned_arrows
        global poison_left
        if arrows_ready == 0 and arrows_quiver == 0:
            input("You don't have any arrows left!")
            return player_turn(room, enemy, turn, alive)
        elif arrows_ready == 0:
            input("You need to draw more arrows!")
            return player_turn(room, enemy, turn, alive)
        else:
            input("You fire an arrow!")
            if using_poisoned_arrows:
                poison_left[which - 1] = 3
        arrows_ready -= 1
        lowest_dmg = -2
        highest_dmg = 15
    damage: int = randint(lowest_dmg, highest_dmg)
    global enemy_distracted
    if enemy_distracted:
        damage += 2
    if weapon == "bow" and enemy[4] >= 50:
        damage -= 1
    global temp_item_buffs_ADS
    global upgrades
    if temp_item_buffs_ADS[0] > 0:
        damage += randint(3, 8)
        temp_item_buffs_ADS[0] -= 1
    if "bishop soul" in upgrades:
        damage += 2
    if "queen soul" in upgrades:
        damage += 104
    if weapon == "bow" and damage < 5:
        damage = 0
    if enemy[3] >= 50:
        damage -= 3
    elif enemy[3] >= 25:
        damage -= 2
    elif enemy[3] >= 10:
        damage -= 1
    if damage < 0:
        damage = 0
    input(f"{damage} damage!")
    if damage == 0:
        input("Miss!")
    elif damage >= highest_dmg - 1:
        input("Critical hit!")
    global enemy_current_health
    enemy_current_health[which - 1] -= damage
    if enemy_current_health[which - 1] <= 0:
        enemy_current_health[which - 1] = 0
        global who_alive
        who_alive[which - 1] = False


def attack_of_opportunity(who_attacking: str, enemy_attack: int, enemy_defense: int, which: int) -> None:
    """Allows the player or enemy to perform a quick attack while the other is occupied for a second."""
    damage: int = randint(0, 4)
    MISS_CHANCE = 25
    if who_attacking == "enemy":
        if enemy_attack >= 60:
            damage += 3
        elif enemy_attack >= 40:
            damage += 2
        elif enemy_attack >= 20:
            damage += 1
        if randint(0, MISS_CHANCE) == 0:
            damage = 0
        take_damage(damage)
    elif who_attacking == "player":
        if enemy_defense < 10:
            damage += 3
        elif enemy_defense < 25:
            damage += 2
        elif enemy_defense < 50:
            damage += 1
        global temp_item_buffs_ADS
        global upgrades
        if temp_item_buffs_ADS[0] > 0:
            damage += randint(1, 3)
        if "bishop soul" in upgrades:
            damage += 1
        if "queen soul" in upgrades:
            damage += 2
        if randint(0, MISS_CHANCE) == 0:
            damage = 0
        global enemy_current_health
        input(f"{damage} damage!")
        if damage == 0:
            input("Miss!")
        enemy_current_health[which - 1] -= damage
        if enemy_current_health[which - 1] <= 0:
            enemy_current_health[which - 1] = 0
            global who_alive
            who_alive[which - 1] = False


def enemy_turn(room: str, enemy: EnemyStats, alive: list[bool]) -> None:
    """During a fight, determine enemy's action each turn."""
    actions: list[str] = ["sword", "dagger", "bow", "magic", "healing"]
    lowest_dmg: int = 0
    highest_dmg: int = 10
    global temp_item_buffs_ADS
    if temp_item_buffs_ADS[2] > 0:
        temp_item_buffs_ADS[2] -= 1
    i: int = 1
    legion_who_acts: list[int] = list()
    if room == "legion":
        i = 1
        pawns_able: int = 0
        while i <= len(alive):
            if alive[i]:
                pawns_able += 1
            i += 1
        i = 0
        while i < 3 and pawns_able > 0:
            j: int = randint(1, 8)
            if alive[j]:
                legion_who_acts.append(j)
                pawns_able -= 1
                i += 1
        input("--Pawn legion's turn.--")
    else:
        legion_who_acts.append(1)
        input(f"--{enemy[0]}'s turn.--")
    for current_which in legion_who_acts:
        action: str = actions[randint(0, 4)]
        i = randint(0, 2)
        print(f"{enemy[0]} ", end="", flush=True)
        if room == "legion":
            print(f"{current_which} ", end="", flush=True)
        if action == "sword":
            lowest_dmg = 1
            highest_dmg = 4
            if i == 0:
                input("swings their sword!")
            elif i == 1:
                input("thrusts their sword!")
            elif i == 2:
                input("slashes at you with their sword!")
        elif action == "dagger":
            lowest_dmg = -1
            highest_dmg = 6
            if i == 0:
                input("stabs at you with their dagger!")
            elif i == 1:
                input("cuts at you with their dagger!")
            elif i == 2:
                input("throws a knife at you!")
        elif action == "bow":
            lowest_dmg = -3
            highest_dmg = 8
            if i == 0:
                input("fires a barrage of arrows at you!")
            elif i == 1:
                input("lines up a shot at you with their bow and fires!")
            elif i == 2:
                input("launches a volley of arrows in your direction!")
        elif action == "magic":
            lowest_dmg = -5
            highest_dmg = 10
            if room == "pawn" or room == "legion":
                action = "water jet"
            elif room == "knight":
                action = "air cutter"
            elif room == "bishop":
                action = "holy light"
            elif room == "rook":
                action = "rock swarm"
            else:
                action = "fireball"
            input(f"casts {action}!")
        elif action == "healing":
            if i == 0:
                input("casts a healing spell on themself!")
                lowest_dmg = -3
                highest_dmg = 15
            elif i == 1:
                input("applies a bandage to themself!")
                lowest_dmg = 0
                highest_dmg = 10
            elif i == 2:
                input("drinks a health potion!")
                lowest_dmg = int(enemy[1] * .12)
                highest_dmg = int(enemy[1] * .4)
            if enemy_current_health[current_which - 1] <= .5 * enemy[1] and enemy_current_health[current_which - 1] > .1:
                lowest_dmg += 3
                highest_dmg += 2
            elif enemy_current_health[current_which - 1] <= .1:
                lowest_dmg -= 1
                highest_dmg += 6
            healing: int = randint(lowest_dmg, highest_dmg)
            if healing <= 0:
                healing = 0
                if i == 0:
                    input(f"{enemy[0]}'s casting fails!")
                elif i == 1:
                    input("The bandage doesn't stick and immediately falls off!")
                elif i == 2:
                    input("Somehow, the health potion doesn't work... it must be defective.")
            elif healing > 0 and healing <= 2:
                if i == 0:
                    input("The spell was incomplete!")
                elif i == 1:
                    input("The bandage is barely hanging on... It doesn't look that effective.")
                elif i == 2:
                    input(f"{enemy[0]}'s face scrunches up reflexively. Seems like the potion was expired.")
            input(f"{healing} health regained!")
            if healing >= highest_dmg - 1:
                input("Critical healing!")
            enemy_current_health[current_which - 1] += healing
        if action != "healing":
            global enemy_distracted
            if enemy[2] >= 60:
                lowest_dmg += 3
                highest_dmg += 3
            elif enemy[2] >= 40:
                lowest_dmg += 2
                highest_dmg += 2
            elif enemy[2] >= 20:
                lowest_dmg += 1
                highest_dmg += 1
            damage: int = randint(lowest_dmg, highest_dmg)
            if enemy_distracted:
                damage -= 2
            if (action == "sword" or action == "dagger") and damage < 0:
                damage = 0
            elif action == "bow" and damage < 3:
                damage = 0
            if damage >= 0:
                take_damage(damage, action)
            else:
                input("The spell backfires!")
                print(f"{enemy[0]} ", end="", flush=True)
                if room == "legion":
                    print(f"{current_which} ", end="", flush=True)
                input("damages themself!")
                input(f"{damage} damage!")
                enemy_current_health[current_which - 1] += damage
    i = 0
    for each_enemy in alive:
        if each_enemy and poison_left[i] > 0:
            poison_left[i] -= 1
            if room == "legion":
                input(f"{enemy[0]} {i + 1} is afflicted by poison!")
                poison_damage: int = randint(2, 4)
                input(f"{poison_damage} damage!")
                enemy_current_health[i] -= poison_damage
        i += 1


def take_damage(damage: int, weapon: str = "Default") -> None:
    """When called, calculate damage done to player."""
    global temp_item_buffs_ADS
    global upgrades
    global health
    if "rook soul" in upgrades:
        damage = int(damage * .9)
    elif "queen soul" in upgrades:
        damage = int(damage * .5)
    if temp_item_buffs_ADS[1] > 0:
        percent_decrease: float = float(randint(30, 80) * .01)
        damage = int(damage * (1 - percent_decrease))
        temp_item_buffs_ADS[1] -= 1
    if temp_item_buffs_ADS[2] > 0:
        input("You raise your shield;")
        i: int = 0
        if "iron shield" in upgrades:
            i = randint(0, 5)
        else:
            i = randint(0, 3)
        if weapon == "dagger":
            input("The blade of the dagger glances off of the shield!")
        elif weapon == "sword":
            input("The sword is deflected, digging into the floor instead!")
        elif weapon == "fireball":
            input("The shield pushes the oncoming flames around it, and they spill off around you!")
        elif weapon == "water jet":
            input("The shield disperses the oncoming stream of water around it, and they splash off around you!")
        elif weapon == "rock swarm":
            input("You duck and use the shield to redirect the oncoming boulders, pushing the larger rocks away, and the smaller ones bounce off!")
        elif weapon == "air cutter":
            input("Taking on the air cutter at an angle, you deflect it away! The wind swirls around you.")
        elif weapon == "holy light":
            input("You lift your shield and shut your eyes as the bishop creates a brilliant, blinding flash!")
        elif weapon == "bow":
            if i == 5:
                input("You skillfully deflect the arrow with the shield, and it spins away and lodges in the floor!")
            else:
                input("The arrow thuds into the shield!")
        if i == 5:
            input("Perfect parry!")
        input("Damage reduced!")
        if i == 0:
            damage = int(damage * .7)
        elif i == 5:
            damage = 0
        else:
            damage = int(damage * .5)
    input(f"{damage} damage!")
    health -= damage
    if health < 0:
        health = 0
    if damage == 0:
        input("Miss!")


def fight_flavor_text(room: str, turn: int, alive: list[bool]) -> None:
    """During a fight, displays every round to add personality to the experience."""
    flavor_texts: list[str] = list()
    overflow_texts: list[str] = list()
    i: int = 0
    if room == "tutorial":
        flavor_texts.append("JESTER: \"During a tussle, you'll have to choose to use your words, items, or muscles!\"")
        flavor_texts.append("JESTER: \"If you occupy your opponent with an action, their attacks will be weakened and yours more effective, as they're too busy with your distraction!\"")
        flavor_texts.append("JESTER: \"Be forewarned, each option is unique; learn to use them well and no doubt you'll end up with a win streak!\"")
        overflow_texts.append("The Jester makes a beckoning hand gesture.")
        overflow_texts.append("The Jester is bouncing with excitement.")
        overflow_texts.append("It's hard to tell if they're holding back or not.")
        overflow_texts.append("The Jester has a detailed guide on how to win battles. Unfortunately, they left it at home.")
        overflow_texts.append("The Jester pulls out a deck of cards, then starts juggling all of them, somehow.")
    elif room == "pawn":
        flavor_texts.append("This pawn looks determined to put a premature end to your plucky push. Luckily, you're determination outways theirs.")
        flavor_texts.append("The pawn has only heard heroic tales of one-hit-kills from its superiors... They look a bit shaken now.")
        flavor_texts.append("They call for backup... but nobody came.")
        overflow_texts.append("The pawn looks a bit panicked...")
        overflow_texts.append("The pawn tries to threaten you, but they can't think of what to say.")
        overflow_texts.append("The pawn looks worried, deep in thought. They're contemplating running away, but can't figure out how that would work.")
        overflow_texts.append("The pawn doesn't know how to actually fight head-on.")
        overflow_texts.append("The pawn tries to call out to their comrades again, but nobody came.")
        overflow_texts.append("The pawn stutters but managers to announce that they, Gary the Bold and Mighty and Incredibly Smart, will put a stop to you!")
        overflow_texts.append("A drop of sweat rolls down the pawn's face.")
    elif room == "knight":
        flavor_texts.append("The knight charges towards you!")
        overflow_texts.append("The knight gallops towards you!")
        overflow_texts.append("The knight is running circles around you! Or rather, making L-shaped passes at you!")
        overflow_texts.append("The knight's horse rears and neighs.")
        overflow_texts.append("You can faintly hear the knight vocalizing the Batman theme under their breath, which is odd considering they're not a Dark Knight.")
        overflow_texts.append("Smells like a barn.")
        overflow_texts.append("The knight's armor shines brilliantly.")
        overflow_texts.append("The knight looks and acts like a main character... but that's not quite accurate, now is it?")
    elif room == "pawn_legion":
        flavor_texts.append("The legion of pawns blocks your way.")
        flavor_texts.append("The pawns begin to close in.")
        flavor_texts.append("The mob glares at you.")
        i = randint(1, 8)
        while not alive[i]:
            i = randint(1, 8)
        overflow_texts.append(f"Pawn {i} gives you a death stare...")
        overflow_texts.append(f"Pawn {i} vows they will avenge their comrades.")
        overflow_texts.append(f"Pawn {i} looks tired.")
        overflow_texts.append(f"Pawn {i} tries to sneakily flank you.")
        overflow_texts.append(f"Pawn {i} looks about ready to snap.")
        overflow_texts.append(f"Pawn {i} secretly wants to go home.")
        overflow_texts.append(f"Pawn {i} lets out a scream of rage.")
        overflow_texts.append(f"Pawn {i} is crying.")
        overflow_texts.append(f"Pawn {i} asks you why you're doing this.")
        overflow_texts.append(f"Pawn {i} practices a mean look in a mirror, then turns to you with the same expression.")
        overflow_texts.append(f"Pawn {i} secretly thinks you look really cool while you're murdering all of them.")
        overflow_texts.append(f"Pawn {i} tries to reason with you, asking you to calm down, to stop this madness. You don't listen.")
    elif room == "bishop":
        flavor_texts.append("The bishop deigns to block your path.")
        flavor_texts.append("The bishop, surprised they didn't immediately destory you, begins to look a little annoyed.")
        flavor_texts.append("The bishop's face scrunches up in disgust after looking at you.")
        flavor_texts.append("Annoyance turns to a bit of worry.")
        overflow_texts.append("The bishop seems desperate.")
        overflow_texts.append("The bishop is panicking a little.")
        overflow_texts.append("The bishop relies on their superior attack power to end conflicts quickly. This has not ended quickly. They gulp.")
        overflow_texts.append("The bishop is trying to keep their distance fom you, but the room isn't that large.")
        overflow_texts.append("BISHOP: \"Why won't you just die already!?!?\"")
    elif room == "rook":
        flavor_texts.append("The rook blocks the way.")
        flavor_texts.append("The rook feels conflicted about attacking such a small pawn.")
        flavor_texts.append("The rook resolves themself.")
        overflow_texts.append("The rook braces themself.")
        overflow_texts.append("The rook grits their teeth.")
        overflow_texts.append("The rook thinks of those it wants to protect.")
        overflow_texts.append("The rook ignores the pain.")
        overflow_texts.append("Smells like a sad movie scene.")
        overflow_texts.append("The rook appeals to your conscience.")
    elif room == "queen":
        flavor_texts.append("QUEEN: \"Haven't you heard? White always goes first!\"\nThe Queen blocks the way.")
        flavor_texts.append("The Queen is incredibly powerful, but also incredibly greedy... Could you use that to your advantage?")
        overflow_texts.append("The Queen towers before you.")
        overflow_texts.append("Imagine an epic boss theme playing.")
        overflow_texts.append("The Queen is emitting a terrible pressure.")
        overflow_texts.append("The Queen's onslaught is pushing you back, but you can't stop now!")
        overflow_texts.append("You strengthen your resolve, pictures of your fallen friends flashing through your mind!")
        overflow_texts.append("The Queen prepares a gambit.")
    elif room == "king":
        global player
        global user_name
        flavor_texts.append("The King stands before you.")
        flavor_texts.append("The King's crown slips down over their brow, covering an eye.")
        flavor_texts.append(f"KING: \"Do it, then. Kill me. I'm sorry, {player}, truly, I am. Now do it {user_name}. Put an end to this.")
        flavor_texts.append("The King lets their shoulders relax. They're still fighting, but only to keep you from feeling guilty if you kill them.")
        overflow_texts.append("The King locks eyes with you.")
        overflow_texts.append("The King's breathing is labored.")
        overflow_texts.append("The King smiles weakly.")
    if turn <= len(flavor_texts):
        input(flavor_texts[turn - 1])
    else:
        i = randint(0, len(overflow_texts) - 1)
        input(overflow_texts[i])


def print_stats() -> None:
    """Print player stats out for use in the shop and in battle."""
    global hp_potions
    global arrows_quiver
    global poisoned_arrow_bunch
    global attack_up_scroll
    global defense_up_ointment
    global gold
    global points
    global health
    global max_health
    global U_BOX_G
    global U_BOX_Y
    global U_BOX_R
    use_u_box: str = ""
    U_MONEYBAG: str = "\U0001F4B0"
    player_name_whitespace: str = ""
    i: int = 0
    while i < len(player):
        player_name_whitespace += " "
        i += 1
    print(f"   {player}")
    print(f"   Inventory:   |   HP Potions: {hp_potions}   |   Arrows: {arrows_quiver + arrows_ready}   |   Poisoned Arrow Bunches: {poisoned_arrow_bunch}")
    print(f"                |   Attack Up Scrolls: {attack_up_scroll}   |   Defense Up Ointment: {defense_up_ointment}")
    print(f"   {U_MONEYBAG} {gold} Gold     |   Adventure Points: {points}")
    print(f"   HP: {health}/{max_health}")
    if health > max_health / 2:
        use_u_box = U_BOX_G
    elif health > max_health / 5:
        use_u_box = U_BOX_Y
    else:
        use_u_box = U_BOX_R
    i = 0
    while i < health:
        print(use_u_box, end="")
        i += 5
    input()


def shop_menu() -> bool:
    """Get the shop ready for interaction."""
    global hp_potions
    global arrows_quiver
    global poisoned_arrow_bunch
    global attack_up_scroll
    global defense_up_ointment
    global gold
    price_pot: ItemPrice = ("HP Potion", 20, "")
    price_arrow: ItemPrice = ("Arrow", 3, " ")
    price_poisoned_arrows: ItemPrice = ("Poisoned Arrow Bunch", 30, "")
    price_atk_up: ItemPrice = ("Attack Up Scroll", 25, "")
    price_def_up: ItemPrice = ("Defense Up Ointment", 35, "")
    bought: bool = False
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print_stats()
    if shop_prices(price_pot, price_arrow, price_poisoned_arrows, price_atk_up, price_def_up):
        bought = True
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    return bought


def shop_prices(p_pot: ItemPrice, p_arw: ItemPrice, p_p_arws: ItemPrice, p_atk: ItemPrice, p_def: ItemPrice) -> bool:
    """Display item prices and allow player to purchase them."""
    global gold
    bought: bool = False
    buying: bool = True
    wares: list[ItemPrice] = [p_pot, p_arw, p_p_arws, p_atk, p_def]
    while buying:
        i: int = 0
        while i < len(wares):
            print(f"{wares[i][1]}{wares[i][2]} - [{i + 1}] {wares[i][0]}")
            i += 1
        print("     [LEAVE]")
        choice: str = input("Which item would you like to look at? ").lower()
        if choice == "leave" or choice == "quit" or choice == "back" or choice == "cancel" or choice == "no":
            buying = False
            return bought
        elif choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5":
            if choice == "1":
                print("Health Potion. Can be consumed in battle to regain 12% - 40% of your HP.  Tastes a bit like honey.")
            elif choice == "2":
                print("Arrows. Used as ammo for your bow. You can have up to 4 ready at a time, but the rest are stored in your quiver.")
            elif choice == "3":
                print("Poisoned Arrows. Can be selected during battle to draw 4 arrows that also inflict extra damage over time ")
                print("                 instead of normal arrows to use in your bow.")
            elif choice == "4":
                print("A Magical Scroll of Attack. Temporarily boosts your damage output by 3-8 damage for 3 turns if used during battle.")
                print("                            either contains a generic motivational quote poster, but about revenge,")
                print("                            or it contains a bad opinion to get angry over.")
            elif choice == "5":
                print("An Magical Ointment of Defense. Reduces incoming damage by 30%-80% if used during battle.")
                print("                                Quite thin; rubs off after absorbing damage from 3 attacks.")
            input(f" {wares[int(choice) - 1][1]}G Each.")
            choice_amt = input("How many would you like to purchase? ")
            choice_int: int = 0
            try:
                choice_int = int(choice_amt)
            except ValueError:
                choice_int = -1
            if choice_int == 0:
                input("Nothing at the moment? That's alright. By all means, though, continue looking.")
            elif choice_int > 0 and wares[int(choice) - 1][1] * choice_int <= gold:
                input(f"{choice_int}... great; that'll be {wares[int(choice) - 1][1] * choice_int}G. After the purchase, you should have {gold - wares[int(choice) - 1][1] * choice_int}G left.")
                choice_confirm: str = input("Would you like to complete the transaction? [YES] or [NO]? ").lower()
                while choice != "yes" and choice != "no":
                    choice_confirm = input("Complete purchase? [YES] or [NO]. ").lower()
                if choice_confirm == "yes":
                    gold -= wares[int(choice) - 1][1] * choice_int
                    if choice == "1":
                        global hp_potions
                        hp_potions += choice_int
                    elif choice == "2":
                        global arrows_quiver
                        arrows_quiver += choice_int
                    elif choice == "3":
                        global poisoned_arrow_bunch
                        poisoned_arrow_bunch += choice_int
                    elif choice == "4":
                        global attack_up_scroll
                        attack_up_scroll += choice_int
                    elif choice == "5":
                        global defense_up_ointment
                        defense_up_ointment += choice_int
                    else:
                        input("Oh... you somehow broke my system... Hmmm... Well, let's just ignore that for now...")
                    input("Wonderful! Would you like anything else?")
                    bought = True
                else:
                    input("Fair enough. Why don't you browse a bit more and return with a purchase you're willing to follow through with?")
            elif choice_int > 0 and wares[int(choice) - 1][1] * choice_int > gold:
                input(f"Oh... It looks as if you don't have quite enough gold... You have {gold}G, but you tried to buy {wares[int(choice) - 1][1] * choice_int}G's worth of goods.")
                input("We can't have that! Here, take a look at the products once more... and pay attention to how you allocate your budget.")
            else:
                input("That... is not a valid quantity. Maybe you need a moment to look at all the items again.")
    return bought


def quit_game() -> None:
    """Quit game when requested or finished."""
    print(f"Thank you so much for playing, {user_name}!")
    print(f"You accumulated {points} \"adventure points\" and {gold} gold!")
    quit()


if __name__ == "__main__":
    main()