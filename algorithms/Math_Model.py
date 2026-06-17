import string
import time
import tracemalloc


def first_char_upper(password):
    # Kiểm tra ký tự đầu có phải chữ hoa hay không.
    return len(password) > 0 and password[0].isupper()


def all_upper(password):
    # Dùng hàm built-in để kiểm tra toàn chuỗi chữ hoa.
    return password.isupper()


def all_lower(password):
    # Dùng hàm built-in để kiểm tra toàn chuỗi chữ thường.
    return password.islower()


def ends_with_digit(password):
    # Kiểm tra ký tự cuối có phải chữ số.
    return len(password) > 0 and password[-1].isdigit()


def ends_with_special(password):
    # Kiểm tra ký tự cuối có thuộc nhóm ký tự đặc biệt hay không.
    return len(password) > 0 and password[-1] in string.punctuation


def starts_with_special(password):
    # Kiểm tra ký tự đầu có phải ký tự đặc biệt hay không.
    return len(password) > 0 and password[0] in string.punctuation


def standard_password(password):
    """
    Math-model style password check.
    Cách viết gọn bằng biểu thức boolean, nhưng logic vẫn giống các module khác.
    """
    return (
        len(password) > 15
        and password[0].isupper()
        and any(c.isdigit() for c in password)
        and any(c in string.punctuation for c in password)
    )


def load_passwords(filename="passwords.txt"):
    # Đọc danh sách password từ file đầu vào.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        return []


def save_results(passwords, filename):
    # Ghi danh sách password hợp lệ ra file output.
    with open(filename, "w", encoding="utf-8") as f:
        for password in passwords:
            f.write(password + "\n")

    print(f"[+] Results saved to: {filename}")


def benchmark(rule_function, passwords, output_file):
    # Chạy kiểm tra và đo hiệu năng cho từng rule.
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

    print("\n============= MATH MODEL RESULT =============")
    print(f"[+] Rule            : {rule_function.__name__}")
    print(f"[+] Solutions Found : {len(matched)}")
    print(f"[+] Execution Time  : {end_time - start_time:.6f} s")
    print(f"[+] Current Memory  : {current_memory / 1024:.2f} KB")
    print(f"[+] Peak Memory     : {peak_memory / 1024:.2f} KB")
    print("=============================================")

    return matched


RULES = {
    # Ánh xạ lựa chọn menu -> hàm kiểm tra -> file output.
    1: (first_char_upper, "output_math_model_first_char_upper.txt"),
    2: (all_upper, "output_math_model_all_upper.txt"),
    3: (all_lower, "output_math_model_all_lower.txt"),
    4: (ends_with_digit, "output_math_model_ends_with_digit.txt"),
    5: (ends_with_special, "output_math_model_ends_with_special.txt"),
    6: (starts_with_special, "output_math_model_starts_with_special.txt"),
    7: (standard_password, "output_math_model_standard_password.txt"),
}


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
