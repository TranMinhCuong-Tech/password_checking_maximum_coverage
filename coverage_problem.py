import itertools
import string
import time
import tracemalloc
from functools import lru_cache


# ============================================================
# CAC HAM KIEM TRA RULE
# Moi ham nhan vao 1 password va tra ve True/False.
# Trong bai toan maximum coverage, moi rule tuong ung voi mot
# tap con cac password duoc no "phu" (cover).
# ============================================================
def first_char_upper(password):
    """Tra ve True neu ky tu dau tien la chu hoa."""
    return len(password) > 0 and password[0].isupper()


def all_upper(password):
    """Tra ve True neu toan bo password la chu hoa."""
    return len(password) > 0 and password.isupper()


def all_lower(password):
    """Tra ve True neu toan bo password la chu thuong."""
    return len(password) > 0 and password.islower()


def ends_with_digit(password):
    """Tra ve True neu ky tu cuoi cung la chu so."""
    return len(password) > 0 and password[-1].isdigit()


def ends_with_special(password):
    """Tra ve True neu ky tu cuoi cung la ky tu dac biet."""
    return len(password) > 0 and password[-1] in string.punctuation


def starts_with_special(password):
    """Tra ve True neu ky tu dau tien la ky tu dac biet."""
    return len(password) > 0 and password[0] in string.punctuation


def standard_password(password):
    """
    Rule tong hop:
    - do dai lon hon 15
    - ky tu dau la chu hoa
    - co it nhat 1 chu so
    - co it nhat 1 ky tu dac biet
    """
    return (
        len(password) > 15
        and password[0].isupper()
        and any(ch.isdigit() for ch in password)
        and any(ch in string.punctuation for ch in password)
    )


# ============================================================
# TAP RULE UNG VIEN
# RULES luu:
# - label: ten hien thi
# - predicate: ham kiem tra rule
# Day la tap cac "set" trong bai toan maximum coverage.
# ============================================================
RULES = {
    1: {"label": "First character is uppercase", "predicate": first_char_upper},
    2: {"label": "All characters are uppercase", "predicate": all_upper},
    3: {"label": "All characters are lowercase", "predicate": all_lower},
    4: {"label": "Last character is a digit", "predicate": ends_with_digit},
    5: {"label": "Last character is a special symbol", "predicate": ends_with_special},
    6: {"label": "First character is a special symbol", "predicate": starts_with_special},
    7: {"label": "Standard password", "predicate": standard_password},
}

RULE_IDS = tuple(RULES.keys())


def load_passwords(filename="passwords.txt"):
    """
    Doc danh sach password tu file dau vao.
    Bo qua cac dong trong de tranh tinh nham vao tap du lieu.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        return []


def build_rule_masks(passwords):
    """
    Chuyen moi rule thanh bitmask.
    Moi bit i = 1 neu password thu i nam trong tap rule do.
    Cach nay giup tinh union cac tap con nhanh hon rat nhieu.
    """
    masks = {}
    for rule_id in RULE_IDS:
        predicate = RULES[rule_id]["predicate"]
        mask = 0
        for index, password in enumerate(passwords):
            if predicate(password):
                mask |= 1 << index
        masks[rule_id] = mask
    return masks


def mask_to_passwords(passwords, mask):
    """Dich bitmask ve lai danh sach password tuong ung."""
    return [password for index, password in enumerate(passwords) if mask & (1 << index)]


def rule_names(rule_ids):
    """Tao nhan hien thi cho danh sach rule da chon."""
    return [f"[{rule_id}] {RULES[rule_id]['label']}" for rule_id in rule_ids]


def passwords_for_rule(rule_id, passwords):
    """Lọc đúng các password thỏa một rule duy nhất."""
    predicate = RULES[rule_id]["predicate"]
    return [password for password in passwords if predicate(password)]


def save_answer(filename, passwords):
    """
    Ghi file output.
    Y nghia output:
    - chi luu dap an cuoi cung
    - khong luu thong so benchmark
    - khong luu danh sach rule
    - khong copy toan bo passwords.txt
    - neu khong co ket qua thi ghi null
    """
    with open(filename, "w", encoding="utf-8") as f:
        if passwords:
            for password in passwords:
                f.write(f"{password}\n")
        else:
            f.write("null\n")

    print(f"[+] Results saved to: {filename}")


def result_payload(method_name, k, selected_rule_ids, passwords, covered_mask):
    """
    Dong goi ket qua ve dang dict.
    Cac solver khac nhau se tra ve cung 1 kieu du lieu de giao dien in ket qua
    va luu file duoc thong nhat.
    """
    covered_passwords = mask_to_passwords(passwords, covered_mask)
    return {
        "method": method_name,
        "k": k,
        "selected_rule_ids": selected_rule_ids,
        "selected_rules": rule_names(selected_rule_ids),
        "covered_mask": covered_mask,
        "covered_passwords": covered_passwords,
        "coverage_count": len(covered_passwords),
        "total_passwords": len(passwords),
    }


def run_solver(method_name, solver, rule_id, passwords, output_prefix):
    """
    Chay 1 solver, do thoi gian va bo nho, roi ghi dap an ra file.
    Day la lop wrapper chung cho ca 4 thuat toan.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    selected_passwords = passwords_for_rule(rule_id, passwords)
    result = {
        "method": method_name,
        "rule_id": rule_id,
        "selected_rule": rule_names([rule_id])[0],
        "covered_passwords": selected_passwords,
        "coverage_count": len(selected_passwords),
        "total_passwords": len(passwords),
    }

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_file = f"{output_prefix}_rule{rule_id}.txt"
    save_answer(output_file, selected_passwords)

    print(f"\n============= {method_name.upper()} =============")
    print(f"[+] Selected Rule  : {result['selected_rule']}")
    print(f"[+] Covered        : {result['coverage_count']}/{result['total_passwords']}")
    print(f"[+] Execution Time : {end_time - start_time:.6f} s")
    print(f"[+] Memory Used    : {current_memory / 1024:.2f} KB | {current_memory / (1024 * 1024):.4f} MB")
    print(f"[+] Peak Memory    : {peak_memory / 1024:.2f} KB | {peak_memory / (1024 * 1024):.4f} MB")
    print("==============================================")
    return result


