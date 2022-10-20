import sys, random, grader, parse

def random_play_single_ghost(problem):
    # Your p1 code here
    score = 0
    isWin = False
    isLose = False
    random.seed(problem['seed'], version=1)
    is_pacman_turn = True
    solution = 'seed: {}\n'.format(problem['seed'])
    solution += '0\n'
    solution += print_map(problem)
    num = 1
    while not isWin and not isLose:
        if is_pacman_turn:
            is_pacman_turn = False
            parameters = get_parameters(problem['size'], problem['pacman'], problem['walls'], problem['ghosts'])
            dir = random.choice(parameters)
            move(dir, problem['pacman'])
            solution += "{}: P moving {}\n".format(num, dir)
            score -= 1
            food_i = -1

            for i in range(len(problem['ghosts'])):
                if problem['ghosts'][i][1][0] == problem['pacman'][0] and problem['ghosts'][i][1][1] == \
                        problem['pacman'][1]:
                    score -= 500
                    isLose = True

            for i in range(len(problem['foods'])):
                if problem['foods'][i][0] == problem['pacman'][0] and problem['foods'][i][1] == problem['pacman'][1]:
                    score += 10
                    food_i = i

            if food_i != -1:
                problem['foods'].pop(food_i)

            if len(problem['foods']) == 0:
                isWin = True
                score += 500

            num += 1

            solution += print_map(problem)
            solution += "score: {}\n".format(score)
        else:
            is_pacman_turn = True
            for ghost in problem['ghosts']:
                parameters = get_parameters(problem['size'], ghost[1], problem['walls'], problem['ghosts'],
                                            isGhost=True)
                if len(parameters) > 0:
                    dir = random.choice(parameters)
                    move(dir, ghost[1])
                else:
                    dir = ''
                solution += "{}: {} moving {}\n".format(num, ghost[0], dir)
                num += 1

                if ghost[1][0] == problem['pacman'][0] and ghost[1][1] == problem['pacman'][1]:
                    score -= 500
                    isLose = True

                solution += print_map(problem)
                solution += "score: {}\n".format(score)

                if isLose:
                    break

    if isWin:
        solution += "WIN: Pacman"
    elif isLose:
        solution += "WIN: Ghost"

    return solution


def move(dir, location):
    if dir == 'W':
        location[0] -= 1

    elif dir == 'E':
        location[0] += 1

    elif dir == 'N':
        location[1] -= 1

    elif dir == 'S':
        location[1] += 1


def get_parameters(size, location, walls, ghosts, isGhost=False):
    parameters = []
    ghost_locs = []
    for ghost in ghosts:
        ghost_locs.append(ghost[1])

    if not isGhost:
        if [location[0] - 1, location[1]] not in walls:
            parameters.append('W')
        if [location[0] + 1, location[1]] not in walls:
            parameters.append('E')
        if [location[0], location[1] - 1] not in walls:
            parameters.append('N')
        if [location[0], location[1] + 1] not in walls:
            parameters.append('S')

    else:
        if [location[0] - 1, location[1]] not in walls and [location[0] - 1, location[1]] not in ghost_locs:
            parameters.append('W')
        if [location[0] + 1, location[1]] not in walls and [location[0] + 1, location[1]] not in ghost_locs:
            parameters.append('E')
        if [location[0], location[1] - 1] not in walls and [location[0], location[1] - 1] not in ghost_locs:
            parameters.append('N')
        if [location[0], location[1] + 1] not in walls and [location[0], location[1] + 1] not in ghost_locs:
            parameters.append('S')
    parameters = sorted(parameters)
    return parameters


def print_map(problem):
    map = ""
    ghost_locs = []
    for ghost in problem['ghosts']:
        ghost_locs.append(ghost[1])
    for j in range(problem['size'][1]):
        for i in range(problem['size'][0]):
            if [i, j] in problem['walls']:
                map += '%'
            elif [i, j] in ghost_locs:
                for ghost in problem['ghosts']:
                    if ghost[1][0] == i and ghost[1][1] == j:
                        map += ghost[0]
            elif i == problem['pacman'][0] and j == problem['pacman'][1]:
                map += 'P'
            elif [i, j] in problem['foods']:
                map += '.'
            else:
                map += ' '
        map += '\n'

    return map

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)