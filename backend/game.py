
# import pygame
# import sys
# import csv
# from datetime import datetime
# from game_engine import GameEngine

# import os


# class GameLoop:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 600))
#         pygame.display.set_caption("Upity Airplane")
#         self.clock = pygame.time.Clock()
#         self.engine = GameEngine()

#         # Define assets directory relative to the script location
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         assets_dir = os.path.join(current_dir, "assets")  # Note: fixed typo in 'assets'

#         # Load assets with relative paths
#         self.airplane_image = pygame.image.load(os.path.join(assets_dir, "airplane.svg"))
#         self.building_image = pygame.image.load(os.path.join(assets_dir, "building.svg"))
#         self.building_image_top = pygame.transform.rotate(self.building_image, 180)
#         self.explosion_image = pygame.image.load(os.path.join(assets_dir, "explosion.png"))

#         # Scale assets
#         self.airplane_image = pygame.transform.scale(self.airplane_image, (70, 40))
#         self.building_image = pygame.transform.scale(self.building_image, (self.engine.BUILDING_WIDTH, 300))
#         self.building_image_top = pygame.transform.scale(self.building_image_top, (self.engine.BUILDING_WIDTH, 300))
#         self.explosion_image = pygame.transform.scale(self.explosion_image, (60, 60))

#         # Load sounds
#         pygame.mixer.init()
#         pygame.mixer.music.load(os.path.join(assets_dir,"gameplay_music.mp3"))
#         pygame.mixer.music.set_volume(0.5)
#         pygame.mixer.music.play(-1)
#         self.explosion_sound = pygame.mixer.Sound(os.path.join(assets_dir,"explosion.mp3"))

#         self.font = pygame.font.Font(None, 48)

#         # Colors
#         self.WHITE = (255, 255, 255)
#         self.BLACK = (0, 0, 0)

#         # Menu state
#         self.menu_active = True
#         self.music_on = True
#         self.selected_option = 0
#         self.menu_options = ["Play", "High Score", "Music", "Exit"]

#         # Game state
#         self.explosion_active = False
#         self.explosion_position = None
#         self.player_name = ""

#     def handle_menu_input(self, event):
#         """Handle input for the main menu."""
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 self.selected_option = (self.selected_option - 1) % len(self.menu_options)
#             elif event.key == pygame.K_DOWN:
#                 self.selected_option = (self.selected_option + 1) % len(self.menu_options)
#             elif event.key == pygame.K_RETURN:
#                 if self.menu_options[self.selected_option] == "Play":
#                     self.menu_active = False
#                 elif self.menu_options[self.selected_option] == "High Score":
#                     self.display_high_score()
#                 elif self.menu_options[self.selected_option] == "Music":
#                     self.music_on = not self.music_on
#                     if self.music_on:
#                         pygame.mixer.music.unpause()
#                     else:
#                         pygame.mixer.music.pause()
#                 elif self.menu_options[self.selected_option] == "Exit":
#                     pygame.quit()
#                     sys.exit()

#     def display_high_score(self):
#         """Display the reigning high score."""
#         reigning_name, reigning_score = self.get_reigning_score()
#         if reigning_name:
#             print(f"High Score: {reigning_name} - {reigning_score}")
#         else:
#             print("No high scores yet.")

#     def input_player_name(self):
#         """Display a text box to enter the player's name."""
#         input_active = True
#         player_name = ""
#         while input_active:
#             self.screen.fill(self.WHITE)
#             prompt_text = self.font.render("Enter Your Name: ", True, self.BLACK)
#             prompt_rect = prompt_text.get_rect(center=(400, 250))
#             self.screen.blit(prompt_text, prompt_rect)

#             name_text = self.font.render(player_name, True, self.BLACK)
#             name_rect = name_text.get_rect(center=(400, 300))
#             self.screen.blit(name_text, name_rect)

#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN:  # Enter to confirm
#                         input_active = False
#                     elif event.key == pygame.K_BACKSPACE:  # Backspace to delete a character
#                         player_name = player_name[:-1]
#                     else:  # Append other characters to the name
#                         player_name += event.unicode
#         return player_name

