import tkinter as tk
from PIL import Image, ImageTk
import random

# Initialize scores
player_score = 0
computer_score = 0
round_count = 0

# Mapping choices to numbers
choices = {
    1: "Rock",
    2: "Paper",
    3: "Scissors",
    4: "Lizard",
    5: "Spock"
}

# Winning conditions
winning_conditions = {
    (3, 2), (2, 1), (1, 4), (4, 5), (5, 3),
    (3, 4), (4, 2), (2, 5), (5, 1), (1, 3)
}

######################################################################################################

def play(player_choice):
    global player_score, computer_score, round_count
    if round_count >= 7:
        return

    computer_choice = random.randint(1, 5)
    result = f"Player: {choices[player_choice]} vs Computer: {choices[computer_choice]}"

    if player_choice == computer_choice:
        result += "\nIt's a tie!"
    elif (player_choice, computer_choice) in winning_conditions:
        result += "\nPlayer 01 gets a point!"
        player_score += 1
    else:
        result += "\nPlayer 02 gets a point!"
        computer_score += 1

    result_text.set(result)
    player_score_text.set(f"Player 01 Score: {player_score}")
    computer_score_text.set(f"Player 02 Score: {computer_score}")

    round_count += 1
    if round_count >= 7:
        game_over()


######################################################################################################

def game_over():
    if player_score > computer_score:
        result_text.set(result_text.get() + "\nPlayer 01 wins the game!")
    elif player_score < computer_score:
        result_text.set(result_text.get() + "\nPlayer 02 wins the game!")
    else:
        result_text.set(result_text.get() + "\nIt's a tie!")

def show_frame(frame):
    frame.tkraise()


######################################################################################################
def start_game():
    global player_score, computer_score, round_count
    player_score = 0
    computer_score = 0
    round_count = 0
    result_text.set("")
    player_score_text.set(f"Player 01 Score: {player_score}")
    computer_score_text.set(f"Player 02 Score: {computer_score}")
    show_frame(game_frame)



######################################################################################################

# Create the main window
root = tk.Tk()
root.title("Rock Paper Scissors Lizard Spock")
root.geometry("700x900")
root.resizable(False, False)  # Disable resizing


# Create frames for different screens
home_frame = tk.Frame(root)
game_frame = tk.Frame(root)
guide_frame = tk.Frame(root)

for frame in (home_frame, game_frame, guide_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Load images
home_image = Image.open("Start.jpg").resize((700, 900))
home_photo = ImageTk.PhotoImage(home_image)

game_image = Image.open("Game.jpg").resize((700, 900))
game_photo = ImageTk.PhotoImage(game_image)

guide_image = Image.open("Help.jpg").resize((700, 900))
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

result_text = tk.StringVar()
player_score_text = tk.StringVar(value=f"Player 01 Score: {player_score}")
computer_score_text = tk.StringVar(value=f"Player 02 Score: {computer_score}")

result_display = game_canvas.create_text(game_photo.width()//2, 50, text="", fill="white", font=("Helvetica", 16), width=300)
player_score_display = game_canvas.create_text(100, 20, text=player_score_text.get(), fill="white", font=("Helvetica", 12))
computer_score_display = game_canvas.create_text(game_photo.width()-100, 20, text=computer_score_text.get(), fill="white", font=("Helvetica", 12))

def update_text():
    game_canvas.itemconfig(result_display, text=result_text.get())
    game_canvas.itemconfig(player_score_display, text=player_score_text.get())
    game_canvas.itemconfig(computer_score_display, text=computer_score_text.get())

result_text.trace_add("write", lambda *args: update_text())
player_score_text.trace_add("write", lambda *args: update_text())
computer_score_text.trace_add("write", lambda *args: update_text())

width = 110
height = 50
rock_image = Image.open("rock.png").resize((width, height))  # Adjust width and height as needed
rock_photo = ImageTk.PhotoImage(rock_image)

paper_image = Image.open("paper.png").resize((width, height))
paper_photo = ImageTk.PhotoImage(paper_image)

scissors_image = Image.open("scissors.png").resize((width, height))
scissors_photo = ImageTk.PhotoImage(scissors_image)

lizard_image = Image.open("lizard.png").resize((width, height))
lizard_photo = ImageTk.PhotoImage(lizard_image)

spock_image = Image.open("spock.png").resize((width, height))
spock_photo = ImageTk.PhotoImage(spock_image)

button_frame = tk.Frame(game_frame)
button_frame.place(relx=0.5, rely=0.75, anchor="center")

rock_button = tk.Button(button_frame, image=rock_photo, command=lambda: play(1), borderwidth=0, highlightthickness=0)
paper_button = tk.Button(button_frame, image=paper_photo, command=lambda: play(2), borderwidth=0, highlightthickness=0)
scissors_button = tk.Button(button_frame, image=scissors_photo, command=lambda: play(3), borderwidth=0, highlightthickness=0)
lizard_button = tk.Button(button_frame, image=lizard_photo, command=lambda: play(4), borderwidth=0, highlightthickness=0)
spock_button = tk.Button(button_frame, image=spock_photo, command=lambda: play(5), borderwidth=0, highlightthickness=0)

guide_button = tk.Button(home_frame, image=guide_photo, command=lambda: show_frame(guide_frame))

rock_button.pack(side=tk.LEFT, padx=0)
paper_button.pack(side=tk.LEFT, padx=0)
scissors_button.pack(side=tk.LEFT, padx=0)
lizard_button.pack(side=tk.LEFT, padx=0)
spock_button.pack(side=tk.LEFT, padx=0)

exit_button = tk.Button(game_frame, text="Exit", command=lambda: show_frame(home_frame))
exit_button.place(relx=0.9, rely=0.9, anchor="center")

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
