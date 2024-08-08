import time
import tkinter as tk
from PIL import Image, ImageTk
import random
from pyfirmata import Arduino, OUTPUT, util
import threading

# Arduino doc
board = Arduino("COM4")

IndicatorLED = board.digital[11]
Buzzer = board.digital[12]

ChoiceLED1 = board.digital[4]
ChoiceLED2 = board.digital[3]
ChoiceLED3 = board.digital[2]

PScoreLED1 = board.digital[7]
PScoreLED2 = board.digital[6]
PScoreLED3 = board.digital[5]

CScoreLED1 = board.digital[10]
CScoreLED2 = board.digital[9]
CScoreLED3 = board.digital[8]


IndicatorLED.mode = OUTPUT
Buzzer.mode = OUTPUT

ChoiceLED1.mode = OUTPUT
ChoiceLED2.mode = OUTPUT
ChoiceLED3.mode = OUTPUT

PScoreLED1.mode = OUTPUT
PScoreLED2.mode = OUTPUT
PScoreLED3.mode = OUTPUT

CScoreLED1.mode = OUTPUT
CScoreLED2.mode = OUTPUT
CScoreLED3.mode = OUTPUT


button1 = board.analog[0]
button2 = board.analog[1]
button3 = board.analog[2]
button4 = board.analog[3]
button5 = board.analog[4]
start_button = board.analog[5]


it = util.Iterator(board)  # Start iterator to receive input data
it.start()

button1.enable_reporting()  # enable reporting for the analog pin
button2.enable_reporting()
button3.enable_reporting()
button4.enable_reporting()
button5.enable_reporting()
start_button.enable_reporting()

##############################################################################################################


# Initialize scores
player_score = 0
computer_score = 0
round_count = 0
player_choice = 6
started = False
waiter = 0
print("WELCOME TO ROCK,PAPER,SCISSORS,LIZARD AND SPOCK GAME")

# Mapping choices to numbers
choices = {
    0: "3sec Penalty",
    1: "Rock",
    2: "Paper",
    3: "Scissors",
    4: "Lizard",
    5: "Spock",
    6: "Time up!"
}

# Winning conditions
winning_conditions = {
    (3, 2), (2, 1), (1, 4), (4, 5), (5, 3),
    (3, 4), (4, 2), (2, 5), (5, 1), (1, 3),
}

#######################################################################################################################


def show_scores(ledset, number):  # To show scores in binary
    if ledset == 1:
        leds = [ChoiceLED1, ChoiceLED2, ChoiceLED3]
    elif ledset == 2:
        leds = [PScoreLED1, PScoreLED2, PScoreLED3]
    elif ledset == 3:
        leds = [CScoreLED1, CScoreLED2, CScoreLED3]
    else:
        return

    binary_number = bin(number)[2:].zfill(3)  # convert number to 3-bit binary string
    for i in range(3):
        leds[i].write(int(binary_number[i]))  # set LED state based on binary digits


def external_timer(x):  # To run a timer without freezing UI
    time.sleep(x)


def monitor_buttons():
    global waiter
    while True:
        if start_button.read() > 0.5:
            if not started:
                lambda event: start_game()
                start_game()
                root.after(100, monitor_buttons())
            elif round_count != 0:
                print("Exiting Game...")
                game_over()
                lets_go_home()
                root.after(1500, root.destroy())

        if button1.read() > 0.5 and waiter == 0:
            set_player_choice(1)
        elif button2.read() > 0.5 and waiter == 0:
            set_player_choice(2)
        elif button3.read() > 0.5 and waiter == 0:
            set_player_choice(3)
        elif button4.read() > 0.5 and waiter == 0:
            set_player_choice(4)
        elif button5.read() > 0.5 and waiter == 0:
            set_player_choice(5)
        board.pass_time(0.05)  # Small delay to prevent excessive CPU usage


#################################################################################################################


def start_round(num):

    global waiter, round_count
    waiter = num
    def countdown(count):
        if count > 0:
            IndicatorLED.write(1)
            result_text.set(f"Time remaining: {count}")
            print (f"Time remaining: {count}")
            root.after(1000, countdown, count - 1)
        else:
            IndicatorLED.write(0)
            buzzoff(0.25)
            selected(player_choice)

    if num > 0:
        result_text.set(f"Next round in\n{num} seconds")
        root.after(1000, start_round, num - 1)
    else:
        show_scores(1, 0)
        IndicatorLED.write(1)
        countdown(3)