#     def save_high_score(self, name, score):
#         """Save high score to high_scores.csv."""
#         with open("high_scores.csv", mode="a", newline="") as file:
#             writer = csv.writer(file)
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             writer.writerow([name, score, timestamp])

#     def update_reigning_score(self):
#         """Update reigning_score.csv with the highest score."""
#         scores = []
#         try:
#             with open("high_scores.csv", mode="r") as file:
#                 reader = csv.reader(file)
#                 for row in reader:
#                     name, score, timestamp = row
#                     scores.append((name, int(score), timestamp))
#         except FileNotFoundError:
#             pass

#         if scores:
#             reigning_score = max(scores, key=lambda x: (x[1], x[2]))
#             self.save_reigning_score(reigning_score[0], reigning_score[1])

#     def save_reigning_score(self, name, score):
#         """Save the reigning high score."""
#         with open("reigning_score.csv", mode="w", newline="") as file:
#             writer = csv.writer(file)
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             writer.writerow([name, score, timestamp])

    

#     def get_reigning_score(self):
#         """Read the reigning high score."""
#         try:
#             with open("reigning_score.csv", mode="r") as file:
#                 reader = csv.reader(file)
#                 try:
#                     name, score, _ = next(reader)
#                     return name, int(score)
#                 except StopIteration:
#                     return None, 0
#         except FileNotFoundError:
#             return None, 0
#     def draw_menu(self):
#         """Render the main menu."""
#         reigning_name, reigning_score = self.get_reigning_score()
#         self.screen.fill(self.WHITE)
#         title = self.font.render("Main Menu", True, self.BLACK)
#         self.screen.blit(title, title.get_rect(center=(400, 100)))

#         if reigning_name:
#             high_score_text = self.font.render(f"High Score: {reigning_name} - {reigning_score}", True, self.BLACK)
#             self.screen.blit(high_score_text, high_score_text.get_rect(center=(400, 150)))

#         for i, option in enumerate(self.menu_options):
#             text_color = (0, 0, 255) if i == self.selected_option else self.BLACK
#             option_text = f"{option} {'(ON)' if option == 'Music' and self.music_on else ''}"
#             option_surface = self.font.render(option_text, True, text_color)
#             self.screen.blit(option_surface, option_surface.get_rect(center=(400, 200 + i * 50)))

#     def pause_menu(self):
#         """Display pause menu."""
#         options = ["Resume", "Main Menu", "Music"]
#         selected_option = 0
#         paused = True

#         while paused:
#             self.screen.fill(self.WHITE)
#             pause_text = self.font.render("Paused", True, self.BLACK)
#             self.screen.blit(pause_text, pause_text.get_rect(center=(400, 200)))

#             for i, option in enumerate(options):
#                 color = (0, 0, 255) if i == selected_option else self.BLACK
#                 option_text = self.font.render(option, True, color)
#                 self.screen.blit(option_text, option_text.get_rect(center=(400, 300 + i * 50)))

#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_UP:
#                         selected_option = (selected_option - 1) % len(options)
#                     elif event.key == pygame.K_DOWN:
#                         selected_option = (selected_option + 1) % len(options)
#                     elif event.key == pygame.K_RETURN:
#                         if options[selected_option] == "Resume":
#                             paused = False
#                         elif options[selected_option] == "Main Menu":
#                             self.menu_active = True
#                             self.player_name = ""
#                             return
#                         elif options[selected_option] == "Music":
#                             self.music_on = not self.music_on
#                             if self.music_on:
#                                 pygame.mixer.music.unpause()
#                             else:
#                                 pygame.mixer.music.pause()

#     def run(self):
#         """Main game loop."""
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if self.menu_active:
#                     self.handle_menu_input(event)
#                     if not self.menu_active and self.player_name == "":
#                         self.player_name = self.input_player_name()
#                 elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
#                     self.pause_menu()

#             if self.menu_active:
#                 self.draw_menu()
#             else:
#                 keys = pygame.key.get_pressed()
#                 thrust = keys[pygame.K_SPACE]
#                 self.engine.update(thrust)
#                 game_state = self.engine.get_game_state()

#                 if game_state['game_over']:
#                     if not self.explosion_active:
#                         self.explosion_active = True
#                         self.explosion_position = (
#                             game_state['airplane']['x']+40,
#                             game_state['airplane']['y']
#                         )
#                         self.screen.blit(self.explosion_image, self.explosion_position)
#                         self.explosion_sound.play()

