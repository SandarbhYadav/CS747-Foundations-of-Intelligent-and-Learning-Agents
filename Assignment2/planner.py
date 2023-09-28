import argparse
import numpy as np
import pulp as plp


def extract_mdp(path):
    mdp = {}
    data = open(path).read().strip().split("\n")
    for row in data:
        col = row.split()
        if col[0] == "numStates":
            mdp["S"] = int(col[-1])
        elif col[0] == "numActions":
            mdp["A"] = int(col[-1])
            mdp["T"] = np.zeros((mdp["S"], mdp["A"], mdp["S"]))
            mdp["R"] = np.zeros((mdp["S"], mdp["A"], mdp["S"]))
        elif col[0] == "end":
            mdp["end"] = list(map(int, col[1:]))
        elif col[0] == "transition":
            s1 = int(col[1])
            ac = int(col[2])
            s2 = int(col[3])
            r = float(col[4])
            p = float(col[5])
            mdp["T"][s1, ac, s2] = p
            mdp["R"][s1, ac, s2] = r
        elif col[0] == "mdptype":
            mdp["mdptype"] = col[-1]
        elif col[0] == "discount":
            mdp["Y"] = float(col[-1])
    return mdp


def extract_policy(path):
    pol = []
    data = open(path).read().strip().split("\n")
    for row in data:
        pol.append(int(row))
    policy = np.array(pol)
    return policy


def value_evaluation(mdp, policy):
    T_policy = mdp["T"][np.arange(mdp["S"]), policy]
    R_policy = mdp["R"][np.arange(mdp["S"]), policy]
    value = np.squeeze(np.linalg.inv(np.eye(mdp["S"]) - mdp["Y"] * T_policy)
                       @ np.sum(T_policy * R_policy, axis=-1, keepdims=True))
    return value


def action_value_evaluation(mdp, value):
    action_value = np.sum(mdp["T"] * (mdp["R"] + mdp["Y"] * value), axis=-1)
    return action_value


def value_iteration(mdp):
    value = np.zeros(mdp["S"])
    value_new = value
    while 1:
        value_new = np.max(np.sum(mdp["T"] * (mdp["R"] + mdp["Y"] * value), axis=-1), axis=-1)
        if np.allclose(value_new, value, rtol=0, atol=1e-9):
            break
        value = value_new
    policy = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["Y"] * value_new), axis=-1), axis=-1)
    return value_new, policy


def howard_policy_iteration(mdp):
    policy = np.random.randint(low=0, high=mdp["A"], size=mdp["S"])
    policy_new = policy
    while 1:
        value = value_evaluation(mdp, policy)
        policy_new = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["Y"] * value), axis=-1), axis=-1)
        if np.array_equal(policy_new, policy):
            break
        policy = policy_new
    return value, policy_new


def linear_programming(mdp):
    prob = plp.LpProblem("MDP", plp.LpMinimize)
    value = np.array(list(plp.LpVariable.dicts("value", [i for i in range(mdp["S"])]).values()))
    prob += plp.lpSum(value)
    for s in range(mdp["S"]):
        for a in range(mdp["A"]):
            prob += value[s] >= plp.lpSum(mdp["T"][s, a] * (mdp["R"][s, a] + mdp["Y"] * value))
    prob.solve(plp.apis.PULP_CBC_CMD(msg=0))
    value = np.array(list(map(plp.value, value)))
    policy = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["Y"] * value), axis=-1), axis=-1)
    return value, policy


def print_output(value, policy):
    for i in range(len(value)):
        print('{:.6f}'.format(round(value[i], 6)) + " " + str(int(policy[i])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp", required=True)
    parser.add_argument("--algorithm", default="hpi")
    parser.add_argument("--policy", default="NA")
    args = parser.parse_args()
    mdp_path = args.mdp
    algo = args.algorithm
    policy_path = args.policy

    extracted_mdp = extract_mdp(mdp_path)

    if policy_path == "NA":
        if algo == "vi":
            optimal_value, optimal_policy = value_iteration(extracted_mdp)
        elif algo == "hpi":
            optimal_value, optimal_policy = howard_policy_iteration(extracted_mdp)
        elif algo == "lp":
            optimal_value, optimal_policy = linear_programming(extracted_mdp)
        print_output(optimal_value, optimal_policy)
    else:
        extracted_policy = extract_policy(policy_path)
        policy_value = value_evaluation(extracted_mdp, extracted_policy)
        print_output(policy_value, extracted_policy)
