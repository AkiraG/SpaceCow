import pygame
import random
import math
from typing import List

ANIMATOR_EVENT = pygame.USEREVENT


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_filename, **kwargs):
        super().__init__()
        self._position_x = kwargs.get('position_x', 0)
        self._position_y = kwargs.get('position_y', 0)
        self.image = pygame.image.load(image_filename).convert()
        self.rect = self.image.get_rect()

    def update_position(self):
        self.rect.x = self._position_x
        self.rect.y = self._position_y

    @property
    def position_x(self):
        return self._position_x

    @property
    def position_y(self):
        return self._position_y


class Animation:
    def __init__(self, name):
        self._name = name
        self._frame_number = 0
        self._fps = 15
        self._animation_frames = []

    def get_frame_count(self):
        return len(self._animation_frames) - 1

    @property
    def name(self):
        return self._name

    @property
    def current_frame(self):
        return self._animation_frames[self._frame_number]

    @property
    def animation_frames(self):
        return self._animation_frames

    @animation_frames.setter
    def animation_frames(self, frames: List):
        self._animation_frames = frames

    def next_frame(self):
        if self._frame_number < self.get_frame_count():
            self._frame_number += 1
        else:
            self._frame_number = 0

    def previous_frame(self):
        if self._frame_number > 0:
            self._frame_number -= 1
        else:
            self._frame_number = self.get_frame_count()

    def reset_animation(self):
        self._frame_number = 0

    def is_ended(self):
        return self._frame_number == self.get_frame_count()