#                     # Save high score and update reigning score
#                     self.save_high_score(self.player_name, game_state['score'])
#                     self.update_reigning_score()

#                     # Display game over options
#                     game_over_rect = pygame.Rect(150, 200, 500, 200)
#                     pygame.draw.rect(self.screen, (255, 255, 255, 150), game_over_rect)
#                     pygame.draw.rect(self.screen, self.BLACK, game_over_rect, 2)

#                     score_text = self.font.render(f"Your Score: {game_state['score']}", True, self.BLACK)
#                     self.screen.blit(score_text, score_text.get_rect(center=(400, 230)))

#                     restart_text = self.font.render("Press SPACE to Replay ", True, self.BLACK)
#                     self.screen.blit(restart_text, restart_text.get_rect(center=(400, 280)))

#                     restart_or_text = self.font.render(" or ", True, self.BLACK)
#                     self.screen.blit(restart_or_text, restart_or_text.get_rect(center=(400, 330)))

#                     restart_esc_text = self.font.render("ESC for Main Menu", True, self.BLACK)
#                     self.screen.blit(restart_esc_text, restart_esc_text.get_rect(center=(400, 380)))

#                     pygame.display.flip()
#                     waiting = True
#                     while waiting:
#                         for event in pygame.event.get():
#                             if event.type == pygame.QUIT:
#                                 pygame.quit()
#                                 sys.exit()
#                             if event.type == pygame.KEYDOWN:
#                                 if event.key == pygame.K_SPACE:
#                                     self.engine.reset_game()
#                                     self.explosion_active = False
#                                     waiting = False
#                                 elif event.key == pygame.K_ESCAPE:
#                                     self.menu_active = True
#                                     self.player_name = ""
#                                     waiting = False

#                 # Render game
#                 self.screen.fill(self.WHITE)
#                 airplane_rect = self.airplane_image.get_rect(
#                     topleft=(game_state['airplane']['x'], game_state['airplane']['y']))
#                 self.screen.blit(self.airplane_image, airplane_rect)

#                 for building in game_state['buildings']:
#                     top_building_y = building['gap_y'] - self.engine.BUILDING_GAP // 2 - 300
#                     self.screen.blit(self.building_image_top, (building['x'], top_building_y))
#                     bottom_building_y = building['gap_y'] + self.engine.BUILDING_GAP // 2
#                     self.screen.blit(self.building_image, (building['x'], bottom_building_y))

                

#                 score_text = self.font.render(f"Score: {game_state['score']}", True, self.BLACK)
#                 self.screen.blit(score_text, score_text.get_rect(topright=(780, 20)))

#             pygame.display.flip()
#             self.clock.tick(60)


# if __name__ == "__main__":
#     game = GameLoop()
#     game.run()


import pygame
import sys
import csv
import os
from datetime import datetime
from random import randint
from game_engine import GameEngine