def buzzoff(x):
    Buzzer.write(1)
    external_timer(x)
    Buzzer.write(0)


def selected(choice):
    play(choice)


def play(player_choice):
    global player_score, computer_score, round_count
    if round_count >= 7:
        return

    computer_choice = random.randint(1, 5)
    if player_choice == 6:
        computer_choice = 0

    user_choice = f"{choices[player_choice]}"
    com_choice = f"{choices[computer_choice]}"

    print(f"\nYour choice: {choices[player_choice]} Vs. Computer choice: {choices[computer_choice]}")
    show_scores(1, computer_choice)

    if player_choice == computer_choice:
        result = "It's a tie!"
    elif (player_choice, computer_choice) in winning_conditions:
        result = "Player gets a point!"
        player_score += 1
    else:
        result = "Computer gets a point!"
        computer_score += 1

    result_text.set(result)
    print(result.replace('\n  ', ''))
    user_choice_text.set(user_choice)
    com_choice_text.set(com_choice)
    player_score_text.set(f"0{player_score}")
    show_scores(2, player_score)
    computer_score_text.set(f"0{computer_score}")
    show_scores(3, computer_score)
    round_count += 1
    round_text.set(f"0{round_count}")

    # Print scores after each round
    print(f"Score after round {round_count}: Player {player_score} - Computer {computer_score}\n")

    if round_count >= 7:
        Buzzer.write(0)
        game_over()
    else:
        print(f"Round {round_count+1}")
        set_player_choice(6)
        start_round(3)


def blinker(seconds):
    if seconds > 0:
        if seconds % 2 == 0:
            show_scores(1, 7)  # Turn on the LEDs
            Buzzer.write(1)
        else:
            show_scores(1, 0)  # Turn off the LEDs
            Buzzer.write(0)
        root.after(250, blinker, seconds - 1)
    else:
        show_scores(1, 0)  # Ensure LEDs are off at the end



def game_over():

    blinker(10)
    if player_score > computer_score:
        final_result_text.set("YOU WON!")
        print ("\nYOU WON!")
    elif player_score < computer_score:
        final_result_text.set("YOU LOSE!")
        print ("\nYOU LOSE!")
    else:
        final_result_text.set("IT'S A TIE!")
        print ("\nIT'S A TIE!")


def show_frame(frame):
    frame.tkraise()


def lets_go_home():
    show_scores(1, 0)
    show_scores(2, 0)
    show_scores(3, 0)
    show_frame(home_frame)

def startBuzzer(x):
    p = 100
    while True:
        buzzoff(0.25)
        external_timer(x/p)
        p=p*2
        if p >= 2048:
            break

def start_game():
    print("""Press Start button to begin.\nYou'll get 3 seconds to choose an option.
          if you fail to choose, computer will get 1 point. 3 second interval between rounds.
          Starting from left to right, the buttons mean,
          1: Spock
          2: Lizard
          3: Scissor
          4: Paper
          5: Rock
          """)
    startBuzzer(1)
    print("Game Starting...\n")
    global player_score, computer_score, round_count, player_choice, started
    player_score = 0
    computer_score = 0
    round_count = 0
    started = True
    print("Round 1")
    set_player_choice(6)
    user_choice_text.set("?")
    com_choice_text.set("?")
    result_text.set("Pick a Choice")
    round_text.set(f"0{round_count}")
    final_result_text.set("")
    player_score_text.set(f"0{player_score}")
    computer_score_text.set(f"0{computer_score}")
    show_frame(game_frame)
    start_round(0)

#######################################################################################################################

# Create the main window
root = tk.Tk()
root.title("Rock Paper Scissors Lizard Spock")
root.geometry("1365x768")  # Set to the new resolution
root.resizable(False, False)  # Disable resizing

# Create frames for different screens
home_frame = tk.Frame(root)
game_frame = tk.Frame(root)
guide_frame = tk.Frame(root)

