def points(games):
    points = 0

    for game in games:
        x, y = map(int, game.split(':'))
        if x > y:
            points += 3
        elif x == y:
            points += 1
        # Si x < y, no se suma ningún punto (points += 0)

    return points