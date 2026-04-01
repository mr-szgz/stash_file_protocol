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

# supported generated asset kinds we support and corresponding folder name for its asset in generated path
STASH_GENERATED_FOLDERS = [
    ("vtts", "vtt"),
    ("sprites", "vtt"),
    ("screenshots", "screenshots"),
    ("previews", "screenshots")
]

def get_config_path() -> Path:
    return Path.home() / ".stash_file_protocol" / "config.json"

def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        response = input("config doesn't exist do you want to create? [y/N]: ").strip().lower()
        if response != "y":
            raise RuntimeError("config not created")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(
                {
                    "stash_url": "http://localhost:9999",
                    "stash_api_key": "",
                    "generated_path": "",
                    "mappings": [],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

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
        "--info",
        "-Info",
        dest="info",
        help="Stash media URI (e.g. stash://scene/123) or URL for JSON info.",
    )
    parser.add_argument(
        "--add",
        "-Add",
        dest="add",
        metavar="MAPPING",
        help="Add mapping in form orig:local.",
    )
    parser.add_argument(
        "--remove",
        "-Remove",
        dest="remove",
        metavar="MAPPING",
        help="Remove mapping in form orig:local.",
    )
    parser.add_argument(
        "--list",
        "-List",
        action="store_true",
        dest="list_mappings",
        help="List mappings.",
    )
    parser.add_argument(
        "--set-url",
        "-SetUrl",
        dest="set_url",
        metavar="URL",
        help="Set stash url in config.",
    )
    parser.add_argument(
        "--set-api-key",
        "-SetApiKey",
        dest="set_api_key",
        metavar="API_KEY",
        help="Set stash api key in config.",
    )
    parser.add_argument(
        "--set-generated",
        "-SetGenerated",
        dest="set_generated",
        metavar="PATH",
        help="Set generated files path in config.",
    )
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--install",
        "-Install",
        nargs="?",
        const="__AUTO__",
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
    
    config_path = get_config_path()
    try:
        config = load_config(config_path)
    except RuntimeError:
        return 1

    if args.set_url:
        config["stash_url"] = args.set_url
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"Set URL {args.set_url}")
        return 0
    if args.set_api_key:
        config["stash_api_key"] = args.set_api_key
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print("Set API key")
        return 0
    if args.set_generated:
        config["generated_path"] = args.set_generated
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"Set generated path {args.set_generated}")
        return 0

    if args.add or args.remove or args.list_mappings:
        mappings = config.get("mappings", [])
        if args.add or args.remove:
            raw_mapping = args.add or args.remove
            if ":" not in raw_mapping:
                print("Invalid mapping format. Use orig:local.")
                return 2
            orig, local = raw_mapping.split(":", 1)
            mapping = {"orig": orig, "local": local}
            if args.add:
                if mapping not in mappings:
                    mappings.append(mapping)
                    print(f"Added mapping {orig}:{local}")
                else:
                    print(f"Mapping exists {orig}:{local}")
            else:
                if mapping in mappings:
                    mappings = [item for item in mappings if item != mapping]
                    print(f"Removed mapping {orig}:{local}")
                else:
                    print(f"Mapping not found {orig}:{local}")
            config["mappings"] = mappings
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            return 0

        for mapping in mappings:
            print(f'{mapping["orig"]}:{mapping["local"]}')
        return 0

    if args.install is not None:
        install_path = args.install
        if install_path == "__AUTO__":
            candidate_paths = []
            if sys.executable.lower().endswith(".exe"):
                candidate_paths.append(Path(sys.executable))
            candidate_paths.append(Path(sys.argv[0]))
            repo_root = Path(__file__).resolve().parents[1]
            candidate_paths.append(repo_root / "dist" / "stash-file-protocol.exe")
            for candidate in candidate_paths:
                if candidate and Path(candidate).exists():
                    install_path = str(Path(candidate).resolve())
                    break
        if not install_path or install_path == "__AUTO__":
            print("Install failed: exe path not provided and auto-detect failed.")
            return 1
        icon_value = f'"{install_path}",0'
        command_value = f'"{install_path}" -Uri "%1"'

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

    if not args.uri and not args.info:
        parser.print_help()
        return 2

    raw_url = (args.info or args.uri).strip().strip('"')

    parsed_url = urlparse(raw_url)
    media_type = parsed_url.netloc.lower()
    path_parts = [part for part in parsed_url.path.lstrip("/").split("/") if part]
    media_id = unquote(path_parts[0]) if path_parts else ""
    media_index = None
    if len(path_parts) > 1 and path_parts[1].isdigit():
        media_index = int(path_parts[1])

    stash_url = config.get("stash_url") or os.environ["STASH_URL"]
    stash_parsed = urlparse(stash_url)

    connection = {
        "Scheme": stash_parsed.scheme,
        "Host": stash_parsed.hostname,
        "ApiKey": config.get("stash_api_key") or os.environ.get("STASH_API_KEY", ""),
    }
    if stash_parsed.port is not None:
        connection["Port"] = stash_parsed.port
    elif stash_parsed.scheme == "https":
        connection["Port"] = 443
    elif stash_parsed.scheme == "http":
        connection["Port"] = 80
    stash = StashInterface(connection)

    mappings = config.get("mappings", [])
    mappings.sort(key=lambda item: len(item["orig"]), reverse=True)

    def collect_media_paths(media: dict, kind: str) -> dict[str, list[str]]:
        files: list[str] = []
        extras: list[str] = []
        seen: set[str] = set()

        def add_path(value: str | None) -> None:
            if isinstance(value, str) and value and value not in seen:
                extras.append(value)
                seen.add(value)

        if kind == "scene":
            for file_entry in media.get("files") or []:
                path_value = file_entry.get("path")
                if isinstance(path_value, str) and path_value and path_value not in seen:
                    files.append(path_value)
                    seen.add(path_value)
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

        return {"files": files, "extras": extras}

    source_path = None
    candidate_paths: list[str] = []

    if args.info:
        if media_type in ["scene", "scenes", "video", "videos"]:
            media = stash.find_scene(
                int(media_id),
                fragment=(
                    "id title code details director urls url rating100 organized "
                    "tags { id name } studio { id name } "
                    "files { path size width height duration format video_codec audio_codec "
                    "frame_rate bit_rate } "
                    "sceneStreams { url mime_type label } "
                    "paths { screenshot preview stream webp vtt sprite funscript "
                    "interactive_heatmap caption }"
                ),
            )
            if not media:
                print("null")
                return 0

            if media_index is not None:
                files = media.get("files") or []
                if media_index < 0 or media_index >= len(files):
                    print("null")
                    return 0
                file_info = dict(files[media_index])
                mapped_path = file_info.get("path")
                for mapping in mappings:
                    if mapped_path and mapped_path.startswith(mapping["orig"]):
                        mapped_path = mapped_path.replace(mapping["orig"], mapping["local"], 1)
                        break
                if mapped_path and mapped_path != file_info.get("path"):
                    file_info["mapped_path"] = mapped_path
                print(json.dumps(file_info, indent=2))
                return 0

            output = {
                "id": media.get("id"),
                "title": media.get("title"),
                "code": media.get("code"),
                "details": media.get("details"),
                "director": media.get("director"),
                "urls": media.get("urls") or ([media["url"]] if media.get("url") else []),
                "rating100": media.get("rating100"),
                "organized": media.get("organized"),
                "studio": media.get("studio"),
                "streams": None,
                "files": [],
                "assets": {},
                "file_path": None,
                "file_mapped_path": None,
                "file_url": None,
                "tags": media.get("tags") or [],
            }
            for file_entry in media.get("files") or []:
                file_info = dict(file_entry)
                mapped_path = file_info.get("path")
                for mapping in mappings:
                    if mapped_path and mapped_path.startswith(mapping["orig"]):
                        mapped_path = mapped_path.replace(mapping["orig"], mapping["local"], 1)
                        break
                if mapped_path and mapped_path != file_info.get("path"):
                    file_info["mapped_path"] = mapped_path
                output["files"].append(file_info)
            if output["files"]:
                first_file = output["files"][0]
                output["file_path"] = first_file.get("path")
                output["file_mapped_path"] = first_file.get("mapped_path", first_file.get("path"))
                output["file_url"] = (
                    f'{stash_url.rstrip("/")}/scene/{media.get("id")}/file'
                    if media.get("id")
                    else None
                )
            streams = media.get("sceneStreams") or []
            if streams:
                direct_stream = next(
                    (item for item in streams if (item.get("label") or "").lower() == "direct stream"),
                    None,
                )
                mp4_720 = next(
                    (
                        item
                        for item in streams
                        if item.get("mime_type") == "video/mp4"
                        and "720" in (item.get("label") or "")
                    ),
                    None,
                )
                mp4_480 = next(
                    (
                        item
                        for item in streams
                        if item.get("mime_type") == "video/mp4"
                        and "480" in (item.get("label") or "")
                    ),
                    None,
                )
                def normalize_stream_url(value: str | None) -> str | None:
                    if not value:
                        return None
                    return value.replace("/stream.mp4", "/stream")

                output["streams"] = {
                    "direct": normalize_stream_url(direct_stream.get("url") if direct_stream else None),
                    "720p": normalize_stream_url(mp4_720.get("url") if mp4_720 else None),
                    "480p": normalize_stream_url(mp4_480.get("url") if mp4_480 else None),
                }
            paths = media.get("paths") or {}
            if paths:
                for group_name, folder_name in STASH_GENERATED_FOLDERS:
                    singular = group_name.rstrip("s")
                    value = paths.get(singular)
                    if value:
                        parsed_asset = urlparse(value)
                        file_name = os.path.basename(parsed_asset.path)
                        generated_path = config.get("generated_path") or ""
                        local_path = (
                            os.path.join(generated_path, folder_name, file_name)
                            if generated_path and file_name
                            else ""
                        )
                        output["assets"][group_name] = {
                            "url": value,
                            "mapped_path": local_path,
                        }
            print(json.dumps(output, indent=2))
            return 0
        elif media_type in ["image", "images"]:
            media = stash.find_image(
                int(media_id),
                fragment=(
                    "id title code details photographer urls url rating100 organized "
                    "tags { id name } studio { id name } "
                    "files { path size width height format } "
                    "visual_files { "
                    "... on ImageFile { path size width height format } "
                    "... on VideoFile { path size width height duration format video_codec "
                    "audio_codec frame_rate bit_rate } "
                    "} paths { thumbnail preview image }"
                ),
            )
            if not media:
                print("null")
                return 0

            files_list = media.get("visual_files") or media.get("files") or []
            if media_index is not None:
                if media_index < 0 or media_index >= len(files_list):
                    print("null")
                    return 0
                file_info = dict(files_list[media_index])
                mapped_path = file_info.get("path")
                for mapping in mappings:
                    if mapped_path and mapped_path.startswith(mapping["orig"]):
                        mapped_path = mapped_path.replace(mapping["orig"], mapping["local"], 1)
                        break
                if mapped_path and mapped_path != file_info.get("path"):
                    file_info["mapped_path"] = mapped_path
                print(json.dumps(file_info, indent=2))
                return 0

            output = {
                "id": media.get("id"),
                "title": media.get("title"),
                "code": media.get("code"),
                "details": media.get("details"),
                "photographer": media.get("photographer"),
                "urls": media.get("urls") or ([media["url"]] if media.get("url") else []),
                "rating100": media.get("rating100"),
                "organized": media.get("organized"),
                "studio": media.get("studio"),
                "files": [],
                "assets": {},
                "file_path": None,
                "file_mapped_path": None,
                "file_url": None,
                "tags": media.get("tags") or [],
            }
            for file_entry in files_list:
                file_info = dict(file_entry)
                mapped_path = file_info.get("path")
                for mapping in mappings:
                    if mapped_path and mapped_path.startswith(mapping["orig"]):
                        mapped_path = mapped_path.replace(mapping["orig"], mapping["local"], 1)
                        break
                if mapped_path and mapped_path != file_info.get("path"):
                    file_info["mapped_path"] = mapped_path
                output["files"].append(file_info)
            if output["files"]:
                first_file = output["files"][0]
                output["file_path"] = first_file.get("path")
                output["file_mapped_path"] = first_file.get("mapped_path", first_file.get("path"))
                output["file_url"] = (
                    f'{stash_url.rstrip("/")}/image/{media.get("id")}/file'
                    if media.get("id")
                    else None
                )

            paths = media.get("paths") or {}
            if paths:
                for group_name, folder_name in STASH_GENERATED_FOLDERS:
                    singular = group_name.rstrip("s")
                    value = paths.get(singular)
                    if value:
                        parsed_asset = urlparse(value)
                        file_name = os.path.basename(parsed_asset.path)
                        generated_path = config.get("generated_path") or ""
                        local_path = (
                            os.path.join(generated_path, folder_name, file_name)
                            if generated_path and file_name
                            else ""
                        )
                        output["assets"][group_name] = {
                            "url": value,
                            "mapped_path": local_path,
                        }
            print(json.dumps(output, indent=2))
            return 0
        else:
            print("null")
            return 0

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
            collected = collect_media_paths(media, "scene")
            files = collected["files"]
            extras = collected["extras"]
            if media_index is not None and 0 <= media_index < len(files):
                candidate_paths = [files[media_index]]
            else:
                candidate_paths = files + extras
    elif media_type in ["image", "images"]:
        media = stash.find_image(
            int(media_id),
            fragment=(
                "id files { path } visual_files { "
                "... on ImageFile { path } "
                "... on VideoFile { path } "
                "} paths { thumbnail preview image }"
            ),
        )
        if media:
            collected = collect_media_paths(media, "image")
            candidate_paths = collected["files"] + collected["extras"]

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
