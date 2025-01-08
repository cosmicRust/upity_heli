import pygame
import random

class GameEngine:
    def __init__(self):
        # Initialize game constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.GRAVITY = 0.5
        self.THRUST = -8
        self.BUILDING_SPEED = 3
        self.BUILDING_GAP = 200
        self.BUILDING_WIDTH = 70
        
        # Initialize game state
        self.reset_game()

    def reset_game(self):
        # Airplane properties
        self.airplane_x = self.SCREEN_WIDTH // 4
        self.airplane_y = self.SCREEN_HEIGHT // 2
        self.airplane_velocity = 0
        
        # Building properties
        self.buildings = []
        self.generate_initial_buildings()
        
        # Game state
        self.score = 0
        self.game_over = False

    def generate_initial_buildings(self):
        # Generate initial set of buildings
        x = self.SCREEN_WIDTH
        for _ in range(3):  # Start with 3 pairs of buildings
            self.generate_building_pair(x)
            x += self.BUILDING_WIDTH + 200

    def generate_building_pair(self, x):
        gap_y = random.randint(self.BUILDING_GAP, self.SCREEN_HEIGHT - self.BUILDING_GAP)
        building_pair = {
            'x': x,
            'gap_y': gap_y,
            'passed': False
        }
        self.buildings.append(building_pair)

    def update(self, thrust):
        if self.game_over:
            return

        # Update Airplane physics
        self.airplane_velocity += self.GRAVITY
        if thrust:
            self.airplane_velocity = self.THRUST
        self.airplane_y += self.airplane_velocity

        # Update buildings
        for building in self.buildings:
            building['x'] -= self.BUILDING_SPEED
            
            # Check if Airplane passed the building
            if not building['passed'] and building['x'] + self.BUILDING_WIDTH < self.airplane_x:
                self.score += 1
                building['passed'] = True

        # Remove off-screen buildings and generate new ones
        self.buildings = [b for b in self.buildings if b['x'] + self.BUILDING_WIDTH > 0]
        if len(self.buildings) < 3:
            self.generate_building_pair(self.buildings[-1]['x'] + self.BUILDING_WIDTH + 200)

        # Check collisions
        if self.check_collision():
            self.game_over = True

    def check_collision(self):
        # Check if Airplane hits the ground or ceiling
        if self.airplane_y <= 0 or self.airplane_y >= self.SCREEN_HEIGHT:
            return True

        # Check building collisions
        airplane_rect = pygame.Rect(self.airplane_x, self.airplane_y, 50, 30)  # Airplane hitbox
        
        for building in self.buildings:
            # Top building
            top_building = pygame.Rect(
                building['x'],
                0,
                self.BUILDING_WIDTH,
                building['gap_y'] - self.BUILDING_GAP // 2
            )
            
            # Bottom building
            bottom_building = pygame.Rect(
                building['x'],
                building['gap_y'] + self.BUILDING_GAP // 2,
                self.BUILDING_WIDTH,
                self.SCREEN_HEIGHT - (building['gap_y'] + self.BUILDING_GAP // 2)
            )
            
            if airplane_rect.colliderect(top_building) or airplane_rect.colliderect(bottom_building):
                return True

        return False

    def get_game_state(self):
        return {
            'airplane': {
                'x': self.airplane_x,
                'y': self.airplane_y,
                'velocity': self.airplane_velocity
            },
            'buildings': self.buildings,
            'score': self.score,
            'game_over': self.game_over
        }