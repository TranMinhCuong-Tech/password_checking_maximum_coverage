try:
    from . import rules
    from .algorithms import Brute_Force as brute_force
    from .algorithms import Greedy as greedy
    from .algorithms import ILP_PuLP_CBC as ilp_pulp_cbc
    from .algorithms import Dynamic_Programming as dynamic_programming
except ImportError:
    import rules
    import algorithms.Brute_Force as brute_force
    import algorithms.Greedy as greedy
    import algorithms.ILP_PuLP_CBC as ilp_pulp_cbc
    import algorithms.Dynamic_Programming as dynamic_programming


def printMenuAlgorithms():
    # chon thuat toan de giai quyet
    menu = """
    [1] Brute Force
    [2] Greedy
    [3] ILP_PuLP_CBC (PuLP + CBC)
    [4] Dynamic Programming
    [0] Return to the previous menu
    [-1] Exit
    """
    print(menu)


def runAlgorithms(k, password_files):
    # vong lap cua giao dien chinh
    while True:
        try:
            printMenuAlgorithms()
            choice_raw = input("\n[+] Enter your choice: ").strip().lower()

            if choice_raw == "e":
                # Thoat chuong trinh.
                print("[*] Exiting...\n")
                return "exit"

            choice = int(choice_raw)

            if choice == 1:
                # thuat toan vet can
                print("[*] Running Brute Force...\n")
                rules.checkPassword(brute_force, k, password_files)

            elif choice == 2:
                # thuat toan tham lam.
                print("[*] Running Greedy...\n")
                rules.checkPassword(greedy, k, password_files)

            elif choice == 3:
                # Exact ILP model solved by PuLP and CBC.
                print("[*] Running ILP_PuLP_CBC (PuLP + CBC)...\n")
                rules.checkPassword(ilp_pulp_cbc, k, password_files)

            elif choice == 4:
                # Memoized exact search.
                print("[*] Running Dynamic Programming...\n")
                rules.checkPassword(dynamic_programming, k, password_files)

            elif choice == 0:
                # Quay ve menu truoc.
                print("[*] Returning to the previous menu...\n")
                return "back"

            elif choice == -1:
                # Thoat chuong trinh.
                print("[*] Exiting...\n")
                return "exit"

            else:
                # Lua chon khong hop le.
                print("[!] Invalid choice!")

        except ValueError:
            # Bat truong hop nguoi dung nhap khong phai so.
            print("[!] Please enter a valid number!")


if __name__ == "__main__":
    runAlgorithms(3, ("real_passwords.txt", "mutated_passwords.txt"))
