import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window

# Mobile preview size
Window.size = (360, 640)


class GameScreen(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background
        self.background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size=Window.size,
            pos=(0, 0)
        )
        self.add_widget(self.background)

        # Egg
        self.egg = Image(
            source="assets/egg.png",
            size_hint=(None, None),
            size=(60, 60),
            pos=(180, 550)
        )
        self.add_widget(self.egg)

        # Bowl
        self.bowl = Image(
            source="assets/bowl.png",
            size_hint=(None, None),
            size=(120, 60),
            pos=(120, 50)
        )
        self.add_widget(self.bowl)

        # Instructions
        self.instruction_label = Label(
            text="Tap Anywhere To Drop Egg",
            font_size=22,
            pos=(0, 180)
        )
        self.add_widget(self.instruction_label)

        # Game state
        self.score = 0
        self.lives = 3
        self.game_over = False

        # Bowl speed
        self.speed = 4

        # Egg physics
        self.egg_falling = False
        self.egg_speed = 0

        # Score label
        self.score_label = Label(
            text="Score: 0",
            font_size=24,
            pos=(0, 280)
        )
        self.add_widget(self.score_label)

        # Lives label
        self.lives_label = Label(
            text="Lives: 3",
            font_size=24,
            pos=(0, 250)
        )
        self.add_widget(self.lives_label)

        # Play Again button
        self.restart_button = Button(
            text="PLAY AGAIN",
            size_hint=(None, None),
            size=(160, 55),
            pos=(100, 200),
            opacity=0
        )

        self.restart_button.bind(on_press=self.restart_game)
        self.add_widget(self.restart_button)

        Clock.schedule_interval(self.update, 1 / 60)

        Clock.schedule_once(
            lambda dt: self.reset_egg(),
            0.1
        )

    def on_touch_down(self, touch):

        if not self.egg_falling and not self.game_over:

            self.egg_falling = True
            self.egg_speed = 0

            self.instruction_label.opacity = 0

        return super().on_touch_down(touch)

    def reset_egg(self):

        egg_width = self.egg.width

        max_x = max(
            20,
            int(Window.width - egg_width - 20)
        )

        random_x = random.randint(20, max_x)

        self.egg.pos = (random_x, 550)

        self.egg_falling = False
        self.egg_speed = 0

        # Random bowl speed and direction
        direction = random.choice([-1, 1])

        self.speed = direction * random.randint(
            3,
            min(8, 3 + self.score // 2)
        )

    def restart_game(self, instance):

        self.score = 0
        self.lives = 3

        self.game_over = False

        self.score_label.text = "Score: 0"
        self.lives_label.text = "Lives: 3"

        self.instruction_label.text = "Tap Anywhere To Drop Egg"
        self.instruction_label.opacity = 1

        self.restart_button.opacity = 0

        self.reset_egg()

    def update(self, dt):

        # Move bowl
        x = self.bowl.x + self.speed

        if x <= 0:
            self.speed = abs(self.speed)

        if x + self.bowl.width >= Window.width:
            self.speed = -abs(self.speed)

        self.bowl.x = x

        # Egg falling
        if self.egg_falling and not self.game_over:

            self.egg_speed += 0.5

            self.egg.y -= self.egg_speed

            if self.egg.y <= self.bowl.y + self.bowl.height:

                egg_center = (
                    self.egg.x + self.egg.width / 2
                )

                # Egg caught
                if self.bowl.x <= egg_center <= self.bowl.x + self.bowl.width:

                    self.score += 1

                    self.score_label.text = (
                        f"Score: {self.score}"
                    )

                # Egg missed
                else:

                    self.lives -= 1

                    self.lives_label.text = (
                        f"Lives: {self.lives}"
                    )

                    if self.lives <= 0:

                        self.game_over = True

                        self.score_label.text = (
                            f"GAME OVER\nScore: {self.score}"
                        )

                        self.restart_button.opacity = 1

                if not self.game_over:
                    self.reset_egg()


class EggGame(App):

    def build(self):
        return GameScreen()


EggGame().run()