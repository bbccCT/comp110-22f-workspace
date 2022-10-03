"""An RPG in a choose-your-own-adventure style."""

__author__ = "930605992"


import time
from random import randint
from typing import overload
from zoneinfo import available_timezones


points: int = 0
gold: int = 50
user_name: str = ""
player: str = ""
max_health: int = 25
health: int = max_health
speed: int = 10
room_id: str = "tutorial"
met_jester: bool = False;
upgrades: list[str] = list()
# other vars like for items and stuff im tired
temp_item_buffs_ADS: list[int] = [0, 0, 0] #attack buff, defense buff, shield active or not
shield_lvl: int = 1
hp_potions: int = 5
arrows_ready: int = 4
arrows_quiver: int = 30
poisoned_arrow_bunch: int = 0
attack_up_scroll: int = 0
defense_up_ointment: int = 0
ItemPrice = tuple[str, int, str] # Name, Price, Extra space if needed
EnemyStats = tuple[str, int, int, int, int, int, int] # Name, Health, Attack, Defense, Speed (inverse to Accuracy Window if have reaction attack upgrade), G on kill, points on win

U_PLAYR: str = "\U0000265F"
U_BOX_G: str = "\U0001F7E9"
U_BOX_Y: str = "\U0001F7E8"
U_BOX_R: str = "\U0001F7E5"


def main() -> None:
    """Entrypoint of program."""
    greet()
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
    input("(When lines of text not requiring input appear, press the ENTER key to progress after reading.)")
    print("(Good. Now, when input is required, options such as [FIGHT] or [TALK] will be included")
    choice: str = input("  and you should type one of them (minus the brackets) (not case sensitive), [OKAY]?) ")
    while choice.lower() != "okay":
        choice = input("(So if the option you want to select is [OKAY], you can type \"okay\", [OKAY]?) ")
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
    global player
    player = input("Now... What's that daring hero's name? ")
    while not player:
        player = input("(Please don't just spam enter. Name the hero.) ")
    input("...Interesting...")
    input(f"And the hero's name... was {player}.")
    global user_name
    input("And what of the user?")
    user_name = input("What is your name? ")
    while not user_name:
        user_name = input("(Really? Don't detract from the experience. What is your real name?) ")
    input("Ah, very good. Well then, it is time to begin your journey.")
    input(f"Good luck, {user_name}.\n")
    input(f"And so, {player} set off, seeking vengeance.")
    input(f"However, they lacked training, and decided to start by stopping by to see an impartial (and rather eccentric) character for some training: the jester.")
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
        choice = input(f"{player} braces themself as they prepare to advance through the Guantlet. There's nothing else to do now but continue [UP] or [QUIT]. " ).lower()
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
        if randint(0,3) == 3:
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
        choice = input(f"What will you do? What can you do, though? [TALK]? [FIGHT]? [QUIT]? ").lower()
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
                choice = input(f"Proceed. [FIGHT]. ").lower
        input("QUEEN: \"You dare to resist us? Have at thee, villainous cur! Off with thy head!\"")
        return "fight"
    elif room == "king":
        input(f"Finally, after a difficult journey plagued with trials, {player} arrives at the throne room: the pinnacle of the Guantlet.")
        input("The enemy King sits before you upon their throne. They raise their gaze, settling upon {player}. Their face bears an expression of weariness.")
        choice = input("This is it. [TALK]. [FIGHT]. [QUIT]. In any case, this is where it ends. ").lower()
        i: int = 0
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
    else:
        input("The room dialogue being called for does not exist. Sorry! You've somehow broken the game.")


def room_fight(room: str) -> str:
    """Begin a fight with the proper character.""" #CURRENTLY UNFINISHED
    choice: str = ""
    fight_over: bool = False
    turn: int = 0
    HEALTH_UPGRADE_HEALTH: int = 50
    who_alive: list[bool] = [True]
    enemy: EnemyStats
    STATS_JESTER: EnemyStats = ("Jester", 50, 15, 20, 999, 30, 50)
    STATS_PAWN: EnemyStats = ("Pawn", 25, 10, 20, 10, 5, 15)
    STATS_KNIGHT: EnemyStats = ("Knight", 75, 25, 25, 80, 50, 30)
    STATS_BISHOP: EnemyStats = ("Bishop", 30, 75, 5, 50, 75, 50)
    STATS_ROOK: EnemyStats = ("Rook", 80, 25, 80, 15, 50, 75)
    STATS_QUEEN: EnemyStats = ("Queen", 100, 80, 60, 90, 300, 100)
    STATS_KING: EnemyStats = ("King", 300, 50, 20, 20, 100, 85)
    if room == STATS_JESTER[0].lower():
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
    while not fight_over:
        if room == "queen":
            fight_over = enemy_turn(room, enemy, turn, who_alive)
        else:
            fight_over = player_turn(room, enemy, turn, who_alive)
        if room != "queen":
            fight_over = enemy_turn(room, enemy, turn, who_alive)
        turn += 1
    global health
    if health > 0:
        global upgrades
        if room == "tutorial":
            upgrades.append("iron shield")
            input("You received the Iron Shield! Much sturdier than your wooden shield. Can reduce incoming damage for 3 turns instead of 2!")
            return "tutorial_intersection"
        elif room == "pawn":
            upgrades.append("pawn soul") #en passant (reactionary attacks)
            input("You've collected the soul of the enemy pawn. It increases your Pawn Power, and through the power of En Passant, your attacks now rely on Reaction Speed!")
            return "knight"
        elif room == "knight":
            upgrades.append("knight soul") #widens window of reactionary attack (not actuall necessary bc of linear progression) and ability to choose RNG or reactionary
            print("You've collected the knight's soul. It increases your accuracy window during Reactionary Attacks, and ")
            input(" it grants you the ability to choose whether to use them or to rely on RNG attacks.")
            return "pawn_legion"
        elif room == "pawn_legion":
            upgrades.append("legion souls")
            input(f"You've obtained the souls of enough pawns that your maximum health has increased from {max_health} to {HEALTH_UPGRADE_HEALTH}! You'll need it if you want to survive the stronger opponants ahead.")
            global max_health
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
        input("Y O U   D I E D .")
        choice = input("[RETRY] or [QUIT]? Keep in mind, only health is reset if you [RETRY]. If you want a better run, [QUIT] and start over. ").lower()
        while choice != "retry":
            if choice == "quit":
                input("That's understandable. Good try.")
                quit_game()
            choice = input("[RETRY] or [QUIT]? ").lower()
        global max_health
        health = max_health
        return room

