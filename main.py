from james_logic import command_fun, get_help, secure_main, command_list, boot_logo, load
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

command_menu = WordCompleter(command_list)


def main():
    load()
    boot_logo()
    while True:
        command = prompt('Bond says type a command or type help/? for help: ', completer=command_menu).lower()
        if not command:
            print(get_help())
        else:
            command_fun(
                command)


if __name__ == "__main__":
    secure_main(main)
