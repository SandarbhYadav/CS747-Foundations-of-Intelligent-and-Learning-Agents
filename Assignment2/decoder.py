import argparse


def decode_solution(value_policy_path, state_path):
    states = []
    value_policy = []
    action_list = [0, 1, 2, 4, 6, 7]

    state_data = open(state_path).read().strip().split("\n")
    for row in state_data:
        states.append(row)
    numStates = len(states)

    value_policy_data = open(value_policy_path).read().strip().split("\n")
    for row in value_policy_data:
        value_policy.append(row)

    for i in range(numStates):
        vp = value_policy[i].split()
        print(states[i], action_list[int(vp[1])], vp[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--value-policy", required=True)
    parser.add_argument("--states", required=True)
    args = parser.parse_args()
    value_policy_path = args.value_policy
    states_path = args.states
    
    decode_solution(value_policy_path, states_path)

