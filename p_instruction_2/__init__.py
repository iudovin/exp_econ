from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'p_instruction_2'
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
                ['C', 'В начале раунда на всех игроков будет выделено 300 000 ккал риса'], 
     ['D', 'Оно известно и видно в начале каждого раунда.']],
            label='Что вам известно о количестве риса на всех игроков? ',
            widget=widgets.RadioSelect
        ) 
    q2 = models.StringField(
            choices=[
                ['A', 'Так, что мяса куплено на все не потраченные на заявленный рис деньги'], 
                ['B', 'Так, что мяса куплено на все не потраченные на фактически полученный рис деньги'], 
                ['C', 'Никто не получит мясо'], 
                ['D', 'Мясо распределится пропорционально заявкам игроков на покупку риса']],
            label='Как высчитывается полученное количество мяса, если игроки превысили лимит риса?',
            widget=widgets.RadioSelect
        )

    q3 = models.StringField(
            choices=[
                ['A', '7 раундов по 1.5 минуты'], 
                ['B', 'Первый раунд - 2 минуты и ещё 6 раундов по 1 минуте.'], 
                ['C', 'Первый раунд - 2.5 минуты и ещё 6 раундов по 1.5 минуты, и таких 3 одинаковых этапа'], 
                ['D', '21 раунд по 1.5 минуты, по 7 раундов в каждом этапе']],
            label='Сколько раундов какой длительности будет играться этот круг?',
            widget=widgets.RadioSelect
        )

def q1_error_message(player, q1):
    if q1 != 'D':
        return "Выбран неверный ответ. Подумайте еще"
def q2_error_message(player, q2):
    if q2 != 'A':
        return "Выбран неверный ответ. Подумайте еще"
def q3_error_message(player, q3):
    if q3 != 'B':
        return "Выбран неверный ответ. Подумайте еще"
    


# PAGES
class Instruction_2(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3']


page_sequence = [Instruction_2]