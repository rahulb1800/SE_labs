import array
import math
import random

import pygame

from game.hole import Hole

ROUND_MS = 30000

DIFFICULTIES = {
    "Easy":   {"spawn_ms": 1000, "up_ms": 1300},
    "Medium": {"spawn_ms": 700,  "up_ms": 950},
    "Hard":   {"spawn_ms": 450,  "up_ms": 650},
}


def make_tone(freq, ms, volume=0.4, sweep_to=None):
    """Build a short beep in memory so no sound files are needed."""
    init = pygame.mixer.get_init()
    if not init:
        return None
    rate, fmt, channels = init
    if abs(fmt) != 16:
        return None
    total = int(rate * ms / 1000)
    samples = array.array("h")
    phase = 0.0
    for i in range(total):
        f = freq if sweep_to is None else freq + (sweep_to - freq) * i / total
        phase += 2 * math.pi * f / rate
        value = int(32767 * volume * (1 - i / total) * math.sin(phase))
        for _ in range(channels):
            samples.append(value)
    return pygame.mixer.Sound(buffer=samples.tobytes())


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 72)

        self.holes = self._create_holes()
        self._init_sounds()
        self._create_buttons()

        self.difficulty = "Medium"
        self.start_round(self.difficulty)

    # ---------- setup ----------
    def _create_holes(self):
        holes = []
        xs = [100, 250, 400]
        ys = [170, 310, 450]
        for y in ys:
            for x in xs:
                holes.append(Hole(x, y, radius=50))
        return holes

    def _init_sounds(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.hit_sound = make_tone(700, 120, sweep_to=1000)
            self.miss_sound = make_tone(180, 150)
            self.end_sound = make_tone(600, 600, sweep_to=200)
        except pygame.error:
            self.hit_sound = self.miss_sound = self.end_sound = None

    def _create_buttons(self):
        w, h = 120, 45
        gap = 20
        start_x = (self.width - (3 * w + 2 * gap)) // 2
        self.buttons = {}
        for i, name in enumerate(["Easy", "Medium", "Hard"]):
            self.buttons[name] = pygame.Rect(start_x + i * (w + gap), 340, w, h)
        self.buttons["Exit"] = pygame.Rect((self.width - 160) // 2, 410, 160, h)

    def _play(self, sound):
        if sound:
            sound.play()

    # ---------- game flow ----------
    def start_round(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.state = "playing"
        self.start_time = pygame.time.get_ticks()
        self.last_spawn = self.start_time
        for hole in self.holes:
            hole.deactivate()

    def end_round(self):
        self.state = "game_over"
        for hole in self.holes:
            hole.deactivate()
        self._play(self.end_sound)

    def time_left_ms(self):
        if self.state != "playing":
            return 0
        return max(0, ROUND_MS - (pygame.time.get_ticks() - self.start_time))

    # ---------- input ----------
    def handle_event(self, event):
        if self.state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._whack(event.pos)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        self._choose(name)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._choose("Easy")
                elif event.key == pygame.K_2:
                    self._choose("Medium")
                elif event.key == pygame.K_3:
                    self._choose("Hard")
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self._choose("Exit")

    def handle_input(self):
        pass  # all input is event-driven; kept because main.py calls it

    def _choose(self, name):
        if name == "Exit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            self.start_round(name)

    def _whack(self, pos):
        # Task 1 fix: a click can only ever resolve to ONE hole,
        # the nearest one whose circle contains the click.
        target = None
        best = float("inf")
        for hole in self.holes:
            d = hole.distance_to(pos)
            if d <= hole.radius and d < best:
                best = d
                target = hole

        if target is not None and target.active:
            self.score += 1
            target.deactivate()
            self._play(self.hit_sound)
        else:
            self._play(self.miss_sound)

    # ---------- update / render ----------
    def update(self):
        if self.state != "playing":
            return
        now = pygame.time.get_ticks()
        if now - self.start_time >= ROUND_MS:
            self.end_round()
            return

        for hole in self.holes:
            hole.update(now)

        cfg = DIFFICULTIES[self.difficulty]
        if now - self.last_spawn >= cfg["spawn_ms"]:
            idle = [h for h in self.holes if not h.active]
            if idle:
                random.choice(idle).activate(now, cfg["up_ms"])
            self.last_spawn = now

    def render(self, screen):
        for hole in self.holes:
            hole.draw(screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        secs = math.ceil(self.time_left_ms() / 1000)
        time_text = self.font.render(f"Time: {secs}", True, (255, 255, 255))
        screen.blit(score_text, (20, 15))
        screen.blit(time_text, (self.width - time_text.get_width() - 20, 15))

        if self.state == "game_over":
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.big_font.render("Game Over", True, (255, 220, 80))
        final = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        prompt = self.small_font.render("Play again? Choose a difficulty", True, (220, 220, 220))
        screen.blit(title, ((self.width - title.get_width()) // 2, 160))
        screen.blit(final, ((self.width - final.get_width()) // 2, 245))
        screen.blit(prompt, ((self.width - prompt.get_width()) // 2, 300))

        for name, rect in self.buttons.items():
            hover = rect.collidepoint(pygame.mouse.get_pos())
            color = (90, 160, 90) if hover else (60, 120, 60)
            if name == "Exit":
                color = (170, 70, 70) if hover else (130, 50, 50)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            label = self.small_font.render(name, True, (255, 255, 255))
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))

        hint = self.small_font.render("Keys: 1 Easy, 2 Medium, 3 Hard, Esc Exit", True, (200, 200, 200))
        screen.blit(hint, ((self.width - hint.get_width()) // 2, 490))