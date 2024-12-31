import pandas as pd
import random
import math as mt
import turtle

df = pd.read_csv('output.csv')


from PIL import Image
import turtle

# Function to resize GIF images
def resize_gif(input_path, output_path, width, height):
    with Image.open(input_path) as img:
        resized_img = img.resize((width, height))  # Resize to the given dimensions
        resized_img.save(output_path)

# List to store resized image paths
imgs = []

# Resize each image in the imgs list before using it in Turtle
for i in list(df["Name"]):
    a = i.split(" ")
    img_path = '' + a[0].lower() + "_" + "of" + "_" + a[-1].lower() + ".gif"
    resized_path = 'resized_' + a[0].lower() + "_" + "of" + "_" + a[-1].lower() + ".gif"
    
    # Resize the image and save it to the new path with the desired height and width
    resize_gif(img_path, resized_path, width=75, height=120)  # Set desired width and height
    imgs.append(resized_path)  # Store resized path in imgs list

# Resize and append the red_joker image
red_joker_path = "red_joker.gif"
resized_red_joker_path = "resized_red_joker.gif"
face_down_path = "face_down.gif"
resized_face_down_path = "resized_face_down.gif"
resize_gif(red_joker_path, resized_red_joker_path, width=75, height=120)
resize_gif(face_down_path, resized_face_down_path, width=75, height=120)
imgs.append(resized_red_joker_path)  # Store resized red joker in imgs list
imgs.append(resized_face_down_path)


# /Users/atulyasharan/Desktop/queen_of_spades.gif

df["Image"] = imgs[:32]

df = df.drop('Unnamed: 0', axis = 1)

class Player():
    def __init__(self, cards, name):
        self.cards = cards
        self.colour_made = False
        self.points_made = 0
        self.name = name
        self.hands_won = []
        self.last_hand_won = False
        
class Robot():
    def __init__(self, cards, name):
        self.cards = cards
        self.colour_made = False
        self.points_made = 0
        self.name = name
        self.hands_won = []
        self.last_hand_won = False
      
class Game():
    def __init__(self):
        self.color = None
        self.last_hand_winner = None
        self.digged = False


class Bid():
    def __init__(self, b1, b2):
        self.how_much_b1 = 17
        self.how_much_b2 = 17
        self.b1_bid = input(f"Do you want to bid {b1.name}? Y/N: ").lower()
        
        if self.b1_bid == "n":
            print(f"{b2.name} wins the bid as {b1.name} passes at {self.how_much_b2}")
            self.winner = b2
        elif self.b1_bid == "y":
            self.b2_bid = input(f"Do you want to bid {b2.name}? Y/N: ").lower()

            if self.b2_bid == "n":
                print(f"{b1.name} wins the bid as {b2.name} passes at {self.how_much_b1}")
                self.winner = b1
            else:
                while self.b1_bid == "y" and self.b2_bid == "y":
                    self.how_much_b1 = int(input(f"How much would you like to bid {b1.name}? (minimum bid is 17): "))
                    self.how_much_b2 = int(input(f"How much would you like to bid {b2.name}? (minimum bid is 17): "))

                    # Ensure minimum bid
                    while self.how_much_b1 < 17 or self.how_much_b2 < 17:
                        print("Invalid bid! The minimum bid is 17.")
                        self.how_much_b1 = int(input(f"How much would you like to bid {b1.name}? (minimum bid is 17): "))
                        self.how_much_b2 = int(input(f"How much would you like to bid {b2.name}? (minimum bid is 17): "))

                    # Determine winner of the bid
                    if self.how_much_b1 < self.how_much_b2:
                        self.b1_bid = input(f"{b2.name} is winning the bid. Do you want to continue, {b1.name}? Y/N: ").lower()
                        if self.b1_bid == "n":
                            print(f"{b2.name} wins the bid as {b1.name} passes at {self.how_much_b2}")
                            self.winner = b2
                    elif self.how_much_b1 > self.how_much_b2:
                        self.b2_bid = input(f"{b1.name} is winning the bid. Do you want to continue, {b2.name}? Y/N: ").lower()
                        if self.b2_bid == "n":
                            print(f"{b1.name} wins the bid as {b2.name} passes at {self.how_much_b1}")
                            self.winner = b1


game = Game()

def shuffle_deck():
    global df
    df = df.sample(frac = 1, ignore_index = True)

