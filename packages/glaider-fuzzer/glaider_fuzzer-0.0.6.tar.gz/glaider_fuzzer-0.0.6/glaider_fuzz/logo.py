import colorama

RESET = colorama.Style.RESET_ALL
DIM_WHITE = colorama.Style.DIM + colorama.Fore.WHITE
LIGHT_MAGENTA = colorama.Fore.LIGHTMAGENTA_EX
MAGENTA = colorama.Fore.CYAN


def print_logo():
    logo = """

      ██████╗ ██╗      █████╗ ██╗██████╗ ███████╗██████╗ 
     ██╔════╝ ██║     ██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
     ██║  ███╗██║     ███████║██║██║  ██║█████╗  ██████╔╝
     ██║   ██║██║     ██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
     ╚██████╔╝███████╗██║  ██║██║██████╔╝███████╗██║  ██║
      ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝


""".replace('█', f"{DIM_WHITE}█{RESET}").replace(' ', f"{LIGHT_MAGENTA} {RESET}").replace('█',
                                                                                          f"{MAGENTA}▓{RESET}").replace(
        '▒', f"{MAGENTA}▒{RESET}").replace('Z', f"{MAGENTA}▒▒▒▒▒▒{RESET}")
    print(logo)
