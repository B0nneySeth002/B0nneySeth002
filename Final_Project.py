from graphics import *
from math import *
from random import *
from time import time as now
from pynput import keyboard

# Define constants for the game
WIDTH = 800
HEIGHT = 600
FRAMERATE = 60
INPUT = {
    "space" : False,
    "enter" : False,
    "esc" : False
}
DIFFICULTY = 1
MAX_FISH = 10
GAME_DURATION = 30
CLOUDS = True

# Define a function to clamp a value between a lower and upper bound
def clamp(x, lower, upper):  # Ensure that lower <= x <= upper
    return min(upper, max(lower, x))

# The shape of the strength in the rectangle
def rectified_sin_wave(time):
    period = 2 
    # Period
    time = time + pi
    return 1 - abs(sin(2 * pi / pow(period, 2) * time))

# The shape of the strength in the rectangle
def triangle_wave(time):
    period = 2 
    # Period
    return 2 * abs(time / period - floor(time / period + 0.5))

# Define Fish and Player classes
class Fish:
    def __init__(self, win):
        self.win = win
        self.progress = 0

        # Pick fish's score based on weighted distribution
        self.score = sample([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 5, 5, 5, 10, 10, 20], 1)[0]

        fish_length = randint(30, 60)  # Adjust size as needed
        fish_width = fish_length // 3
        self.circle = Oval(Point(0, 450), Point(0 + fish_length, 450 + fish_width))
        self.circle.setWidth(2)

        fish_color = color_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
        if self.score == 20:
            fish_color = color_rgb(251, 222, 51)
        self.circle.setFill(fish_color)
        self.circle.setOutline(fish_color)

        self.reach_time = 5 / DIFFICULTY * (self.score / 1.5) 
        path_of_fish = []
        container = 0
        x = WIDTH / 6
        y = 0
        path_of_fish.append((x, y + 450))  
        # Offset by 450 to convert to correct screenspace coordinates
        while container < 2:
            x += randint(5, 50)
            y += randint(-30, 30)
            y = clamp(y, - HEIGHT / 4, HEIGHT / 4 - 1 / 10 * HEIGHT)
            path_of_fish.append((x, y + 3 / 4 * HEIGHT))
            if x > WIDTH:     
                container += 1
        self.path = path_of_fish

    def draw(self):
        self.circle.draw(self.win)

    # Calculate and set the position of the fish along its path based on progress
    def position_on_path(self, delta):
        fraction = delta / self.reach_time
        self.progress += fraction
        # Find the index of the current segment in the path
        segment_index = int(self.progress * (len(self.path) - 1))
        
        # Calculate the fractional part for interpolation
        fraction_in_segment = self.progress * (len(self.path) - 1) - segment_index

        # Ensure that the segment index is within bounds
        segment_index = clamp(segment_index, 0, len(self.path) - 2)

        # Interpolate between two points to find the current position
        x1, y1 = self.path[segment_index]
        x2, y2 = self.path[segment_index + 1]
        x = x1 + (x2 - x1) * fraction_in_segment
        y = y1 + (y2 - y1) * fraction_in_segment

        # Set the new position of the fish
        self.circle.move(x - self.circle.getCenter().getX(), y - self.circle.getCenter().getY())

    # Check if the fish is caught by the player's hook
    def is_caught(self, hook_bounds):
        p1, p2 = self.circle.getP1(), self.circle.getP2()
        hp1, hp2 = hook_bounds.getP1(), hook_bounds.getP2()

        x1_fish, y1_fish, x2_fish, y2_fish = p1.getX(), p1.getY(), p2.getX(), p2.getY()
        x1_hook, y1_hook, x2_hook, y2_hook = hp1.getX(), hp1.getY(), hp2.getX(), hp2.getY()

        if x2_fish <= x1_hook or x2_hook <= x1_fish:
            return False

        if y2_fish <= y1_hook or y2_hook <= y1_fish:
            return False

        return True

    # Hide the fish by undrawing it
    def hide(self):
        self.circle.undraw()

