from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_instruction_0'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):    
    q1 = models.StringField(
        choices=[
            ['A', '1000'], 
            ['B', '1500'], 
            ['C', '1200'], 
            ['D', '30 000']],
        label='Какой минимум ккал за день надо набрать?',
        widget=widgets.RadioSelect
    ) 
    q2 = models.StringField(
        choices=[
            ['A', 'Ввести количество денег, которое планируете потратить на рис, а затем нажать кнопку "Проверить"'], 
            ['B', 'Ввести количество мяса, которое планируем приобрести, затем нажать кнопку "Купить"'], 
            ['C', 'Ввести количество риса, которое планируем приобрести, затем нажать кнопку "Проверить"'], 
            ['D', 'Ввести количество риса, которое планируем приобрести, затем нажать кнопку "Купить"']],
        label='Как посчитать функцию полезности перед покупкой?',
        widget=widgets.RadioSelect
    )
    q3 = models.StringField(
        choices=[
            ['A', '300 000 у.е.'], 
            ['B', '1500 у.е.'], 
            ['C', '10 000 у.е.'], 
            ['D', '30 000 у.е.']],
        label='Каким бюджетом на день вы располагаете?',
        widget=widgets.RadioSelect
    )
    q4 = models.StringField(
        choices=[
            ['A', '10 раундов по 1.5 минуты'], 
            ['B', '7 раундов, первый длится 2 минуты, остальные – по 1 минуте'], 
            ['C', 'Первый раунд - 5 минут и ещё 6 раундов по 2 минуты'], 
            ['D', 'Первые 2 раунда по 2.5 минуты и ещё 6 раундов по 1.5 минуты']],
        label='Сколько раундов какой длительности будет играться этот круг?',
        widget=widgets.RadioSelect
    )
    

def q1_error_message(player, q1):
    if q1 != 'B':
        return "Выбран неверный ответ. Подумайте еще"
def q2_error_message(player, q2):
    if q2 != 'C':
        return "Выбран неверный ответ. Подумайте еще"
def q3_error_message(player, q3):
    if q3 != 'A':
        return "Выбран неверный ответ. Подумайте еще"
def q4_error_message(player, q4):
    if q4 != 'B':
        return "Выбран неверный ответ. Подумайте еще"   
    
    
    
# PAGES
class Instruction_0(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']


page_sequence = [Instruction_0]
