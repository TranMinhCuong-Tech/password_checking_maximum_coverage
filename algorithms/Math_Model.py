try:
    from ..coverage_problem import run_solver, load_passwords, solve_math_model
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_math_model


def solve_max_coverage(k, passwords):
    """Goi giai phap bitmask exact."""
    return run_solver("math model", solve_math_model, k, passwords, "output_math_model")


def check_password(k, passwords=None):
    """Ham goi chung de giu cau truc dong nhat voi module khac."""
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
