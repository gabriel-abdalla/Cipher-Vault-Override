import pygame
import pygame_widgets
import random
from pygame_widgets.textbox import TextBox   

# Initializes Pygame
pygame.init()

# Sets up the display window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Worst Interface Challenge: Time-Attack Cipher Vault")

# Game Loop variables
running = True
clock = pygame.time.Clock()

# --- TIMER CONFIGURATION ---
TIMER_LIMIT = 60
start_ticks = pygame.time.get_ticks()  

# ----- Classes -----
class GameState:
    """
    Class for the state of the game
    Attributes (class):
        + val (None)
        - combinedval (str)
        + accepted_number (str)
    Methods:
        + __init__(): void
        - combinedval(self): str
        - combinedval(self, value): void
    """
    def __init__(self):
        """
        Initializes a new GameState object.
        """
        self.val = None
        self._combinedval = ""  
        
        # CHANGED: Generates a completely unique, random 4-digit code using keys '1'-'9'
        self.accepted_number = "".join(random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9"]) for _ in range(4))

    @property
    def combinedval(self):
        """Returns the combinedval."""
        return self._combinedval

    @combinedval.setter
    def combinedval(self, value):
        """
        Makes sure that combinedval is not over 4 digits.
    
        Args:
            value (str): Proposed combinedval
        """
        self._combinedval = value
        if len(self._combinedval) == 5:
            self._combinedval = ""

# Creates a GameState object to manipulate attributes.      
state = GameState()

def initalization():
    """
    Intializes the program with the creation of the dictionary for the random language.
    
    Returns:
        dictionary_for_symbols (dict): Dictionary of the new language of symbols
        possible_letters2 (list): List of possible symbols
        words_dict (dict): Dictionary between numbers and their word counterpart.
        rendering_dictionary_for_symbols (dict): Altered version of dictionary_for_symbols used in rendering to hide a few values.
    """
    possible_letters = [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", 
        "-", "_", "+", "=", "[", "]", "{", "}", ";", ":", 
        "'", '"', ",", ".", "<", ">"
    ]

    possible_letters2 = possible_letters.copy()

    possible_actual_letters = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z"
    ]

    words_dict = {
        "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
    }

    dictionary_for_symbols = {}

    # Creates the dictionary for the language.
    for t in range(26):
        temp1 = random.choice(possible_letters)
        temp2 = random.choice(possible_actual_letters)
        possible_letters.remove(temp1)
        possible_actual_letters.remove(temp2)
        dictionary_for_symbols[temp1] = temp2

    # Makes a clone of that dictionary.
    rendering_dictionary_for_symbols = dictionary_for_symbols.copy()

    # Replaces some letters with a question mark on random.
    for value in rendering_dictionary_for_symbols:
        if random.choice([1, 2, 3]) in [1]:
            rendering_dictionary_for_symbols[value] = "?"

    return dictionary_for_symbols, possible_letters2, words_dict, rendering_dictionary_for_symbols

# Intializes the dictionaries containing the symbol language  
dictionary_for_symbols, possible_letters2, words_dict, rendering_dictionary_for_symbols = initalization()

def output(dictionary_for_symbols, possible_letters2, words_dict):
    """
    Creates an output based on the user's input into the box and updates val and combinedval.

    Args:
        dictionary_for_symbols (dict): Dictionary of the new language of symbols
        possible_letters2 (list): List of possible symbols
        words_dict (dict): Dictionary between numbers and their word counterpart.
    """
    state.val = textbox.getText()
    word = ""
    for symbol in state.val:
        if symbol not in possible_letters2:
            break
        else:
            word = word + dictionary_for_symbols[symbol]
    if word not in words_dict:
        print("Invalid")
    else:
        state.combinedval = state.combinedval + words_dict[word]
        textbox.setText("") 

def find_all_translations():
    """
    Creates a shuffled list of the number words in the language

    Returns:
        translated_list (list): List of Number Words translated into the language
    """

    def get_symbol_for_letter(letter):
        """
        Returns the symbol corresponding to letter argument

        Args:
            letter (str): The letter of a number word
        Returns:
            symbol (str): The symbol counterpart
            "?" (str): The symbol returned if there isn't a counterpart
        """
        for symbol, mapped_letter in dictionary_for_symbols.items():
            if mapped_letter == letter:
                return symbol
        return "?"  

    def recursive_translate_word(word_str):
        """
        Recursive function to build the translation of a number word.

        Args:
            word_str (str) - number word
        Returns:
            (str) - Combined translated word
        """
        # Base case when the string is empty.
        if not word_str:
            return ""
        
        first_letter = word_str[0] # Takes the first letter
        symbol = get_symbol_for_letter(first_letter) # Translates it
        return symbol + recursive_translate_word(word_str[1:]) # Repeats the process for each letter, and combines them together.

    # For each word, a translation is found, and it's added to a list.
    translated_list = []
    for word_number in words_dict.keys(): 
        translated_symbols = recursive_translate_word(word_number)
        translated_list.append(translated_symbols)

    # The list is then shuffled and returned.
    random.shuffle(translated_list)
    return translated_list

# Creates a list of all the translated number words shuffled.
translated_list = find_all_translations()

