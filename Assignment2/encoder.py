import argparse


def decode_balls_runs(s):
    p = s[0]
    b = int(s[1:3])
    r = int(s[3:])
    return p, b, r


def encode_balls_runs(b, r, o, p):
    bb = b-1
    rr = r-o
    bbrr = str(bb).zfill(2) + str(rr).zfill(2)
    if p == "A":
        if (b % 6) == 1:
            if o == 0 or o == 2 or o == 4 or o == 6:
                bbrr = "B"+bbrr
            else:
                bbrr = "A"+bbrr
        else:
            if o == 1 or o ==3:
                bbrr = "B"+bbrr
            else:
                bbrr = "A"+bbrr
    elif p == "B":
        if (b % 6) == 1:
            if o == 0:
                bbrr = "A"+bbrr
            else:
                bbrr = "B"+bbrr
        else:
            if o == 1:
                bbrr = "A"+bbrr
            else:
                bbrr = "B"+bbrr
    return bbrr


def get_next_state(balls_left, runs_req, outcome, player):
    if outcome == -1:
        return "loss"
    else:
        if outcome >= runs_req:
            return "win"
        else:
            if balls_left == 1:
                return "loss"
            else:
                s = encode_balls_runs(balls_left, runs_req, outcome, player)
                return s


def get_reward(st):
    if st == "win":
        return 1
    else:
        return 0


def get_prob_B(outcome_B, q):
    if outcome_B == -1:
        return q
    else:
        return (1 - q) / 2.0


def print_transition(states_list, prob_list, numActions, q):
    num_states = len(states_list)
    action_list = [0, 1, 2, 4, 6, 7]
    outcome_list_A = [0, 1, 2, 3, 4, 6, -1]
    outcome_list_B = [0, 1, -1]
    for s1 in range(num_states-2):
        state = states_list[s1]
        player, balls_left, runs_req = decode_balls_runs(state)
        if player == "A":
            for ac in range(numActions-1):
                prob_W = 0.0
                prob_L = 0.0
                for oc_A in range(7):
                    outcome_A = outcome_list_A[oc_A]
                    next_state_A = get_next_state(balls_left, runs_req, outcome_A, player)
                    s2_A = states_list.index(next_state_A)
                    reward_A = get_reward(next_state_A)
                    if next_state_A == "win":
                        prob_W += float(prob_list[ac][oc_A])
                    elif next_state_A == "loss":
                        prob_L += float(prob_list[ac][oc_A])
                    else:
                        prob_A = float(prob_list[ac][oc_A])
                        if prob_A != 0:
                            print("transition", s1, ac, s2_A, reward_A, prob_A)
                if prob_W != 0:
                    print("transition", s1, ac, states_list.index("win"), 1, prob_W)
                if prob_L != 0:
                    print("transition", s1, ac, states_list.index("loss"), 0, prob_L)
        elif player == "B":
            for oc_B in range(3):
                outcome_B = outcome_list_B[oc_B]
                next_state_B = get_next_state(balls_left, runs_req, outcome_B, player)
                s2_B = states_list.index(next_state_B)
                reward_B = get_reward(next_state_B)
                prob_B = get_prob_B(outcome_B, q)
                if prob_B != 0:
                    print("transition", s1, 5, s2_B, reward_B, prob_B)


def encode_mdp(state_path, parameter_path, q):
    states = []
    state_list = []
    state_data = open(state_path).read().strip().split("\n")
    for row in state_data:
        states.append(row)
    for state in states:
        state_list.append("A"+state)
    for state in states:
        state_list.append("B"+state)

    state_list.append("loss")
    state_list.append("win")
    numStates = len(state_list)

    numActions = 0
    prob_list = []
    parameter_data = open(parameter_path).read().strip().split("\n")
    for row in parameter_data:
        col = row.split()
        if col[0] != "action":
            temp = col[2:]
            temp.append(col[1])
            prob_list.append(temp)
            numActions += 1

    # dummy action for player B
    numActions += 1

    print("numStates", numStates)
    print("numActions", numActions)
    print("end", numStates-2, numStates-1)
    print_transition(state_list, prob_list, numActions, q)
    print("mdptype", "episodic")
    print("discount", 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--states", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--q", type=float, required=True)
    args = parser.parse_args()
    states_path = args.states
    parameters_path = args.parameters
    weakness_q = args.q

    encode_mdp(states_path, parameters_path, weakness_q)
