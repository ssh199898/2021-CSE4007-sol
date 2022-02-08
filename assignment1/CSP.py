from utils import visualize, checkNoPair, cvtIndex

# domain: 0~N column queens
# value: 0~N row position
def csp(N):
    # based on DFS
    stack = []
    
    # initial state: start filling from left
    # state can have N values, within range from 0 to N
    init_queens = []
    stack.append(init_queens)

    goal_queens = []

    while len(stack) != 0:
        state_queens = stack.pop()
        
        # check no queens pair is attacking
        if checkNoPair(state_queens):
            
            # N queens with no pair (solution)
            if len(state_queens) == N: 
                # assign goal state
                # clear stack (to stop search here)
                goal_queens = cvtIndex(state_queens)
                stack.clear()

            # less queens with no pair (valid state)
            else:
                # add successors to the stack
                # branching factor of N
                for i in range(N):
                    # generating successor (copy state and add a queen)
                    successor_queens = list(state_queens)
                    successor_queens.append(i)
                    stack.append(successor_queens)

        # if some queens are attacking each other
        else:
            # backtrack (do nothing)
            pass

    return goal_queens
    

if __name__ == "__main__":
    N = int(input("Type number N: "))

    solutions = csp(N)
    visualize(solutions)