def distribute_cards():
    global df
    global player, robot_1, robot_2, robot_3
    player = Player(df[0:8], input("What is your name? "))
    robot_1 = Robot(df[8:16], 'Robot 1')
    robot_2 = Robot(df[16:24], 'Robot 2')
    robot_3 = Robot(df[24:32], 'Robot 3')

def play_card(name, player):
    global current_hand
    current_hand = pd.concat([current_hand, df[df['Name'] == name]], ignore_index = True)
    # pd.concat([new_data, data], ignore_index=True)
    player.cards = player.cards.drop(player.cards[player.cards['Name'] == name].index)

def setup():
    
    shuffle_deck() # Shuffling all the cards
    distribute_cards() # Distributing all the cards
    print("Nice to meet you {}".format(player.name))
    print("Welcome to our newly made game of 29. We hope you enjoy it")
    print(player.cards[:4]) # Showing the player their first 4 cards
    global game,player_bid,r1_bid,r2_bid,r3_bid,max_bid
    game = Game()
        
    # BIDDING
    player_bid = int(input('How much do you want to bid?: '))
    
    # robot_1
    r1_bid = 0
    if len(robot_1.cards[:4]['Suit'].mode() == 1):
        r1_mode_suit = robot_1.cards[:4]['Suit'].mode().iloc[0]
        r1_color = robot_1.cards[:4]['Suit'].value_counts()[r1_mode_suit]
        r1_points = robot_1.cards[:4][robot_1.cards[:4]['Suit'] == r1_mode_suit]['Points'].sum()
        
        if mt.floor(r1_points) == 3 :
            if r1_color == 2: r1_bid = 18
            if r1_color == 3: r1_bid = 19
        if mt.floor(r1_points) == 4 :
            if r1_color == 2: r1_bid = 18
            if r1_color == 3: r1_bid = 19
        if mt.floor(r1_points) == 5:
            if r1_color == 2: r1_bid = 19
            if r1_color == 3: r1_bid = 20
        if mt.floor(r1_points) == 6 :
            if r1_color == 3: r1_bid = 22
        if mt.floor(r1_points) == 6 or mt.floor(r1_points) == 7:
            if r1_color == 4: r1_bid = 22
    
    # robot_2
    r2_bid = 0
    if len(robot_2.cards[:4]['Suit'].mode() == 2):
        r2_mode_suit = robot_2.cards[:4]['Suit'].mode().iloc[0]
        r2_color = robot_2.cards[:4]['Suit'].value_counts()[r2_mode_suit]
        r2_points = robot_2.cards[:4][robot_2.cards[:4]['Suit'] == r2_mode_suit]['Points'].sum()
        
        if mt.floor(r2_points) == 3 :
            if r2_color == 2: r2_bid = 18
            if r2_color == 3: r2_bid = 19
        if mt.floor(r2_points) == 4 :
            if r2_color == 2: r2_bid = 18
            if r2_color == 3: r2_bid = 19
        if mt.floor(r2_points) == 5:
            if r2_color == 2: r2_bid = 19
            if r2_color == 3: r2_bid = 20
        if mt.floor(r2_points) == 6 :
            if r2_color == 3: r2_bid = 22
        if mt.floor(r2_points) == 6 or mt.floor(r2_points) == 7:
            if r2_color == 4: r2_bid = 22
    
    # robot_3
    r3_bid = 0
    if len(robot_3.cards[:4]['Suit'].mode() == 3):
        r3_mode_suit = robot_3.cards[:4]['Suit'].mode().iloc[0]
        r3_color = robot_3.cards[:4]['Suit'].value_counts()[r3_mode_suit]
        r3_points = robot_3.cards[:4][robot_3.cards[:4]['Suit'] == r3_mode_suit]['Points'].sum()
        
        if mt.floor(r3_points) == 3 :
            if r3_color == 2: r3_bid = 18
            if r3_color == 3: r3_bid = 19
        if mt.floor(r3_points) == 4 :
            if r3_color == 2: r3_bid = 18
            if r3_color == 3: r3_bid = 19
        if mt.floor(r3_points) == 5:
            if r3_color == 2: r3_bid = 19
            if r3_color == 3: r3_bid = 20
        if mt.floor(r3_points) == 6 :
            if r3_color == 3: r3_bid = 22
        if mt.floor(r3_points) == 6 or mt.floor(r3_points) == 7:
            if r3_color == 4: r3_bid = 22
    bidding = [player_bid, r1_bid, r2_bid, r3_bid]
    max_bid = max(bidding)
    max_bid_index = bidding.index(max_bid)
    if max_bid <17:
        r3_bid = 17
        winner = robot_3.name
        max_bid = r3_bid
    else:
        if max_bid_index == 0: 
            winner = player.name
        if max_bid_index == 1: 
            winner = robot_1.name
        if max_bid_index == 2: 
            winner = robot_2.name
        if max_bid_index == 3: 
            winner = robot_3.name
    print('{} won the bet and will make the color on {} points.'.format(winner, max_bid))
    if winner == player.name:
        player.colour_made = True
        game.color = input(f"What is the colour {player.name}?")
    if winner == robot_1.name:
        game.color = r1_mode_suit
    if winner == robot_2.name:
        game.color = r2_mode_suit
    if winner == robot_3.name:
        game.color = r3_mode_suit
    game.color = game.color.capitalize()
