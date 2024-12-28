import pygame
import random
import numpy as np
import sys  # Added for system exit

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen Setup
WIDTH, HEIGHT = 1200, 800
print("Initializing screen...")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Infant Keyboard Fun")

# Colors
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255)   # Cyan
]

# Emojis
EMOJIS = [
    "😄", "🌈", "🎈", "🌟", "🦄", "🍭", 
    "🚀", "🎉", "🌞", "🐶", "🐱", "🦁"
]

# Fireworks Class
class Firework:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.particles = []
        self.create_particles()
        self.lifetime = 60

    def create_particles(self):
        for _ in range(100):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(2, 8)
            dx = speed * np.cos(angle)
            dy = speed * np.sin(angle)
            self.particles.append([self.x, self.y, dx, dy])

    def update(self):
        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3]
            particle[2] *= 0.95
            particle[3] *= 0.95

        self.lifetime -= 1

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, self.color, 
                               (int(particle[0]), int(particle[1])), 2)

# Sound Setup
def load_piano_sounds():
    sounds = []
    try:
        for i in range(1, 9):
            # Generate a simple stereo tone
            sample_rate = 44100
            duration = 0.5  # half a second
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create stereo sound (2D array)
            tone_left = np.sin(2 * np.pi * 220 * i * t)  # Left channel
            tone_right = np.sin(2 * np.pi * 220 * i * t)  # Right channel
            
            # Combine into stereo array
            stereo_tone = np.column_stack((tone_left, tone_right))
            
            # Scale to 16-bit range
            stereo_tone = (stereo_tone * 32767).astype(np.int16)
            
            sound = pygame.sndarray.make_sound(stereo_tone)
            sounds.append(sound)
    except Exception as e:
        print(f"Error creating sounds: {e}")
        # Create a silent sound as fallback
        silent_sound = pygame.sndarray.make_sound(np.zeros((44100, 2), dtype=np.int16))
        sounds = [silent_sound]
    return sounds

# Main Game Loop
def main():
    print("Starting main game loop...")
    clock = pygame.time.Clock()
    fireworks = []
    piano_sounds = load_piano_sounds()
    
    # Use a system font that's more likely to support emojis
    font = pygame.font.SysFont('arial', 200)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Allow quitting with ESC key
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Create Firework
                color = random.choice(COLORS)
                fireworks.append(Firework(
                    random.randint(0, WIDTH), 
                    random.randint(0, HEIGHT), 
                    color
                ))

                # Play Random Piano Sound
                try:
                    random.choice(piano_sounds).play()
                except Exception as e:
                    print(f"Sound play error: {e}")

                # Display Random Emoji
                try:
                    emoji_text = font.render(random.choice(EMOJIS), True, color)
                    emoji_rect = emoji_text.get_rect(center=(WIDTH//2, HEIGHT//2))
                    screen.blit(emoji_text, emoji_rect)
                except Exception as e:
                    print(f"Emoji render error: {e}")

        # Clear Screen
        screen.fill((0, 0, 0))

        # Update and Draw Fireworks
        for firework in fireworks[:]:
            firework.update()
            firework.draw(screen)
            if firework.lifetime <= 0:
                fireworks.remove(firework)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        print("Game is starting...")
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
