~ Maze Solver ~ 
Griffin Kao, October 2019

Description:
A simple python program to solve and check a maze given through some API 

Running Solution: 
- Make sure to have Python installed
- Simply navigate to the root directory (containing this readme and the maze_solver.py file) in terminal/command prompt 
- Run "python maze_solver.py"

Design Notes:
- You'll note I used DFS (depth-first search) to explore the maze since with BFS (breadth-first search) we always reach close to worst case time complexity given that the bottom right corner of the maze is likely one of the farthest points from the top left.
- You'll also see the gross couple of lines in the recursive DFS function. Here, I opted for speed over style since returning immediately could save us lengthy path explorations. 
- For error handling, I generally attempted to explicitly handle what I believed to be the most common errors. Because there are a large number of general http errors, I used some general error handling for the rest.
- Retry limit: for cases where we get a 503 error code indicating a generally temporary server-side error, I opted to retry the request until some globally set limit (easily modified at the top of the program). This gives us a better chance at success for each request while preventing the program from hanging.
- I used anonymous functions defined at the top of the program for url generality and code cleanliness.
