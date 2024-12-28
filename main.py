import pygame
import random
import numpy as np
import sys
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen Setup
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Infant Sensory Playground")

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

# Sound Generators
class SoundGenerator:
    @staticmethod
    def generate_piano_tone(i, duration=0.5, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone_left = np.sin(2 * np.pi * 220 * i * t)
        tone_right = np.sin(2 * np.pi * 220 * i * t)
        stereo_tone = np.column_stack((tone_left, tone_right))
        return (stereo_tone * 32767).astype(np.int16)

    @staticmethod
    def generate_nature_sounds(i, duration=0.5, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        # Simulate bird chirps or water sounds
        tone = np.sin(2 * np.pi * 300 * i * t) * np.sin(2 * np.pi * 10 * t)
        stereo_tone = np.column_stack((tone, tone))
        return (stereo_tone * 32767).astype(np.int16)

    @staticmethod
    def generate_galaxy_sounds(i, duration=0.5, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        # Simulate space-like electronic tones
        tone = np.sin(2 * np.pi * 100 * i * t) * np.sin(2 * np.pi * 5 * t)
        stereo_tone = np.column_stack((tone, tone))
        return (stereo_tone * 32767).astype(np.int16)

    @staticmethod
    def generate_xylophone_tone(i, duration=0.5, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        # Simulate xylophone-like tone with quick decay
        tone = np.sin(2 * np.pi * 440 * i * t) * np.exp(-t * 10)
        stereo_tone = np.column_stack((tone, tone))
        return (stereo_tone * 32767).astype(np.int16)

    @staticmethod
    def generate_drumkit_sound(i, duration=0.5, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        # Simulate drum-like noise burst
        noise = np.random.uniform(-1, 1, len(t))
        tone = noise * np.exp(-t * 20)
        stereo_tone = np.column_stack((tone, tone))
        return (stereo_tone * 32767).astype(np.int16)

# Visualization Generators
class VisualizationGenerator:
    @staticmethod
    def fireworks(screen, color):
        firework = Firework(
            random.randint(0, WIDTH), 
            random.randint(0, HEIGHT), 
            color
        )
        return firework

    @staticmethod
    def ripples(screen, color):
        # Create expanding circular ripples
        class Ripple:
            def __init__(self, x, y, color):
                self.x = x
                self.y = y
                self.color = color
                self.max_radius = 200
                self.current_radius = 0
                self.lifetime = 60

            def update(self):
                self.current_radius += 5
                self.lifetime -= 1

            def draw(self, surface):
                pygame.draw.circle(surface, self.color, 
                                   (int(self.x), int(self.y)), 
                                   int(self.current_radius), 2)

        ripple = Ripple(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            color
        )
        return ripple

    @staticmethod
    def stars(screen, color):
        # Create twinkling stars
        class Star:
            def __init__(self, x, y, color):
                self.x = x
                self.y = y
                self.color = color
                self.size = random.randint(1, 5)
                self.lifetime = 60
                self.alpha = 255

            def update(self):
                self.lifetime -= 1
                self.alpha = max(0, self.alpha - 5)

            def draw(self, surface):
                star_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
                pygame.draw.circle(star_surface, (*self.color, self.alpha), 
                                   (self.size, self.size), self.size)
                surface.blit(star_surface, (self.x, self.y))

        stars = [Star(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            color
        ) for _ in range(50)]
        return stars

    @staticmethod
    def light_bars(screen, color):
        # Create vertical light bars
        class LightBar:
            def __init__(self, x, color):
                self.x = x
                self.color = color
                self.height = random.randint(50, HEIGHT)
                self.lifetime = 60
                self.alpha = 255

            def update(self):
                self.lifetime -= 1
                self.alpha = max(0, self.alpha - 5)

            def draw(self, surface):
                bar_surface = pygame.Surface((20, self.height), pygame.SRCALPHA)
                bar_surface.fill((*self.color, self.alpha))
                surface.blit(bar_surface, (self.x, HEIGHT - self.height))

        bars = [LightBar(
            _ * 20,
            color
        ) for _ in range(WIDTH // 20)]
        return bars

    @staticmethod
    def drum_beat_waves(screen, color):
        # Create wave-like oscillations
        class WaveLine:
            def __init__(self, color):
                self.color = color
                self.phase = 0
                self.lifetime = 60

            def update(self):
                self.phase += 0.1
                self.lifetime -= 1

            def draw(self, surface):
                points = []
                for x in range(0, WIDTH, 10):
                    y = HEIGHT//2 + int(math.sin(x * 0.1 + self.phase) * 100)
                    points.append((x, y))
                
                if len(points) > 1:
                    pygame.draw.lines(surface, self.color, False, points, 3)

        return WaveLine(color)

# Fireworks Class (kept from previous version)
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

# Sound and Visualization Modes
SOUND_MODES = {
    'piano': SoundGenerator.generate_piano_tone,
    'nature': SoundGenerator.generate_nature_sounds,
    'galaxy': SoundGenerator.generate_galaxy_sounds,
    'xylophone': SoundGenerator.generate_xylophone_tone,
    'drumkit': SoundGenerator.generate_drumkit_sound
}

VISUALIZATION_MODES = {
    'fireworks': VisualizationGenerator.fireworks,
    'ripples': VisualizationGenerator.ripples,
    'stars': VisualizationGenerator.stars,
    'light_bars': VisualizationGenerator.light_bars,
    'drum_beat_waves': VisualizationGenerator.drum_beat_waves
}

# Sound Loading Function
def load_sounds(mode='piano'):
    sounds = []
    try:
        for i in range(1, 9):
            tone = SOUND_MODES[mode](i)
            sound = pygame.sndarray.make_sound(tone)
            sounds.append(sound)
    except Exception as e:
        print(f"Error creating sounds: {e}")
        # Create a silent sound as fallback
        silent_sound = pygame.sndarray.make_sound(np.zeros((44100, 2), dtype=np.int16))
        sounds = [silent_sound]
    return sounds

# Main Game Loop
def main():
    print("Starting Infant Sensory Playground...")
    clock = pygame.time.Clock()
    
    # Current mode selections
    current_sound_mode = 'piano'
    current_visual_mode = 'fireworks'
    
    # Sound and Visualization Lists
    sound_modes = list(SOUND_MODES.keys())
    visual_modes = list(VISUALIZATION_MODES.keys())
    
    # Load initial sounds
    piano_sounds = load_sounds(current_sound_mode)
    
    # Visualization tracking
    visualizations = []
    
    # Use a system font that's more likely to support emojis
    font = pygame.font.SysFont('arial', 200)
    mode_font = pygame.font.SysFont('arial', 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Allow quitting with ESC key
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Change sound mode with F1-F5
                elif event.key == pygame.K_F1:
                    current_sound_mode = sound_modes[(sound_modes.index(current_sound_mode) + 1) % len(sound_modes)]
                    piano_sounds = load_sounds(current_sound_mode)
                    print(f"Sound mode changed to: {current_sound_mode}")
                
                # Change visualization mode with F6-F10
                elif event.key == pygame.K_F6:
                    current_visual_mode = visual_modes[(visual_modes.index(current_visual_mode) + 1) % len(visual_modes)]
                    print(f"Visual mode changed to: {current_visual_mode}")
                
                # Create Visualization and Sound
                color = random.choice(COLORS)
                
                # Play Random Sound
                try:
                    random.choice(piano_sounds).play()
                except Exception as e:
                    print(f"Sound play error: {e}")

                # Create Visualization
                vis = VISUALIZATION_MODES[current_visual_mode](screen, color)
                if vis:
                    visualizations.append(vis)

                # Display Random Emoji
                try:
                    emoji_text = font.render(random.choice(EMOJIS), True, color)
                    emoji_rect = emoji_text.get_rect(center=(WIDTH//2, HEIGHT//2))
                    screen.blit(emoji_text, emoji_rect)
                except Exception as e:
                    print(f"Emoji render error: {e}")

        # Clear Screen
        screen.fill((0, 0, 0))

        # Update and Draw Visualizations
        for vis in visualizations[:]:
            if isinstance(vis, Firework):
                vis.update()
                vis.draw(screen)
                if vis.lifetime <= 0:
                    visualizations.remove(vis)
            elif isinstance(vis, list):
                for v in vis:
                    v.update()
                    v.draw(screen)
                    if hasattr(v, 'lifetime') and v.lifetime <= 0:
                        vis.remove(v)
            else:
                vis.update()
                vis.draw(screen)
                if hasattr(vis, 'lifetime') and vis.lifetime <= 0:
                    visualizations.remove(vis)

        # Display current modes
        mode_text_sound = mode_font.render(f"Sound: {current_sound_mode}", True, (255,255,255))
        mode_text_visual = mode_font.render(f"Visual: {current_visual_mode}", True, (255,255,255))
        screen.blit(mode_text_sound, (10, 10))
        screen.blit(mode_text_visual, (10, 50))

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
