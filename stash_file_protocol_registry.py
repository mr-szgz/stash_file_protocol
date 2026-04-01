import argparse
import winreg

from winregistry import open_key

PROTOCOL_KEY = r"HKCU\\Software\\Classes\\stash-file"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install or uninstall stash-file URL protocol registry keys.",
    )
    parser.add_argument(
        "action",
        choices=["install", "uninstall"],
        nargs="?",
        default="install",
        help="Action to perform (default: install)",
    )
    parser.add_argument(
        "--exe",
        "-Exe",
        default=r"S:\Spaces\Stash\Apps\stash_file_protocol\dist\stash-file-protocol.exe",
        help="Path to stash-file-protocol.exe",
    )
    args = parser.parse_args()

    if args.action == "install":
        icon_value = f'"{args.exe}",0'
        command_value = f'"{args.exe}" "%1"'

        with open_key(
            PROTOCOL_KEY,
            sub_key_ensure=True,
            sub_key_access=winreg.KEY_WRITE,
        ) as key:
            key.set_value("", winreg.REG_SZ, "URL:Stash File Protocol")
            key.set_value("URL Protocol", winreg.REG_SZ, "")

        with open_key(
            PROTOCOL_KEY + r"\\DefaultIcon",
            sub_key_ensure=True,
            sub_key_access=winreg.KEY_WRITE,
        ) as key:
            key.set_value("", winreg.REG_SZ, icon_value)

        with open_key(
            PROTOCOL_KEY + r"\\shell",
            sub_key_ensure=True,
            sub_key_access=winreg.KEY_WRITE,
        ) as key:
            key.set_value("", winreg.REG_SZ, "open")

        with open_key(
            PROTOCOL_KEY + r"\\shell\\open\\command",
            sub_key_ensure=True,
            sub_key_access=winreg.KEY_WRITE,
        ) as key:
            key.set_value("", winreg.REG_SZ, command_value)

        print("Installed stash-file protocol registry keys.")
        print(f"Command: {command_value}")
        return 0

    with open_key(
        r"HKCU\\Software\\Classes",
        sub_key_access=winreg.KEY_WRITE,
    ) as classes_key:
        print(f"Uninstalling stash-file protocol..")
        classes_key.delete_key("stash-file", recursive=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
