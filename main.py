import tkinter as tk
import random
import time


# ================== Окно ==================
root = tk.Tk()
root.title("Фруктовый переполох")

WIDTH = 500
HEIGHT = 500

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()


# ================== Фон ==================
# Если картинки img/tree.png нет — закомментируй 2 строки ниже
# и раскомментируй строку с зелёным фоном.
bg_image = tk.PhotoImage(file="img/tree.png")
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#a8e6a1", outline="")


# ================== Уровень 4: таймер вместо жизней ==================
GAME_TIME = 30
start_time = time.time()
time_left = GAME_TIME

score = 0
game_active = True

score_text = canvas.create_text(
    70, 20,
    text="Счёт: 0",
    font=("Arial", 14, "bold"),
    fill="black"
)

timer_text = canvas.create_text(
    WIDTH - 80, 20,
    text=f"⏱ {time_left}",
    font=("Arial", 14, "bold"),
    fill="darkred"
)


# ================== Корзинка ==================
basket_x = WIDTH // 2
basket_y = HEIGHT - 50

basket = canvas.create_text(
    basket_x, basket_y,
    text="🧺",
    font=("Arial", 40),
    fill="brown"
)


# ================== Падающие предметы ==================
objects = []

BASE_FALL_STEP = 6
BASE_DELAY = 60


# ================== Уровень 3: ускорение по счёту ==================
def get_fall_step():
    """Чем больше очков — тем больше пикселей за кадр."""
    return BASE_FALL_STEP + score // 5


def get_frame_delay():
    """Чем больше очков — тем меньше пауза между кадрами (мин. 20 мс)."""
    delay = BASE_DELAY - score * 2
    return max(20, delay)


# ================== Создание предметов ==================
def create_object():
    if not game_active:
        return

    x = random.randint(30, WIDTH - 30)
    y = 50

    r = random.randint(1, 10)

    if r == 1:
        # 💣 бомба: −2 очка
        item = canvas.create_text(x, y, text="💣", font=("Arial", 28))
        object_type = "bomb"
    elif r <= 3:
        # 🥫 банка: −1 очко
        item = canvas.create_text(x, y, text="🥫", font=("Arial", 28))
        object_type = "trash"
    elif r <= 6:
        # 🍐 груша: +2 очка
        item = canvas.create_text(x, y, text="🍐", font=("Arial", 28))
        object_type = "pear"
    else:
        # 🍎 яблоко: +1 очко
        item = canvas.create_text(x, y, text="🍎", font=("Arial", 28))
        object_type = "apple"

    objects.append([item, x, y, object_type])

    # Чем больше очков — тем чаще появляются предметы
    spawn_delay = max(400, 1000 - score * 20)
    root.after(spawn_delay, create_object)


# ================== Управление корзинкой ==================
def move_left(_):
    global basket_x
    if game_active and basket_x > 30:
        basket_x -= 25
        canvas.move(basket, -25, 0)


def move_right(_):
    global basket_x
    if game_active and basket_x < WIDTH - 30:
        basket_x += 25
        canvas.move(basket, 25, 0)


# ================== Очки ==================
def apply_score(delta):
    global score
    score += delta
    if score < 0:
        score = 0
    canvas.itemconfig(score_text, text=f"Счёт: {score}")


# ================== Игровой цикл ==================
def update_game():
    global game_active, time_left

    if not game_active:
        return

    # ---- Таймер ----
    elapsed = time.time() - start_time
    time_left = max(0, int(GAME_TIME - elapsed))

    color = "red" if time_left <= 5 else "darkred"
    canvas.itemconfig(timer_text, text=f"⏱ {time_left}", fill=color)

    if time_left <= 0:
        game_active = False
        end_game()
        return

    step = get_fall_step()

    for obj in objects[:]:
        item, x, y, object_type = obj

        y += step
        obj[2] = y
        canvas.move(item, 0, step)

        # ---- Попадание в корзину ----
        if basket_y - 30 <= y <= basket_y + 20 and abs(x - basket_x) < 45:
            if object_type == "apple":
                apply_score(+1)
            elif object_type == "pear":
                apply_score(+2)
            elif object_type == "trash":
                apply_score(-1)
            elif object_type == "bomb":
                apply_score(-2)

            canvas.delete(item)
            objects.remove(obj)
            continue

        # ---- Упало мимо ----
        if y > HEIGHT:
            canvas.delete(item)
            objects.remove(obj)

    if game_active:
        root.after(get_frame_delay(), update_game)


# ================== Конец игры ==================
def end_game():
    canvas.delete("all")

    canvas.create_text(
        WIDTH // 2, HEIGHT // 2 - 40,
        text="⏰ Время вышло!",
        font=("Arial", 26, "bold"),
        fill="darkred"
    )

    canvas.create_text(
        WIDTH // 2, HEIGHT // 2 + 10,
        text=f"Ты набрал {score} очков",
        font=("Arial", 18, "bold")
    )

    canvas.create_text(
        WIDTH // 2, HEIGHT // 2 + 50,
        text="Обнови окно, чтобы сыграть снова",
        font=("Arial", 12),
        fill="gray"
    )


# ================== Управление ==================
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)


# ================== Запуск ==================
root.focus_force()
create_object()
update_game()

root.mainloop()