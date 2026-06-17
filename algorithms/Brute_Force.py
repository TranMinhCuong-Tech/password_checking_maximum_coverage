import string
import time
import tracemalloc

# Nhóm hàm kiểm tra rule cơ bản.
def first_char_upper(password):
    return len(password) > 0 and password[0].isupper()


def all_upper(password):
    return len(password) > 0 and password.isupper()


def all_lower(password):
    return len(password) > 0 and password.islower()


def ends_with_digit(password):
    return len(password) > 0 and password[-1].isdigit()


def ends_with_special(password):
    return len(password) > 0 and password[-1] in string.punctuation


def starts_with_special(password):
    return len(password) > 0 and password[0] in string.punctuation

# Rule mật khẩu chuẩn: dài hơn 15 ký tự, bắt đầu bằng chữ hoa,
# đồng thời phải có ít nhất một chữ số và một ký tự đặc biệt.
def standard_password(password):
    """
    Standard Password:
    - First character is uppercase
    - Contains at least one digit
    - Contains at least one special character
    - Length > 15
    """
    return (
        len(password) > 15
        and password[0].isupper()
        and any(c.isdigit() for c in password) # co so trong password
        and any(c in string.punctuation for c in password) # co ky tu dac biet trong password
    )


# Ánh xạ lựa chọn menu -> hàm kiểm tra -> file output.
RULES = {
    1: (first_char_upper,    "output_brute_first_char_upper.txt"),
    2: (all_upper,           "output_brute_all_upper.txt"),
    3: (all_lower,           "output_brute_all_lower.txt"),
    4: (ends_with_digit,     "output_brute_ends_with_digit.txt"),
    5: (ends_with_special,   "output_brute_ends_with_special.txt"),
    6: (starts_with_special, "output_brute_starts_with_special.txt"),
    7: (standard_password,   "output_brute_standard_password.txt"),
}


# Đọc danh sách password từ file passwords.txt, bỏ qua các dòng rỗng.
def load_passwords(filename="passwords.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        return []

# Lưu các password thỏa điều kiện ra file output.
def save_results(passwords, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for password in passwords:
            f.write(password + "\n")
    print(f"[+] Results saved to: {filename}")


# Benchmark: duyệt toàn bộ password, đo thời gian và bộ nhớ.
def benchmark(rule_function, passwords, output_file):
    tracemalloc.start()
    start_time = time.perf_counter()

    # Brute Force: kiểm tra từng password lần lượt.
    matched = []
    for password in passwords:
        if rule_function(password):
            matched.append(password)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    save_results(matched, output_file)

    print("\n============= BRUTE FORCE RESULT =============")
    print(f"[+] Rule            : {rule_function.__name__}")
    print(f"[+] Solutions Found : {len(matched)}")
    print(f"[+] Execution Time  : {end_time - start_time:.6f} s")
    print(f"[+] Current Memory  : {current_memory / 1024:.2f} KB")
    print(f"[+] Peak Memory     : {peak_memory / 1024:.2f} KB")
    print("===============================================")

    return matched


def check_password(choice, passwords=None):
    # Chọn rule theo menu rồi chạy benchmark.
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
