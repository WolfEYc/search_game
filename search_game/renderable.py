from abc import ABC, abstractmethod
from enum import Enum

import pygame


class RenderLayer(Enum):
    GRID = 0
    OBJECTS = 1
    UI = 2


class Renderable(ABC):
    @abstractmethod
    def render(self, screen: pygame.Surface): ...


RenderDict = dict[RenderLayer, list[Renderable]]


def generate_renderable_list() -> RenderDict:
    return {k: [] for k in RenderLayer}
