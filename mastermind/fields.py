from django.db import models


class ColorField(models.CharField):

    class ColorChoices(models.TextChoices):
        RED = 'red', 'Red'
        BLUE = 'blue', 'Blue'
        WHITE = 'white', 'White'
        GREEN = 'green', 'Green'
        BLACK = 'black', 'Black'
        YELLOW = 'yellow', 'Yellow'

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.ColorChoices.choices
        kwargs['max_length'] = 6
        super().__init__(*args, **kwargs)