class GameLoop:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Upity Airplane")
        self.clock = pygame.time.Clock()
        self.engine = GameEngine()

        # Define assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")

        # Load assets
        self.airplane_image = pygame.image.load(os.path.join(assets_dir, "airplane.svg"))
        self.building_image = pygame.image.load(os.path.join(assets_dir, "building.svg"))
        self.building_image_top = pygame.transform.rotate(self.building_image, 180)
        self.explosion_image = pygame.image.load(os.path.join(assets_dir, "explosion.png"))
        self.cloud_image = pygame.image.load(os.path.join(assets_dir, "cloud.png"))

        # Scale assets
        self.airplane_image = pygame.transform.scale(self.airplane_image, (70, 40))
        self.building_image = pygame.transform.scale(self.building_image, (self.engine.BUILDING_WIDTH, 300))
        self.building_image_top = pygame.transform.scale(self.building_image_top, (self.engine.BUILDING_WIDTH, 300))
        self.explosion_image = pygame.transform.scale(self.explosion_image, (60, 60))
        self.cloud_image = pygame.transform.scale(self.cloud_image, (100, 50))

        # Load sounds
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(assets_dir, "gameplay_music.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.explosion_sound = pygame.mixer.Sound(os.path.join(assets_dir, "explosion.mp3"))
        self.score_sound = pygame.mixer.Sound(os.path.join(assets_dir, "score_sound.mp3"))

        self.font = pygame.font.Font(None, 48)

        # Colors
        self.SKY_BLUE = (135, 206, 235)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Menu state
        self.menu_active = True
        self.music_on = True
        self.selected_option = 0
        self.menu_options = ["Play", "High Score", "Music", "Exit"]

        # Game state
        self.explosion_active = False
        self.explosion_position = None
        self.player_name = ""

        # Clouds for the background
        self.clouds = [(randint(0, 800), randint(0, 300)) for _ in range(5)]

    def draw_background(self):
        """Draw a procedural background with a blue sky and clouds."""
        self.screen.fill(self.SKY_BLUE)
        for cloud in self.clouds:
            self.screen.blit(self.cloud_image, cloud)

        # Move clouds for procedural effect
        self.clouds = [(x - 1 if x > -100 else 800, y) for x, y in self.clouds]

    def handle_menu_input(self, event):
        """Handle input for the main menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.menu_options[self.selected_option] == "Play":
                    self.menu_active = False
                elif self.menu_options[self.selected_option] == "High Score":
                    self.display_high_score()
                elif self.menu_options[self.selected_option] == "Music":
                    self.music_on = not self.music_on
                    if self.music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif self.menu_options[self.selected_option] == "Exit":
                    pygame.quit()
                    sys.exit()

    def display_high_score(self):
        """Display the reigning high score."""
        reigning_name, reigning_score = self.get_reigning_score()
        if reigning_name:
            print(f"High Score: {reigning_name} - {reigning_score}")
        else:
            print("No high scores yet.")

    def input_player_name(self):
        """Display a text box to enter the player's name."""
        input_active = True
        player_name = ""
        while input_active:
            self.screen.fill(self.WHITE)
            prompt_text = self.font.render("Enter Your Name: ", True, self.BLACK)
            prompt_rect = prompt_text.get_rect(center=(400, 250))
            self.screen.blit(prompt_text, prompt_rect)

            name_text = self.font.render(player_name, True, self.BLACK)
            name_rect = name_text.get_rect(center=(400, 300))
            self.screen.blit(name_text, name_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter to confirm
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:  # Backspace to delete a character
                        player_name = player_name[:-1]
                    else:  # Append other characters to the name
                        player_name += event.unicode
        return player_name

    def save_high_score(self, name, score):
        """Save high score to high_scores.csv."""
        with open("high_scores.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([name, score, timestamp])

    def update_reigning_score(self):
        """Update reigning_score.csv with the highest score."""
        scores = []
        try:
            with open("high_scores.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    name, score, timestamp = row
                    scores.append((name, int(score), timestamp))
        except FileNotFoundError:
            pass

        if scores:
            reigning_score = max(scores, key=lambda x: (x[1], x[2]))
            self.save_reigning_score(reigning_score[0], reigning_score[1])

    def save_reigning_score(self, name, score):
        """Save the reigning high score."""
        with open("reigning_score.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([name, score, timestamp])

    def get_reigning_score(self):
        """Read the reigning high score."""
        try:
            with open("reigning_score.csv", mode="r") as file:
                reader = csv.reader(file)
                name, score, _ = next(reader)
                return name, int(score)
        except FileNotFoundError:
            return None, 0

    def draw_menu(self):
        """Render the main menu."""
        reigning_name, reigning_score = self.get_reigning_score()
        self.screen.fill(self.WHITE)
        title = self.font.render("Main Menu", True, self.BLACK)
        self.screen.blit(title, title.get_rect(center=(400, 100)))

        if reigning_name:
            high_score_text = self.font.render(f"High Score: {reigning_name} - {reigning_score}", True, self.BLACK)
            self.screen.blit(high_score_text, high_score_text.get_rect(center=(400, 150)))

        for i, option in enumerate(self.menu_options):
            text_color = (0, 0, 255) if i == self.selected_option else self.BLACK
            option_text = f"{option} {'(ON)' if option == 'Music' and self.music_on else ''}"
            option_surface = self.font.render(option_text, True, text_color)
            self.screen.blit(option_surface, option_surface.get_rect(center=(400, 200 + i * 50)))

    def pause_menu(self):
        """Display pause menu."""
        options = ["Resume", "Main Menu", "Music"]
        selected_option = 0
        paused = True

        while paused:
            self.screen.fill(self.WHITE)
            pause_text = self.font.render("Paused", True, self.BLACK)
            self.screen.blit(pause_text, pause_text.get_rect(center=(400, 200)))

            for i, option in enumerate(options):
                color = (0, 0, 255) if i == selected_option else self.BLACK
                option_text = self.font.render(option, True, color)
                self.screen.blit(option_text, option_text.get_rect(center=(400, 300 + i * 50)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if options[selected_option] == "Resume":
                            paused = False
                        elif options[selected_option] == "Main Menu":
                            self.menu_active = True
                            self.player_name = ""
                            return
                        elif options[selected_option] == "Music":
                            self.music_on = not self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()

    def run(self):
        """Main game loop."""
        last_score = -1  # Track the last score to play the sound only when score changes

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.menu_active:
                    self.handle_menu_input(event)
                    if not self.menu_active and self.player_name == "":
                        self.player_name = self.input_player_name()
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.pause_menu()

            if self.menu_active:
                self.draw_menu()
            else:
                keys = pygame.key.get_pressed()
                thrust = keys[pygame.K_SPACE]
                self.engine.update(thrust)
                game_state = self.engine.get_game_state()

                if game_state['game_over']:
                    if not self.explosion_active:
                        self.explosion_active = True
                        self.explosion_sound.play()
                        self.explosion_position = (
                            game_state['airplane']['x'] + 40,
                            game_state['airplane']['y']
                        )
                        # self.explosion_sound.play()
                        self.screen.blit(self.explosion_image, self.explosion_position)

                    # Save high score and update reigning score
                    self.save_high_score(self.player_name, game_state['score'])
                    self.update_reigning_score()

                    # Display game over screen
                    game_over_rect = pygame.Rect(150, 200, 500, 200)
                    pygame.draw.rect(self.screen, (255, 255, 255, 150), game_over_rect)
                    pygame.draw.rect(self.screen, self.BLACK, game_over_rect, 2)

                    score_text = self.font.render(f"Your Score: {game_state['score']}", True, self.BLACK)
                    self.screen.blit(score_text, score_text.get_rect(center=(400, 230)))

                    restart_text = self.font.render("Press SPACE to Replay ", True, self.BLACK)
                    self.screen.blit(restart_text, restart_text.get_rect(center=(400, 280)))

                    restart_or_text = self.font.render(" or ", True, self.BLACK)
                    self.screen.blit(restart_or_text, restart_or_text.get_rect(center=(400, 330)))

                    restart_esc_text = self.font.render("ESC for Main Menu", True, self.BLACK)
                    self.screen.blit(restart_esc_text, restart_esc_text.get_rect(center=(400, 380)))

                    pygame.display.flip()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.explosion_sound.stop()
                                    self.engine.reset_game()
                                    self.explosion_active = False
                                    
                                    waiting = False
                                elif event.key == pygame.K_ESCAPE:
                                    self.menu_active = True
                                    self.player_name = ""
                                    waiting = False

                # Render game
                self.draw_background()
                airplane_rect = self.airplane_image.get_rect(
                    topleft=(game_state['airplane']['x'], game_state['airplane']['y']))
                self.screen.blit(self.airplane_image, airplane_rect)

                for building in game_state['buildings']:
                    top_building_y = building['gap_y'] - self.engine.BUILDING_GAP // 2 - 300
                    self.screen.blit(self.building_image_top, (building['x'], top_building_y))
                    bottom_building_y = building['gap_y'] + self.engine.BUILDING_GAP // 2
                    self.screen.blit(self.building_image, (building['x'], bottom_building_y))

                # Play score sound if score changes
                if game_state['score'] != last_score:
                    self.score_sound.play()
                    last_score = game_state['score']

                # Render score
                score_text = self.font.render(f"Score: {game_state['score']}", True, self.BLACK)
                self.screen.blit(score_text, score_text.get_rect(topright=(780, 20)))

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = GameLoop()
    game.run()
