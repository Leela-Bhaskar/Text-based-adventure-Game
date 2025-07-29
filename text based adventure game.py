import time
import textwrap

def print_slow(text, delay=0.03):
    """Prints text with a slight delay between characters for a dramatic effect."""
    for char in textwrap.fill(text, 80):
        print(char, end='', flush=True)
        time.sleep(delay)
    print("\n")

def get_choice(choices):
    """
    Gets user input and validates it against the available choices.

    Args:
        choices (dict): A dictionary where keys are the valid choices.

    Returns:
        str: The user's valid choice, converted to lowercase.
    """
    while True:
        print("What do you do?")
        for choice in choices:
            print(f"- {choice.capitalize()}")
        
        user_input = input("> ").lower().strip()
        
        if user_input in choices:
            return user_input
        else:
            print_slow("That's not a valid option. Try again.")

def play_game():
    """Main function to run the text-based adventure game."""

    # --- Game Data: Locations, descriptions, and choices ---
    game_map = {
        'start': {
            'description': "You awaken in a dimly lit, ancient forest. Towering trees form a thick canopy, blocking most of the sunlight. You see a narrow path heading north and hear the faint sound of running water to the east.",
            'choices': {
                'go north': 'path',
                'go east': 'river',
                'look around': 'start_look'
            }
        },
        'start_look': {
            'description': "You take a moment to observe your surroundings. The air is damp and smells of moss and earth. The trees are ancient, with gnarled roots that look like grasping claws. The path north seems well-trodden, but the sound from the east is intriguing.",
            'choices': {
                'go north': 'path',
                'go east': 'river'
            }
        },
        'path': {
            'description': "You follow the path north. It winds deeper into the woods. After a few minutes, you come to a fork. A signpost is barely readable. One arrow points west, another points east.",
            'choices': {
                'go west': 'clearing',
                'go east': 'cave_entrance',
                'go back': 'start'
            }
        },
        'river': {
            'description': "You head east and find a swift-flowing river. The water is crystal clear. You see a rickety-looking rope bridge crossing the river. It doesn't look very safe.",
            'choices': {
                'cross bridge': 'bridge_cross',
                'follow river': 'river_follow',
                'go back': 'start'
            }
        },
        'clearing': {
            'description': "You arrive in a sun-dappled clearing. In the center stands a solitary, ancient oak tree. There seems to be something carved into its trunk.",
            'choices': {
                'examine tree': 'tree_examine',
                'leave clearing': 'path'
            }
        },
        'tree_examine': {
            'description': "You approach the oak tree and see an intricate carving of a key. Below it, nestled in a hollow of the root, you find a small, rusty iron key. You take it.",
            'choices': {
                'leave clearing': 'path'
            },
            'item': 'key'
        },
        'cave_entrance': {
            'description': "You find the entrance to a dark cave. A cool breeze emanates from within, carrying a faint, metallic scent. It's unnervingly dark inside.",
            'choices': {
                'enter cave': 'cave_inside',
                'go back': 'path'
            }
        },
        'cave_inside': {
            'description': "You step into the cave. It's too dark to see anything. You stumble around in the blackness.",
            'choices': {
                'go back': 'cave_entrance'
                # A choice for 'use light' could be added if a light source exists
            }
        },
        'bridge_cross': {
            'description': "You cautiously step onto the rope bridge. It sways precariously with every step. Halfway across, a rope snaps! You lose your footing and fall into the rushing water below.",
            'choices': {}, # End of game
            'ending': 'bad'
        },
        'river_follow': {
            'description': "You decide to follow the river downstream. The forest thins, and you see a small, wooden cabin ahead. Smoke curls gently from its chimney.",
            'choices': {
                'approach cabin': 'cabin',
                'go back': 'river'
            }
        },
        'cabin': {
            'description': "You approach the cabin. The door is old and heavy, with a large, rusty lock. It seems you need a key to open it.",
            'choices': {
                'use key': 'cabin_unlocked',
                'knock on door': 'cabin_knock',
                'leave': 'river_follow'
            }
        },
        'cabin_knock': {
            'description': "You knock, but there's no answer. The cabin remains silent and still.",
            'choices': {
                'use key': 'cabin_unlocked',
                'leave': 'river_follow'
            }
        },
        'cabin_unlocked': {
            'description': "You try the rusty key you found. It fits perfectly! With a click, the lock opens. You push the door open and step inside.",
            'choices': {
                'enter': 'ending_win'
            }
        },
        'ending_win': {
            'description': "Inside, the cabin is warm and cozy. A friendly-looking old man sits by a fireplace. He looks up and smiles. 'Ah, a visitor! I've been expecting you. You've found your way out of the Whispering Woods. Well done!' You feel a sense of relief and safety.",
            'choices': {},
            'ending': 'good'
        }
    }

    # --- Game State ---
    current_location = 'start'
    inventory = []

    # --- Game Intro ---
    print_slow("--- The Whispering Woods ---")
    print_slow("An interactive text adventure.")
    print_slow("Type your choices to navigate the world.")
    print("-" * 30)

    # --- Main Game Loop ---
    while True:
        location = game_map[current_location]
        
        print_slow(location['description'])

        # --- Check for Endings ---
        if location.get('ending'):
            if location['ending'] == 'good':
                print_slow("\nCongratulations! You have won the game.")
            else:
                print_slow("\nGame Over. Better luck next time.")
            break

        # --- Handle Items ---
        if 'item' in location and location['item'] not in inventory:
            inventory.append(location['item'])
            print_slow(f"You have acquired a {location['item']}.")

        # --- Get Player Choice ---
        # Modify choices based on inventory
        available_choices = location['choices'].copy()
        if current_location == 'cabin' and 'key' not in inventory:
            # Player can't use a key they don't have
            if 'use key' in available_choices:
                del available_choices['use key']
        
        if not available_choices:
            print_slow("There's nothing more you can do here.")
            break

        choice = get_choice(available_choices)

        # --- Update Game State ---
        if choice == 'use key':
            if 'key' in inventory:
                current_location = location['choices']['use key']
            else:
                # This case is handled by removing the choice, but as a fallback:
                print_slow("You don't have a key to use.")
        else:
            current_location = location['choices'][choice]
        
        print("-" * 30)


if __name__ == "__main__":
    play_game()
