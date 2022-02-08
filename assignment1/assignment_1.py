from BFS import bfs
from HC import hc
from CSP import csp

# read inputs
def read_inputs(path=".\input.txt"):
    with open(path, 'r') as f:
        input_lines = f.readlines()
        inputs = []

        for input_line in input_lines:
            N, type = input_line.split()
            inputs.append([int(N), type])

    return inputs

# run each search algorithm
def run_search(inputs):
    results = []

    for i in range(len(inputs)):
        N, type = inputs[i]
        if type == 'bfs':
            sol = bfs(N)
            results.append([N, 'bfs', sol])
        elif type == 'hc':
            sol = hc(N)
            results.append([N, 'hc', sol])
        elif type == 'csp':
            sol = csp(N)
            results.append([N, 'csp', sol])
        else:
            print("wrong input")

    return results

# write output
def write_output(results):
    for result in results:
        N, type, sol = result
        f_name = f".\{N}_{type}_output.txt"

        if len(sol) != 0:
            output = ''.join(str(v)+" " for v in sol)
        else:
            output = 'no solution'

        with open(f_name, 'w') as f:
            f.write(output)


######################################
# main
######################################
inputs = read_inputs()
results = run_search(inputs)
write_output(results)