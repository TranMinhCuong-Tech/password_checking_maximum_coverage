try:
    from . import rules
    from .algorithms import Brute_Force as brute_force
    from .algorithms import Dynamic_Programming as dynamic_programming
    from .algorithms import Greedy as greedy
    from .algorithms import Hill_Climbing as hill_climbing
    from .algorithms import ILP_PuLP_CBC as ilp_pulp_cbc
    from .algorithms import Randomized_Search as randomized_search
    from .coverage_problem import load_passwords
except ImportError:
    import rules
    import algorithms.Brute_Force as brute_force
    import algorithms.Dynamic_Programming as dynamic_programming
    import algorithms.Greedy as greedy
    import algorithms.Hill_Climbing as hill_climbing
    from coverage_problem import load_passwords
    import algorithms.ILP_PuLP_CBC as ilp_pulp_cbc
    import algorithms.Randomized_Search as randomized_search


# Module nay la bo dieu khien menu thuat toan.
# Ban than no khong giai bai toan.
# No chi:
# - tai du lieu dau vao
# - hien thi menu bo giai
# - chuyen lua chon cua nguoi dung sang module phu hop
ALGORITHMS = {
    1: ("Brute Force", brute_force),
    2: ("Greedy", greedy),
    3: ("Dynamic Programming", dynamic_programming),
    4: ("ILP + PuLP + CBC", ilp_pulp_cbc),
    5: ("Randomized Search", randomized_search),
    6: ("Hill Climbing", hill_climbing),
}

# Ham printMenuAlgorithms: in menu lua chon cac thuat toan.
def printMenuAlgorithms():
    # Giu van ban menu o mot noi de de cap nhat.
    menu = """
    [1] Brute Force
    [2] Greedy
    [3] Dynamic Programming
    [4] ILP + PuLP + CBC
    [5] Randomized Search
    [6] Hill Climbing
    [0] Return to the previous menu
    [-1] Exit
    """
    print(menu)

# Ham load_password_data: tai du lieu mat khau va kiem tra tinh hop le.
def load_password_data(password_files):
    # Tai ca hai file mat khau truoc khi nguoi dung chon thuat toan.
    password_data = load_passwords(password_files)
    real_count = len(password_data.get("real", []))
    mutated_count = len(password_data.get("mutated", []))

    print(f"[+] Da tai mat khau that    : {real_count}")
    print(f"[+] Da tai mat khau bien doi : {mutated_count}")

    if real_count == 0 or mutated_count == 0:
        print("[!] Thieu du lieu mat khau. Vui long kiem tra cac file dau vao.")
        return None

    return password_data

# Ham run_selected_algorithm: chay thuat toan duoc nguoi dung chon.
def run_selected_algorithm(choice, k, password_data):
    # Anh xa lua chon menu -> module bo giai.
    algorithm_name, algorithm_module = ALGORITHMS[choice]
    print(f"[*] Dang chay {algorithm_name} voi k = {k}...\n")
    return algorithm_module.solve_max_coverage(k, password_data)

# Ham runAlgorithms: vong lap chinh de dieu huong menu thuat toan.
def runAlgorithms(k, password_files):
    # Vong lap nay se hoi cho den khi nguoi dung thoat hoac quay lai.
    password_data = load_password_data(password_files)
    if password_data is None:
        return

    print(f"[+] Tong so luat ung vien    : {len(rules.RULES)}")
    print(f"[+] So luat can chon co dinh k: {k}")

    while True:
        try:
            printMenuAlgorithms()
            choice_raw = input("\n[+] Nhap lua chon cua ban: ").strip().lower()
            choice = int(choice_raw)

            if choice == 0:
                # Quay lai menu truoc trong __init__.py.
                print("[*] Quay lai menu truoc...\n")
                return "back"

            if choice == -1:
                print("[*] Dang thoat...\n")
                return "exit"

            if choice not in ALGORITHMS:
                print("[!] Lua chon khong hop le!")
                continue

            run_selected_algorithm(choice, k, password_data)

        except ValueError:
            print("[!] Vui long nhap mot so hop le!")


if __name__ == "__main__":
    runAlgorithms(3, ("real_passwords.txt", "mutated_passwords.txt"))
