from fileinput import filename
import os
import platform
from pynput import keyboard

"""
    Shell Simulator - should work on both windows and unix-like 
"""
VALID_COMMANDS = ["cd", "clr", "dir",
                  "environ", "echo", "help", "pause", "quit"]


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:                        # For unix-like
        os.system("clear")


def list_dir(directory: str):
    for item in os.listdir(directory):
        if not item.startswith("."):  # Hide dotfolders by default
            print(item)


def echo_text(text):
    print(" ".join(text[:]))    # Echo Text, multiple spaces reduced to 1


def on_press(key):
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))
        
    if key == keyboard.Key.enter:
        return False


def print_envs():
    for var, value in os.environ.items():
        print(f"{var}={value}")


def pause_shell():
    with keyboard.Listener(
                on_press=on_press, suppress=True) as listener:
        listener.join()

        
def parse_command(command: list[str]):

    if command[0] == "clr":
        clear_screen()
    if command[0] == "cd":
        if len(command) == 1:
            print(os.getcwd())
        elif len(command) > 2:
            print("This command can only accept 1 argument")
        else:
            os.chdir(command[1])

    if command[0] == "dir":
        if len(command) > 2:
            print("This command can only accept 1 argument")
        elif len(command) == 1:
            list_dir(".")
        else:
            list_dir(command[1])

    if command[0] == "environ":
        if len(command) > 1:
            print("This command can only accept 1 argument")
        else:
            print_envs()

    if command[0] == "echo":
        echo_text(command[1:])

    if command[0] == "pause":
        pause_shell()

    if command[0] == "quit":  # Quit Shell
        exit()


def run_cli():
    while True:
        print("PyShell>", end=' ')
        command = input().split()
        if command:
            if command[0] not in VALID_COMMANDS:  # First non-space element is command
                print("Command is not defined/invalid input")
            else:
                parse_command(command)


if __name__ == "__main__":
    run_cli()