class Player:
    def __init__(self, win):
        self.win = win
        self.hook = Circle(Point(-10, -10), 5)
        self.hook.setFill("red")

        self.player_body = []
        torso = Oval(Point(0, 0), Point(20, 50))
        torso.setFill("green")
        torso.setOutline("green")
        head = Circle(Point(10, -10), 10)
        head.setFill("brown")
        head.setOutline("brown")
        legs = Polygon(Point(0, 50), Point(0, 80), Point(7, 80), Point(7, 60), Point(13, 60), Point(13, 80), Point(20, 80), Point(20, 50))
        legs.setFill("blue")
        legs.setOutline("blue")

        self.player_body.append(torso)
        self.player_body.append(head)
        self.player_body.append(legs)

        for i in self.player_body:
            i.move(1 / 10 * WIDTH, 1 / 3 * HEIGHT)

    def draw(self):
        self.hook.draw(self.win)
        for i in self.player_body:
            i.draw(self.win)

    def undraw(self):
        self.hook.undraw()
        for i in self.player_body:
            i.undraw()

    def set_hook_position(self, tx, ty): # Target x and target y
        # Get current x and current y
        cx = self.hook.getCenter().getX()
        cy = self.hook.getCenter().getY()
        # Find new coordinates
        dx = tx - cx
        dy = ty - cy
        self.hook.move(dx, dy)

