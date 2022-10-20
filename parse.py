import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    f = open(file_path)
    seed = 0
    ghosts = []
    pacman = []
    foods = []
    walls = []
    lines = f.readlines()
    i = 0
    y = 0
    for line in lines:
        line = line.replace('\n', '')
        if i == 0:
            seed = int(line.split(': ')[1])
        else:
            x = 0
            for j in range(len(line)):
                if line[j] == '%':
                    walls.append([x, y])
                if line[j] in ['W', 'X', 'Y', 'Z']:
                    ghosts.append((line[j], [x, y]))
                elif line[j] == '.':
                    foods.append([x, y])
                elif line[j] == 'P':
                    pacman = [x, y]
                x += 1
            y += 1
        i += 1

    width = len(lines[1])-1
    length = len(lines)-1
    ghosts = sorted(ghosts)
    problem = {'seed': seed, 'size': [width, length], 'walls': walls ,'pacman': pacman, 'foods': foods, 'ghosts': ghosts}
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')