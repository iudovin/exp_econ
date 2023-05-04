from otree.api import *
import numpy as np


doc = """
Модификация 2. Информация известна
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_giffen_2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    PLAYER_INCOME = 300000
    a = 20
    b = 1500
    delta = 0.99


def utility_function(x_meat, x_rice):
    return 0 if (x_meat + x_rice < C.b or x_meat*x_rice < 0) else max(0, np.log(x_meat+x_rice-C.b) + C.a*np.log(1+x_meat))


def current_rice_price(round_num):
    a = [0] + list(np.linspace(72, 190, C.NUM_ROUNDS))
    return a[round_num]


def eq_rice_amount(round_num, p_meat):
    return (
        C.b+(C.PLAYER_INCOME-current_rice_price(round_num)*C.b) / (C.a+1) * 
        (p_meat-current_rice_price(round_num)*(C.a+1)) / current_rice_price(round_num) / (p_meat-current_rice_price(round_num))
    )


def current_rice_amount(round_num, n_players, p_meat):
    return eq_rice_amount(round_num, p_meat) * n_players * C.delta



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):    
    rice_left = models.FloatField(initial=0)
    rice_left_d = models.FloatField(initial=0)
    rice_bought = models.FloatField(initial=0)
    p_meat = models.FloatField(initial=320)
    p_rice = models.FloatField(initial=70)
    p_rice_d = models.FloatField(initial=70)
    eq_rice = models.FloatField(initial=0)


class Player(BasePlayer):
    x_rice = models.FloatField(initial=0)
    x_rice_d = models.FloatField(initial=0)
    x_rice_actual = models.FloatField(initial=0)
    x_rice_actual_d = models.FloatField(initial=0)
    x_meat = models.FloatField(initial=0)
    max_rice = models.FloatField(initial=0)
    utility = models.FloatField(initial=0)
    utility_d = models.FloatField(initial=0)
    result = models.FloatField(initial=0)
    result_d = models.FloatField(initial=0)


# PAGES
class StartPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        p = group.get_players()
        group.p_rice = current_rice_price(group.round_number)     
        group.rice_left = current_rice_amount(group.round_number, len(p), group.p_meat)
        group.rice_left_d = round(group.rice_left, 2)
        group.eq_rice = eq_rice_amount(group.round_number, group.p_meat)
        for pl in p:
            pl.max_rice = round(C.PLAYER_INCOME / group.p_rice, 2)


class BuyPage(Page):
    timeout_seconds = 90
    
    def live_method(player, x):
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
            group.rice_bought += p.x_rice
        for p in group.get_players():
            p.x_rice_actual = p.x_rice
            if group.rice_bought > group.rice_left:
                p.x_rice_actual *= group.rice_left / group.rice_bought
            p.utility = utility_function(p.x_meat, p.x_rice_actual)
            p.result = p.utility 
            if p.round_number > 1:
                p_prev = p.in_round(p.round_number - 1)
                p.result += p_prev.result
            
            p.x_rice_d = round(p.x_rice, 2)
            p.x_rice_actual_d = round(p.x_rice_actual, 2)
            p.utility_d = round(p.utility, 2)
            p.result_d = round(p.result, 2)


class Results(Page):
    timeout_seconds = 10


page_sequence = [StartPage, BuyPage, ResultsWaitPage, Results]
