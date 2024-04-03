import tkinter as tk
import tkinter.messagebox

import mysql.connector
import time
import random
from datetime import date

from turtle import Screen
from snake import Snake
from food import Food
from score import Score

leaderboard_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash@130422",
    database="game_leaderboard"
)
cursor = leaderboard_db.cursor()

cur_player_name = ""
game_platform_key = 271828
result_key = {
    "Game Over!": 200,
    "New Personal Best!": 300,
    "Top 10 in Leaderboard!": 400
}


def init_db():

    for result_type in result_key:

        cursor.execute(f"""
        insert into rank_result_type
        values({result_key[result_type]}, '{result_type}')
        """)

    cursor.execute(f"""
    insert into game_platform
    values({game_platform_key}, '{'SnakeOS'}')
    """)


def gen_game_completion_key():
    cursor.execute("""
    select game_completion_key from game_completion_history
    """)
    existing_game_keys = cursor.fetchall()
    rnd_key = random.randint(1, 1000000)

    while existing_game_keys and rnd_key in existing_game_keys[0]:
        rnd_key = random.randint(1, 1000000)
    return rnd_key


def get_rank_result_type(score, p_key):

    cursor.execute(f"""
    select max(game_completion_score)
    from game_completion_history 
    where player_key = {p_key}
    """)
    max_score_data = cursor.fetchall()

    cursor.execute(f"""
    select game_completion_score
    from game_completion_history
    """)
    top_10_score_data = cursor.fetchmany(10)

    if max_score_data:
        best_score = max_score_data[0][0]

        if score > best_score:
            if top_10_score_data and score >= top_10_score_data[0][0]:
                return "Top 10 in Leaderboard!"
            else:
                return "New Personal Best!"
        else:
            return "Game Over!"

    return "New Personal Best!"


def game():
    screen = Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("black")
    screen.tracer(False)
    screen.title(f"{cur_player_name}")

    game_is_running = True

    snake = Snake()
    food = Food()
    score = Score()

    screen.listen()
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")

    while game_is_running:
        screen.update()
        time.sleep(0.135)

        snake.move()

        if snake.head.distance(food) < 15:
            food.new_location()
            score.update_score()
            snake.grow()

        if snake.did_hit_wall() or snake.did_collide_itself():
            game_is_running = False
            score.game_over()

    update_db(cur_player_name, score.score)

    screen.exitonclick()


def fetch_player_name():
    player_name = player_entry.get()

    if not player_name:
        tk.messagebox.showinfo(message="Player Name field is empty!")
    else:
        global cur_player_name

        cur_player_name = player_name

        close()
        game()
        show_leaderboard()


def get_player_name(key):
    cursor.execute(f"""
    select player_gamer_alias from player
    where player_key = {key} 
    """)
    name = cursor.fetchall()
    return str(name[0][0])


def show_leaderboard():
    board = tk.Tk()
    board.geometry("900x900")
    board.title("Leaderboard")

    e = tk.Label(board, width=10, text='Name', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=0)
    e = tk.Label(board, width=10, text='Platform', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=1)
    e = tk.Label(board, width=10, text='Snapshot', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=2)
    e = tk.Label(board, width=10, text='Date', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=3)
    e = tk.Label(board, width=10, text='Result', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=4)
    e = tk.Label(board, width=10, text='Level', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=5)
    e = tk.Label(board, width=10, text='Score', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=6)
    e = tk.Label(board, width=10, text='Misc.', borderwidth=2, relief='ridge', anchor='w', bg='yellow', fg='black')
    e.grid(row=0, column=7)

    cursor.execute("""
    select * from leaderboard_snapshot limit 0,10
    """)
    player_data = cursor.fetchall()

    r = 8
    for player in player_data:
        for c in range(len(player)):
            e = tk.Entry(board, width=10, fg='red')
            e.grid(row=r, column=c)
            if c == 0:
                player_name = get_player_name(player[c])
                e.insert(0, player_name)
            else:
                e.insert(0, player[c])
        r += 1

    board.mainloop()


def update_db(player_name, score):

    cursor.execute("""
    select count(player_key)
    from player
    """)
    cur_player_count = cursor.fetchall()
    cur_completion_key = gen_game_completion_key()
    cur_completion_date = str(date.today())

    cursor.execute(f"""
    select * from player
    where player_gamer_alias = '{player_name}'
    """)
    player_exists = cursor.fetchall()

    if not player_exists:

        new_player_count = cur_player_count[0][0] + 1

        cursor.execute(f"""
        insert into player
        values({new_player_count}, {new_player_count * 10}, '{player_name}')""")

        cursor.execute(f"""
        insert into game_completion_history
        values({cur_completion_key}, '{cur_completion_date}', {new_player_count}, {game_platform_key}, {1}, {score})
        """)
        result_type = get_rank_result_type(score, new_player_count)

        cursor.execute(f"""
        insert into leaderboard_snapshot
        values({new_player_count}, {game_platform_key}, '{cur_completion_date}', '{cur_completion_date}', 
        {result_key[result_type]}, {1}, 
        {score}, {1})
        """)
    else:
        cur_player_key = player_exists[0][0]

        cursor.execute(f"""
        insert into game_completion_history
        values({cur_completion_key}, '{cur_completion_date}', {cur_player_key}, {game_platform_key}, {1}, {score})
        """)

        result_type = get_rank_result_type(score, cur_player_key)

        cursor.execute(f"""
        insert into leaderboard_snapshot
        values({cur_player_key}, {game_platform_key}, '{cur_completion_date}', '{cur_completion_date}', 
        {result_key[result_type]}, {1}, 
        {score}, {1})
        """)

    leaderboard_db.commit()


def close():
    root.destroy()


# init_db()

root = tk.Tk()
root.geometry("500x300")
root.title("Welcome!")

player_name_label = tk.Label(root, text="Enter your Player Name: ", font=('Arial', 18))
player_name_label.pack(padx=20, pady=20)

player_entry = tk.Entry(root)
player_entry.pack()

start_game_button = tk.Button(root, text="Start Game!", font=('Arial', 18), command=lambda: [fetch_player_name()])
start_game_button.pack(padx=5, pady=5)

view_leaderboard_button = tk.Button(root, text="View Leaderboard", font=('Arial', 18),
                                    command=lambda: [show_leaderboard()])
view_leaderboard_button.pack(padx=5, pady=5)

root.mainloop()
