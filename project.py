from itertools import combinations
import csv
from graphs import minColouring

def gamesOK(games):
    players = set()
    edges = set()
    for game in games:
        players.update(game)
        edges.add(game)
        edges.add((game[1], game[0]))  # add the reverse edge
    for A in players:
        for B in players:
            if A != B:
                path_exists = False
                for C in players:
                    if (A, C) in edges and (C, B) in edges:
                        path_exists = True
                        break
                if not path_exists:
                    if (A, B) not in edges:
                        return False
    return True

def potentialReferees(refereecsvfilename, player1, player2):
    with open(refereecsvfilename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        potential_referees = set()
        for row in reader:
            referee = row[0]
            conflicts = set(row[1:])
            if player1 not in conflicts and player2 not in conflicts and referee not in (player1, player2):
                potential_referees.add(referee)
    return potential_referees


def gameReferees(gamePotentialReferees):
    def assign_referee(game_idx, used_referees, assigned_referees):
        if game_idx == len(gamePotentialReferees):
            return True

        game = list(gamePotentialReferees.keys())[game_idx]
        potential_referees = gamePotentialReferees[game]

        for referee in potential_referees:
            if referee not in used_referees:
                assigned_referees[game] = referee
                used_referees.add(referee)
                if assign_referee(game_idx + 1, used_referees, assigned_referees):
                    return True
                used_referees.remove(referee)
                del assigned_referees[game]

        return False

    assigned_referees = {}
    used_referees = set()

    if assign_referee(0, used_referees, assigned_referees):
        return assigned_referees
    else:
        return None

def is_safe(vertex, graph, color_assignment, color):
    for neighbor in graph[vertex]:
        if color_assignment[neighbor] == color:
            return False
    return True

def k_coloring(graph, color_assignment, k, vertex):
    if vertex == len(graph):
        return color_assignment

    for color in range(1, k + 1):
        if is_safe(vertex, graph, color_assignment, color):
            color_assignment[vertex] = color
            result = k_coloring(graph, color_assignment, k, vertex + 1)
            if result:
                return result
            color_assignment[vertex] = 0

    return None

def gameSchedule(assigned_referees):
    schedule = []
    games = list(assigned_referees.keys())
    while games:
        time_slot = set()
        used_people = set()
        remaining_games = games.copy()
        for game in games:
            referee = assigned_referees[game]
            if game[0] not in used_people and game[1] not in used_people and referee not in used_people:
                time_slot.add((*game, referee))
                used_people.add(game[0])
                used_people.add(game[1])
                used_people.add(referee)
                remaining_games.remove(game)
        schedule.append(time_slot)
        games = remaining_games
    return schedule

def ranking(games):
    player_ranking = []
    remaining_games = set(games)
    
    while remaining_games:
        winners = {game[0] for game in remaining_games}
        losers = {game[1] for game in remaining_games}
        top_candidates = winners - losers

        if not top_candidates:
            return None

        top_player = top_candidates.pop()
        player_ranking.append(top_player)
        remaining_games = {game for game in remaining_games if game[0] != top_player}

    all_players = {player for game in games for player in game}
    remaining_players = all_players - set(player_ranking)
    player_ranking.extend(remaining_players)

    return player_ranking