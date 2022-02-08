from queue import Queue
from utils import visualize, checkNoPair, cvtIndex

def bfs(N):
    # using queue for BFS
    queue = Queue()

    # initial state: start filling from left
    # state can have N values, within range from 0 to N
    init_queens = []
    queue.put(init_queens)

    # the list will be assigned when goal state is found
    # if not, empty list will be returned.
    goal_queens = []

    # perform bfs until queue is empty (all states have been reached)
    while not queue.empty():
        state_queens = queue.get()

        # check no queens pair is attacking
        if checkNoPair(state_queens):
            # N queens with no pair (solution)
            if len(state_queens) == N:
                # assign goal state
                # clear queue (to stop search here)
                goal_queens = cvtIndex(state_queens)
                queue.queue.clear()

            # less queens with no pair (valid state)
            else:
                # add successors to the queue
                # branching factor of N
                for i in range(N):
                    # generating successor (copy state and add a queen)
                    successor_queens = list(state_queens) 
                    successor_queens.append(i)
                    queue.put(successor_queens)

        # if some queens are attacking each other
        else:
            # backtrack (do nothing)
            pass
    
    # return empty list when bfs fails
    return goal_queens


if __name__ == "__main__":
    N = int(input("Type number N: "))

    solutions = bfs(N)
    visualize(solutions)
