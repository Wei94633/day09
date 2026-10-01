import builtins
import sys
from types import SimpleNamespace
import pygame
PAPER, INK, SAGE, PINK = ('#f7f3e8', '#34475b', '#a7b7a0', '#d89b8c')

class PygameUI:

    def __init__(self):
        self.screen = None
        self.message = 'Take your time. One letter, one little step.'
        self.buffer, self.focus = ('', False)
        self.state = {}

    def reset(self):
        self.message = 'Take your time. One letter, one little step.'
        self.buffer, self.focus = ('', False)
        self.state = {}

    def open(self):
        if self.screen is not None:
            return
        pygame.init()
        pygame.display.set_caption('Word Walk')
        self.screen = pygame.display.set_mode((960, 760))
        self.clock = pygame.time.Clock()
        path = pygame.font.match_font('segoeui,arial')
        self.fonts = {size: pygame.font.Font(path, size) for size in (16, 20, 24, 34, 40)}
        self.entry = pygame.Rect(60, 636, 430, 48)
        self.submit = pygame.Rect(510, 636, 160, 48)
        self.hint = pygame.Rect(690, 636, 210, 48)
        self.restart = pygame.Rect(310, 636, 340, 48)
        self.keys = {}
        for row, letters in enumerate(('QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM')):
            left = (960 - len(letters) * 58) // 2
            for col, letter in enumerate(letters):
                self.keys[letter.lower()] = pygame.Rect(left + col * 58, 456 + row * 54, 48, 44)

    def print(self, *values, **kwargs):
        builtins.print(*values, **kwargs)
        if kwargs.get('file') is sys.stderr:
            return
        text = ' '.join((str(v) for v in values))
        if text.startswith('guessed letters:') or text.endswith('penalties'):
            return
        self.message = text
        if text == 'you lose!':
            self.message = 'you lose!'
        elif text.startswith('the correct answer is'):
            self.message = 'you lose! / ' + text

    def text(self, value, position, size=20, center=False, color=INK, max_width=None):
        image = self.fonts[size].render(value, True, color)
        if max_width and image.get_width() > max_width:
            scale = max_width / image.get_width()
            image = pygame.transform.smoothscale(image, (max_width, max(1, int(image.get_height() * scale))))
        rect = image.get_rect(center=position) if center else image.get_rect(topleft=position)
        self.screen.blit(image, rect)

    def button(self, rect, label, color, disabled=False):
        pygame.draw.rect(self.screen, '#e8e3d8' if disabled else color, rect, border_radius=10)
        if rect.collidepoint(pygame.mouse.get_pos()) and (not disabled):
            pygame.draw.rect(self.screen, INK, rect, 1, border_radius=10)
        self.text(label, rect.center, center=True, color='#9a9a93' if disabled else INK)

    def illustration(self):
        s, d = (self.screen, pygame.draw)
        d.circle(s, '#e8c786', (752, 148), 29)
        d.ellipse(s, '#e5e9dd', (60, 210, 490, 170))
        d.ellipse(s, '#d7dfcf', (435, 190, 470, 190))
        d.rect(s, PAPER, (0, 325, 960, 65))
        d.line(s, INK, (65, 324), (895, 324), 2)
        d.ellipse(s, '#cbd3c2', (410, 310, 145, 25))
        d.lines(s, INK, False, [(525, 303), (563, 292), (573, 265), (566, 255)], 4)
        d.ellipse(s, '#fffcf4', (433, 234, 94, 88))
        d.ellipse(s, INK, (433, 234, 94, 88), 3)
        ears = [(428, 222), (430, 170), (458, 190), (500, 190), (530, 170), (533, 222)]
        d.polygon(s, '#fffcf4', ears)
        d.lines(s, INK, False, ears, 3)
        d.ellipse(s, '#fffcf4', (428, 187, 106, 80))
        d.ellipse(s, INK, (428, 187, 106, 80), 3)
        for x in (451, 509):
            if self.game.finished and self.game.won:
                d.lines(s, INK, False, [(x - 5, 226), (x, 221), (x + 5, 226)], 2)
            else:
                d.circle(s, INK, (x, 224), 4)
        d.polygon(s, PINK, [(476, 237), (485, 237), (481, 243)])
        d.lines(s, INK, False, [(472, 249), (481, 245), (489, 249)], 2)
        for x in (415, 526):
            d.line(s, INK, (x, 234), (x + 20, 237), 2)
            d.line(s, INK, (x, 248), (x + 20, 243), 2)
        for x in (443, 512):
            d.ellipse(s, '#eed3c6', (x, 240, 17, 7))
        for x in (455, 503):
            d.line(s, INK, (x, 296), (x, 318), 2)
        self.text('one letter,', (112, 154), 24)
        self.text('one little step.', (112, 185), 24)
        remaining = max(0, self.game.limit - self.game.penalty)
        for i in range(12):
            d.ellipse(s, SAGE if i < round(12 * remaining / self.game.limit) else '#e6e0d4', (305 + i * 30, 343, 20, 10))

    def draw(self, finished=False):
        s = self.state
        word = s['word']
        hidden = s['hidden_word']
        limit = s['args'].penalties
        won = finished and (s.get('guess') == word or '-' not in hidden)
        self.game = SimpleNamespace(limit=max(1, limit), penalty=s['penalty'], finished=finished, won=won)
        self.screen.fill(PAPER)
        self.text('Word Walk', (48, 26), 34)
        self.text('A LITTLE CAT, A LITTLE WORD', (606, 40), 16)
        best = s['best_attempts'] if s['best_attempts'] is not None else '—'
        self.text(f"Penalties {s['penalty']} / {limit}   ·   Attempts {s['attempts']}   ·   Previous best {best}", (480, 98), center=True)
        self.illustration()
        displayed = word if finished else ''.join(hidden)
        self.text(' '.join(displayed), (480, 390), 40, True, max_width=860)
        self.text(self.message, (480, 427), 20, True, max_width=870)
        for letter, rect in self.keys.items():
            used = letter in s['guessed_letters']
            color = SAGE if letter in hidden else PINK if used else '#ede8db'
            self.button(rect, letter.upper(), color, finished)
        if finished:
            self.button(self.restart, 'Play again / Enter', SAGE)
        else:
            pygame.draw.rect(self.screen, '#fffcf4', self.entry, border_radius=10)
            pygame.draw.rect(self.screen, SAGE if self.focus else '#ded7c8', self.entry, 2, border_radius=10)
            self.text(self.buffer or 'Type a guess, then press Enter', (74, 649), max_width=400)
            self.button(self.submit, 'Submit', SAGE)
            self.button(self.hint, 'Hint (-2)', '#ead5bd')
        self.text('Wrong letter: +1 penalty | Wrong word: +5 | Hint: +2 | Repeats count', (480, 714), 16, True)
        pygame.display.flip()

    def input(self, prompt, state):
        self.open()
        self.state = state
        self.buffer = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.submit.collidepoint(event.pos):
                        return self.buffer
                    if self.hint.collidepoint(event.pos):
                        return 'hint'
                    self.focus = self.entry.collidepoint(event.pos)
                    for letter, rect in self.keys.items():
                        if rect.collidepoint(event.pos):
                            return letter
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.buffer
                    if event.key == pygame.K_ESCAPE:
                        self.focus = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.buffer = self.buffer[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        if self.focus:
                            self.buffer += event.unicode
                        else:
                            return event.unicode
            self.draw()
            self.clock.tick(60)

    def finish(self, state):
        self.open()
        self.state, self.buffer = (state, '')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart.collidepoint(event.pos):
                        return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return True
            self.draw(finished=True)
            self.clock.tick(60)
