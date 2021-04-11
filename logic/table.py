from logic import database

def create_table(players):
    LEN_OF_NAME = 5
    len_of_columns = [len(i.name[:LEN_OF_NAME]) for i in players]

    msg = "```\n"
    msg += '│ ' + ' │ '.join([i.name[:LEN_OF_NAME] for i in players]) + ' │ \n'
    msg += '\n'

    for state in database.points_for_3.keys():
        for i, l in zip(players, len_of_columns):
            num = getattr(i, state)
            first = (l - len(str(num))) // 2
            msg += '│ ' + ' ' * first + str(num) + ' ' * (l - len(str(num)) - first) + ' '
        msg += '│\n'

    msg += '\n'
    width = sum([i + 2 for i in len_of_columns]) + len(len_of_columns) - 1
    msg += '│' + ' ' * ((width - 4) // 2) + "Итог" + ' ' * (width - 4 - (width - 4) // 2) + '│\n'
    msg += '\n'

    msg += '│ '
    for i, l in zip(players, len_of_columns):
        total = 0
        for state in database.points_for_3.keys():
            total += getattr(i, state)
        first = (l - len(str(total))) // 2
        msg += ' ' * first + str(total) + ' ' * (l - len(str(total)) - first) + ' ' + '│ '
    msg += '\n```'
    #
    #
    #
    # __msg = """
    # │ Name │ Names │ First │
    # ╞══════╪═══════╪═══════╡
    # │  12  │   13  │   15  │
    # │  45  │   45  │   45  │
    # │  15  │   12  │   12  │
    # ╞══════╧═══════╧═══════╡
    # │    Positive Rounds   │
    # ╞══════╤═══════╤═══════╡
    # │  12  │   13  │   15  │
    # │  45  │  45   │   45  │
    # │  15  │  12   │   12  │
    # ╞══════╧═══════╧═══════╡
    # │        Results       │
    # ╞══════╦═══════╦═══════╡
    # ║  45  ║  45   ║   45  ║
    #
    # """
    return msg

if __name__ == "__main__":
    from db_setup import User, Player
    import database
    players = database.session.query(Player).all()
    print(create_table(players))