def solve_bruteforce(passwords, k):
    """
    Giai dung bai toan maximum coverage bang cach duyet tat ca to hop.
    Day la cach exact, cho ket qua dung tuyet doi, nhung chi phi tang nhanh
    theo so luong rule.
    """
    rule_masks = build_rule_masks(passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

    if k == 0 or not passwords:
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
    Giai xap xi bang tham lam.
    Moi buoc chon rule lam tang so password duoc phu nhieu nhat hien tai.
    Cach nay nhanh, nhung khong bao dam toi uu toan cuc.
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


def solve_math_model(passwords, k):
    """
    Duyet tat ca tap con co dung k rule bang bitmask.
    Cach nay gan voi mo hinh toan hoc cua maximum coverage va de trinh bay
    trong bao cao.
    """
    rule_masks = build_rule_masks(passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

    if k == 0 or not passwords:
        return result_payload("math model", k, [], passwords, 0)

    best_subset_mask = 0
    best_coverage_mask = 0
    best_count = -1
    total_subsets = 1 << len(rule_ids)

    for subset_mask in range(total_subsets):
        if subset_mask.bit_count() != k:
            continue

        coverage_mask = 0
        for index, rule_id in enumerate(rule_ids):
            if subset_mask & (1 << index):
                coverage_mask |= rule_masks[rule_id]

        coverage_count = coverage_mask.bit_count()
        if coverage_count > best_count:
            best_count = coverage_count
            best_subset_mask = subset_mask
            best_coverage_mask = coverage_mask

    selected_rule_ids = [
        rule_id
        for index, rule_id in enumerate(rule_ids)
        if best_subset_mask & (1 << index)
    ]
    return result_payload("math model", k, selected_rule_ids, passwords, best_coverage_mask)


def solve_dp(passwords, k):
    """
    Dung memoization de luu ket qua tot nhat cho moi trang thai.
    Ban chat day van la exact search, nhung co cache de tranh tinh lai.
    """
    rule_masks = build_rule_masks(passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

    if k == 0 or not passwords:
        return result_payload("dynamic programming", k, [], passwords, 0)

    @lru_cache(maxsize=None)
    def best_solution(selected_mask, remaining):
        # selected_mask: trang thai cac rule da chon
        # remaining: so rule con lai can chon
        if remaining == 0:
            return 0, ()

        best_mask = 0
        best_selected = ()
        for index, rule_id in enumerate(rule_ids):
            if selected_mask & (1 << index):
                # Da chon rule nay roi thi bo qua.
                continue
            rest_mask, rest_selected = best_solution(selected_mask | (1 << index), remaining - 1)
            candidate_mask = rule_masks[rule_id] | rest_mask
            if candidate_mask.bit_count() > best_mask.bit_count() or not best_selected:
                best_mask = candidate_mask
                best_selected = (rule_id,) + rest_selected
        return best_mask, best_selected

    covered_mask, selected_rules = best_solution(0, k)
    return result_payload("dynamic programming", k, list(selected_rules), passwords, covered_mask)
