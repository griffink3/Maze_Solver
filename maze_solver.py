import requests 
import json

base_url = "https://www.maze_generator.com/"
check_move = lambda z, x, y: base_url + str(z) + "/check?x=" + str(x) + "&y=" + str(y)
position = lambda x, y: "Position: " + str(x) + ", " + str(y)
submit = lambda z: base_url + str(z) + "/solve"
retry_limit = 1

def print_error(function, code):
    print("ERROR: Error returned while " + function + " with code " + str(code))

def get_maze(retry_count):
    """ This function makes a post request to the maze api to get the maze 
    (and it takes in how many times this specific post request has been made). 
    Returns: (maze id, height, width) 
            or None + prints general error
    """
    r = requests.post(base_url, auth=('user','pass')) 
    if r.status_code == 201:
        j = json.loads(r.text)
        return (j['id'], j['height'], j['width'])
    elif r.status_code == 503 and retry_count < retry_limit:
        return get_maze(retry_count+1)
    else:
        print_error("getting maze", r.status_code)

def solve_maze(maze, h, w):
    """ This function calls solve_recurs to recursively solve the maze through
    a depth-first search. 
    Returns: solution to the maze as an array of location objects 
            or [] if no solution was found (this can be from a request error, rather than the maze)
            or None + prints invalid maze error 
    """
    if h < 0 or w < 0 or not valid_move(maze, h, w, 0, 0) or not valid_move(maze, h, w, w-1, h-1):
        print("ERROR: We have an invalid maze :/")
        return
    visited = set()
    solution = solve_recurs(maze, h, w, 0, 0, visited)
    if not solution:
        return []
    solution.reverse()
    return solution

def solve_recurs(maze, h, w, x, y, visited):
    loc = {"x": x, "y": y}
    if x == w - 1 and y == h - 1:
        return [loc] 
    if (x, y) in visited or not valid_move(maze, h, w, x, y):
        return
    visited.add((x, y))
    path = solve_recurs(maze, h, w, x-1, y, visited)
    if path: 
        path.append(loc)
        return path
    path = solve_recurs(maze, h, w, x, y-1, visited)
    if path:
        path.append(loc)
        return path
    path = solve_recurs(maze, h, w, x+1, y, visited)
    if path:
        path.append(loc)
        return path
    path = solve_recurs(maze, h, w, x, y+1, visited)
    if path:
        path.append(loc)
        return path

def valid_move(maze, h, w, x, y):
    """ This function makes a get request to check whether a given spot
    in the maze (given by x and y coordinates) is a valid move. It will 
    repeat the request given a 503 up to the retry_limit.  
    Returns: True if valid move
            or False if invalid move 
            or False if general error (will print error if not 403 
                denoting invalid maze move)
    """
    if x < 0 or y < 0 or x > w - 1 or y > h - 1:
        return False
    return valid_move_retry(maze, x, y, 0)

def valid_move_retry(maze, x, y, retry_count):
    r = requests.get(check_move(maze, x, y), auth=('user','pass'))
    if r.status_code == 200:
        assert(r.text == position(x, y))
        return True
    elif r.status_code == 503 and retry_count < retry_limit:
        return valid_move_retry(maze, x, y, retry_count+1)
    else:
        if r.status_code != 403:
            print_error("checking move", r.status_code)
        return False

def submit_solution(maze, solution, retry_count):
    """ This function submits the solution by making a post request to the 
     maze api. We again retry up to the limit if a 503 error is received.
    Returns: prints out description of outcome
    """
    r = requests.post(submit(maze), auth=('user','pass'), data=json.dumps(solution))
    if r.status_code == 200:
        print("Success!")
    elif r.status_code == 503 and retry_count < retry_limit:
        submit_solution(maze, solution, retry_count+1)
    elif r.status_code == 422:
        print("ERROR: Oh no, we messed up! Wrong solution submitted")
    else:
        print_error("submitting solution", r.status_code)

if __name__== "__main__" :
    maze, h, w = get_maze(0)
    if maze:
        submit_solution(maze, solve_maze(maze, h, w), 0)

