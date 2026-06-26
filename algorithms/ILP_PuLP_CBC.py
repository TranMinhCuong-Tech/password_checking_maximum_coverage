try:
    from ..coverage_problem import run_solver, load_passwords, solve_ilp_pulp_cbc
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_ilp_pulp_cbc


def solve_max_coverage(k, passwords):
    # Solve the Maximum Coverage ILP with PuLP and CBC.
    return run_solver("ILP_PuLP_CBC", solve_ilp_pulp_cbc, k, passwords, "output_ILP_PuLP_CBC")


def check_password(k, passwords=None):
    # Ham goi chung de giu cau truc dong nhat voi module khac
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
