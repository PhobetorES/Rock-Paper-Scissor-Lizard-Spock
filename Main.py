import tkinter as tk
from PIL import Image, ImageTk
import random

# Initialize scores
player_score = 0
computer_score = 0
round_count = 0
player_choice = 6

# Mapping choices to numbers
choices = {
    1: "Rock",
    2: "Paper",
    3: "Scissors",
    4: "Lizard",
    5: "Spock",
    6: "Time up!",
    7: "3sec Penalty"
}

# Winning conditions
winning_conditions = {
    (3, 2), (2, 1), (1, 4), (4, 5), (5, 3),
    (3, 4), (4, 2), (2, 5), (5, 1), (1, 3),
}

def start_round():    # This function makes each round last 3 seconds
    def countdown(count):
        if count > 0:
            result_text.set(f"Time remaining: {count}")
            root.after(1000, countdown, count - 1)
        else:
            selected(player_choice)

    # Sound the buzzer
    # Turn on the light
    countdown(3)

def selected(choice):
    play(choice)

def play(player_choice):
    global player_score, computer_score, round_count
    if round_count >= 7:
        return

    computer_choice = random.randint(1, 5)
    if player_choice == 6:
        computer_choice = 7

    user_choice = f"{choices[player_choice]}"
    com_choice = f"{choices[computer_choice]}"

    if player_choice == computer_choice:
        result = "It's a tie!"
    elif (player_choice, computer_choice) in winning_conditions:
        result = "Player gets\n   a point!"
        player_score += 1
    else:
        result = " Computer gets\n      a point!"
        computer_score += 1

    result_text.set(result)
    user_choice_text.set(user_choice)
    com_choice_text.set(com_choice)
    player_score_text.set(f"0{player_score}")
    computer_score_text.set(f"0{computer_score}")
    round_count += 1
    round_text.set(f"0{round_count}")
    if round_count >= 7:
        game_over()
    else:
        start_round()

def game_over():
    if player_score > computer_score:
        final_result_text.set("You WON!")
    elif player_score < computer_score:
        final_result_text.set("Computer wins the game!")
    else:
        final_result_text.set("It's a tie!")

def show_frame(frame):
    frame.tkraise()

def start_game():
    global player_score, computer_score, round_count, player_choice
    player_score = 0
    computer_score = 0
    round_count = 0
    player_choice = 6
    user_choice_text.set("?")
    com_choice_text.set("?")
    result_text.set("Pick a Choice")
    round_text.set(f"0{round_count}")
    final_result_text.set("")
    player_score_text.set(f"0{player_score}")
    computer_score_text.set(f"0{computer_score}")
    show_frame(game_frame)

    start_round()

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

start_image = Image.open("start_button.png").resize((250, 85))
start_photo = ImageTk.PhotoImage(start_image)

guide_image2 = Image.open("guide_button.png").resize((200, 60))
guide_photo2 = ImageTk.PhotoImage(guide_image2)

start_button = tk.Button(home_frame, image=start_photo, command=start_game)
start_button.place(relx=0.5, rely=0.4, anchor="center")

guide_button = tk.Button(home_frame, text="Guide", command=lambda: show_frame(guide_frame))
guide_button.place(relx=0.5, rely=0.5, anchor="center")

# Game Screen
game_canvas = tk.Canvas(game_frame, width=game_photo.width(), height=game_photo.height())
game_canvas.pack(fill="both", expand=True)
game_canvas.create_image(0, 0, anchor="nw", image=game_photo)

user_choice_text = tk.StringVar()
com_choice_text = tk.StringVar()
result_text = tk.StringVar()
round_text = tk.StringVar(value=f"0{round_count}")
final_result_text = tk.StringVar()
player_score_text = tk.StringVar(value=f"0{player_score}")
computer_score_text = tk.StringVar(value=f"0{computer_score}")

user_choice_display = game_canvas.create_text(260, 378, text="", fill="white", font=("Poppins", 20, "bold"))
com_choice_display = game_canvas.create_text(1100, 378, text="", fill="white", font=("Poppins", 20, "bold"))
result_display = game_canvas.create_text(682, 340, text="", fill="white", font=("Helvetica", 16))
player_score_display = game_canvas.create_text(484, 600, text=player_score_text.get(), fill="#121b2a",
                                               font=("Poppins", 40, "bold"))
computer_score_display = game_canvas.create_text(877, 604, text=computer_score_text.get(), fill="#121b2a",
                                                 font=("Poppins", 40, "bold"))
round_display = game_canvas.create_text(683, 630, text=round_text.get(), fill="#121b2a", font=("Poppins", 37))
final_result_display = game_canvas.create_text(683, 75, text="", fill="yellow", font=("Poppins", 25, "bold"))

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

# Load button images
width = 110
height = 52
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
    player_choice = choice

# Create and place choice buttons
rock_button_frame = tk.Frame(game_frame)
rock_button_frame.place(relx=0.57, rely=0.55, anchor="center")
rock_button = tk.Button(rock_button_frame, image=rock_photo, command=lambda: set_player_choice(1), borderwidth=0,
                        highlightthickness=0)

paper_button_frame = tk.Frame(game_frame)
paper_button_frame.place(relx=0.6, rely=0.35, anchor="center")
paper_button = tk.Button(paper_button_frame, image=paper_photo, command=lambda: set_player_choice(2), borderwidth=0,
                         highlightthickness=0)

scissors_button_frame = tk.Frame(game_frame)
scissors_button_frame.place(relx=0.5, rely=0.22, anchor="center")
scissors_button = tk.Button(scissors_button_frame, image=scissors_photo, command=lambda: set_player_choice(3),
                            borderwidth=0, highlightthickness=0)

lizard_button_frame = tk.Frame(game_frame)
lizard_button_frame.place(relx=0.42, rely=0.55, anchor="center")
lizard_button = tk.Button(lizard_button_frame, image=lizard_photo, command=lambda: set_player_choice(4), borderwidth=0,
                          highlightthickness=0)

spock_button_frame = tk.Frame(game_frame)
spock_button_frame.place(relx=0.4, rely=0.35, anchor="center")
spock_button = tk.Button(spock_button_frame, image=spock_photo, command=lambda: set_player_choice(5), borderwidth=0,
                         highlightthickness=0)

rock_button.pack(side=tk.LEFT)
paper_button.pack(side=tk.LEFT)
scissors_button.pack(side=tk.LEFT)
lizard_button.pack(side=tk.LEFT)
spock_button.pack(side=tk.LEFT)

# Exit button on game screen
exit_canvas = tk.Canvas(game_frame, width=137, height=42, highlightthickness=0)
exit_canvas.place(relx=0.498, rely=0.909, anchor="center")
background_image = Image.open("exit.jpg")
background_image = background_image.resize((140, 42))  # Adjust the size as needed
background_photo = ImageTk.PhotoImage(background_image)
exit_canvas.create_image(0, 0, anchor="nw", image=background_photo)
exit_canvas.bind("<Button-1>", lambda event: show_frame(home_frame))

# Guide Screen
guide_canvas = tk.Canvas(guide_frame, width=guide_photo.width(), height=guide_photo.height())
guide_canvas.pack(fill="both", expand=True)
guide_canvas.create_image(0, 0, anchor="nw", image=guide_photo)

exit_button_guide = tk.Button(guide_frame, text="Exit", command=lambda: show_frame(home_frame))
exit_button_guide.place(relx=0.9, rely=0.9, anchor="center")

# Start with home frame
show_frame(home_frame)

# Run the application
root.mainloop()