setup()
import turtle

player_cards = []
for i in range(8):
    player_cards.append(player.cards.iloc[i]["Image"])

print(player_cards)

# Create the screen object
win = turtle.Screen()

# Set the background color
win.bgcolor("green")
win.setup(height=1.0, width=1.0)
win.tracer(10)

# Add resized images to the screen
for img in imgs:
    win.addshape(img)

pen = turtle.Turtle()
pen.pu()
pen.ht()

pen1 = turtle.Turtle()
pen1.pu()
pen1.ht()
current_hand = pd.DataFrame(data = {}, columns = df.columns)
def flow_chart(r):
   
    global current_hand, game
    global df

    r.suits = list(r.cards["Suit"])
    if len(current_hand) == 0:
        if len(r.cards[r.cards['Points'] == 3]) > 0:
            card_to_play = r.cards[r.cards['Points'] == 3].sample(n = 1, random_state = None)['Name'].iloc[0]
            if r == robot_1:
                        pen1.goto(-97.5,0)
                        pen1.shape(df[df["Name"] == card_to_play]["Image"])
            elif r == robot_2:
                        pen1.goto(97.5,0)
                        pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                        pen1.stamp()
            elif r == robot_3:
                        pen1.goto(0,92.5)
                        pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                        pen1.stamp()
            play_card(card_to_play, r)
        else: 
            card_to_play = r.cards[r.cards['Points'] == r.cards['Points'].min()].sample(n = 1, random_state = None)['Name'].iloc[0]
            if r == robot_1:
                                pen1.goto(-97.5,0)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
            elif r == robot_2:
                                pen1.goto(97.5,0)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
            elif r == robot_3:
                                pen1.goto(0,92.5)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
            play_card(card_to_play,r)
    else: 
        current_suit = current_hand.iloc[0]['Suit']
        
        if current_suit in r.suits:
            how_many = r.suits.count(current_suit)

            if how_many == 1:
                card_to_play = r.cards[r.cards['Suit'] == current_suit]['Name']
                card_to_play = card_to_play.iloc[0]
                if r == robot_1:
                            pen1.goto(-97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_2:
                            pen1.goto(97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_3:
                            pen1.goto(0,92.5)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                play_card(card_to_play, r)

            if how_many > 1:

                if game.digged and game.color in list(current_hand['Suit']):
                    find_in = current_hand[current_hand['Suit'] == game.color]
                    winner_index = find_in[find_in['Points'] == find_in['Points'].max()].index
                elif not game.color in list(current_hand['Suit']) or not game.digged:
                    c_s = current_hand['Suit'].iloc[0]
                    find_in = current_hand[current_hand['Suit'] == c_s]
                    winner_index = find_in[find_in['Points'] == find_in['Points'].max()].index
                    
                if len(r.cards[(r.cards['Suit'] == current_suit) & (r.cards['Points'] == 3)]) == 0:    
                    #CHECK WHO IS WINNING
                    if winner_index == len(current_hand) - 1 or winner_index == len(current_hand) - 3:
                        cs = r.cards[r.cards['Suit'] == current_suit]
                        card_to_play = cs[cs['Points'] == cs['Points'].min()].sample(n = 1)['Name']
                        card_to_play = card_to_play.iloc[0]
                        if r == robot_1:
                                    pen1.goto(-97.5,0)
                                    pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                    pen1.stamp()
                        elif r == robot_2:
                                    pen1.goto(97.5,0)
                                    pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                    pen1.stamp()
                        elif r == robot_3:
                                    pen1.goto(0,92.5)
                                    pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                    pen1.stamp()
                                    
                        play_card(card_to_play, r)
                    elif winner_index == len(current_hand) - 2:
                        cs = r.cards[r.cards['Suit'] == current_suit]
                        card_to_play = cs[cs['Points'] == cs['Points'].max()].sample(n = 1)['Name']
                        card_to_play = card_to_play.iloc[0]
                    if r == robot_1:
                                pen1.goto(-97.5,0)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
                    elif r == robot_2:
                                pen1.goto(97.5,0)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()

                    elif r == robot_3:
                                pen1.goto(0,92.5)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()                      
                    play_card(card_to_play, r)
                        

                else:
                    card_to_play = r.cards[(r.cards['Suit'] == current_suit) & (r.cards['Points'] == 3)]['Name']
                    card_to_play = card_to_play.iloc[0]
                    if r == robot_1:
                                pen1.goto(-97.5,0)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
                    elif r == robot_2:
                                pen1.goto(97.5,0)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
                    elif r == robot_3:
                                pen1.goto(0,92.5)
                                pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                                pen1.stamp()
                    play_card(card_to_play, r)

        if not game.digged and current_suit not in r.suits:
            print(f'{r.name} has revealed the trump card. It is {game.color}')
            if len(r.cards[(r.cards['Suit'] == game.color)]) > 0:
                cs = r.cards[r.cards['Suit'] == game.color]
                card_to_play = cs[cs['Points'] == cs['Points'].min()].sample(n = 1)['Name']
                card_to_play = card_to_play.iloc[0]
                if r == robot_1:
                            pen1.goto(-97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_2:
                            pen1.goto(97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_3:
                            pen1.goto(0,92.5)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                play_card(card_to_play, r)
            else: 
                card_to_play = r.cards[r.cards['Points'] == r.cards['Points'].min()].sample(n = 1, random_state = None)['Name'].iloc[0]
                if r == robot_1:
                            pen1.goto(-97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_2:
                            pen1.goto(97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_3:
                            pen1.goto(0,92.5)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                play_card(card_to_play, r)
            game.digged = True
        elif game.digged and current_suit not in r.suits:
            if len(r.cards[(r.cards['Suit'] == game.color)]) > 0:
                cs = r.cards[r.cards['Suit'] == game.color]
                card_to_play = cs[cs['Points'] == cs['Points'].min()].sample(n = 1)['Name']
                card_to_play = card_to_play.iloc[0]
                if r == robot_1:
                            pen1.goto(-97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_2:
                            pen1.goto(97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_3:
                            pen1.goto(0,92.5)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()    
                play_card(card_to_play, r)
            else: 
                card_to_play = r.cards[r.cards['Points'] == r.cards['Points'].min()].sample(n = 1, random_state = None)['Name'].iloc[0]
                if r == robot_1:
                            pen1.goto(-97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_2:
                            pen1.goto(97.5,0)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                elif r == robot_3:
                            pen1.goto(0,92.5)
                            pen1.shape(df[df["Name"] == card_to_play]["Image"].iloc[0])
                            pen1.stamp()
                play_card(card_to_play, r)
   
    

def play_game():
    import warnings

    warnings.filterwarnings(
        "ignore",
        category=FutureWarning, 
        message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated"
    )

 
    #DO THE GLOBALS
    global player, robot_1, robot_2, robot_3, game, current_hand, last_hand, winner_index, r1_bid,r2_bid,r3_bid,player_bid, max_bid,card
    #print(player.cards)
    #PLAYE ALL THE 8 HANDS
    for i in range(0, 8):
        current_hand = pd.DataFrame(data = {}, columns = df.columns)
       
       
        if player.last_hand_won: 


            
            
            play_card(card, player)
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
            index_selctor = {"player":0,"robot_1":1,"robot_2":2,"robot_3":3}
            print("player")
        elif robot_1.last_hand_won: 
            
            flow_chart(robot_1)
  
            flow_chart(robot_2)
            flow_chart(robot_3)
            print() 
          

            
            
            play_card(card, player)
            index_selctor = {"robot_1":0,"robot_2":1,"robot_3":2,"player":3}
            print("r1")
        elif robot_2.last_hand_won:
          
            flow_chart(robot_2)

            flow_chart(robot_3)
            
         
          
            play_card(card, player)
            flow_chart(robot_1)
            index_selctor = {"robot_2":0,"robot_3":1,"player":2,"robot_1":3}
            
            print("r2")
        elif robot_3.last_hand_won:
            
            flow_chart(robot_3) 
            play_card(card, player)
            flow_chart(robot_1)
            flow_chart(robot_2)
            index_selctor = {"robot_3":0,"player":1,"robot_1":2,"robot_2":3}
            print("r3")
        elif not robot_1.last_hand_won and not robot_2.last_hand_won and not robot_3.last_hand_won and not player.last_hand_won : 
           
            play_card(card, player)
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
            index_selctor = {"player":0,"robot_1":1,"robot_2":2,"robot_3":3}
            print("None")
        if game.digged and game.color in list(current_hand['Suit']):
            find_in = current_hand[current_hand['Suit'] == game.color]
            winner_index = find_in[find_in['Points'] == find_in['Points'].max()].index
        elif not game.color in list(current_hand['Suit']) or not game.digged:
            c_s = current_hand['Suit'].iloc[0]
            find_in = current_hand[current_hand['Suit'] == c_s]
            winner_index = find_in[find_in['Points'] == find_in['Points'].max()].index
        if winner_index == index_selctor["player"]: 
                for c in list(current_hand["Name"]): 
                    player.hands_won.append(c)
                player.last_hand_won = True
                robot_1.last_hand_won = False
                robot_2.last_hand_won = False
                robot_3.last_hand_won = False
                current_hand = pd.DataFrame(data = {}, columns = df.columns)
        elif winner_index == index_selctor["robot_1"]: 
                for c in  list(current_hand["Name"]):
                    robot_1.hands_won.append(c)
                player.last_hand_won = False
                robot_1.last_hand_won = True
                robot_2.last_hand_won = False
                robot_3.last_hand_won = False
                current_hand = pd.DataFrame(data = {}, columns = df.columns)
        elif winner_index == index_selctor["robot_2"]: 
                for c in list(current_hand["Name"]):
                    robot_2.hands_won.append(c)
                player.last_hand_won = False
                robot_1.last_hand_won = False
                robot_2.last_hand_won = True
                robot_3.last_hand_won = False
                current_hand = pd.DataFrame(data = {}, columns = df.columns)
        elif winner_index == index_selctor["robot_3"]: 
                for c in list(current_hand["Name"]): 
                    robot_3.hands_won.append(c)
                player.last_hand_won = False
                robot_1.last_hand_won = False
                robot_2.last_hand_won = False
                robot_3.last_hand_won = True
                current_hand = pd.DataFrame(data = {}, columns = df.columns)
        
        
        
        last_hand =  pd.DataFrame(data = {}, columns = df.columns)
        last_hand = current_hand
        current_hand = pd.DataFrame(data = {}, columns = df.columns)
    

    import math as mt

    sprites = [player,robot_1,robot_2,robot_3]
    for sprite in sprites:
        sprite.points_made = 0
    # Calculate points for each sprite
    for sprite in sprites:
        for s_c in sprite.hands_won:
            points = df[df["Name"] == s_c]["Points"] 
            sprite.points_made += points.iloc[0]  # Extract the first value
        if sprite.last_hand_won:
            sprite.points_made += 1

        round(sprite.points_made)

    # Calculate team points
    team_1_points = player.points_made + robot_2.points_made
    team_2_points =robot_1.points_made + robot_3.points_made

    # Determine the winning team
    bids = {
        player_bid: team_1_points,
        r1_bid: team_2_points,
        r2_bid: team_1_points,
        r3_bid: team_2_points,
    }

    if max_bid in bids:
        if bids[max_bid] >= max_bid:
            print(f"Team_{1 if max_bid in [player_bid, r2_bid] else 2} wins!")
        else:
            print(f"Team_{1 if max_bid in [player_bid, r2_bid] else 2} loses!")






import turtle

player_cards = []
for i in range(8):
    player_cards.append(player.cards.iloc[i]["Image"])

print(player_cards)

# Create the screen object
win = turtle.Screen()

# Set the background color
win.bgcolor("green")
win.setup(height=1.0, width=1.0)
win.tracer(10)

# Add resized images to the screen
for img in imgs:
    win.addshape(img)

pen = turtle.Turtle()
pen.pu()
pen.ht()

pen.color("green")
pen.goto(-50, 250)
pen.color("black")
pen.write("29", align="center", font=("Times New Roman", 40, "bold"))

game_description = '''The newly developed game of "29" is a fast-paced card game that combines strategy, skill, and teamwork. It is typically played by four players, divided into two teams,
using a standard deck of 52 cards. The objective is to be the first team to reach a total of 29 points. Points are scored based on the cards played, with certain cards
having higher values than others. In "29", players bid to determine the trump suit, which gives certain cards special power during gameplay. The highest bidder leads the play,
and players must work with their partners to outsmart the opposing team by playing their cards strategically. The game is a race to score 29 points, making it thrilling and full of
tactical decisions. A blend of communication, clever card combinations, and careful bidding makes "29" an exciting game, perfect for those who enjoy a mix of strategy
and competitive fun.'''

pen.goto(-550, 100)
pen.write(game_description, align="left", font=("Times New Roman", 16, "italic"))

pen.goto(0, -200)
pen.write("Press P to Play ", align="center", font=("Agency FB", 50, "italic"))
pc = list(player.cards["Name"])

def press_p():
    global pen ,cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8, crs,win,pc
    win.tracer(100)
    cr1 = False
    cr2 = False
    cr3 = False
    cr4 = False
    cr5 = False
    cr6 = False
    cr7 = False
    cr8 = False
    
    crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
    
    print(player_cards)
    
    def re_arrange_cards():
        global crs,pc
        pen.clear()
        pen.goto(-560, 0)
        pen.write("Robot - 1 ", font=("Agency FB", 20, "italic"))
        pen.goto(540, 0)
        pen.write("Robot - 3 ", font=("Agency FB", 20, "italic"))
        pen.goto(0, 300)
        pen.write("Robot - 2 ", font=("Agency FB", 20, "italic"))
        pen.goto(0, -300)
        pen.write("Player ", font=("Agency FB", 20, "italic"))
        pen.goto(450,0)
        pen.shape("resized_face_down.gif")
        pen.stamp()
        pen.goto(-400,0)
        pen.shape("resized_face_down.gif")
        pen.stamp()
        pen.goto(0,205)
        pen.shape("resized_face_down.gif")
        pen.stamp()
        for i in range (0, 8):
            if not crs[i]:
                pen.shape(player_cards[i])  # Example of resized image
                
                pen.goto(-350+100*i,-205)
                pen.stamp()
        
    re_arrange_cards()
            
   
    win.listen()
    def get_card(x,y):
        global cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8,crs,pc
        
    
    
        
        if x > -387.5 and x < -312.5 and y > -265 and y < -145 and not cr1:
            print("Card 1 clicked")
            play_card(pc[0],player)
        
            cr1 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[0]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
          
    
        elif x > -287.5 and x < -212.5 and y > -265 and y < -145 and not cr2:
            print('Card 2 clicked')
            play_card(pc[1],player)
            
            pen.ht()
            cr2 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[1]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
        elif x > -187.5  and x < -112.5 and y > -265 and y < -145 and not cr3:
            print('Card 3 clicked')
            play_card(pc[2],player)
        
            cr3 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[2]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
        elif x > -87.5 and x < -12.5 and y > -265 and y < -145 and not cr4:
            print('Card 4 clicked')
            play_card(pc[3],player)
            
            cr4 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[3]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
        elif x > 12.5 and x < 87.5 and y > -265 and y < -145 and not cr5:
            print('Card 5 clicked')
            play_card(pc[4],player)
           
            cr5 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[4]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
        elif x > 112.5 and x < 187.5 and y > -265 and y < -145 and not cr6:
            print('Card 6 clicked')
            play_card(pc[5],player)
          
            cr6 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[5]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
        elif x > 212.5 and x < 287.5 and y > -265 and y < -145 and not cr7:
            print('Card 7 clicked')
            play_card(pc[6],player)
           
            cr7 = True
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()
            pen.shape(player_cards[6]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
        elif x > 312.5 and x < 387.5 and y > -265 and y < -145 and not cr8:
            print('Card 8 clicked')   
            play_card(pc[7],player)
           
            cr8 = True   
            crs = [cr1,cr2,cr3,cr4,cr5,cr6,cr7,cr8]
            re_arrange_cards()  
            pen.shape(player_cards[7]) 
            pen.goto(0,-92.5)
            pen.st()
            
            pen.stamp()
            pen.ht()
            flow_chart(robot_1)
            flow_chart(robot_2)
            flow_chart(robot_3)
    win.onclick(get_card)

# Bind the press_p function to the "P" key
win.onkeypress(press_p, "p")
win.onkeypress(press_p, "P")
win.listen()
win.mainloop()


player.cards









