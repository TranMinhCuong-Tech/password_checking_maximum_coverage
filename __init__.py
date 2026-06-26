REAL_PASSWORD_FILE = "real_passwords.txt"
MUTATED_PASSWORD_FILE = "mutated_passwords.txt"
PASSWORD_FILES = (REAL_PASSWORD_FILE, MUTATED_PASSWORD_FILE)


def showBanner():
    banner = """
                ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
                ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
                ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
                ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
                ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
                ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                
                 ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗      
                ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝      
                ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗     
                ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║     
                ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝     
                 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                             
    """
    print(banner)

    description = """
    Universe:
        - real_passwords.txt: original password dataset
        - mutated_passwords.txt: transformed password dataset

    Goal:
        Select exactly k rules from rules.py so the covered passwords are maximized.
    """
    print(description)


def prompt_k():
    print("\n[+] Choose a fixed number of rules before selecting an algorithm.")
    while True:
        try:
            k_raw = input(f"[+] Enter number of rules k (1-{len(rules.RULES)}): ").strip().lower()
            if int(k_raw) == 0:
                return "exit"

            k = int(k_raw)
            if 1 <= k <= len(rules.RULES):
                return k
            print(f"[!] Please enter a number between 1 and {len(rules.RULES)}.")
        except ValueError:
            print("[!] Please enter a valid number.")


try:
    from . import pwd_checking
    from . import rules
except ImportError:
    import pwd_checking
    import rules


if __name__ == "__main__":
    showBanner()
    while True:
        rules.printRuleCatalog()
        selected_k = prompt_k()
        if selected_k == "exit":
            print("[*] Exiting...\n")
            break
        print(f"\n[+] Fixed number of selected rules: {selected_k}")
        print("[+] Now choose an algorithm to find the best coverage.")
        result = pwd_checking.runAlgorithms(selected_k, PASSWORD_FILES)
        if result == "exit":
            break
