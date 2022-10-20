import sys, parse, math, random, collections
import time, os, copy

def better_play_mulitple_ghosts(problem):
    score = 0
    isWin = False
    isLose = False
    is_pacman_turn = True
    solution = 'seed: {}\n'.format(problem['seed'])
    solution += '0\n'
    solution += print_map(problem)
    num = 1
    while not isWin and not isLose:
        if is_pacman_turn:
            is_pacman_turn = False
            parameters = get_parameters(problem['size'], problem['pacman'], problem['walls'], problem['ghosts'])
            dir = evaluate_choice(problem['pacman'], problem['ghosts'], problem['foods'], problem['walls'], parameters)
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
        winner = "Pacman"
    elif isLose:
        solution += "WIN: Ghost"
        winner = "Ghost"

    return solution, winner


def move(dir, location):
    if dir == 'W':
        location[0] -= 1

    elif dir == 'E':
        location[0] += 1

    elif dir == 'N':
        location[1] -= 1

    elif dir == 'S':
        location[1] += 1


def evaluate_choice(pacman, ghosts, foods, walls, parameters):
    optimal_dir = ''
    optimal_val = 2147483647
    for dir in parameters:
        value = 0
        x = pacman[0]
        y = pacman[1]
        if dir == 'N':
            y -= 1
        elif dir == 'S':
            y += 1
        elif dir == 'W':
            x -= 1
        elif dir == 'E':
            x += 1

        ghost_locs = []
        for ghost in ghosts:
            ghost_locs.append(ghost[1])

        max_ghost = math.log(2.4 / (1 + get_min_distance([x, y], ghost_locs, walls)), 1.2)
        # value = math.fabs(food[0] - x) + math.fabs(food[1] - y)
        min_food = get_min_distance([x, y], foods, walls)

        value = min_food + max_ghost
        # print("Value: {}, min_food: {}, max_ghost: {}".format(value, min_food, max_ghost))
        if value < optimal_val:
            optimal_val = value
            optimal_dir = dir

    return optimal_dir


def get_min_distance(pacman, location_list, walls):
    frontier = collections.deque([[pacman]])
    explored = []
    result = []

    while True:
        node = frontier.popleft()
        # print(node, " ", location_list)
        if node[-1] in location_list:
            result = node
            break

        if node[-1] not in walls and node[-1] not in explored:
            explored.append(node[-1])
            for candidate in [[node[-1][0] - 1, node[-1][1]], [node[-1][0] + 1, node[-1][1]],
                              [node[-1][0], node[-1][1] - 1], [node[-1][0], node[-1][1] + 1]]:
                node1 = copy.copy(node)
                node1.append(candidate)
                frontier.append(node1)

    return len(result) - 1


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
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)