import itertools
import time
import tracemalloc
from functools import lru_cache

try:
    import pulp
except ImportError:  # pragma: no cover - dependency is optional until installed
    pulp = None

try:
    from .rules import RULES, RULE_IDS
except ImportError:
    from rules import RULES, RULE_IDS


def load_passwords(filenames=("real_passwords.txt", "mutated_passwords.txt")):
    """
    Doc file password that va file password bien tau.
    Moi dong la mot password. Dong trong se bi bo qua.
    """
    if isinstance(filenames, str):
        filenames = (filenames, "mutated_passwords.txt")

    real_file = filenames[0] if len(filenames) > 0 else "real_passwords.txt"
    mutated_file = filenames[1] if len(filenames) > 1 else "mutated_passwords.txt"

    data = {"real": [], "mutated": []}
    for key, filename in (("real", real_file), ("mutated", mutated_file)):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data[key] = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] File '{filename}' not found.")
    return data


def get_universe_passwords(password_data):
    if isinstance(password_data, dict):
        return password_data.get("real", [])
    return password_data


def get_mutated_passwords(password_data):
    if isinstance(password_data, dict):
        return set(password_data.get("mutated", []))
    return set(password_data)


def normalize_candidates(candidates):
    if isinstance(candidates, str):
        return (candidates,)
    return tuple(candidates)


def build_rule_masks(passwords):
    """
    Chuyen moi rule thanh bitmask.
    Bit i = 1 neu password that thu i tao ra it nhat mot bien the
    nam trong mutated_passwords.txt khi ap dung rule do.
    """
    real_passwords = get_universe_passwords(passwords)
    mutated_passwords = get_mutated_passwords(passwords)
    masks = {}
    for rule_id in RULE_IDS:
        transform = RULES[rule_id]["transform"]
        mask = 0
        for index, password in enumerate(real_passwords):
            candidates = normalize_candidates(transform(password))
            if any(candidate in mutated_passwords for candidate in candidates):
                mask |= 1 << index
        masks[rule_id] = mask
    return masks


def mask_to_passwords(passwords, mask):
    real_passwords = get_universe_passwords(passwords)
    return [password for index, password in enumerate(real_passwords) if mask & (1 << index)]


def rule_names(rule_ids):
    return [f"[{rule_id}] {RULES[rule_id]['label']}" for rule_id in rule_ids]


def result_payload(method_name, k, selected_rule_ids, passwords, covered_mask):
    covered_passwords = mask_to_passwords(passwords, covered_mask)
    total_passwords = len(get_universe_passwords(passwords))
    return {
        "method": method_name,
        "k": k,
        "selected_rule_ids": selected_rule_ids,
        "selected_rules": rule_names(selected_rule_ids),
        "covered_mask": covered_mask,
        "covered_passwords": covered_passwords,
        "coverage_count": len(covered_passwords),
        "total_passwords": total_passwords,
    }


def save_answer(filename, result):
    """
    Ghi ket qua theo format:
    - Method
    - Fixed k
    - Selected rules
    - Covered passwords
    - Coverage
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Method:\n")
        f.write(f"{result['method']}\n")

        f.write("\nFixed number of selected rules:\n")
        f.write(f"{result['k']}\n")

        f.write("\nSelected rules:\n")
        if result["selected_rules"]:
            for rule in result["selected_rules"]:
                f.write(f"{rule}\n")
        else:
            f.write("null\n")

        f.write("\nCovered passwords:\n")
        if result["covered_passwords"]:
            for password in result["covered_passwords"]:
                f.write(f"{password}\n")
        else:
            f.write("null\n")

        f.write("\nCoverage:\n")
        f.write(f"{result['coverage_count']} / {result['total_passwords']}\n")

    print(f"[+] Results saved to: {filename}")


def run_solver(method_name, solver, k, passwords, output_prefix):
    """
    Chay solver, do thoi gian va bo nho, roi ghi dap an ra file.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    result = solver(passwords, k)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_file = f"{output_prefix}_k{k}.txt"
    save_answer(output_file, result)

    print(f"\n============= {method_name.upper()} =============")
    print("[+] Selected Rules :")
    if result["selected_rules"]:
        for rule in result["selected_rules"]:
            print(f"    {rule}")
    else:
        print("    null")
    print(f"[+] Covered        : {result['coverage_count']}/{result['total_passwords']}")
    print(f"[+] Execution Time : {end_time - start_time:.6f} s")
    print(f"[+] Memory Used    : {current_memory / 1024:.2f} KB | {current_memory / (1024 * 1024):.4f} MB")
    print(f"[+] Peak Memory    : {peak_memory / 1024:.2f} KB | {peak_memory / (1024 * 1024):.4f} MB")
    print("==============================================")
    return result


