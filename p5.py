import sys, parse, collections
import time, os, copy

def min_max_mulitple_ghosts(problem, k):
    #Your p5 code here
    solution = ''
    winner = ''
    return solution, winner

class Node:
    problem = {}
    action = ''
    children = []
    score = 0
    terminate_flag = False

    def __init__(self, problem, action, score):
        self.problem = problem
        self.action = action
        self.score = score

    def add_child(self, child_node):
        self.children.append(child_node)

def search_k(problem, k):
    root = Node(problem, '', 0)


def build_pacman_node(node, index, k):
    if index < k and not node.terminate_flag:
        parameter = get_parameters(node.problem['pacman'], node.problem['walls'], node.problem['ghosts'])
        for dir in parameter:
            new_problem, score, is_win, is_lose = simulate(node.problem, node.score, dir, 'pacman')
            new_node = Node(new_problem, dir, score)
            node.add_child(new_node)
            if is_win or is_lose:
                new_node.terminate_flag = True
            else:
                build_ghosts_node(new_node, index + 1, k)

def build_ghosts_node(node, index, k):
    if index < k and not node.terminate_flag:
        raw_parameter = []
        for ghosts in node.problem['ghosts']:
            parameter = get_parameters(ghosts[1], node.problem['walls'], node.problem['ghosts'], isGhost=True)
            raw_parameter.append(parameter)



def simulate(problem, score, instruction, flag):
    is_win = False
    is_lose = False
    problem_copy = copy.copy(problem)
    new_score = score
    if flag == 'pacman':
        move(instruction[0], problem_copy['pacman'])
        new_score -= 1
        food_i = -1

        for ghost in problem_copy['ghosts']:
            if ghost[1][0] == problem_copy['pacman'][0] and ghost[1][1] == problem_copy['pacman'][1]:
                is_lose = True
                new_score -= 500
                return problem_copy, new_score, is_win, is_lose

        for i in range(len(problem_copy['foods'])):
            if problem_copy['foods'][i][0] == problem_copy['pacman'][0] and problem_copy['foods'][i][1] == problem_copy['pacman'][1]:
                food_i = i
                new_score += 10

        if food_i != -1:
            problem_copy['foods'].pop(food_i)

        if len(problem_copy['foods']) == 0:
            is_win = True
            new_score += 500
            return problem_copy, new_score, is_win, is_lose

    elif flag == 'ghost':
        j = 0
        for ghost in problem_copy['ghosts']:
            move(instruction[j], ghost[1])

            if ghost[1][0] == problem_copy['pacman'][0] and ghost[1][1] == problem_copy['pacman'][1]:
                is_lose = True
                new_score -= 500
                return problem_copy, new_score, is_win, is_lose

            j += 1

    return problem_copy, new_score, is_win, is_lose

def get_parameters(location, walls, ghosts, isGhost=False):
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

def move(dir, location):
    if dir == 'W':
        location[0] -= 1

    elif dir == 'E':
        location[0] += 1

    elif dir == 'N':
        location[1] -= 1

    elif dir == 'S':
        location[1] += 1

def join_list(data):
    result = [[]]
    for list_pool in data:
        lis = []
        for i in result:
            for j in list_pool:
                lis.append(i+[j])

        result = lis

    return result

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)