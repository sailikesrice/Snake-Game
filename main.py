import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=500, height=500, bg="black")
        self.canvas.pack()

        self.score = 0
        self.game_over = False

        # Snake and food properties
        self.snake = [(240, 240), (230, 240), (220, 240)]  # Snake body parts (x, y)
        self.snake_dir = "Right"  # Initial direction
        self.food = self.create_food()

        # Draw the initial snake and food
        self.draw_snake()
        self.food_item = self.canvas.create_rectangle(
            self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red"
        )

        # Bind keys for snake movement
        self.root.bind("<Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<Right>", lambda e: self.change_direction("Right"))

        # Start the game loop
        self.move_snake()

    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + 10, y + 10, fill="green", tag="snake"
            )

    def create_food(self):
        """Generate food at a random location."""
        while True:
            x = random.randint(0, 49) * 10
            y = random.randint(0, 49) * 10
            if (x, y) not in self.snake:  # Ensure food doesn't overlap with the snake
                return x, y

    def move_snake(self):
        """Move the snake in the current direction."""
        if self.game_over:
            return

        head_x, head_y = self.snake[0]

        # Determine new head position
        if self.snake_dir == "Up":
            head_y -= 10
        elif self.snake_dir == "Down":
            head_y += 10
        elif self.snake_dir == "Left":
            head_x -= 10
        elif self.snake_dir == "Right":
            head_x += 10

        new_head = (head_x, head_y)

        # Check for collisions
        if (
            head_x < 0
            or head_y < 0
            or head_x >= 500
            or head_y >= 500
            or new_head in self.snake
        ):
            self.game_over = True
            self.canvas.create_text(
                250,
                250,
                text=f"Game Over!\nScore: {self.score}",
                fill="white",
                font=("Arial", 24),
            )
            return

        # Add new head to the snake
        self.snake.insert(0, new_head)

        # Check if snake eats the food
        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
            self.canvas.coords(
                self.food_item,
                self.food[0],
                self.food[1],
                self.food[0] + 10,
                self.food[1] + 10,
            )
        else:
            # Remove the tail if no food eaten
            self.snake.pop()

        # Redraw the snake
        self.draw_snake()

        # Continue the game loop
        self.root.after(100, self.move_snake)

    def change_direction(self, new_dir):
        """Change the direction of the snake."""
        opposites = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if new_dir != opposites.get(self.snake_dir):  # Prevent reversing direction
            self.snake_dir = new_dir



root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