for frame in (home_frame, game_frame, guide_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Load images
home_image = Image.open("Start.jpg").resize((1365, 768))
home_photo = ImageTk.PhotoImage(home_image)

game_image = Image.open("Game.jpg").resize((1365, 768))
game_photo = ImageTk.PhotoImage(game_image)

guide_image = Image.open("Help.jpg").resize((1365, 768))
guide_photo = ImageTk.PhotoImage(guide_image)

# Home Screen
home_canvas = tk.Canvas(home_frame, width=home_photo.width(), height=home_photo.height())
home_canvas.pack(fill="both", expand=True)
home_canvas.create_image(0, 0, anchor="nw", image=home_photo)


#######################################################################################################################

start_image = Image.open("start_button.png").resize((137, 43))
start_photo = ImageTk.PhotoImage(start_image)

guide_image2 = Image.open("guide_button.png").resize((137, 43))
guide_photo2 = ImageTk.PhotoImage(guide_image2)

exit_photo = Image.open("exit_button_home.png").resize((137, 43))
exit_photo = ImageTk.PhotoImage(exit_photo)

back_photo = Image.open("back.png").resize((137, 43))
back_photo = ImageTk.PhotoImage(back_photo)


def exitor():
    print("Exiting Game...")
    root.destroy()


# Start Button
start_canvas = tk.Canvas(home_frame, width=137, height=43, highlightthickness=0)
start_canvas.place(relx=0.685, rely=0.505, anchor="center")
start_canvas.create_image(0, 0, anchor="nw", image=start_photo)
start_canvas.bind("<Button-1>", lambda event: start_game())

# Guide Button
guide_canvas = tk.Canvas(home_frame, width=137, height=43, highlightthickness=0)
guide_canvas.place(relx=0.685, rely=0.57, anchor="center")
guide_canvas.create_image(0, 0, anchor="nw", image=guide_photo2)
guide_canvas.bind("<Button-1>", lambda event: show_frame(guide_frame))

# Exit Button on home screen
guide_canvas = tk.Canvas(home_frame, width=137, height=43, highlightthickness=0)
guide_canvas.place(relx=0.685, rely=0.635, anchor="center")
guide_canvas.create_image(0, 0, anchor="nw", image=exit_photo)
guide_canvas.bind("<Button-1>", lambda event: exitor())


# Game Screen
game_canvas = tk.Canvas(game_frame, width=game_photo.width(), height=game_photo.height())
game_canvas.pack(fill="both", expand=True)
game_canvas.create_image(0, 0, anchor="nw", image=game_photo)

#######################################################################################################################


user_choice_text = tk.StringVar()
com_choice_text = tk.StringVar()
result_text = tk.StringVar()
round_text = tk.StringVar(value=f"0{round_count}")
final_result_text = tk.StringVar()
player_score_text = tk.StringVar(value=f"0{player_score}")
computer_score_text = tk.StringVar(value=f"0{computer_score}")

user_choice_display = game_canvas.create_text(260, 338, text="", fill="white", font=("Poppins", 20, "bold"))
com_choice_display = game_canvas.create_text(1100, 338, text="", fill="white", font=("Poppins", 20, "bold"))
result_display = game_canvas.create_text(682, 310, text="", fill="white", font=("Poppins", 12), justify = 'center')
player_score_display = game_canvas.create_text(484, 575, text=player_score_text.get(), fill="#121b2a",
                                               font=("Poppins", 40, "bold"))
computer_score_display = game_canvas.create_text(877, 575, text=computer_score_text.get(), fill="#121b2a",
                                                 font=("Poppins", 40, "bold"))
round_display = game_canvas.create_text(683, 598, text=round_text.get(), fill="#121b2a", font=("Poppins", 37, "bold"))
final_result_display = game_canvas.create_text(682, 50, text="", fill="yellow", font=("Poppins", 25, "bold"), justify = 'center')


def update_text():
    game_canvas.itemconfig(user_choice_display, text=user_choice_text.get())
    game_canvas.itemconfig(com_choice_display, text=com_choice_text.get())
    game_canvas.itemconfig(result_display, text=result_text.get())
    game_canvas.itemconfig(round_display, text=round_text.get())
    game_canvas.itemconfig(player_score_display, text=player_score_text.get())
    game_canvas.itemconfig(computer_score_display, text=computer_score_text.get())
    game_canvas.itemconfig(final_result_display, text=final_result_text.get())


result_text.trace_add("write", lambda *args: update_text())
player_score_text.trace_add("write", lambda *args: update_text())
computer_score_text.trace_add("write", lambda *args: update_text())
final_result_text.trace_add("write", lambda *args: update_text())

#######################################################################################################################

# Load button images
width = 81
height = width
rock_image = Image.open("rock.png").resize((width, height))
rock_photo = ImageTk.PhotoImage(rock_image)

paper_image = Image.open("paper.png").resize((width, height))
paper_photo = ImageTk.PhotoImage(paper_image)

scissors_image = Image.open("scissors.png").resize((width, height))
scissors_photo = ImageTk.PhotoImage(scissors_image)

lizard_image = Image.open("lizard.png").resize((width, height))
lizard_photo = ImageTk.PhotoImage(lizard_image)

spock_image = Image.open("spock.png").resize((width, height))
spock_photo = ImageTk.PhotoImage(spock_image)


# Function to set player choice
def set_player_choice(choice):
    global player_choice
    if waiter==0:
        player_choice = choice


# Create and place choice buttons
rock_button_frame = tk.Frame(game_frame)
rock_button_frame.place(relx=0.5585, rely=0.52, anchor="center")
rock_button = tk.Button(rock_button_frame, image=rock_photo, command=lambda: set_player_choice(1), borderwidth=0,
                        highlightthickness=0)

paper_button_frame = tk.Frame(game_frame)
paper_button_frame.place(relx=0.592, rely=0.3283, anchor="center")
paper_button = tk.Button(paper_button_frame, image=paper_photo, command=lambda: set_player_choice(2), borderwidth=0,
                         highlightthickness=0)

scissors_button_frame = tk.Frame(game_frame)
scissors_button_frame.place(relx=0.4985, rely=0.2066, anchor="center")
scissors_button = tk.Button(scissors_button_frame, image=scissors_photo, command=lambda: set_player_choice(3),
                            borderwidth=0, highlightthickness=0)

lizard_button_frame = tk.Frame(game_frame)
lizard_button_frame.place(relx=0.43718, rely=0.5188, anchor="center")
lizard_button = tk.Button(lizard_button_frame, image=lizard_photo, command=lambda: set_player_choice(4), borderwidth=0,
                          highlightthickness=0)

spock_button_frame = tk.Frame(game_frame)
spock_button_frame.place(relx=0.40285, rely=0.3274, anchor="center")
spock_button = tk.Button(spock_button_frame, image=spock_photo, command=lambda: set_player_choice(5), borderwidth=0,
                         highlightthickness=0)

rock_button.pack(side=tk.LEFT)
paper_button.pack(side=tk.LEFT)
scissors_button.pack(side=tk.LEFT)
lizard_button.pack(side=tk.LEFT)
spock_button.pack(side=tk.LEFT)


#######################################################################################################################

# Exit button on game screen
exit_canvas = tk.Canvas(game_frame, width=137, height=42, highlightthickness=0)
exit_canvas.place(relx=0.498, rely=0.868, anchor="center")
background_image = Image.open("exit.jpg").resize((140, 42))
background_photo = ImageTk.PhotoImage(background_image)
exit_canvas.create_image(0, 0, anchor="nw", image=background_photo)
exit_canvas.bind("<Button-1>", lambda event: lets_go_home())


# Guide Screen
guide_canvas = tk.Canvas(guide_frame, width=guide_photo.width(), height=guide_photo.height())
guide_canvas.pack(fill="both", expand=True)
guide_canvas.create_image(0, 0, anchor="nw", image=guide_photo)

exit_canvas_guide = tk.Canvas(guide_frame, width=140, height=42, highlightthickness=0)
exit_canvas_guide.place(relx=0.715, rely=0.665, anchor="center")
background_image_guide = Image.open("back.png")
background_image_guide = background_image_guide.resize((140, 42))
background_photo_guide = ImageTk.PhotoImage(background_image_guide)
exit_canvas_guide.create_image(0, 0, anchor="nw", image=background_photo_guide)
exit_canvas_guide.bind("<Button-1>", lambda event: lets_go_home())


# Start the button monitoring thread
button_thread = threading.Thread(target=monitor_buttons, daemon=True)
button_thread.start()

time_thread = threading.Thread(target=external_timer(0), daemon=True)
time_thread.start()


# Start with home frame
lets_go_home()


# Run the application
root.mainloop()
