#!/usr/bin/env python3

import mutagen
from typing import List, Tuple
from pathlib import Path
import argparse
from sys import exit


def approval():
    answers = ["yes", "no"]
    ans = ""
    while ans.lower() not in answers:
        ans = input("> Your Choice [y/n]: ").strip().lower()
        if ans == "y":
            ans = "yes"
        elif ans == "n":
            ans = "no"
    return ans


def run(target: str, tags: List[Tuple[str, str]], auto_confirm: bool):
    path = Path(target)
    if path.is_dir():
        print("[*] Iterating over:", str(target))
        for child in path.iterdir():
            if not auto_confirm and child.is_dir():
                print(
                    "[?] You are targeting a nested directory. Are you sure you want to iterate over it?"
                )
                ans = approval()
                if ans == "no":
                    print(
                        "[*] Very well, modify your target to point somewhere else. Adios for now."
                    )
                    exit(1)
            run(str(child), tags, auto_confirm)
        return 0
    elif not path.is_file():
        print(
            "[!] Target path is neither a directory or file. Please make sure it exists: "
            + target
        )
        exit(1)
    print("[*] Current target: " + str(path))
    if len(tags) == 0:
        print(
            "[!] No tags to assign to target. I'm just going to take a nap. Let me know when you have tags"
        )
        exit(1)
    muter = None
    try:
        muter = mutagen.File(str(path))
    except Exception as e:
        print(
            "[!] Error getting mutagen file for target. Hopefull it's your fault and not mine"
        )
        print("[!] Error Type: " + str(type(e)))
        print("[!] Error: ")
        print(e)
        exit(1)
    if not muter:
        print("[!] Unable to get mutagen file for target. It may not be supported.")
        exit(1)
    for tag in tags:
        if len(tag) != 2:
            print("[!] Tag is not a tuple. Don't know how we got here.")
            print("[!] Tags: " + str(tags))
            print("[!] Tag: " + str(tag))
            exit(1)
        print("[*] Setting tag '" + str(tag[0]) + "' with value '" + str(tag[1]) + "'")
        muter[tag[0]] = tag[1]
    if not auto_confirm:
        print("[?] Do you want to commit to saving?")
        ans = approval()
        if ans == "no":
            print("[*] Very well. Not saving for now. See you later alligator.")
            exit(0)
    print("[*] Saving...")
    muter.save()
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Tag files or directories")
    p.add_argument(
        "-t",
        "--tag",
        action="append",
        nargs=2,
        help="Tag key/value to add (repeatable)",
        required=True,
    )
    p.add_argument("-c", "--confirm", action="store_true", help="auto confirm")
    p.add_argument("target", help="Individual file or directory to tag")
    args = p.parse_args()
    tags = args.tag
    if not tags:
        tags = []
    confirm = bool(args.confirm)
    exit(run(args.target, tags, confirm))
