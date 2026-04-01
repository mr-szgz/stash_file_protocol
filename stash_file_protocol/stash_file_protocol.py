import argparse
import json
import os
import sys
import re
import shutil
import traceback
import urllib.request
import winreg
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlparse, urlunparse

from stashapi.stashapp import StashInterface
from tqdm import tqdm
from winregistry import open_key

__version__ = os.environ.get("STASH_FILE_PROTOCOL_VERSION", "0.0.0")
PROTOCOL_KEY = r"HKCU\\Software\\Classes\\stash"

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
                    "user_downloads": "",
                    "browser": "",
                    "browser_prefs": "",
                    "mappings": [],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_vivaldi_prefs_path() -> Path | None:
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        return None
    prefs_path = Path(local_appdata) / "Vivaldi" / "User Data" / "Default" / "Preferences"
    if not prefs_path.exists():
        return None
    return prefs_path

def get_vivaldi_downloads_dir(prefs_path: Path) -> str:
    try:
        with prefs_path.open("r", encoding="utf-8") as f:
            prefs = json.load(f)
    except (OSError, json.JSONDecodeError):
        return ""
    return str(prefs.get("download", {}).get("default_directory", "") or "")

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
        "positional_uri",
        nargs="?",
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
    parser.add_argument(
        "--set-downloads",
        "-SetDownloads",
        dest="set_downloads",
        metavar="PATH",
        help="Set downloads path in config.",
    )
    parser.add_argument(
        "--set-vivaldi-downloads",
        "-SetVivaldiDownloads",
        action="store_true",
        dest="set_vivaldi_downloads",
        help="Set downloads path from Vivaldi Preferences.",
    )
    parser.add_argument(
        "--sync-browser",
        "-SyncBrowser",
        action="store_true",
        dest="sync_browser",
        help="Sync downloads path from configured browser Preferences.",
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
    if args.set_downloads:
        downloads_path = str(Path(args.set_downloads).expanduser().resolve())
        config["user_downloads"] = downloads_path
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"Set downloads path {downloads_path}")
        return 0
    if args.set_vivaldi_downloads:
        prefs_path = get_vivaldi_prefs_path()
        if not prefs_path:
            print("Vivaldi Preferences not found.")
            return 1
        downloads_dir_raw = get_vivaldi_downloads_dir(prefs_path)
        if not downloads_dir_raw:
            print("Vivaldi downloads path not found in Preferences.")
            return 1
        downloads_path = str(Path(downloads_dir_raw).expanduser().resolve())
        config["user_downloads"] = downloads_path
        config["browser"] = "vivaldi"
        config["browser_prefs"] = str(prefs_path)
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"Set downloads path {downloads_path}")
        print("Set browser vivaldi")
        print(f"Set browser prefs {prefs_path}")
        return 0
    if args.sync_browser:
        if (config.get("browser") or "").lower() != "vivaldi":
            print("Sync skipped: browser is not set to vivaldi.")
            return 1
        prefs_path_raw = config.get("browser_prefs") or ""
        prefs_path = Path(prefs_path_raw) if prefs_path_raw else get_vivaldi_prefs_path()
        if not prefs_path or not prefs_path.exists():
            print("Vivaldi Preferences not found.")
            return 1
        downloads_dir_raw = get_vivaldi_downloads_dir(prefs_path)
        if not downloads_dir_raw:
            print("Vivaldi downloads path not found in Preferences.")
            return 1
        downloads_path = str(Path(downloads_dir_raw).expanduser().resolve())
        config["user_downloads"] = downloads_path
        config["browser_prefs"] = str(prefs_path)
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"Set downloads path {downloads_path}")
        print("Synced browser vivaldi")
        print(f"Set browser prefs {prefs_path}")
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
        else:
            install_path = str(Path(install_path).expanduser().resolve())
        if not install_path or install_path == "__AUTO__":
            print("Install failed: exe path not provided and auto-detect failed.")
            return 1
        if not Path(install_path).exists():
            print(f"Install failed: exe path not found: {install_path}")
            return 1
        icon_value = f'"{install_path}",0'
        command_value = f'"{install_path}" "%1"'

        with open_key(
            PROTOCOL_KEY,
            sub_key_ensure=True,
            sub_key_access=winreg.KEY_WRITE,
        ) as key:
            key.set_value("", winreg.REG_SZ, "URL:Stash Protocol")
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
        print(f"Path: {install_path}")
        print(f"Root key: {PROTOCOL_KEY}")
        print(f"Command saved: {command_value}")
        print("Example: stash://scene/221714")
        return 0

    if args.uninstall:
        with open_key(
            r"HKCU\\Software\\Classes",
            sub_key_access=winreg.KEY_WRITE,
        ) as classes_key:
            print("Uninstalling stash protocol registry key: HKCU\\Software\\Classes\\stash")
            classes_key.delete_key("stash", recursive=True)
        return 0

    if not args.uri and not args.info and not args.positional_uri:
        parser.print_help()
        return 2

    raw_url = (args.info or args.uri or args.positional_uri).strip().strip('"')

    parsed_url = urlparse(raw_url)
    media_type = parsed_url.netloc.lower()
    raw_query_options = parse_qs(parsed_url.query, keep_blank_values=True)
    query_options = {key.lower(): value for key, value in raw_query_options.items()}
    play_values = query_options.get("play", [])
    play_value = play_values[-1] if play_values else None
    play_requested = (play_value or "").strip().lower() in ("1", "true", "yes", "y", "on")
    download_values = query_options.get("download", [])
    download_value = download_values[-1] if download_values else None
    download_requested = (download_value or "").strip().lower() in ("1", "true", "yes", "y", "on")
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

    def append_query_param(url: str, key: str, value: str) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query, keep_blank_values=True)
        query[key] = [value]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    def build_file_url(
        media_kind: str,
        media: dict | None,
        file_index: int | None,
        base_url: str,
    ) -> str | None:
        if not media or not media.get("id"):
            return None
        media_id_value = media.get("id")
        base = base_url.rstrip("/")
        if media_kind in ["scene", "scenes", "video", "videos"]:
            files = media.get("files") or []
            file_entry = None
            if file_index is not None and 0 <= file_index < len(files):
                file_entry = files[file_index]
            elif files:
                file_entry = files[0]
            file_id_value = file_entry.get("id") if isinstance(file_entry, dict) else None
            if file_id_value:
                return f"{base}/scene/{media_id_value}/stream?file_id={file_id_value}"
            return f"{base}/scene/{media_id_value}/file"
        if media_kind in ["image", "images"]:
            return f"{base}/image/{media_id_value}/file"
        return None

    def build_download_url(file_url: str | None) -> str | None:
        if not file_url:
            return None
        return append_query_param(file_url, "download", "1")

    def _pick_filename_from_headers(headers: dict, fallback: str) -> str:
        disposition = headers.get("Content-Disposition") or headers.get("content-disposition") or ""
        if disposition:
            match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^\";]+)"?', disposition)
            if match:
                return os.path.basename(match.group(1))
        return fallback

    def _unique_path(folder: Path, filename: str) -> Path:
        candidate = folder / filename
        if not candidate.exists():
            return candidate
        stem = candidate.stem
        suffix = candidate.suffix
        counter = 1
        while True:
            candidate = folder / f"{stem} ({counter}){suffix}"
            if not candidate.exists():
                return candidate
            counter += 1

    def download_to_file(
        url: str,
        api_key: str,
        fallback_name: str,
        download_dir: Path,
    ) -> Path | None:
        download_dir.mkdir(parents=True, exist_ok=True)
        headers = {}
        if api_key:
            headers["ApiKey"] = api_key
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            filename = _pick_filename_from_headers(response.headers, fallback_name)
            target_path = _unique_path(download_dir, filename)
            total_bytes = response.headers.get("Content-Length")
            total = int(total_bytes) if total_bytes and total_bytes.isdigit() else None
            with open(target_path, "wb") as target:
                with tqdm(
                    total=total,
                    desc=f"Downloading {filename} -> {download_dir}",
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    mininterval=0.1,
                ) as progress:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        target.write(chunk)
                        progress.update(len(chunk))
            return target_path

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
                    "files { id path size width height duration format video_codec audio_codec "
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
                file_url = build_file_url(media_type, media, media_index, stash_url)
                file_info["file_url"] = file_url
                file_info["download_url"] = build_download_url(file_url)
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
                "download_url": None,
                "download_url": None,
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
                output["file_url"] = build_file_url(media_type, media, None, stash_url)
                output["download_url"] = build_download_url(output["file_url"])
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
                    "files { id path size width height format } "
                    "visual_files { "
                    "... on ImageFile { id path size width height format } "
                    "... on VideoFile { id path size width height duration format video_codec "
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
                file_url = build_file_url(media_type, media, media_index, stash_url)
                file_info["file_url"] = file_url
                file_info["download_url"] = build_download_url(file_url)
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
                output["file_url"] = build_file_url(media_type, media, None, stash_url)
                output["download_url"] = build_download_url(output["file_url"])

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
                    "id files { id path } "
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
                "id files { id path } visual_files { "
                "... on ImageFile { id path } "
                "... on VideoFile { id path } "
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

    file_url = build_file_url(media_type, media, media_index, stash_url) if "media" in locals() else None
    download_url = build_download_url(file_url)

    if download_requested:
        if download_url:
            fallback_name = f"{media_type}-{media_id}"
            if isinstance(media_index, int):
                fallback_name = f"{fallback_name}-{media_index}"
            fallback_name = f"{fallback_name}.bin"
            api_key = connection.get("ApiKey", "")
            downloads_dir_raw = config.get("user_downloads") or ""
            download_dir = (
                Path(downloads_dir_raw).expanduser().resolve()
                if downloads_dir_raw
                else Path.home() / "Downloads"
            )
            try:
                target = download_to_file(download_url, api_key, fallback_name, download_dir)
            except Exception:
                target = None
            if target:
                os.startfile(target.parent)
                print(str(target))
                return 0
        print("null")
        return 0

    if play_requested:
        if source_path and os.path.exists(source_path):
            os.startfile(source_path)
            return 0
        print("null")
        return 0

    print(source_path)
    return 0


def _wait_for_keypress() -> None:
    try:
        import msvcrt

        print("Press any key to close...", flush=True)
        msvcrt.getch()
    except Exception:
        try:
            input("Press Enter to close...")
        except Exception:
            pass


if __name__ == "__main__":
    exit_code = 0
    try:
        exit_code = main()
    except SystemExit as exc:
        exit_code = exc.code if exc.code is not None else 0
        if not isinstance(exit_code, int):
            print(exit_code)
            exit_code = 1
    except Exception:
        traceback.print_exc()
        exit_code = 1

    if exit_code:
        _wait_for_keypress()
    sys.exit(exit_code)
