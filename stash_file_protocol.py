import json
import os
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from stashapi.stashapp import StashInterface


def _resolve_config_path() -> Path:
    if os.environ.get("STASH_PATH_MAPPINGS_FILE"):
        return Path(os.environ["STASH_PATH_MAPPINGS_FILE"])

    candidates = ["config.json", "path_mappings.json"]
    search_roots = [Path.cwd(), Path(__file__).parent]

    # PyInstaller one-file extracts bundled data into sys._MEIPASS.
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        search_roots.insert(0, Path(meipass))

    for root in search_roots:
        for name in candidates:
            path = root / name
            if path.exists():
                return path

    raise FileNotFoundError(
        "Could not find config file. Expected config.json or path_mappings.json."
    )


def main() -> int:
    # TODO: replace with argparse proper arg parsing
    if len(sys.argv) < 2:
        return 1

    raw_url = sys.argv[1].strip().strip('"')
    parsed_url = urlparse(raw_url)

    media_type = parsed_url.netloc.lower()
    media_id = unquote(parsed_url.path.lstrip("/").split("/")[0])

    stash_url = os.environ.get("STASH_URL", "https://stash.shoji.me")
    stash_parsed = urlparse(stash_url)
    
    # TODO: add argparse for --version/-Version (double dash and SINGLE dash argument aliases)
    # TODO: add argparse --uri/-Uri  (double dash and SINGLE dash argument aliases)

    connection = {
        "Scheme": stash_parsed.scheme,
        "Host": stash_parsed.hostname,
        "Port": stash_parsed.port or (443 if stash_parsed.scheme == "https" else 80),
        "ApiKey": os.environ.get("STASH_API_KEY", ""),
    }
    stash = StashInterface(connection)

    with _resolve_config_path().open("r", encoding="utf-8") as f:
        config = json.load(f)

    mappings = config["mappings"]
    mappings.sort(key=lambda item: len(item["orig"]), reverse=True)
    source_path = None

    if media_type in ["scene", "scenes", "video", "videos"]:
        media = stash.find_scene(media_id, fragment="id files { path }")
        if media and media.get("files"):
            source_path = media["files"][0]["path"]
    elif media_type in ["image", "images"]:
        media = stash.find_image(media_id, fragment="id files { path }")
        if media and media.get("files"):
            source_path = media["files"][0]["path"]
    elif media_type in ["gallery", "galleries"]:
        media = stash.find_gallery(media_id, fragment="id files { path }")
        if media and media.get("files"):
            source_path = media["files"][0]["path"]
    elif media_type in ["scene-marker", "scene_marker", "marker"]:
        markers = stash.find_scene_markers(
            {"id": {"value": int(media_id), "modifier": "EQUALS"}},
            fragment="id scene { files { path } }",
        )
        if markers and markers[0].get("scene", {}).get("files"):
            source_path = markers[0]["scene"]["files"][0]["path"]

    if not source_path:
        return 1

    for mapping in mappings:
        if source_path.startswith(mapping["orig"]):
            source_path = source_path.replace(mapping["orig"], mapping["local"], 1)
            break

    print(source_path)
    return 0
