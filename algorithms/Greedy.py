try:
    from ..coverage_problem import run_solver, load_passwords, solve_greedy
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_greedy


def solve_max_coverage(k, passwords):
    """Goi giai phap tham lam xap xi."""
    return run_solver("greedy", solve_greedy, k, passwords, "output_greedy")


def check_password(k, passwords=None):
    """Ham goi chung de giu cau truc dong nhat voi module khac."""
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
