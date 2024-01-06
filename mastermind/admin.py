from django.contrib import admin

from mastermind.models import Game, Guess


class GuessInline(admin.TabularInline):
    model = Guess


class GameAdmin(admin.ModelAdmin):
    inlines = [GuessInline]


admin.site.register(Game, GameAdmin)