# Textbox intializaton
textbox = TextBox(
    screen, 120, 500, 560, 80, fontSize=25,
    borderColour=(152, 219, 123), textColour=(25, 26, 31),
    onSubmit=lambda: output(dictionary_for_symbols, possible_letters2, words_dict), radius=10, borderThickness=5,
)

# Text fonts
title_font = pygame.font.SysFont('calibri', 24, bold=True)
label_font = pygame.font.SysFont('calibri', 18, bold=True)
sub_font = pygame.font.SysFont('calibri', 15, italic=True)
timer_font = pygame.font.SysFont('calibri', 28, bold=True)

# MAIN GAME LOOP
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # Checks if the user clicked the delete button to remove their inputs.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                state.combinedval = state.combinedval[:-1]

    # --- TIMER TRACKING SYSTEM ---
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_remaining = max(0, int(TIMER_LIMIT - seconds_passed))

    # If the time reaches 0, reset everything.
    if time_remaining <= 0:
        screen.fill((200, 40, 40))
        pygame.display.flip()
        pygame.time.wait(200)
        
        state.combinedval = ""
        start_ticks = pygame.time.get_ticks()  
        dictionary_for_symbols, possible_letters2, words_dict, rendering_dictionary_for_symbols = initalization()
        translated_list = find_all_translations()
        state.accepted_number = "".join(random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9"]) for _ in range(4))
        textbox.setText("")
        continue

    screen.fill((25, 26, 31))

    # ================= ONBOARDING LABELS =================
    title_surf = title_font.render(f"CIPHER VAULT OVERRIDE", True, (235, 52, 88))
    screen.blit(title_surf, (30, 25))
    
    timer_color = (235, 52, 88) if time_remaining <= 10 else (152, 219, 123)
    timer_surf = timer_font.render(f"TIME REMAINING: {time_remaining}s", True, timer_color)
    screen.blit(timer_surf, (520, 22))
    
    help_text = "Complete the verification process before the data purge."
    help_surf = sub_font.render(help_text, True, (170, 175, 190))
    screen.blit(help_surf, (30, 65))

    help_text2 = "Try typing the code by entering the number as a word one by one."
    help_surf2 = sub_font.render(help_text2, True, (170, 175, 190))
    screen.blit(help_surf2, (120, 475))
    
    help_text3 = "The vault does not accept letters, but maybe it will accept something else..."
    help_surf3 = sub_font.render(help_text3, True, (170, 175, 190))
    screen.blit(help_surf3, (350, 345))

    help_text4 = "These words might be the number words in the correct language...."
    help_surf4 = sub_font.render(help_text4, True, (170, 175, 190))
    screen.blit(help_surf4, (350, 145))

    verification_text = f"Your verification code is {state.accepted_number}"
    verification_text_surf = title_font.render(verification_text, True, (235, 52, 88))
    screen.blit(verification_text_surf, (30, 95))

    lbl1_surf = label_font.render("UPLOADED NUMBER WORD DATA:", True, (152, 219, 123))
    screen.blit(lbl1_surf, (15, 145))
    
    lbl2_surf = label_font.render("MATRIX KEY ENGINE [Symbol -> Letter]:", True, (152, 219, 123))
    screen.blit(lbl2_surf, (15, 345))
    # =====================================================

    # Delete Layout Button
    button_rect = pygame.Rect(700, 500, 88, 80)
    pygame.draw.rect(screen, (235, 52, 88), button_rect, border_radius=10)
    button_font = pygame.font.SysFont('calibri', 22)
    text_surf = button_font.render("Delete", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    # Output Progress field layout
    value_tracker = pygame.Rect(12, 500, 85, 80)
    pygame.draw.rect(screen, (152, 219, 123), value_tracker, 3, border_radius=10)
    value_font = pygame.font.SysFont('calibri', 25)
    text_surf = value_font.render(state.combinedval, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=value_tracker.center)
    screen.blit(text_surf, text_rect)
    
    # Key mapping matrix table layout
    number = 12
    value_font = pygame.font.SysFont('calibri', 20)
    for element in rendering_dictionary_for_symbols:
        i = pygame.Rect(number, 380, 28, 32)
        pygame.draw.rect(screen, (152, 219, 123), i, 1)
        text_surf = value_font.render(element, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=i.center)
        screen.blit(text_surf, text_rect)

        i = pygame.Rect(number, 415, 28, 32)
        pygame.draw.rect(screen, (152, 219, 123), i, 1)
        text_surf = value_font.render(rendering_dictionary_for_symbols[element], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=i.center)
        screen.blit(text_surf, text_rect)
        number = number + 30

    # Scrambled words box layout values
    number = 15
    for words in translated_list:
        i = pygame.Rect(number, 180, 80, 45)
        pygame.draw.rect(screen, (152, 219, 123), i, 1, border_radius=4)
        text_surf = (pygame.font.SysFont('calibri', 18)).render(words, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=i.center)
        screen.blit(text_surf, text_rect)
        number = number + 86

    # If the user enters the right code, end the program
    if state.combinedval == state.accepted_number:
        print("Code Entered Sucessfully!")
        running = False

    pygame_widgets.update(events)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


