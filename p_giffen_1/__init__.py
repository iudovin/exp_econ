from otree.api import *
import numpy as np


doc = """
Модификация 1. Участники разбиваются на 2 группы. В первой выбираем delta=(0.99, 0.89, 1.01). Во второй (1.01, 0.99, 0.89)
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_giffen_1'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_DELTA = 7
    NUM_ROUNDS = 3 * ROUNDS_PER_DELTA
    PLAYER_INCOME = 300000
    a = 20
    b = 1500


def current_delta(player):
    _delta = [
        [0] + [0.99] * C.ROUNDS_PER_DELTA + [0.89] * C.ROUNDS_PER_DELTA + [1.01] * C.ROUNDS_PER_DELTA,
        [0] + [1.01] * C.ROUNDS_PER_DELTA + [0.99] * C.ROUNDS_PER_DELTA + [0.89] * C.ROUNDS_PER_DELTA
    ]
    return _delta[player.id_in_group % 2][player.group.round_number]



def utility_function(x_meat, x_rice):
    return 0 if (x_meat + x_rice < C.b or x_meat*x_rice < 0) else max(0, np.log(x_meat+x_rice-C.b) + C.a*np.log(1+x_meat))


def current_rice_price(round_num):
    a = [0] + list(np.linspace(72, 190, C.ROUNDS_PER_DELTA)) + list(np.linspace(72, 190, C.ROUNDS_PER_DELTA)) + list(np.linspace(72, 190, C.ROUNDS_PER_DELTA))
    return a[round_num]


def eq_rice_amount(round_num, p_meat):
    return (
        C.b+(C.PLAYER_INCOME-current_rice_price(round_num)*C.b) / (C.a+1) * 
        (p_meat-current_rice_price(round_num)*(C.a+1)) / current_rice_price(round_num) / (p_meat-current_rice_price(round_num))
    )


def current_rice_amount(player, round_num, n_players, p_meat):
    return eq_rice_amount(round_num, p_meat) * n_players * current_delta(player)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    n_players_0 = models.IntegerField()
    n_players_1 = models.IntegerField()
    
    rice_left_0 = models.FloatField(initial=0)
    rice_left_1 = models.FloatField(initial=0)
    rice_bought_0 = models.FloatField(initial=0)
    rice_bought_1 = models.FloatField(initial=0)
    p_meat = models.FloatField(initial=320)
    p_rice = models.FloatField(initial=70)
    p_rice_d = models.FloatField(initial=70)
    eq_rice = models.FloatField(initial=0)
    #L = models.FloatField()
    #R = models.FloatField()


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
        
        group.n_players_0 = len(p) // 2
        group.n_players_1 = (len(p) + 1) // 2
        
        group.p_rice = current_rice_price(group.round_number)        
        group.rice_left_0 = current_rice_amount(
            p[0], group.round_number, group.n_players_0, group.p_meat
        )
        group.rice_left_1 = current_rice_amount(
            p[1], group.round_number, group.n_players_1, group.p_meat
        )
        group.eq_rice = eq_rice_amount(group.round_number, group.p_meat)
        for pl in group.get_players():
            pl.max_rice = round(C.PLAYER_INCOME / group.p_rice, 2)


class BuyPage(Page):
    timeout_seconds = 60
    
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
            
            #group.L = .75*L+.25*R
            #group.R = .25*L+.75*R
            
            player.x_rice = np.random.uniform(.75*L+.25*R, .25*L+.75*R)
            player.x_meat = (C.PLAYER_INCOME - player.x_rice*group.p_rice) / group.p_meat
            player.utility = utility_function(player.x_meat, player.x_rice)



class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.p_rice_d = round(group.p_rice,2)
        for p in group.get_players():
            if p.id_in_group % 2:
                group.rice_bought_1 += p.x_rice
            else:
                group.rice_bought_0 += p.x_rice
        for p in group.get_players():
            p.x_rice_actual = p.x_rice
            if p.id_in_group % 2:
                if group.rice_bought_1 > group.rice_left_1:
                    p.x_rice_actual *= group.rice_left_1 / group.rice_bought_1
            else:
                if group.rice_bought_0 > group.rice_left_0:
                    p.x_rice_actual *= group.rice_left_0 / group.rice_bought_0
            p.utility = utility_function(p.x_meat, p.x_rice_actual)
            p.result = p.utility 
            if p.round_number > 1:
                p_prev = p.in_round(p.round_number - 1)
                p.result += p_prev.result
            p.x_rice_d = round(p.x_rice,2)
            p.x_rice_actual_d = round(p.x_rice_actual,2)
            p.utility_d = round(p.utility,2)
            p.result_d = round(p.result,2)
            
            p.payoff = p.result * 1e2
            p.participant.result = p.result
    


class Results(Page):
    timeout_seconds = 10
    
class BlockResults(Page):
    timeout_seconds = 20
    
    @staticmethod
    def is_displayed(player):
        return True if (player.round_number % C.ROUNDS_PER_DELTA == 0) else False
        
    @staticmethod
    def vars_for_template(player):
        return dict(step=(player.round_number-1) // C.ROUNDS_PER_DELTA + 1)


page_sequence = [StartPage, BuyPage, ResultsWaitPage, Results, BlockResults]
