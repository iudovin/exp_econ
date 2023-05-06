from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_instruction_3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(
            choices=[
                ['A', 'Ничего'], 
                ['B', 'Оно ограничено, но неизвестно игрокам'], 
                ['C', 'Оно бесконечно'], 
     ['D', 'Оно известно и видно в начале каждого раунда']],
            label='Что вам известно о количестве риса на всех игроков? ',
            widget=widgets.RadioSelect
        ) 
    q2 = models.StringField(
            choices=[
                ['A', 'От купленного в этом раунде риса'], 
                ['B', 'От фактически полученного риса после распределения на всех игроков'], 
                ['C', 'От того риса, который «съедается» в раунде'], 
                ['D', 'От риса, запасённого за все раунды']],
            label='Как будет высчитываться функция полезности за раунд?',
            widget=widgets.RadioSelect
        )
    q3 = models.StringField(
            choices=[
                ['A', 'Не больше, чем заявленного на покупку'], 
                ['B', 'Не больше, чем фактически полученного в раунде'], 
                ['C', 'Не больше, чем имеется в запасах за все раунды + фактически получено сегодня'], 
                ['D', 'Не больше, чем позволяет купить бюджет']],
            label='Сколько риса можно съесть в раунде?',
            widget=widgets.RadioSelect
        )
    q4 = models.StringField(
            choices=[
                ['A', '7 раундов по 1.5 минуты'], 
                ['B', '7 раундов, 1 минута на покупку риса, и 1 минута на поедание'], 
                ['C', 'Первый раунд - 2.5 минуты и ещё 6 раундов по 1.5 минуты, и таких 3 одинаковых этапа'], 
                ['D', '7 раундов. В первом - 1.5 минуты на покупку риса, и 2 минуты на поедание, в остальных – 1 минута на покупку и 1 минута на поедание']],
            label='Сколько раундов какой длительности будет играться этот круг?',
            widget=widgets.RadioSelect
        )
    
def q1_error_message(player, q1):
    if q1 != 'D':
        return "Выбран неверный ответ. Подумайте еще"
def q2_error_message(player, q2):
    if q2 != 'C':
        return "Выбран неверный ответ. Подумайте еще"
def q3_error_message(player, q3):
    if q3 != 'C':
        return "Выбран неверный ответ. Подумайте еще"
def q4_error_message(player, q4):
    if q4 != 'D':
        return "Выбран неверный ответ. Подумайте еще"


# PAGES
class Instruction_3(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']


page_sequence = [Instruction_3]