def player_turn(room: str, enemy: EnemyStats, turn: int, alive: list(bool)) -> bool:
    """During a fight, determine player's action each turn."""
    global player
    global upgrades
    choice: str = ""
    fight_flavor_text(room, turn, alive)
    input(f"--{player}'s turn.--")
    if choice == "fight":
        use_reactionary_attack: bool = False
        if "pawn soul" in upgrades and "knight soul" in upgrades:
            choice = input("Would you like to use a [SPEED]-based attack or [RNG]-based attack? ").lower()
            while choice != "speed" and choice != "rng":
                if choice == "quit":
                    quit_game()
                choice = input("[SPEED]-based attack, where damage relies on your reflexes, or [RNG]-based attack, where appropriately-balanced random number generators decide damage? ")
            if choice == "speed":
                use_reactionary_attack = True
        elif "pawn soul" in upgrades and "knight soul" not in upgrades:
            use_reactionary_attack = True


def fight_flavor_text(room: str, turn: int, alive: list(bool)) -> None:
    flavor_texts: list[str] = list()
    overflow_texts: list[str] = list()
    if room == "tutorial":
        flavor_texts.append("JESTER: \"During a tussle, you'll have to choose to use your words, items, or muscles!\"")
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
        i: int = randint(1, 8)
        while alive[i] == False:
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
        i: int = randint(0, len(overflow_texts) - 1)
        input(overflow_texts[i])


def enemy_turn(room: str, stats: EnemyStats, turn: int) -> bool:
    """During a fight, determine enemy's action each turn."""
    input() #temp


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
    if health > max_health/2:
        use_u_box = U_BOX_G
    elif health > max_health/5:
        use_u_box = U_BOX_Y
    else:
        use_u_box = U_BOX_R
    i = 0
    while i < health:
        print(use_u_box, end = '')
        i += 5
    input()


def shop_menu() -> bool:
    """Get the shop ready for interaction."""
    global hp_potions
    global arrows_quiver
    global poisoned_arrow_bunch
    global attack_up_scroll #contains generic motivational quote poster but about revenge OR contains a bad opinion to get angry over
    global defense_up_ointment #thin layer, so it only lasts 1 turn
    global gold
    price_pot: ItemPrice = ("HP Potion", 20, "")
    price_arrow: ItemPrice = ("Arrow", 3, " ")
    price_poisoned_arrows: ItemPrice = ("Poisoned Arrow Bunch", 30, "")
    price_atk_up: ItemPrice = ("Attack Up Scroll", 25, "")
    price_def_up: ItemPrice = ("Defense Up Ointment", 15, "")
    bought: bool = False
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print_stats()
    if shop_prices(price_pot, price_arrow, price_poisoned_arrows, price_atk_up, price_def_up):
        bought = True
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


def shop_prices(p_pot: ItemPrice, p_arw: ItemPrice, p_p_arws: ItemPrice, p_atk: ItemPrice, p_def: ItemPrice) -> bool:
    """Display item prices and allow player to purchase them."""
    global gold
    bought: bool = False;
    buying: bool = True;
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
                choice = input("Would you like to complete the transaction? [YES] or [NO]? ").lower()
                while choice != "yes" and choice != "no":
                    choice = input("Complete purchase? [YES] or [NO]. ").lower()
                if choice == "yes":
                    gold -= wares[int(choice) - 1][1] * choice_int
                    bought = True;
                    input("Wonderful! Would you like anything else?")
                else:
                    input("Fair enough. Why don't you browse a bit more and return with a purchase you're willing to follow through with?")
            elif choice_int > 0 and wares[int(choice) - 1][1] * choice_int > gold:
                input(f"Oh... It looks as if you don't have quite enough gold... You have {gold}G, but you tried to buy {wares[int(choice) - 1][1] * choice_int}G's worth of goods.")
                input("We can't have that! Here, take a look at the products once more... and pay attention to how you allocate your budget.")
            else:
                input("That... is not a valid quantity. Maybe you need a moment to look at all the items again.")


def quit_game() -> None:
    """Quit game when requested or finished."""
    print(f"Thank you so much for playing, {user_name}!")
    print(f"You accumulated {points} \"adventure points\" and {gold} gold!")
    quit()


if __name__ == "__main__":
  main()