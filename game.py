from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import random
import time

root = tk.Tk()
root.title("Hearths")
root.geometry("800x600")

values = ['A', 'Q', 'K', 'J', '2', '3', '4', '5', '6', '7', '8', '9', '10']
suits = ['♠','♥','♦', '♣']

me = 100
bot = 100
my_button = None
play_button = None
fold_button = None


card_frame = tk.Frame(root)
card_frame.pack()


def generate_card_image(value, suit):
    card = Image.new('RGB', (100, 150), color='white')
    draw = ImageDraw.Draw(card)
    draw.rectangle([0, 0, 99, 149], outline='black', width=2)

    # Load font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    color = 'black' if suit in ['♠', '♣'] else 'red'
    draw.text((10, 10), value, font=font, fill=color)
    draw.text((10, 40), suit, font=font, fill=color)

    return card


def draw_suit():
    suit = random.choice(suits)
    return suit


def draw_value():
    value = random.choice(values)
    return value

def rev_bool(b):
    if b == True:
        b = False
    else:
        b = True

my_turn = True


cards_in_game = []
cards_of_the_opponent = []
my_cards = []

def points(list_of_two_cards):
    s = 0
    converts = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    if list_of_two_cards[0][1] == list_of_two_cards[1][1]:
        for i in list_of_two_cards:
            if i[0] == 'J' or i[0] == 'Q' or i[0] == 'K':
                s = s + 10
            elif i[0] in converts:
                s = s + int(i[0])
            else:
                s = s + 11
    else: 
        for i in list_of_two_cards:
            if i[0] == 'J' or i[0] == 'Q' or i[0] == 'K':
                if s < 10:
                    s = 10
            elif i[0] in converts:
                if s < int(i[0]):
                    s = int(i[0])
            else:
                if s < 11:
                    s = 11

    
    return s


def draw_for_opponent():
    global play_button, fold_button

    one_value_op = draw_value()
    one_suit_op = draw_suit()
    two_value_op = draw_value()
    two_suit_op = draw_suit()
    #debug print
    print(f"draw_for_opponent 1st call: {one_value_op}{one_suit_op} {two_value_op}{two_suit_op}")
    if one_value_op == two_value_op and one_suit_op == two_suit_op:
        draw_for_opponent()
    else:
        onebuf = [one_value_op, one_suit_op]
        twobuf = [two_value_op, two_suit_op]
        
        two = ''.join(twobuf)
        one = ''.join(onebuf)
        cards_for_if = [one, two]
        print(f'd_f_o 2nd call: {cards_for_if}')        
        c = 0

        for i in cards_for_if:
            if i in cards_in_game:
                c = c + 1
                draw_for_opponent()
        if c == 0:
            cards_in_game.append(one)
            cards_of_the_opponent.append(one)
            cards_in_game.append(two)
            cards_of_the_opponent.append(two)
            
            ##Tuk beshe original_button.destroy()
            
            play_button = tk.Button(root, text="Bet", command=doyouplay)
            play_button.pack()

            fold_button = tk.Button(root, text="Fold", command=start_game)
            fold_button.pack()
        

