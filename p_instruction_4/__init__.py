from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_instruction_4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(
            choices=[
                ['A', '2 минуты'], 
                ['B', '1.5 минуты '], 
                ['C', '1 минуту'], 
     ['D', 'Пока в магазине не кончится рис']],
            label='Сколько длятся торги? ',
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
                ['A', 'Да'], 
                ['B', 'Нет']],
            label='Можно ли делать покупку больше одного раза, если в магазине ещё есть рис?',
            widget=widgets.RadioSelect
        )
    q4 = models.StringField(
            choices=[
                ['A', 'Столько, сколько заявил'], 
                ['B', 'Зависит от того, сколько купили другие'], 
                ['C', 'Столько, сколько осталось в магазине на момент поступления его заявки']],
            label='Сколько риса сможет купить последний покупатель?',
            widget=widgets.RadioSelect
        ) 
    q5 = models.StringField(
            choices=[
                ['A', '7 раундов по 1.5 минуты'], 
      ['B', 'Первый раунд - 2 минуты на покупку, затем торги затем 2 минуты на запасание, затем ещё 6 раундов по 1 минуте на покупку и 1 минуте на запасание'], 
                ['C', '7 раундов, и в каждом раунд 1 минута на проверку выгоды, затем торги до конца запасов магазина и 1 минута на распределение запасов.'], 
                ['D', '21 раунд, в каждом 1 минута на покупку риса, и 1 минута на поедание']],
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
    if q3 != 'A':
        return "Выбран неверный ответ. Подумайте еще"
def q4_error_message(player, q4):
    if q4 != 'C':
        return "Выбран неверный ответ. Подумайте еще"
def q5_error_message(player, q5):
    if q5 != 'C':
        return "Выбран неверный ответ. Подумайте еще"
    


# PAGES
class Instruction_4(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5']


page_sequence = [Instruction_4]