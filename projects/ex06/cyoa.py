"""An RPG in a choose-your-own-adventure style."""

__author__ = "930605992"


import time


points: int = 0
gold: int = 50
user_name: str = ""
player: str = ""
max_health: int = 25
health: int = max_health
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
ItemPrice = tuple[str, int, str]

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
            room_fight(room_id)
        else:
            room_id = path
        


def greet() -> None:
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
    time.sleep(2)
    input("...Interesting...")
    input(f"And the hero's name... was {player}.")
    time.sleep(2)
    global user_name
    input("And what of the user?")
    user_name = input("What is your name? ")
    while not user_name:
        user_name = input("(Really? Don't detract from the experience. What is your real name?) ")
    input("Ah, very good. Well then, it is time to begin your journey.")
    input(f"Good luck, {user_name}.")
    time.sleep(2)
    input(f"And so, {player} set off, seeking vengeance.")
    input(f"However, they lacked training, and decided to start by stopping by to see an impartial (and rather eccentric) character for some training: the jester.")
    points += 5


def draw_map(room: str) -> None:
    global U_PLAYR
    U_BWALL: str = "\U00002B1B"
    U_FLOOR: str = "\U00002B1C"
    U_JOKER: str = "\U0001F0CF"
    U_WPAWN: str = "\U00002659"
    U_KNGHT: str = "\U00002658"
    U_BSHOP: str = "\U00002657"
    U_WROOK: str = "\U00002656"
    U_QUEEN: str = "\U00002655"
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
    elif room == "king":
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
        U_WKING_ROTATED: str = "\U0001FA09"
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
    choice: str = ""
    global points
    if room == "tutorial":
        print(f"{player} arrives near the entrance to the White Castle, colloquially referred to as \"The Guantlet\" because of its")
        input("oddly linear path and progression of difficulty leading straight to the castle, which strikes most as strategically inept.")
        input(f"Ahead of {player} is the local jester - a neutral party and a bit of a wild card, but more than happy to spar.")
        input("Some training might be useful before wagering your life in a series of disadventageous battles. And who knows? He could offer a reward for beating him.")
        choice = input("Would you like to [TALK], skip him and go [RIGHT] to the Guantlet, or [QUIT] here? ").lower()
        while choice != "talk" and choice != "right" and choice != "quit":
            choice = input("[TALK] to the jester, go [RIGHT], or [QUIT] the game? ").lower()
        if choice == "quit":
            quit_game()
        elif choice == "right":
            return "tutorial_intersection"
        else:
            global met_jester 
            met_jester = True
            points += 10
            print("JESTER: \"Uee hee hee! You want to learn to keep yourself out of a garbage bin?")
            input("         You'll be glad you came to me! I'll teach you how to win, win, win!")
            print("         Go right for a fight, but you pay for that fray...")
            input("         But not with me; this brawl is free!\"")
            return "fight"
    elif room == "tutorial_intersection":
        choice = input(f"{player} braces themself as they prepare to advance through the Guantlet. There's nothing else to do now but continue [UP] or [QUIT]." ).lower()
        if choice == "quit":
            quit_game()
        i: int = 0
        while choice != "up":
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
        if choice == "quit":
            quit_game()
        while choice != "fight" and choice != "talk":
            choice = input(f"{player} is too blinded by fury to do anything but [FIGHT]... at least for now. ")
            if choice == "quit":
                quit_game()
        input("PAWN: \"Oh? A survivor? Go back home and sulk, you miserable wretch. Your side's been beaten!\"")
        input("      \"Really? You're gonna face me head-on? Bring it! I'm due for a promotion soon anyway!\"")
        points += 5
        return "fight"
    elif room == "knight":
        choice = input(f"In this section of the Guantlet, {player} encounters a fearsome knight atop their horse. Will you [TALK], [FIGHT], or [QUIT]? ").lower()
        if choice == "quit":
            quit_game()
        while choice != "fight" and choice != "talk":
            choice = input("Your only choices here are [TALK] and [FIGHT], and given the look of disgust on the knight's face, they'll do the same thing... ")
            if choice == "quit":
                quit_game()
        if choice == "talk":
            points += 15
            input("KNIGHT: \"Um.\"")
            input("        \"What are you doing here? You already destroyed you lot.\"")
            input("        \"Leave before I make you leave, knave.\"")
            choice = input("Well, it was worth a shot. [FIGHT]. ").lower()
            while choice != "fight":
                choice = input("Proceed to the [FIGHT]. ")
        print("        \"Alright, that's it. I'm gonna fry your liver. You can try to put up a fight and make it challenging, I guess.")
        input("        \"Catch me if you can!\"")
        input("        \"Spoiler alert: you can't!")
        return "fight"
    elif room == "pawn_legion":
        #REVENGE
        input() #temp
    elif room == "shop_intersection":
        choice = input(f"{player} comes across a branch in the path. Do you [QUIT], investigate [RIGHT], or continue [UP]? You won't be able to return if you proceed upwards. ").lower()
        if choice == "quit":
            quit_game()
        while choice != "up" and choice != "right":
            choice = input("Deviate and go [RIGHT] or continue fighting [UP] without resting.").lower()
            if choice == "quit":
                quit_game()
    elif room == "shop":
        points += 10
        choice = input(f"{player} comes across a wooden structure with a sign advertising \"shop\", with a flashy, unfamiliar shopkeep seated inside. [TALK] to them, go back [LEFT], or [QUIT]? ").lower()
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
                    points += 15
            return "shop_intersection"
    elif room == "bishop":
        #bishop dialogue
        input() #temp
    elif room == "rook":
        #rook dialogue
        input() #temp
    elif room == "queen":
        #queen dialogue
        # Haven't you heard? White always goes first!
        input() #temp
    elif room == "king":
        #king dialogue before fight and after if spare
        input() #temp
    elif room == "king_dead":
        #narration & jester dialogue (evil)
        input() #temp


