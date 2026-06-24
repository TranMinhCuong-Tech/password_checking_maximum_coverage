try:
    from ..coverage_problem import run_solver, load_passwords, solve_dp
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_dp


def solve_max_coverage(k, passwords):
    """Goi giai phap exact co memoization."""
    return run_solver("dynamic programming", solve_dp, k, passwords, "output_dp")


def check_password(k, passwords=None):
    """Ham goi chung de giu cau truc dong nhat voi module khac."""
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
