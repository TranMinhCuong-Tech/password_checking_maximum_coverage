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
    # Menu cấp 1: cho người dùng chọn thuật toán muốn benchmark.
    menu = """
    [1] Brute Force
    [2] Greedy
    [3] Math Model
    [4] Dynamic Programming
    [0] Exit
    """
    print(menu)


def runAlgorithms():
    # Vòng lặp chính của chương trình, chạy cho tới khi người dùng chọn thoát.
    while True:
        try:
            printMenuAlgorithms()
            choice = int(input("\n[+] Enter your choice: "))

            if choice == 1:
                # Chạy thuật toán Brute Force.
                print("[*] Running Brute Force...\n")
                rules.checkPassword(brute_force)

            elif choice == 2:
                # Chạy thuật toán Greedy.
                print("[*] Running Greedy...\n")
                rules.checkPassword(greedy)

            elif choice == 3:
                # Chạy thuật toán Math Model.
                print("[*] Running Math Model...\n")
                rules.checkPassword(math_model)

            elif choice == 4:
                # Chạy thuật toán Dynamic Programming.
                print("[*] Running Dynamic Programming...\n")
                rules.checkPassword(dynamic_programming)

            elif choice == 0:
                # Thoát khỏi chương trình.
                print("[*] Exiting...\n")
                break

            else:
                # Người dùng nhập giá trị không hợp lệ.
                print("[!] Invalid choice!")

        except ValueError:
            # Bắt lỗi khi người dùng nhập không phải số.
            print("[!] Please enter a valid number!")


if __name__ == "__main__":
    runAlgorithms()
