import sys
from typing import Dict


def query_yes_no(question: str, default: str = "no") -> bool:
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is one of "yes" or "no".
    """
    valid: Dict[str, bool] = {"yes": True, "y": True, "ye": True,
                              "no": False, "n": False}
    if default is None:
        prompt: str = " [y/n] "
    elif default == "yes":
        prompt: str = " [Y/n] "
    elif default == "no":
        prompt: str = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