def doyouplay():
    global bot, me
    global my_button, play_button, fold_button

    play_button.destroy()
    fold_button.destroy()
    if cards_of_the_opponent[1][0:2] == '10' and cards_of_the_opponent[0][0:2] == '10':
        one_value_op = cards_of_the_opponent[0][0:2]
        one_suit_op = cards_of_the_opponent[0][2]

        two_value_op = cards_of_the_opponent[1][0:2]
        two_suit_op = cards_of_the_opponent[1][2]


    elif cards_of_the_opponent[0][0:2] == '10':
        one_value_op = cards_of_the_opponent[0][0:2]
        one_suit_op = cards_of_the_opponent[0][2]

        two_value_op = cards_of_the_opponent[1][0]
        two_suit_op = cards_of_the_opponent[1][1]

    elif cards_of_the_opponent[1][0:2] == '10':
        one_value_op = cards_of_the_opponent[0][0]
        one_suit_op = cards_of_the_opponent[0][1]

        two_value_op = cards_of_the_opponent[1][0:2]
        two_suit_op = cards_of_the_opponent[1][2]

    else:
        one_value_op = cards_of_the_opponent[0][0]
        one_suit_op = cards_of_the_opponent[0][1]

        two_value_op = cards_of_the_opponent[1][0]
        two_suit_op = cards_of_the_opponent[1][1]


    card1 = generate_card_image(one_value_op, one_suit_op)

    card2 = generate_card_image(two_value_op, two_suit_op)

    tk_card1 = ImageTk.PhotoImage(card1)
    tk_card2 = ImageTk.PhotoImage(card2)

    label1 = tk.Label(card_frame, image=tk_card1)
    label1.image = tk_card1
    label2 = tk.Label(card_frame, image=tk_card2)
    label2.image = tk_card2

    label1.pack(side=tk.LEFT, padx=10, pady=10)
    label2.pack(side=tk.LEFT, padx=10, pady=10)
    
    my_points = points(my_cards)
    enemy_points = points(cards_of_the_opponent)
    #time.sleep(5)
    if my_points > enemy_points:
        me = me + 10
        bot = bot - 10
    elif my_points < enemy_points:
        bot = bot + 10
        me = me - 10
    
    start_game()


def draw():
    #Трябва да добавя текст който да изписва баланса
    my_button.destroy()
    # Clear previous cards
    for widget in card_frame.winfo_children():
        widget.destroy()
    
    one_value = draw_value()
    one_suit = draw_suit()
    two_value = draw_value()
    two_suit = draw_suit()
    if one_value == two_value and one_suit == two_suit:
        draw()
    else:
        onebuf = [one_value, one_suit]
        twobuf = [two_value, two_suit]

        one = ''.join(onebuf)
        cards_in_game.append(one)
        my_cards.append(one)        

        two = ''.join(twobuf)
        cards_in_game.append(two)
        my_cards.append(two)

        card3 = generate_card_image(one_value, one_suit)

        card4 = generate_card_image(two_value, two_suit)

        tk_card1 = ImageTk.PhotoImage(card3)
        tk_card2 = ImageTk.PhotoImage(card4)

        label1 = tk.Label(card_frame, image=tk_card1)
        label1.image = tk_card1
        label2 = tk.Label(card_frame, image=tk_card2)
        label2.image = tk_card2

        label1.pack(side=tk.LEFT, padx=10, pady=10)
        label2.pack(side=tk.LEFT, padx=10, pady=10)

        draw_for_opponent()
        

def start_game():
    global bot, me
    global my_button, fold_button, top_frame
    
    try:
        fold_button.destroy()
        play_button.destroy()
    except Exception as e:
        print("An error occurred:", e)

    try:
        top_frame.destroy()
    except Exception as e:
        print("Ab error occured:", e)

    if bot == 0:
        label_text = tk.StringVar()
        label_text.set("You won!")
        label = tk.Label(root, textvariable=label_text)
        label.pack(padx=20, pady=20)
        
        time.sleep(5)
        label.destroy()

        me = 100
        bot = 100
        

    elif me == 0:
        label_text = tk.StringVar()
        label_text.set("You lost!")
        label = tk.Label(root, textvariable=label_text)
        label.pack(padx=20, pady=20)

        time.sleep(5)
        label.destroy()

        me = 100
        bot = 100
    

    top_frame = tk.Frame(root)
    top_frame.pack(fill='x')

    mestr = f'You {str(me)}'
    botstr = f'Bot {str(bot)}'
    left_label = tk.Label(top_frame, text=mestr, bg="lightblue")
    left_label.pack(side='left')

    right_label = tk.Label(top_frame, text=botstr, bg="lightgreen")
    right_label.pack(side='right')


    cards_in_game.clear()
    cards_of_the_opponent.clear()
    my_cards.clear()

    my_button = tk.Button(root, text="Start", command=draw)
    my_button.pack(padx=20, pady=20)


start_game()
root.mainloop()