def solve_bruteforce(passwords, k):
    """
    Exact search: duyet tat ca to hop gom dung k rule.
    """
    rule_masks = build_rule_masks(passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

    if k == 0 or not get_universe_passwords(passwords):
        return result_payload("brute force", k, [], passwords, 0)

    best_rule_ids = []
    best_mask = 0
    best_count = -1

    for combo in itertools.combinations(rule_ids, k):
        mask = 0
        for rule_id in combo:
            mask |= rule_masks[rule_id]
        count = mask.bit_count()
        if count > best_count:
            best_count = count
            best_mask = mask
            best_rule_ids = list(combo)

    return result_payload("brute force", k, best_rule_ids, passwords, best_mask)


def solve_greedy(passwords, k):
    """
    Greedy: moi buoc chon rule tang coverage nhieu nhat.
    """
    rule_masks = build_rule_masks(passwords)
    remaining_rule_ids = set(RULE_IDS)
    selected_rule_ids = []
    covered_mask = 0
    k = max(0, min(k, len(RULE_IDS)))

    while len(selected_rule_ids) < k and remaining_rule_ids:
        best_rule_id = None
        best_mask = covered_mask
        best_gain = -1

        for rule_id in sorted(remaining_rule_ids):
            candidate_mask = covered_mask | rule_masks[rule_id]
            gain = candidate_mask.bit_count() - covered_mask.bit_count()
            if gain > best_gain:
                best_gain = gain
                best_rule_id = rule_id
                best_mask = candidate_mask

        if best_rule_id is None:
            break

        selected_rule_ids.append(best_rule_id)
        remaining_rule_ids.remove(best_rule_id)
        covered_mask = best_mask

    return result_payload("greedy", k, selected_rule_ids, passwords, covered_mask)


def solve_ilp_pulp_cbc(passwords, k):
    """
    Exact 0-1 Integer Linear Programming model for Maximum Coverage.

    Decision variables:
    - x_i = 1 if rule i is selected
    - y_j = 1 if password j is covered

    Objective:
    maximize sum(y_j)

    Constraints:
    - sum(x_i) = k
    - y_j <= sum(a_ij * x_i) for every password j
    - x_i, y_j are binary

    The model is solved by PuLP using CBC.
    """
    if pulp is None:
        raise RuntimeError(
            "PuLP is required for ILP_PuLP_CBC. Install it with `pip install pulp`."
        )

    rule_masks = build_rule_masks(passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

    if k == 0 or not get_universe_passwords(passwords):
        return result_payload("ILP_PuLP_CBC", k, [], passwords, 0)

    real_passwords = get_universe_passwords(passwords)

    problem = pulp.LpProblem("MaximumCoverage", pulp.LpMaximize)
    x_vars = {
        rule_id: pulp.LpVariable(f"x_{rule_id}", cat=pulp.LpBinary)
        for rule_id in rule_ids
    }
    y_vars = {
        index: pulp.LpVariable(f"y_{index}", cat=pulp.LpBinary)
        for index in range(len(real_passwords))
    }

    problem += pulp.lpSum(y_vars[index] for index in range(len(real_passwords)))
    problem += pulp.lpSum(x_vars[rule_id] for rule_id in rule_ids) == k

    for index, password in enumerate(real_passwords):
        covering_rules = []
        for rule_id in rule_ids:
            if rule_masks[rule_id] & (1 << index):
                covering_rules.append(x_vars[rule_id])

        if covering_rules:
            problem += y_vars[index] <= pulp.lpSum(covering_rules)
        else:
            problem += y_vars[index] == 0

    solver = pulp.PULP_CBC_CMD(msg=False)
    status = problem.solve(solver)
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(
            f"CBC did not find an optimal solution. Status: {pulp.LpStatus[status]}"
        )

    selected_rule_ids = [
        rule_id
        for rule_id in rule_ids
        if pulp.value(x_vars[rule_id]) and pulp.value(x_vars[rule_id]) > 0.5
    ]

    coverage_mask = 0
    for rule_id in selected_rule_ids:
        coverage_mask |= rule_masks[rule_id]

    return result_payload(
        "ILP_PuLP_CBC",
        k,
        selected_rule_ids,
        passwords,
        coverage_mask,
    )


def solve_dp(passwords, k):
    """
    Exact search co memoization.
    """
    rule_masks = build_rule_masks(passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

    if k == 0 or not get_universe_passwords(passwords):
        return result_payload("dynamic programming", k, [], passwords, 0)

    @lru_cache(maxsize=None)
    def best_solution(start_index, remaining):
        if remaining == 0:
            return 0, ()

        best_mask = 0
        best_selected = ()
        last_start = len(rule_ids) - remaining + 1
        for index in range(start_index, last_start):
            rule_id = rule_ids[index]
            rest_mask, rest_selected = best_solution(index + 1, remaining - 1)
            candidate_mask = rule_masks[rule_id] | rest_mask
            if candidate_mask.bit_count() > best_mask.bit_count() or not best_selected:
                best_mask = candidate_mask
                best_selected = (rule_id,) + rest_selected
        return best_mask, best_selected

    covered_mask, selected_rules = best_solution(0, k)
    return result_payload("dynamic programming", k, list(selected_rules), passwords, covered_mask)
