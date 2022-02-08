from random import randrange

BONUS = 1
DECAY = 0.9

MAP_DICT = { "S": 1, "G": 2, "T": 9, "B": -1, "P": 0 }
INV_MAP_DICT = { 1: "S", 2: "G", 9: "T", -1: "B", 0: "P" }
REWARD_DICT = { "S": 0, "G": 100, "T": BONUS, "B": -100, "P": 0 }
DIR_DICT = { "R": 0, "B": 1, "L": 2, "T": 3 }
INV_DIR_DICT = { 0:"R", 1:"B", 2:"L", 3:"T"}

def read_input():
    with open('./input.txt', 'r') as f:
        lines = f.read().splitlines()
        map_ = []

        for line in lines:
            map_row = []
            for c in line:
                map_row.append(MAP_DICT[c]) 
            map_.append(map_row)

    return map_

def write_output(path, qval):
    f_name = "output.txt"
    with open(f_name, 'w') as f:
        for v in path:
            f.write(f"{v} ")
        f.write("\n")
        f.write(f"{qval}")

def write_qtable_output(q_table):
    f_name = "qtable_output.txt"
    with open(f_name, 'w') as f:
        for i in range(5):
            for k in range(4):
                f.write(f"{INV_DIR_DICT[k]}) ")
                for j in range(5):
                    f.write(f"{q_table[i][j][k]:-20.10f}")
                f.write("\n")
            f.write("\n")
                    
class QLearner:

    def __init__(self, MAP, DECAY):
        self.DECAY = DECAY
        self.MAP = MAP

        # init starting point
        for i, row in enumerate(MAP):
            if MAP_DICT['S'] in row:
                self.START = (i, row.index(MAP_DICT['S']))

        self.q_table = [[[0, 0, 0, 0] for j in range(5)] for i in range(5)] # i x j x 4 size q-table
        self.reward_table = [[REWARD_DICT[INV_MAP_DICT[MAP[i][j]]] for j in range(5)] for i in range(5)]
        self.policy_table = [[-1 for j in range(5)] for i in range(5)]

    def train(self):
        # repeat until training satisfies termination condition
        for iter in range(1000):
            # start training at random point in the map
            state = [randrange(0, 5), randrange(0, 5)] 

            # training iteration
            while not self._isBomb(state) and not self._isGoal(state):
                # 이동 가능한 방향중 랜덤 선택.
                next_state, action = self._random_walk(state)
                i, j = state
                i_, j_ = next_state
                # q-table update
                self.q_table[i][j][DIR_DICT[action]] = self.reward_table[i_][j_] + self.DECAY*self._delayed_reward(next_state) 
                        
                # visualization in terminal
                # self._visualize(state, iter, action)    

                # 폭탄, 골을 만나면 다음 while loop시, q-table을 update하지 않고 종료                
                state = next_state
                  
            print("Iteration Terminated!")   

    def define_policy(self):
        for i in range(5):
            for j in range(5):
                state = [i, j]
                # no policy for bomb and goal point
                if not self._isBomb(state) and not self._isGoal(state):    
                    # find optimum direction
                    optimum_val = 0
                    optimum_dir = -1
                    for k in range(4):
                        if self.q_table[i][j][k] > optimum_val:
                            optimum_val = self.q_table[i][j][k]
                            optimum_dir = INV_DIR_DICT[k]
                    # if max value is 0, no policy is established for that cell. (-1)
                    self.policy_table[i][j] = optimum_dir

    def get_optimum_path(self):
        i, j = self.START
        path = [i*5+j]

        while self.MAP[i][j] != MAP_DICT["G"]:
            policy = self.policy_table[i][j]
            i, j = self._move_state_action([i, j], policy)
            path.append(i*5+j)
            
        return path

    def get_start_qvalue(self):
        i, j = self.START
        max_q_val = max(self.q_table[i][j])

        return max_q_val

    def _random_walk(self, state):
        possible_action = self._get_possible_action(state)
        walk = randrange(0, len(possible_action))
        action = possible_action[walk]
        next_state = self._move_state_action(state, action)

        return next_state, action
      
    def _get_possible_action(self, state):
        possible_action = ["R", "B", "L", "T"]
        if state[0] == 0: # i index minimum
            possible_action.remove("T")
        if state[0] == 4: # i index maximum
            possible_action.remove("B")
        if state[1] == 0: # j index minimum
            possible_action.remove("L")
        if state[1] == 4: # j index maximum
            possible_action.remove("R")

        return possible_action

    def _move_state_action(self, state, action):
        next_state = list(state) #copy
        if action == "R":
            next_state[1] += 1 # move j+1
        elif action == "B":
            next_state[0] += 1 # move i+1
        elif action == "L":
            next_state[1] -= 1 # move j-1
        elif action == "T":
            next_state[0] -= 1 # move i-1
        
        return next_state
    
    def _delayed_reward(self, next_state):
        possible_action = self._get_possible_action(next_state)

        max = 0
        for action in possible_action:
            i_, j_ = next_state
            reward = self.q_table[i_][j_][DIR_DICT[action]]
            if max < reward:
                max = reward
        
        return max

    def _isBomb(self, state):
        if self.MAP[state[0]][state[1]] == MAP_DICT["B"]:
            return True
        else:
            return False

    def _isGoal(self, state):
        if self.MAP[state[0]][state[1]] == MAP_DICT["G"]:
            return True
        else:
            return False

    def _visualize(self, state, iter, action):
        i_, j_ = state
       
        print(f'{iter}) Q-Table update: [{i_}][{j_}][{action}] = {self.q_table[i_][j_][DIR_DICT[action]]:15.10f}')
        
        for i in range(5):
            for j in range(5):
                if state == [i, j]:
                    print("◎", end='')
                else:
                    if self.MAP[i][j] == MAP_DICT["S"]:
                        print("S", end="")
                    elif self.MAP[i][j] == MAP_DICT["G"]:
                        print("G", end='')
                    elif self.MAP[i][j] == MAP_DICT["T"]:
                        print("★", end='')
                    elif self.MAP[i][j] == MAP_DICT["B"]:
                        print("※", end='')
                    elif self.MAP[i][j] == MAP_DICT["P"]:
                        print(" ", end='')
                print('|', end='')
            print("")


MAP = read_input()
qlearner = QLearner(MAP, DECAY)
qlearner.train()
# write_qtable_output(qlearner.q_table)
qlearner.define_policy()
path = qlearner.get_optimum_path()
val = qlearner.get_start_qvalue()
write_output(path, val)
