try:
    from .algorithms import Brute_Force as brute_force
    from .algorithms import Greedy as greedy
    from .algorithms import Math_Model as math_model
    from .algorithms import Dynamic_Programming as dynamic_programming
except ImportError:
    import algorithms.Brute_Force as brute_force
    import algorithms.Greedy as greedy
    import algorithms.Math_Model as math_model
    import algorithms.Dynamic_Programming as dynamic_programming


def printMenuRoles():
    # Menu cấp 2: cho người dùng chọn rule cần kiểm tra.
    menu = """
    [1] First character is uppercase
    [2] All characters are uppercase
    [3] All characters are lowercase
    [4] Last character is a digit
    [5] Last character is a special symbol
    [6] First character is a special symbol
    [7] Standard Password
    [0] Back
    """
    print(menu)


def checkPassword(algorithm_module):
    """
    Hiển thị menu rule và gọi check_password(choice) của module thuật toán.
    algorithm_module: một trong brute_force / greedy / math_model / dynamic_programming.
    """
    # Đọc file passwords.txt một lần, rồi tái sử dụng cho mọi lần chọn rule trong phiên này.
    passwords = algorithm_module.load_passwords()
    if not passwords:
        print("[!] No passwords loaded. Returning...")
        return

    # Cho phép người dùng đổi rule nhiều lần mà không phải quay lại menu chính.
    while True:
        try:
            printMenuRoles()
            choice = int(input("[+] Enter your choice: "))

            if choice == 0:
                # Quay về menu trước.
                print("[*] Returning to previous menu...\n")
                break

            if 1 <= choice <= 7:
                # Gọi hàm check_password của module thuật toán đã chọn.
                print("[*] Checking...\n")
                algorithm_module.check_password(choice, passwords)
            else:
                # Giá trị nằm ngoài phạm vi menu.
                print("[!] Invalid choice!")

        except ValueError:
            # Bắt lỗi khi nhập không phải số.
            print("[!] Please enter a valid number!\n")
