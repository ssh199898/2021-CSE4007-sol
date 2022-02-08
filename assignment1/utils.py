
def cvtIndex(queens):
    return [v+1 for v in queens]


# return True when two queens are attacking
def isPair(q0, q1):
    # check queen pair
    if (q0[0] == q1[0] or                       # check x position
        q0[1] == q1[1] or                       # check y position
        abs(q0[0]-q1[0]) == abs(q0[1]-q1[1])):  # check diagonal difference
        return True
    else:
        return False


# return True when no pairs
def checkNoPair(queens):
    N = len(queens)

    # iterating all pairs in the list
    for i in range(N):
        for j in range(i+1, N):
            q0 = [i, queens[i]]
            q1 = [j, queens[j]]
            
            # check queen pair
            if isPair(q0, q1):  
                # return False if any of pairs is invalid
                return False

    # no pairs found
    return True


# print solution
def visualize(solution, verbose=2):
    queens = [v-1 for v in solution]

    print("Solution: ")
    N = len(queens)

    # check no solution case
    if N == 0:
        print("No Solution")
    else:
        print("Solution Found")
        # print position index
        if verbose>=1:    
            for p in queens:
                print(f' {p:2d}', end="")
            print()
        
        # print full chessboard
        if verbose>=2:
            for i in range(N):
                for j in range(N):
                    if(queens[j] == i):
                        print ("|★ ", end="")
                    else:
                        print("|  ", end="")
                print("|")