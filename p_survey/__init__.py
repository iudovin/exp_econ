from otree.api import *


doc = """
Анкета (игроки вводят ФИО)
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(label='Введите фамилию и имя')


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['name']
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.name = player.name



page_sequence = [Survey]