def room_fight(room: str) -> None:
    #fights here
    input() #temp


def print_stats() -> None:
    global hp_potions
    global arrows_quiver
    global poisoned_arrow_bunch
    global attack_up_scroll
    global defense_up_ointment
    global gold
    global points
    global health
    global maxHealth
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
    print(f"   HP: {health}/{maxHealth}")
    if health > maxHealth/2:
        use_u_box = U_BOX_G
    elif health > maxHealth/5:
        use_u_box = U_BOX_Y
    else:
        use_u_box = U_BOX_R
    i = 0
    while i < health:
        print(use_u_box, end = '')
        i += 5
    input()


def shop_menu() -> bool:
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
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print_stats()
    if shop_prices(price_pot, price_arrow, price_poisoned_arrows, price_atk_up, price_def_up):
        bought = True
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


def shop_prices(p_pot: ItemPrice, p_arw: ItemPrice, p_p_arws: ItemPrice, p_atk: ItemPrice, p_def: ItemPrice) -> bool:
    global gold
    bought: bool = False;
    buying: bool = True;
    while buying:
        print(f"{p_pot[1]}{p_pot[2]} - [1] {p_pot[0]}")
        print(f"{p_arw[1]}{p_arw[2]}  - [2] {p_arw[0]}")
        print(f"{p_p_arws[1]}{p_p_arws[2]} - [3] {p_p_arws[0]}")
        print(f"{p_atk[1]}{p_atk[2]} - [4] {p_atk[0]}")
        print(f"{p_def[1]}{p_def[2]} - [5] {p_def[0]}")
        print("     [LEAVE]")
        choice: str = input("Which item would you like to look at? ").lower()
        if choice == "leave" or choice == "quit" or choice == "back" or choice == "cancel" or choice == "no":
            buying = False
            return bought
        elif choice == "1":
            print("Health Potion. 25G Each. Can be consumed in battle to regain 12% - 40% of your HP.  Tastes a bit like honey.")
            choice = input("How many potions would you like to purchase? ")
            choice_int: int = 0
            try:
                choice_int = int(choice)
            except ValueError:
                choice_int = -1
            if choice_int == 0:
                print("Nothing at the moment? That's alright. By all means, though, continue looking.")
            elif choice_int > 0 and choice_int <= gold:
                print(f"{choice_int} health potions... great; that'll be {p_pot * choice_int}G. After the purchase, you should have {gold - p_pot * choice_int}G left.")
                choice = input("Would you like to complete the transaction? [YES] or [NO]? ").lower()
                if choice == "yes":
                    gold -= p_pot * choice_int
                    bought = True;
                    print("Wonderful! Would you like anything else?")
            else:
                print("That... is not a valid quantity. Maybe you need a moment to look at all the items again.")


def quit_game() -> None:
    print(f"Thank you so much for playing, {user_name}!")
    print(f"You accumulated {points} \"adventure points\" and {gold} gold!")
    quit()


if __name__ == "__main__":
  main()