import argparse
import json
import os
import sys
import winreg
from pathlib import Path
from urllib.parse import unquote, urlparse

from stashapi.stashapp import StashInterface
from winregistry import open_key

__version__ = os.environ.get("STASH_FILE_PROTOCOL_VERSION", "0.0.0")
PROTOCOL_KEY = r"HKCU\\Software\\Classes\\stash-file"

def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Stash file protocol tools.")
    parser.add_argument(
        "--version",
        "-Version",
        action="version",
        version=f"stash_file_protocol {__version__}",
    )
    parser.add_argument(
        "--uri",
        "-Uri",
        dest="uri",
        help="Stash media URI (e.g. stash://scene/123) or URL.",
    )
    parser.add_argument(
        "--config",
        "-Config",
        nargs="?",
        const="__PRINT_CONFIG__",
        dest="config",
        help="Config path. When passed without a value, prints config path and contents.",
    )
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--install",
        "-Install",
        nargs="?",
        metavar="EXE",
        help="Install Windows registry protocol keys using the provided EXE path.",
    )
    action_group.add_argument(
        "--uninstall",
        "-Uninstall",
        action="store_true",
        help="Uninstall Windows registry protocol keys.",
    )

    args = parser.parse_args(argv)
    
    config_path = Path.cwd() / "config.json"
    if args.config and args.config != "__PRINT_CONFIG__":
        config_path = Path(args.config)
    
    if not config_path.exists():
        config_path.write_text('{"mappings": []}', encoding="utf-8")
    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
        
    if args.config == "__PRINT_CONFIG__":
        print(str(config_path))
        print(json.dumps(config, indent=2))
        return 0

    if args.install is not None:
        icon_value = f'"{args.install}",0'
        command_value = f'"{args.install}" -Uri "%1"'

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

    if args.uninstall:
        with open_key(
            r"HKCU\\Software\\Classes",
            sub_key_access=winreg.KEY_WRITE,
        ) as classes_key:
            print("Uninstalling stash-file protocol..")
            classes_key.delete_key("stash-file", recursive=True)
        return 0

    if not args.uri:
        parser.print_help()
        return 2

    raw_url = args.uri.strip().strip('"')

    parsed_url = urlparse(raw_url)
    media_type = parsed_url.netloc.lower()
    media_id = unquote(parsed_url.path.lstrip("/").split("/")[0])

    stash_url = os.environ["STASH_URL"]
    stash_parsed = urlparse(stash_url)

    connection = {
        "Scheme": stash_parsed.scheme,
        "Host": stash_parsed.hostname,
        "Port": stash_parsed.port,
        "ApiKey": os.environ["STASH_API_KEY"],
    }
    stash = StashInterface(connection)

    mappings = config["mappings"]
    mappings.sort(key=lambda item: len(item["orig"]), reverse=True)

    def collect_media_paths(media: dict, kind: str) -> list[str]:
        collected: list[str] = []
        seen: set[str] = set()

        def add_path(value: str | None) -> None:
            if isinstance(value, str) and value and value not in seen:
                collected.append(value)
                seen.add(value)

        if kind == "scene":
            for file_entry in media.get("files") or []:
                add_path(file_entry.get("path"))
            paths = media.get("paths") or {}
            for key in (
                "screenshot",
                "preview",
                "stream",
                "webp",
                "vtt",
                "sprite",
                "funscript",
                "interactive_heatmap",
                "caption",
            ):
                add_path(paths.get(key))
        elif kind == "image":
            for file_entry in media.get("visual_files") or []:
                add_path(file_entry.get("path"))
            for file_entry in media.get("files") or []:
                add_path(file_entry.get("path"))
            paths = media.get("paths") or {}
            for key in ("image", "preview", "thumbnail"):
                add_path(paths.get(key))

        return collected

    source_path = None
    candidate_paths: list[str] = []

    if media_type in ["scene", "scenes", "video", "videos"]:
        media = stash.find_scene(
            int(media_id),
            fragment=(
                "id files { path } "
                "paths { screenshot preview stream webp vtt sprite funscript "
                "interactive_heatmap caption }"
            ),
        )
        if media:
            candidate_paths = collect_media_paths(media, "scene")
    elif media_type in ["image", "images"]:
        media = stash.find_image(
            int(media_id),
            fragment="id files { path } visual_files { path } paths { thumbnail preview image }",
        )
        if media:
            candidate_paths = collect_media_paths(media, "image")

    for candidate in candidate_paths:
        mapped = candidate
        for mapping in mappings:
            if mapped.startswith(mapping["orig"]):
                mapped = mapped.replace(mapping["orig"], mapping["local"], 1)
                break
        if mapped != candidate:
            source_path = mapped
            break
        if source_path is None:
            source_path = mapped

    print(source_path)
    return 0