class Animator:
    _instances = 0

    def __init__(self, sprite_sheet, frame_dimension, fps=15):
        self.sprite_sheet = sprite_sheet
        self.animations = {}
        self.FPS = 1000 // fps
        self._current_animation = None
        self.sprite_sheet_frames = []
        self.animation_event = ANIMATOR_EVENT + self.get_instance_id()
        self.extract_frames(frame_dimension)
        pygame.time.set_timer(self.animation_event, self.FPS)

    @classmethod
    def get_instance_id(cls):
        cls._instances += 1
        return cls._instances

    def image_cut(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        rect = pygame.Rect(x, y, width, height)
        image.blit(self.sprite_sheet, (0, 0), rect)
        image.set_colorkey((0, 0, 0))
        return image

    def extract_frames(self, dimensions):
        total_width = self.sprite_sheet.get_width()
        total_height = self.sprite_sheet.get_height()
        columns = total_width // dimensions[0]
        rows = total_height // dimensions[1]

        for y in range(rows):
            for x in range(columns):
                frame_cut = self.image_cut(x * dimensions[0],
                                           y * dimensions[1],
                                           dimensions[0],
                                           dimensions[1])
                self.sprite_sheet_frames.append(frame_cut)

    def create_animation(self, animation_name, frame_address, repeat=1):
        animation = Animation(animation_name)
        animation.animation_frames = self.sprite_sheet_frames[frame_address[0]:frame_address[1] + 1] * repeat
        self.animations[animation_name] = animation

    @property
    def display_frame(self):
        return self._current_animation.current_frame

    @property
    def animation(self):
        return self._current_animation

    @animation.setter
    def animation(self, animation_name):
        if self._current_animation is None:
            self._current_animation = self.animations[animation_name]
        elif self._current_animation.name != animation_name:
            self._current_animation = self.animations[animation_name]
            self._current_animation.reset_animation()

    def update_animation(self):
        event = pygame.event.get(self.animation_event)
        if len(event) > 0:
            self.animation.next_frame()


class SoundEffect:
    _instances = 5

    def __init__(self, mixer, files):
        self._add_instance()
        self._sound_mixer = mixer
        self._sounds = {name: self._sound_mixer.Sound(file) for name, file in files.items()}
        self._channel = self._sound_mixer.Channel(self._get_instance())
        self._channel.set_volume(0.2)

    def play_sound(self, sound_name, loops=0, maxtime=0, fade_ms=0):
        self._channel.play(self._sounds[sound_name], loops, maxtime, fade_ms)

    def is_busy(self):
        return self._channel.get_busy()

    @classmethod
    def _get_instance(cls):
        return cls._instances

    @classmethod
    def _add_instance(cls):
        cls._instances += 1


class Farmer(GameObject):
    def __init__(self, spritesheet, **kwargs):
        super().__init__(spritesheet, **kwargs)
        self.speed = 0
        self.movement = {'left': False, 'right': False}
        self._action = False
        self.animator = Animator(sprite_sheet=self.image, frame_dimension=(64, 80))

        self.sound = SoundEffect(mixer=kwargs.get('mixer'),
                                 files={'tie': 'sound/tiedcow.wav',
                                        'walk': 'sound/walk.wav',
                                        'push': 'sound/push.wav'})

        self.animator.create_animation(animation_name='left', frame_address=(0, 12))
        self.animator.create_animation(animation_name='right', frame_address=(13, 25))
        self.animator.create_animation(animation_name='tie', frame_address=(26, 34))
        self.animator.create_animation(animation_name='push', frame_address=(35, 38), repeat=3)
        self.animator.create_animation(animation_name='idle', frame_address=(0, 0))

        self.animator.animation = 'idle'

        self.image = self.animator.display_frame
        self.rect = self.animator.display_frame.get_rect()

    def update(self):
        if not self._action:
            self.update_movement()
            self.update_position()
        elif self.animator.animation.is_ended():
            self._action = False
        self.update_animation()

    def update_movement(self):
        if not self.movement['left'] and not self.movement['right']:
            self.speed = 0
            self.animator.animation = 'idle'
        elif self.movement['left'] and not self.movement['right']:
            self.animator.animation = 'left'
            self.speed = -3
        elif not self.movement['left'] and self.movement['right']:
            self.animator.animation = 'right'
            self.speed = 3

        if self.speed != 0 and not self.sound.is_busy():
            self.sound.play_sound('walk')

        self._position_x += self.speed

    def update_animation(self):
        self.animator.update_animation()
        self.image = self.animator.display_frame

    def rescue_cow(self, cow):
        self._action = True
        self.animator.animation = 'push'
        self.sound.play_sound('push')

    def tie_cow(self, cow):
        self._action = True
        self.animator.animation = 'tie'
        self.sound.play_sound('tie')


class Cow(GameObject):
    def __init__(self, spritesheet, **kwargs):
        super().__init__(spritesheet, **kwargs)
        self._is_hunted = False
        self.animator = Animator(self.image, (128, 128))

        self.animator.create_animation('idle', (12, 17))
        self.animator.create_animation('idle_tied', (29, 34))
        self.animator.animation = 'idle'
        self.image = self.animator.display_frame
        self.rect = self.animator.display_frame.get_rect()

        self.sound = "sound_class"

    @property
    def is_hunted(self):
        return self._is_hunted

    @is_hunted.setter
    def is_hunted(self, value):
        self._is_hunted = value

    def update(self):
        self.update_animation()

    def update_movement(self):
        pass

    def update_animation(self):
        self.animator.update_animation()
        self.image = self.animator.display_frame


class Ship(GameObject):
    def __init__(self, spritesheet, **kwargs):
        super().__init__(spritesheet, **kwargs)
        self._speed = 1
        self.movement = {'left': False, 'right': False}
        self._action = False

        self.animator = Animator(sprite_sheet=self.image, frame_dimension=(128, 128))
        self.animator.create_animation(animation_name='abducting', frame_address=(36, 41))
        self.animator.create_animation(animation_name='idle', frame_address=(0, 10))
        self.animator.animation = 'idle'

        self.image = self.animator.display_frame
        self.rect = self.animator.display_frame.get_rect()

        self.target = None
        # self.sound = "sound_class" TODO implement sound effects

    def update(self):
        if not self._action:
            self.update_movement()
            self.update_position()
        self.update_animation()

    def search_cow(self, cow_list):
        free_cows = [cow for cow in cow_list if not cow.is_hunted]
        random.shuffle(free_cows)

        self.target = free_cows[0]
        self.target.is_hunted = True

    def update_movement(self):
        if self._position_x > self.target.position_x:
            self.movement['left'] = True
        else:
            self.movement['right'] = True
        pass

    def update_animation(self):
        pass
