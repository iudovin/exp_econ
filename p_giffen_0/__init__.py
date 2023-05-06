from otree.api import *
import numpy as np


doc = """
Модификация 0. Кол-во риса неограничено
"""

# TODO добавить таймаут-переменную


class C(BaseConstants):
    NAME_IN_URL = 'p_giffen_0'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 7
    PLAYER_INCOME = 300000
    a = 20
    b = 1500




def utility_function(x_meat, x_rice):
    return 0 if (x_meat + x_rice < C.b or x_meat*x_rice < 0) else max(0, np.log(x_meat+x_rice-C.b) + C.a*np.log(1 + x_meat))


def current_rice_price(round_num):
    a = [0] + list(np.round(np.linspace(72, 190, C.NUM_ROUNDS)))
    return a[round_num]

def eq_rice_amount(round_num, p_meat):
    return (
        C.b+(C.PLAYER_INCOME-current_rice_price(round_num)*C.b) / (C.a+1) * 
        (p_meat-current_rice_price(round_num)*(C.a+1)) / current_rice_price(round_num) / (p_meat-current_rice_price(round_num))
    )

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    p_meat = models.FloatField(initial=320)
    p_rice = models.FloatField(initial=70)
    p_rice_d = models.FloatField(initial=70)
    eq_rice = models.FloatField(initial=0)


class Player(BasePlayer):
    x_rice = models.FloatField(initial=0, min=0)
    x_rice_d = models.FloatField(initial=0, min=0)
    max_rice = models.FloatField(initial=0)
    x_meat = models.FloatField(initial=0)
    utility = models.FloatField(initial=0)
    utility_d = models.FloatField(initial=0)
    result = models.FloatField(initial=0)
    result_d = models.FloatField(initial=0)


# PAGES

class StartPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.p_rice = current_rice_price(group.round_number)
        group.eq_rice = eq_rice_amount(group.round_number, group.p_meat)
        for p in group.get_players():
            p.max_rice = round(C.PLAYER_INCOME / group.p_rice, 2)


class BuyPage(Page):
    @staticmethod
    def get_timeout_seconds(group: Group):
        return 90 if group.round_number==1 else 60
    
    def live_method(player, x):
        if x < 0:
            return
        group = player.group
        player.x_rice = min(x, player.max_rice)
        player.x_meat = max(0, (C.PLAYER_INCOME - player.x_rice*group.p_rice) / group.p_meat)
        player.utility = utility_function(player.x_meat, player.x_rice)
        response = dict(rice_amt=player.x_rice, meat_amt=player.x_meat, utility=player.utility)
        return {player.id_in_group: response}
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            group = player.group
            
            L = (group.p_meat * C.b - C.PLAYER_INCOME)/(group.p_meat - group.p_rice)
            R = group.eq_rice
            
            player.x_rice = np.random.uniform(.75*L+.25*R, .25*L+.75*R)
            player.x_meat = (C.PLAYER_INCOME - player.x_rice*group.p_rice) / group.p_meat
            player.utility = utility_function(player.x_meat, player.x_rice)
    


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.p_rice_d = round(group.p_rice, 2) 
        for p in group.get_players():
            p.result = p.utility 
            if p.round_number > 1:
                p_prev = p.in_round(p.round_number - 1)
                p.result += p_prev.result
            p.x_rice_d = round(p.x_rice, 2)
            p.utility_d = round(p.utility, 2) 
            p.result_d = round(p.result, 2)
            
            p.payoff = p.result * 1e2
            p.participant.result = p.result 
            


class Results(Page):
    timeout_seconds = 10


page_sequence = [StartPage, BuyPage, ResultsWaitPage, Results]
