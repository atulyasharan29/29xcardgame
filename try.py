import turtle
import pandas as pd

# Example setup (replace with actual data)
# Assuming you have a DataFrame for cards
imgs = ['resized_queen_of_spades.gif', 'resized_8_of_spades.gif', 'resized_king_of_diamonds.gif', 'resized_10_of_diamonds.gif', 'resized_10_of_spades.gif', 'resized_queen_of_clubs.gif', 'resized_7_of_hearts.gif', 'resized_king_of_hearts.gif']
df = pd.DataFrame({
    "Name": [f"Card_{i}" for i in range(8)],
    "Image": [ f"{imgs[i]}"for i in range(8)],
    "Points": [i for i in range(8)],
    "Suit": ["Hearts", "Diamonds", "Clubs", "Spades"] * 2
})

player = {"cards": df[:8]}  # Example player hand (subset of cards)
player_cards = list(player["cards"]["Image"])  # List of card images

# Set up the screen
win = turtle.Screen()
win.bgcolor("green")
win.setup(width=1.0, height=1.0)
win.tracer(10)

# Add card images as shapes
for img in player_cards:
    win.addshape(img)

pen = turtle.Turtle()
pen.pu()
pen.ht()

# Display game title
pen.goto(0, 250)
pen.write("29", align="center", font=("Times New Roman", 40, "bold"))

# Display description
game_description = '''
"29" is a thrilling card game combining strategy, skill, and teamwork. Played with four players split into two teams, the goal is to score 29 points first. Enjoy the race to victory!
'''
pen.goto(-550, 100)
pen.write(game_description, align="left", font=("Times New Roman", 12, "italic"))

# Display play prompt
pen.goto(0, -200)
pen.write("Press P to Play", align="center", font=("Agency FB", 50, "italic"))

# Global state variables
player_hands = [False] * 8  # Whether a card is played
selected_card = None

def re_arrange_cards():
    """Rearrange cards on the screen based on their state."""
    pen.clear()
    pen.goto(0, 250)
    pen.write("29", align="center", font=("Times New Roman", 40, "bold"))

    for i, card in enumerate(player_cards):
        if not player_hands[i]:
            pen.shape(card)
            pen.goto(-350 + 100 * i, -250)
            pen.stamp()

def handle_card_click(x, y):
    """Handle a card click and update the game state."""
    global selected_card
    for i in range(8):
        card_x_min = -400 + i * 100
        card_x_max = card_x_min + 75
        if card_x_min <= x <= card_x_max and -300 <= y <= -200 and not player_hands[i]:
            print(f"Card {i + 1} clicked: {player_cards[i]}")
            selected_card = player_cards[i]
            player_hands[i] = True
            re_arrange_cards()
            break

def play_game():
    """Set up the main game display and logic."""
    re_arrange_cards()
    win.onclick(handle_card_click)

def press_p():
    """Start the game when P is pressed."""
    play_game()

# Bind the "P" key to start the game
win.onkeypress(press_p, "p")
win.onkeypress(press_p, "P")
win.listen()
win.mainloop()
