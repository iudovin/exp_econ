from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_final'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES

class Results(Page):
   @staticmethod
   def vars_for_template(player: Player):
       group = player.group
       return dict(
           n_players=len(group.get_players()),
           names=[p.participant.name for p in group.get_players()],
           results=[p.participant.result for p in group.get_players()]
       )


page_sequence = [Results]
