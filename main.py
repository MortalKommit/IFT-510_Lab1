from asyncore import write
import os
import platform
import traceback
from pynput import keyboard

"""
    Shell Simulator - should work on both windows and unix-like
"""
VALID_COMMANDS = ["cd", "clr", "dir",
                  "environ", "echo", "help", "pause", "quit"]

HELP_TEXT = """
PyShell, version 1.0
These shell commands are defined internally, type help to see this list

cd <directory>              change the current directory to <directory> if it exists
clr                         clear the screen
dir <directory              list the contents of <directory>, including hidden files
environ                     list all environment variables
echo <comment>              display <comment> on a new line
help                        help text
pause                       pause operation of the shell
quit                        quit the shell
Optional arguments          command [> | >> filename] - executes command and redirects output
                            either truncating (>) or appending (>>) to [filename]
"""


def clear_screen(write_to_file=(False, None, 'w')):
    try:
        if write_to_file[0]:  # If > or >> appears
            with open(write_to_file[1], write_to_file[2]) as f:
                pass  # Creates an empty file
        if platform.system() == "Windows":
            os.system("cls")
        else:                        # For unix-like
            os.system("clear")
    except Exception:
        print("Error:", traceback.format_exc())


def list_dir(directory: str, write_to_file=(False, None, 'w')):
    try:
        if write_to_file[0]:
            with open(write_to_file[1], write_to_file[2]) as f:
                for item in os.listdir(directory):
                    if not item.startswith("."):  # Hide dotfolders by default
                        print(item, file=f)
        else:
            for item in os.listdir(directory):
                if not item.startswith("."):  # Hide dotfolders by default
                    print(item)
    except:
        print("Error: ", traceback.format_exc())


def echo_text(text, write_to_file=(False, None, 'w')):
    try:
        if write_to_file[0]:
            with open(write_to_file[1], write_to_file[2]) as f:
                # Echo Text, multiple spaces reduced to 1
                print(" ".join(text[:]), file=f)
        else:
            print(" ".join(text[:]))
    except Exception:
        print("Error:", traceback.format_exc())


def on_press(key):
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

    if key == keyboard.Key.enter:
        return False


def print_envs(write_to_file=(False, None, "w")):
    try:
        if write_to_file[0]:
            with open(write_to_file[1]) as f:
                for var, value in os.environ.items():
                    print(f"{var}={value}", file=f)
        else:
            for var, value in os.environ.items():
                print(f"{var}={value}")

    except Exception:
        print("Error: ", traceback.format_exc())


def change_dir(directory: str, write_to_file=(False, None, "w")):
    try:
        if write_to_file[0]:  # Write to file flag check
            with open(write_to_file[1], write_to_file[2]) as f:
                if directory == ".":
                    print(os.getcwd(), file=f)
                else:
                    os.chdir(directory)
                    os.environ['pwd'] = directory
        else:
            if directory == ".":
                print(os.getcwd())
            else:
                os.chdir(directory)
                os.environ['pwd'] = directory
    except KeyError:
        print("Error: Can't set pwd environment variable value")
    except OSError:
        print("Error: No such file or directory")
    except Exception:
        print("Error:", traceback.format_exc())


def pause_shell(write_to_file=(False, None, "w")):

    if write_to_file[0]:
        with open(write_to_file[1], write_to_file[2]) as f:
            print("Press Enter to continue...:", file=f)
    else:
        print("Press Enter to continue...:")
    with keyboard.Listener(
            on_press=on_press, suppress=True) as listener:
        listener.join()


def display_help(write_to_file=(False, None, 'w')):
    try:
        if write_to_file[0]:
            with open(write_to_file[1], write_to_file[2]) as f:
                print(HELP_TEXT, file=f)
        else:
            print(HELP_TEXT)
    except Exception:
        print("Error: ", traceback.format_exc())


def parse_command(command: list[str]):
    # 3-tuple of (flag, file_name, file_mode)
    write_to_file = (False, None, "w")
    directory = "."  # Default cd, dir as current directory
    text = ""
    # Redirect operator checking, better and more correctly done with regex which handles
    # multiple redirect files and redirect operators but this works for simple cases
    try:
        if len(command) >= 2:
            # cd and dir specific, which take directory parameter
            if command[0] == "cd" or command[0] == "dir":
                if len(command) == 2 or len(command) > 3:
                    directory = command[1]
    
                if command[1] == ">":
                    write_to_file = (True, command[2], "w")
                elif command[1] == ">>":
                    write_to_file = (True, command[2], "a")

                if len(command) > 3:
                    if command[2] == ">":
                        write_to_file = (True, command[3], "w")
                    elif command[2] == ">>":
                        write_to_file = (True, command[3], "a")
            # echo specific which can take n string arguments
            elif command[0] == "echo":
                try:
                    if ">" in command[1:]:
                        redir_position = command.index(">")
                        text = command[1:redir_position]
                        write_to_file = (
                            True, command[redir_position + 1], "w")
                    elif ">>" in command[1:]:
                        redir_position = command.index(">>")
                        text = command[1:redir_position]
                        write_to_file = (
                            True, command[redir_position + 1], "a")

                except IndexError:  # Not necessary but a safeguard
                    pass
            else:
                if command[1] == ">":
                    write_to_file = (True, command[2], "w")
                elif command[1] == ">>":
                    write_to_file = (True, command[2], "a")

        if command[0] == "clr":
            clear_screen(write_to_file=write_to_file)

        if command[0] == "cd":
            change_dir(directory, write_to_file=write_to_file)

        if command[0] == "dir":
            list_dir(directory, write_to_file=write_to_file)

        if command[0] == "environ":
            print_envs(write_to_file=write_to_file)

        if command[0] == "echo":
            echo_text(text, write_to_file=write_to_file)

        if command[0] == "pause":
            pause_shell(write_to_file=write_to_file)

        if command[0] == "quit":  # Quit Shell
            if write_to_file[0]:
                with open(write_to_file[1], write_to_file[2]):
                    pass  # Does not write anything to file
            exit()

        if command[0] == "help":
            display_help(write_to_file=write_to_file)

    except IndexError:
        print("Error: Invalid number of arguments")
        print(traceback.format_exc())
    except Exception:
        print("Error: Syntax error unexpected tokens")
        print(traceback.format_exc())


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
