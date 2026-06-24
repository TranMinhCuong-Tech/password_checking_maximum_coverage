try:
    from ..coverage_problem import run_solver, load_passwords, solve_bruteforce
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_bruteforce


def solve_max_coverage(k, passwords):
    """Goi giai phap exact bang duyet to hop."""
    return run_solver("brute force", solve_bruteforce, k, passwords, "output_brute")


def check_password(k, passwords=None):
    """Ham goi chung de giu cau truc dong nhat voi cac module khac."""
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
