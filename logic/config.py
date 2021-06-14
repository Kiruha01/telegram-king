from enum import Enum

rounds = [
    'negative_bribes',
    'negative_hearts',
    'negative_boys',
    'negative_girls',
    'negative_king',
    'negative_last',
    'negative_patchwork',

    'positive_bribes',
    'positive_hearts',
    'positive_boys',
    'positive_girls',
    'positive_king',
    'positive_last',
    'positive_patchwork'
]


points_for_3 = {
    'negative_bribes': -4,
    'negative_hearts': -5,
    'negative_boys': -10,
    'negative_girls': -10,
    'negative_king': -40,
    'negative_last': -20,

    'positive_bribes': 4,
    'positive_hearts': 5,
    'positive_boys': 10,
    'positive_girls': 10,
    'positive_king': 40,
    'positive_last': 20
}

points_for_4 = {
    'negative_bribes': -2,
    'negative_hearts': -2,
    'negative_boys': -4,
    'negative_girls': -4,
    'negative_king': -16,
    'negative_last': -8,

    'positive_bribes': 2,
    'positive_hearts': 2,
    'positive_boys': 4,
    'positive_girls': 4,
    'positive_king': 16,
    'positive_last' : 8
}


NUM_OF_ROUNDS = 6


class State(Enum):
    start = 0
    names = 1

    negative_bribes = 2
    negative_hearts = 3
    negative_boys = 4
    negative_girls = 5
    negative_king = 6
    negative_last = 7
    negative_patchwork = 8

    positive_bribes = 9
    positive_hearts = 10
    positive_boys = 11
    positive_girls = 12
    positive_king = 13
    positive_last = 14
    positive_patchwork = 15

    final = 16
