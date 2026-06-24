try:
    from . import rules
    from .algorithms import Brute_Force as brute_force
    from .algorithms import Greedy as greedy
    from .algorithms import Math_Model as math_model
    from .algorithms import Dynamic_Programming as dynamic_programming
except ImportError:
    import rules
    import algorithms.Brute_Force as brute_force
    import algorithms.Greedy as greedy
    import algorithms.Math_Model as math_model
    import algorithms.Dynamic_Programming as dynamic_programming


def printMenuAlgorithms():
    """
    In menu cap 1.
    Nguoi dung se chon 1 trong 4 cach giai maximum coverage.
    """
    menu = """
    [1] Brute Force
    [2] Greedy
    [3] Math Model
    [4] Dynamic Programming
    [0] Exit
    """
    print(menu)


def runAlgorithms():
    """Vong lap giao dien chinh cua chuong trinh."""
    while True:
        try:
            printMenuAlgorithms()
            choice = int(input("\n[+] Enter your choice: "))

            if choice == 1:
                # Exact search: duyet to hop rule.
                print("[*] Running Brute Force maximum coverage...\n")
                rules.checkPassword(brute_force)

            elif choice == 2:
                # Thuat toan tham lam.
                print("[*] Running Greedy maximum coverage...\n")
                rules.checkPassword(greedy)

            elif choice == 3:
                # Bitmask exact search.
                print("[*] Running Math Model maximum coverage...\n")
                rules.checkPassword(math_model)

            elif choice == 4:
                # Memoized exact search.
                print("[*] Running Dynamic Programming maximum coverage...\n")
                rules.checkPassword(dynamic_programming)

            elif choice == 0:
                # Thoat chuong trinh.
                print("[*] Exiting...\n")
                break

            else:
                # Lua chon khong hop le.
                print("[!] Invalid choice!")

        except ValueError:
            # Bat truong hop nguoi dung nhap khong phai so.
            print("[!] Please enter a valid number!")


if __name__ == "__main__":
    runAlgorithms()
