import random
from utils import isPair, visualize, cvtIndex


def countPairs(queens):
    N = len(queens)

    count = 0
    # iterating all pairs in the list
    for i in range(N):
        for j in range(i+1, N):
            q0 = [i, queens[i]]
            q1 = [j, queens[j]]
            
            # check queen pair
            if isPair(q0, q1):
                count += 1

    return count


def hc(N):
    # boundary value, no solution exist
    if 2 <= N and N <= 3:
        return []

    # goal states to be returned
    goal_queens = []

    local_minimum_h = -1
    while local_minimum_h != 0:
        # init queens with random state
        state_queens = [random.randrange(0,N) for i in range(N)]

        # init heuristic with worst case value
        predecessor_h = N*(N-1)/2 + 1
        state_h = N*(N-1)/2
        
        # depth = 0
        # stop loop when heuristic value do not decrease
        while state_h < predecessor_h:
            # init minimum h value
            successor_h_min = state_h
            successor_h_min_positions = []

            # search heuristic values
            for x in range(N):      # x index
                for y in range(N):  # y index
                    # generate successor
                    successor = state_queens.copy()
                    successor[x] = y
                    h_value = countPairs(successor)

                    # if h value of current position is smaller than minimum
                    if (h_value < successor_h_min):
                        # renew h_min and positions
                        successor_h_min = h_value
                        successor_h_min_positions = [[x, y]]
                    # if h value of current position equals minimum
                    elif (h_value == successor_h_min):
                        # keep tracking positions
                        successor_h_min_positions.append([x, y])
                    # if h value is higher
                    else:
                        # do nothing
                        pass
                    
            # randomly select one successor
            successor_x, successor_y = random.choice(successor_h_min_positions)
            state_queens[successor_x] = successor_y

            # update heuristic value
            predecessor_h = state_h
            state_h = successor_h_min


        if state_h == 0:
            goal_queens = cvtIndex(state_queens)

        local_minimum_h = state_h


    return goal_queens


if __name__ == "__main__":
    N = int(input("Type number N: "))

    solutions = hc(N)
    visualize(solutions)