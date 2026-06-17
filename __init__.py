def showBanner():
    # Hàm này chỉ dùng để in banner ASCII và phần mô tả ngắn cho chương trình.
    banner = """
            ██████▄ ▄█████▄ ▄█████▄ ▄█████▄ ██ ██ ██ ▄█████▄ ██████▄ ██████▄
            ██▄▄▄██ ██▄▄▄██ ██▄▄▄▄  ██▄▄▄▄  ██ ██ ██ ██   ██ ██   ██ ██   ██
            ██▀▀▀▀  ██▀▀▀██  ▀▀▀▀██  ▀▀▀▀██ ██ ██ ██ ██   ██ ██████  ██   ██
            ██      ██   ██ ▀█████▀ ▀█████▀ ▀██████▀ ▀█████▀ ██  ▀██ ██████▀

            ▄█████▄ ██   ██ ▄██████ ▄█████▄ ██  ▄██ ▐██▌ ▄█████▄ ▄█████▄
            ██      ██▄▄▄██ ██▄▄▄▄  ██      ██▄██▀   ██  ██   ██ ██  ▄▄▄
            ██      ██▀▀▀██ ██▀▀▀▀  ██      ██▀██▄   ██  ██   ██ ██   ██
            ▀█████▀ ██   ██ ▀██████ ▀█████▀ ██  ▀██ ▐██▌ ██   ██ ▀█████▀
    """
    print(banner)

    description = """
    The group project involves analyzing and implementing algorithms for rule-based password checking,
    with a focus on execution time, solution quality, and space complexity.
    """
    print(description)

# Gọi banner ngay khi file được nạp, để người dùng thấy giao diện giới thiệu trước.
showBanner()

try:
    # Import theo kiểu package, phù hợp khi chạy dự án như một module.
    from . import pwd_checking
except ImportError:
    # Fallback khi chạy file trực tiếp trong thư mục hiện tại.
    import pwd_checking


if __name__ == "__main__":
    # Nếu đây là file được chạy trực tiếp, mở menu chính của chương trình.
    pwd_checking.runAlgorithms()
