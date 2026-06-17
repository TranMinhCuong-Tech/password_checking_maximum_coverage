"""
Greedy Algorithm
----------------
Tại mỗi bước, thuật toán đưa ra quyết định tối ưu cục bộ:
- Duyệt từng ký tự một lần duy nhất (early-exit ngay khi thoả điều kiện).
- Không quay lui, không lưu trạng thái toàn cục.

So với Brute Force:
- Cùng O(n * m) worst-case, nhưng best/average case nhanh hơn nhờ early-exit.
- Space complexity O(1) per password (kiểm tra tại chỗ, không build list phụ).
"""

import string
import time
import tracemalloc


def first_char_upper(password):
    # Chỉ cần xem ký tự đầu tiên là đủ kết luận.
    return len(password) > 0 and password[0].isupper()


def all_upper(password):
    # Dừng ngay khi gặp ký tự không phải chữ hoa.
    if not password:
        return False
    for ch in password:
        if not ch.isupper():
            return False
    return True


def all_lower(password):
    # Dừng ngay khi gặp ký tự không phải chữ thường.
    if not password:
        return False
    for ch in password:
        if not ch.islower():
            return False
    return True


def ends_with_digit(password):
    # Chỉ cần kiểm tra ký tự cuối.
    return len(password) > 0 and password[-1].isdigit()


def ends_with_special(password):
    # Chỉ cần kiểm tra ký tự cuối.
    return len(password) > 0 and password[-1] in string.punctuation


def starts_with_special(password):
    # Chỉ cần kiểm tra ký tự đầu.
    return len(password) > 0 and password[0] in string.punctuation


def standard_password(password):
    """
    Greedy Standard Password – sắp xếp điều kiện từ rẻ → đắt:
    1. Kiểm tra độ dài trước.
    2. Kiểm tra ký tự đầu.
    3. Duyệt một lần để tìm cả số và ký tự đặc biệt.
    """
    if len(password) <= 15:
        return False
    if not password[0].isupper():
        return False

    has_digit = False
    has_special = False
    for ch in password:
        if ch.isdigit():
            has_digit = True
        elif ch in string.punctuation:
            has_special = True
        if has_digit and has_special:   # Đủ điều kiện thì thoát sớm.
            return True
    return False

# Ánh xạ lựa chọn menu -> hàm kiểm tra -> file output.
RULES = {
    1: (first_char_upper,    "output_greedy_first_char_upper.txt"),
    2: (all_upper,           "output_greedy_all_upper.txt"),
    3: (all_lower,           "output_greedy_all_lower.txt"),
    4: (ends_with_digit,     "output_greedy_ends_with_digit.txt"),
    5: (ends_with_special,   "output_greedy_ends_with_special.txt"),
    6: (starts_with_special, "output_greedy_starts_with_special.txt"),
    7: (standard_password,   "output_greedy_standard_password.txt"),
}


def load_passwords(filename="passwords.txt"):
    # Đọc danh sách password từ file, bỏ qua các dòng rỗng.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        return []


def save_results(passwords, filename):
    # Ghi các password thỏa điều kiện ra file kết quả.
    with open(filename, "w", encoding="utf-8") as f:
        for password in passwords:
            f.write(password + "\n")
    print(f"[+] Results saved to: {filename}")


def benchmark(rule_function, passwords, output_file):
    # Đo thời gian và bộ nhớ trong lúc kiểm tra toàn bộ danh sách password.
    tracemalloc.start()
    start_time = time.perf_counter()

    matched = []
    for password in passwords:
        if rule_function(password):
            matched.append(password)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    save_results(matched, output_file)

    print("\n============= GREEDY RESULT =============")
    print(f"[+] Rule            : {rule_function.__name__}")
    print(f"[+] Solutions Found : {len(matched)}")
    print(f"[+] Execution Time  : {end_time - start_time:.6f} s")
    print(f"[+] Current Memory  : {current_memory / 1024:.2f} KB")
    print(f"[+] Peak Memory     : {peak_memory / 1024:.2f} KB")
    print("==========================================")

    return matched


def check_password(choice, passwords=None):
    # Hàm điều phối: chọn rule theo menu rồi chạy benchmark.
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []

    if choice == 0:
        print("[*] Exiting...")
        return []

    if choice not in RULES:
        print("[!] Invalid choice!")
        return []

    rule_function, output_file = RULES[choice]
    return benchmark(rule_function, passwords, output_file)
