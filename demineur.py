"""
MINOU

Jeu - Demineur

But du jeu ?

Le jeu consiste à trouver toutes les mines présentes sur le plateau de jeu.
Pour trouver les mines il suffit de devoiler certaines cases, attention si
le joueur devoile une case qui n'est pas une mine, la partie se terminera.
Pour gagner il vous faudra trouver toutes les mines présentes en plaçant un drapeau
ou en devoilant tout le plateau de jeu sans dévoiler de mine.
"""

######################### IMPORTS ######################################

import random
import sys

################################ CONFIGURATION #########################################

LISTE_DEPLACEMENTS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
sys.setrecursionlimit(999999)

################################ FONCTION ##############################################


def create_board(n, m):
    """
    Construit un tableau de taille NxM, avec chaque case
    qui contient un caractère.
    :param n: Nombre de ligne
    :param m: Nombre de colonne
    :return: le plan sous forme List[List[str]]
    """

    return [[" . " for _ in range(m)] for _ in range(n)]


def print_board(board):
    """
    Permet d'afficher le plateau de jeu dans le terminal pour
    que le joueur puisse jouer.
    :param board: Plateau
    :return: None
    """

    print("   ", end='')
    for col_number in range(len(board[0])):  # label des colonnes
        if col_number // 10 != 0:
            print("  " + str(col_number // 10), end='')
        else:
            print("   ", end="")

    print("\n", "  ", end='')
    for line_number in range(len(board[0])):
        print("  " + str(line_number % 10), end='')

    print("\n    " + "-" * (len(board[0]) * 3))
    for i in range(len(board)):  # impression des lignes
        print(f"{i:2} |", end="")
        for j in range(len(board[0])):  # x
            print(board[i][j], end='')
            if j == len(board[0]) - 1:
                print("|")
    print("    " + "-" * (len(board[0]) * 3))


def get_size(board):
    """
    Calcule les dimensions du plateau de jeu.
    :param board:
    :return: Tuple(int,int)
    """
    return len(board), len(board[0])


def get_neighbors(board, pos_x, pos_y):
    """
    Affiche toutes les cases voisines d'une case.
    :param board:
    :param pos_x:
    :param pos_y:
    :return: List[Tuple(int,int)] liste de toutes les cases voisines.
    """

    neighbors_list, dimension = [], get_size(board)
    for i in range(8):
        neighbors_coords = (pos_x + LISTE_DEPLACEMENTS[i][0], pos_y + LISTE_DEPLACEMENTS[i][1])
        # Vérification si une case calculé est en dehors du plateau, si non on ajoute à la liste des voisins
        if neighbors_coords[0] in range(0, dimension[0]) and neighbors_coords[1] in range(0, dimension[1]):
            neighbors_list.append(neighbors_coords)
    return neighbors_list


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    """
    Placement aleatoire des mines sur le plateau de reference en fonction de la
    première case choisi par le joueur.
    :param reference_board:
    :param number_of_mines:
    :param first_pos_x:
    :param first_pos_y:
    :return: List[Tuple(int,int)]
    """

    first_coord, list_of_bombs, size, count = (first_pos_x, first_pos_y), [], get_size(reference_board), 0
    neighbor = get_neighbors(reference_board, first_coord[1], first_coord[0])
    while count != number_of_mines:
        x, y = random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)

        # Verification qu'une mine n'est pas placé à des endroits critiques
        if (x, y) in list_of_bombs or (x, y) == first_coord or (x, y) in neighbor:
            number_of_mines += 1
        else:
            list_of_bombs.append((x, y))
            reference_board[x][y] = " X " # Placement de la mine sur le plateau de reference
        count += 1
    return list_of_bombs


def fill_in_board(reference_board):
    """
    Calculer le nombre de mine présente dans le voisinage d'une case sur le plateau de reference.
    :param reference_board:
    :return: None
    """

    bombs_count = 0

    for pos_x in range(len(reference_board)):
        for pos_y in range(len(reference_board[0])):
            voisin = get_neighbors(reference_board, pos_x, pos_y)
            for k in range(len(voisin)):
                # Verification du nombre de mine dans le voisinage d'une case
                if reference_board[voisin[k][0]][voisin[k][1]] == " X " and reference_board[pos_x][pos_y] != " T " \
                        and reference_board[pos_x][pos_y] != " X ":
                    bombs_count += 1
                    reference_board[pos_x][pos_y] = " " + str(bombs_count) + " "
                elif reference_board[pos_x][pos_y] == " . ":
                    reference_board[pos_x][pos_y] = " 0 "
            bombs_count = 0


def propagate_click(game_board, reference_board, pos_x, pos_y):
    """
    MAJ du plateau de jeu tant que qu'il y a 0 mines aux alentours.
    :param game_board:
    :param reference_board:
    :param pos_x:
    :param pos_y:
    :return: None
    """

    neighbor = get_neighbors(reference_board, pos_x, pos_y)
    for i in range(len(neighbor)):
        # Tant qu'un 0 est dans le voisinage on continue de dévoiler et on afficher la case sur le plateau de jeu
        if reference_board[neighbor[i][0]][neighbor[i][1]] == " 0 " and game_board[neighbor[i][0]][neighbor[i][1]] == ' . ':
            game_board[neighbor[i][0]][neighbor[i][1]] = reference_board[neighbor[i][0]][neighbor[i][1]]
            propagate_click(game_board, reference_board, neighbor[i][0], neighbor[i][1])

        # Quand un chiffre autre que 0 est dans le voisinage on arrête de dévoiler et on affiche cette case
        elif reference_board[neighbor[i][0]][neighbor[i][1]] != " 0 " and reference_board[neighbor[i][0]][
            neighbor[i][1]] != " X " and \
                reference_board[neighbor[i][0]][neighbor[i][1]] != " T ":
            game_board[neighbor[i][0]][neighbor[i][1]] = reference_board[neighbor[i][0]][neighbor[i][1]]


def parse_input(n, m):
    """
    Choix de l'action effectué par le joueur, poser un flag ou dévoiler case.
    :param n:
    :param m:
    :return: Tuple(str,int,int)
    """
    try:
        action_player = input("Choix de la case: ")
        action_player = action_player.split()
        pos_x, pos_y, action_lower = int(action_player[1]), int(action_player[2]), action_player[0].lower()

    except (IndexError,ValueError): # Mauvaise valeur rentré
        print("Mauvais donnée ! Réessaye !")
        return parse_input(n,m)
    else:
        # Verification que coordonnée de la case choisi est dans le plateau
        if pos_x in range(0, n + 1) and pos_y in range(0, m + 1) and action_lower == "c" or action_lower == "f":
            return action_lower, pos_x, pos_y
        else:
            print("Mauvais donnée ! Réessaye !")
            return parse_input(n, m)


def spoil(game, ref):
    """
    Affiche la case choisi par le joueur sur le plateau de jeu.
    :param game:
    :param ref:
    :return:
    """

    size = get_size(game)
    position, explosion = parse_input(size[0] - 1, size[1] - 1), None

    if position[0] == "c":
        if ref[position[1]][position[2]] == " X ":
            explosion = True
            print("Dommage ! Tu as perdu la partie...")
        elif ref[position[1]][position[2]] != " 0 ":
            game[position[1]][position[2]] = ref[position[1]][position[2]]
        else:
            game[position[1]][position[2]] = ref[position[1]][position[2]]
            propagate_click(game, ref, position[1], position[2])

    elif position[0] == "f" :
        if game[position[1]][position[2]] == " . ":  # Ajout d'un drapeau sur le plateau de jeu
            game[position[1]][position[2]] = " f "
        elif game[position[1]][position[2]] == " f ":  # Supression d'un drapeau sur le plateau de jeu
            game[position[1]][position[2]] = " . "
    else:
        spoil(game, ref)

    return position[1], position[2], explosion


def check_win(game_board, reference_board, mines_list, total_flags):
    """
    La fonction vérifie si le joueur a gagné ou pas.
    :param game_board:
    :param reference_board:
    :param mines_list:
    :param total_flags:
    :return: Booleen
    """
    victory,list_position = None, find(game_board)

    # Verification que chaque case libre = mine
    if sorted(list_position[0]) == sorted(mines_list) and len(list_position[1]) <= total_flags:
        victory = True

    # Verification que chaque drapeau posé = mine
    elif sorted(list_position[1]) == sorted(mines_list) and len(list_position[1]) <= total_flags:
        victory = True
    return victory


def find(game):
    """
    Donne les cases non dévoilés/case avec un drapeau
    :param game:
    :return: Une liste des position non dévoilé et une liste des drapeaux posés
    """
    # Case non exploré.
    free_case = [(j, i) for i in range(len(game[0])) for j in range(len(game)) if game[j][i] == " . "]
    # Case où un drapeau est posé
    flag_case = [(j, i) for i in range(len(game[0])) for j in range(len(game)) if game[j][i] == " f "]

    return free_case,flag_case


def set_start(game_board, reference_board, position):
    """
    Création d'une case spéciale pour la première case dévoilé par le joueur.
    :param game_board:
    :param reference_board:
    :param position:
    :return:
    """
    game_board[position[0]][position[1]] = " 0 "
    reference_board[position[0]][position[1]] = " T "


def init_game(n, m, number_of_mines):
    """
    Permet de générer les plateaux de jeu. Demande au joueur la première case à dévoiler.
    Depôt des mines sur le plateau de reference.
    Génération du nombre de mine dans le voisinage d'une case.

    :param n: Nombre de ligne
    :param m: Nombre de colonne
    :param number_of_mines: Nombre de mine
    :return: game_board, reference_board, mines_list
    """
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)

    action_player = parse_input(n, m)
    first_pos_x, first_pos_y = int(action_player[2]), int(action_player[1])
    set_start(game_board, reference_board, (first_pos_y, first_pos_x))

    liste_of_mine = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, first_pos_y, first_pos_x)

    return game_board, reference_board, liste_of_mine


def main():
    if __name__ == "__main__":
        print("\nLancement du du demineur...\n")
        n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        game_data, explosion, total_flag = init_game(n, m, number_of_mines), False, number_of_mines

        while check_win(game_data[0], game_data[1], game_data[2], total_flag) is None and not explosion:
            print_board(game_data[0])
            win_data = spoil(game_data[0], game_data[1])

            if win_data[2]: # Verification qu'une mine n'est pas dévoilé
                explosion = True
            check_win(game_data[0], game_data[1], game_data[2], total_flag)

        if check_win(game_data[0], game_data[1], game_data[2], total_flag):
            print("Let's gooo, tu viens de gagner la partie avec succès")

######################### JEU ######################################

main()