class FishingGame:
    def __init__(self, win):
        self.win = win
        self.high_score = 0

        self.reset()

        # Create a list of rectangles as slices of a bar to show the cast strength
        PLACEMENT = 2 / 5 * HEIGHT

        temporary_list = []
        for i in range(100):
            stacked_slices = Rectangle(Point(0, 0), Point(10, -2))
            if i < 50:
                col = color_rgb(int(255 / 50 * i), 255, 50)
            else:
                col = color_rgb(255, int(255 / 50 * (100 - i)), 50)
            stacked_slices.setFill(col)
            stacked_slices.setOutline(col)

            # Stack the slices on top of each other
            stacked_slices.move(0, -2 * i)

            # Adjust the position of the whole bar
            stacked_slices.move(10, PLACEMENT)
            temporary_list.append(stacked_slices)
        
        self.cast_strength_indicator = temporary_list

        temp_rect = Rectangle(Point(-2, -2), Point(12, -204))
        temp_rect.move(10, PLACEMENT + 4)
        self.cast_strength_outline = temp_rect

    # Add a new fish to the game
    def add_fish(self):
        newFish = Fish(self.win)
        newFish.draw()
        self.fish_list.append(newFish)

    # Update the positions of fish along their paths
    def update_fish_positions(self, delta):
        for fish in self.fish_list:
            fish.position_on_path(delta)
            if fish.circle.getCenter().getX() > WIDTH:
                self.fish_list.remove(fish)
                fish.hide()

    def create_cloud(self, numCircles, origin, chaos, color):
        newCloud = []
        for i in range(numCircles):
            # Create a circle at the specified origin with a small radius of 5
            circ = Circle(origin, sample([5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 12, 13, 14, 15], 1)[0])
            
            # Randomly move the circle within a defined chaos factor
            circ.move(random() * 10 * chaos, random() * 10 * chaos)
            circ.setFill(color)
            circ.setOutline(color)
            newCloud.append(circ)
        return newCloud

    def game_over(self):
        for i in self.map:
            i.undraw()
        if CLOUDS:
            for cloud in self.clouds:
                for c in cloud:
                    if type(c) != float:
                        c.undraw()
        self.score_text.undraw()
        self.timer_text.undraw()
        self.combo_text.undraw()
        self.player.undraw()
        for fish in self.fish_list:
            fish.hide()

        # High score logic
        new_high = self.score > self.high_score
        if new_high:
            self.high_score = self.score
            hs = Text(Point(WIDTH / 2, HEIGHT / 3 + 50), "NEW HIGH SCORE!")
            hs.setSize(16)
            hs.setTextColor("white")
            hs.draw(self.win)
        
        # Display game over UI
        self.win.setBackground("black")

        end_text = Text(Point(WIDTH / 2, HEIGHT / 3), "GAME OVER!")
        end_text.setSize(32)
        end_text.setTextColor("white")

        score = Text(Point(WIDTH / 2, HEIGHT / 2), str(self.score))
        score.setSize(32)
        if new_high:
            score.setTextColor("gold")
        else:
            score.setTextColor("green")

        pts = Text(Point(WIDTH / 2, HEIGHT / 2 + 40), "POINTS")
        pts.setSize(16)
        pts.setTextColor("white")

        high = Text(Point(WIDTH / 2, HEIGHT * 2 / 3), "HIGH SCORE")
        high.setSize(16)
        high.setTextColor("white")

        hscore = Text(Point(WIDTH / 2, HEIGHT * 2 / 3 + 40), str(self.high_score))
        hscore.setSize(32)
        hscore.setTextColor("gold")

        play_again = Text(Point(WIDTH / 2, 9 / 10 * HEIGHT), "PRESS ENTER TO PLAY AGAIN")
        play_again.setSize(12)
        play_again.setTextColor("grey")

        _exit = Text(Point(1 / 8 * WIDTH, 1 / 15 * HEIGHT), "PRESS ESC TO QUIT")
        _exit.setSize(12)
        _exit.setTextColor("grey") 

        end_text.draw(self.win)
        score.draw(self.win)
        pts.draw(self.win)
        high.draw(self.win)
        hscore.draw(self.win)
        play_again.draw(self.win)
        _exit.draw(self.win)

        while self.win.isOpen():
            key = self.win.checkKey()
            if INPUT["esc"]:
                exit()
            elif INPUT["enter"]:
                end_text.undraw()
                score.undraw()
                pts.undraw()
                high.undraw()
                hscore.undraw()
                play_again.undraw()
                _exit.undraw()
                if new_high:
                    hs.undraw()

                self.reset()
                self.play()
    
    def reset(self):
        self.win.setBackground(color_rgb(191, 226, 255))
        self.player = Player(self.win)
        self.fish_list = []
        self.score = 0
        self.game_timer = GAME_DURATION
        self.holding = False
        self.hold_time = 0
        self.cast_state = 0
        self.cast_states = ["not", "casting", "waiting", "reeling"]
        self.cast_data = {}
        self.catch = []
        self.catch_counter = 0
        self.combo_text_timer = 0
        self.plumb_shot_count = 0
        self.plumb_shot_text_timer = 0

        # Generate the game map
        self.map = []

        # Create the background sky layer
        point_list = []
        for i in range(11):
            x = WIDTH * (i / 10)
            y = randint(30, 90)
            point_list.append(Point(x, y))
        bgland = Polygon(point_list + [Point(WIDTH, 0), Point(0, 0)])
        bgland_col = color_rgb(169, 215, 252)
        bgland.setFill(bgland_col)
        bgland.setOutline(bgland_col)
        self.map.append(bgland)

        # Create background clouds
        for i in range(10):
            oval = Oval(Point(randint(-50, -30), randint(-20, -10)), Point(randint(30, 50), randint(10, 20)))
            oval.move(0, WIDTH / 4)
            oval.move(randint(0, WIDTH), randint(-HEIGHT / 4, HEIGHT / 4))
            r = randint(200, 255)
            oval_col = color_rgb(r, r, r)
            oval.setFill(oval_col)
            oval.setOutline(oval_col)
            self.map.append(oval)

        # Create the background landmass layer 1
        point_list = []
        for i in range(11):
            x = WIDTH * (i / 10)
            y = HEIGHT / 2 - randint(30, 90)
            point_list.append(Point(x, y))
        bgland = Polygon(point_list + [Point(WIDTH, HEIGHT), Point(0, HEIGHT)])
        bgland_col = color_rgb(107, 176, 137)
        bgland.setFill(bgland_col)
        bgland.setOutline(bgland_col)
        self.map.append(bgland)

        # Create the background landmass layer 2
        point_list = []
        for i in range(11):
            x = WIDTH * (i / 10)
            y = HEIGHT / 2 - randint(20, 70)
            point_list.append(Point(x, y))
        bgland2 = Polygon(point_list + [Point(WIDTH, HEIGHT), Point(0, HEIGHT)])
        bgland2_col = color_rgb(57, 145, 95)
        bgland2.setFill(bgland2_col)
        bgland2.setOutline(bgland2_col)
        self.map.append(bgland2)

        # Create the water
        water = Rectangle(Point(0, HEIGHT / 2), Point(WIDTH, HEIGHT))
        water_col = color_rgb(0, 83, 150)
        water.setFill(water_col)
        water.setOutline(water_col)
        self.map.append(water)

        # Create the player's landmass
        land = Polygon(Point(0, HEIGHT / 2), Point(0, HEIGHT / 2 - HEIGHT / 30), Point(WIDTH / 7, HEIGHT / 2 - HEIGHT / 30), Point(WIDTH / 6, HEIGHT / 2))
        land_col = color_rgb(153, 102, 53)
        land.setFill(land_col)
        land.setOutline(land_col)
        self.map.append(land)

        # Create the underwater landmass
        underland = Polygon(Point(0, HEIGHT), Point(0, HEIGHT / 2), Point(WIDTH / 6, HEIGHT / 2), Point(WIDTH / 2, HEIGHT))
        underland_col = color_rgb(100, 75, 103)
        underland.setFill(underland_col)
        underland.setOutline(underland_col)
        self.map.append(underland)

        for i in self.map:
            i.draw(self.win)

        # Create clouds
        if CLOUDS:
            self.clouds = []
            for i in range(3):
                cloud = self.create_cloud(randint(1, 5), Point(WIDTH / (i + 1), HEIGHT / 8), 3, "white")
                for c in cloud:
                    c.draw(self.win)
                cloud.append(random() * 100)
                self.clouds.append(cloud)

        # Create a Text object to display the score
        self.score_text = Text(Point(WIDTH - 1 / 10 * WIDTH, 1 / 15 * HEIGHT), "Score: 0 ")
        self.score_text.setSize(18)
        self.score_text.setTextColor("green")
        self.score_text.draw(self.win)

        # Create a Text object to display combos
        self.combo_text = Text(Point(WIDTH / 2, 1 / 5 * HEIGHT), "none")
        self.combo_text.setSize(32)

        self.plumb_shot_text = Text(Point(WIDTH / 2, 1 / 6 * HEIGHT), "none")
        self.combo_text.setSize(32)

        # Create a Text object to display the game timer
        self.timer_text = Text(Point(1 / 10 * WIDTH, 1 / 15 * HEIGHT), str(self.game_timer))
        self.timer_text.setSize(24)
        self.timer_text.setTextColor("black")
        self.timer_text.draw(self.win)
            
    def play(self):
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        prev_time = now()
        self.add_fish()
        self.player.draw()
        
        while self.win.isOpen():
          
             # Calculate time between each frame
            curr_time = now()
            delta = curr_time - prev_time
            prev_time = curr_time
         
            # Handle player's input (e.g., spacebar to move the hook)
            key = self.win.checkKey()

            if self.cast_state != 0:
                if self.cast_state == 1:
                    cast_time = curr_time - self.cast_data["time_of_cast"]

                    # Find position of hook from delta and casting parabola
                    x = cast_time * 2
                    h = self.cast_data["strength"] * 1.2
                    
                    # Detect if hook is underwater, slow it down if it is
                    if self.player.hook.getP1().getY() > HEIGHT / 2:
                        if "surface_intersect" not in self.cast_data:
                            self.cast_data["surface_intersect"] = self.player.hook.getP1()
                            # Saves the point where the hook first enters the water

                        dist_to_stop = HEIGHT * 9/10 - self.player.hook.getP1().getY()

                        if dist_to_stop <= 0:
                            self.cast_data["stop_point"] = self.player.hook.getP1()
                            self.cast_state = 2

                    y = -1 / h * pow(x - h, 2) + h

                    # Multiply to screenspace coordinates
                    x *= 5 / 16 * WIDTH
                    y *= -1 / 3 * HEIGHT

                    # Offset to correct starting point
                    x += 1 / 16 * WIDTH
                    y += 1 / 3 * HEIGHT

                    self.player.set_hook_position(x, y)

                if self.cast_state == 2:
                    if INPUT["space"]:
                        self.cast_data["time_of_reel"] = curr_time
                        self.cast_state = 3

                if self.cast_state == 3:
                    reel_time = (curr_time - self.cast_data["time_of_reel"]) * 2

                    # Linearly interpolate between the bottom point and surface point
                    bottom = self.cast_data["stop_point"]
                    surface = self.cast_data["surface_intersect"]

                    x = bottom.getX() + reel_time * (surface.getX() - bottom.getX())
                    y = bottom.getY() + reel_time * (surface.getY() - bottom.getY())

                    # Check if hook has come above water
                    if y <= HEIGHT / 2:
                        # Check for combos
                        if self.catch_counter > 1:
                            match self.catch_counter:
                                case 2:
                                    self.combo_text.setText("DOUBLE")
                                case 3:
                                    self.combo_text.setText("TRIPLE")
                                case 4:
                                    self.combo_text.setText("QUADRUPLE")
                                case 5:
                                    self.combo_text.setText("PENTUPLE")
                                case 6:
                                    self.combo_text.setText("SEXTUPLE")
                                case _:
                                    self.combo_text.setText("INSANE COMBO")
                            self.combo_text.setTextColor(color_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
                            self.combo_text_timer = 2
                        
                        # Reset casting
                        self.cast_state = 0
                        self.player.set_hook_position(-10, -10)
                        self.cast_data = {}

                        # Calculate points
                        score_sum = 0

                        for score in self.catch:
                            multiplied_score = fish.score
                            if self.plumb_shot_count > 0:
                                multiplied_score *= 2
                                self.plumb_shot_count -= 1
                            score_sum += multiplied_score

                        self.score += score_sum * self.catch_counter
                    else:
                        self.player.set_hook_position(x, y)
            else:
                if self.holding:
                    if INPUT["space"]:
                        self.hold_time += delta
                        # Update strength indicator
                        strength = rectified_sin_wave(self.hold_time)  # Change both of these as desired

                        # Update strength indicator
                        for i in range(len(self.cast_strength_indicator)):
                            if (i + 1) / 100 <= strength:
                                try:
                                    self.cast_strength_indicator[i].draw(self.win)
                                except Exception:
                                    pass
                            else:
                                self.cast_strength_indicator[i].undraw()
                    else:
                        self.hold_time += delta

                        self.cast_state = 1
                        self.cast_data["time_of_cast"] = curr_time
                        self.cast_data["strength"] = rectified_sin_wave(self.hold_time)  # Change both of these as desired
                        self.holding = False

                        self.hold_time = 0

                        for slice in self.cast_strength_indicator:
                            slice.undraw()
                        self.cast_strength_outline.undraw()

                elif INPUT["space"]:
                    self.catch_counter = 0
                    self.catch_points = 0
                    self.holding = True
                    self.cast_strength_outline.draw(self.win)

            # Move fish
            self.update_fish_positions(delta)

            # Check for collisions (hook and fish)
            for fish in self.fish_list:
                if fish.is_caught(Rectangle(self.player.hook.getP1(), self.player.hook.getP2())):
                    # Fish is caught
                    self.catch_counter += 1
                    self.catch.append(fish.score)
                    if self.cast_state == 1:
                        # If we are currently casting the hook
                        self.plumb_shot_count += 1
                        if self.cast_data['strength'] > 0.6:
                            self.plumb_shot_text.setText("SNIPED")
                        else:
                            self.plumb_shot_text.setText("PLUMB SHOT")
                        self.plumb_shot_text.setTextColor(color_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
                        self.plumb_shot_text_timer = 2

                    fish.hide()
                    self.fish_list.remove(fish)
            
            if len(self.fish_list) < MAX_FISH and random() < 0.02:
                self.add_fish()

            # Update game timer
            self.game_timer -= delta

            # Update the score text
            self.score_text.setText("SCORE: " + str(self.score))
            self.timer_text.setText(str(round(self.game_timer, 1)))

            # Do combo_text timing
            if self.combo_text_timer > 0:
                try:
                    self.combo_text.draw(self.win)
                except GraphicsError:
                    pass
                self.combo_text.setSize(clamp(5, int(32 * self.combo_text_timer), 1000))
                self.combo_text_timer -= delta
            else:
                self.combo_text.undraw()
            
            # Do plumb shot text timing
            if self.plumb_shot_text_timer > 0:
                try:
                    self.plumb_shot_text.draw(self.win)
                except GraphicsError:
                    pass
                self.plumb_shot_text.setSize(clamp(5, int(32 * self.plumb_shot_text_timer), 1000))
                self.plumb_shot_text_timer -= delta
            else:
                self.plumb_shot_text.undraw()
            
            # Draw clouds moving
            if CLOUDS:
                for cloud in self.clouds:
                    speed = cloud[-1]
                    for circle in cloud:
                        # Ensure the circle being processed is not the speed indicator for the cloud
                        if circle != speed:
                        # Check if the circle has moved past the right edge of the screen
                            if circle.getP1().getX() > WIDTH:
                                circle.undraw()
                                cloud.remove(circle)
                                continue
                        # This moves the circle horizontally based on the simulation speed.
                            circle.move(speed * delta, 0)
                    if len(cloud) == 1:
                        self.clouds.remove(cloud)
                        replacementCloud = self.create_cloud(randint(1, 5), Point(-10, HEIGHT / 8), 3, "white")
                        for c in replacementCloud:
                            c.draw(self.win)
                        replacementCloud.append(random() * 10)
                        self.clouds.append(replacementCloud)
            
            # End the game if a condition is met
            if self.game_timer <= 0:
                self.game_over()

            update(FRAMERATE)

# Main function
def main():
    win = GraphWin("Fishing at a River", WIDTH, HEIGHT)
    game = FishingGame(win)
    game.play()
    win.getMouse()
    win.close()

def on_press(key):
    match key:
        case keyboard.Key.space:
            INPUT["space"] = True
        case keyboard.Key.enter:
            INPUT["enter"] = True
        case keyboard.Key.esc:
            INPUT["esc"] = True

def on_release(key):
    match key:
        case keyboard.Key.space:
            INPUT["space"] = False
        case keyboard.Key.enter:
            INPUT["enter"] = False
        case keyboard.Key.esc:
            INPUT["esc"] = False

if __name__ == "__main__": 
    main()