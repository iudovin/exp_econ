from os import environ

SESSION_CONFIGS = [
    dict(
         name='game0',
         app_sequence=['p_survey', 'p_instruction_0', 'p_giffen_0', 'p_final'],
         num_demo_participants=2,
    ),
    dict(
         name='game1',
         app_sequence=['p_survey', 'p_instruction_1', 'p_giffen_1', 'p_final'],
         num_demo_participants=4,
    ),
    dict(
         name='game2',
         app_sequence=['p_survey', 'p_instruction_2', 'p_giffen_2', 'p_final'],
         num_demo_participants=2,
    ),
    dict(
         name='game3',
         app_sequence=['p_survey', 'p_instruction_3', 'p_giffen_3', 'p_final'],
         num_demo_participants=2,
    ),
    dict(
         name='game4',
         app_sequence=['p_survey', 'p_instruction_4', 'p_giffen_4', 'p_final'],
         num_demo_participants=2,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['name', 'result']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3130674831267'
