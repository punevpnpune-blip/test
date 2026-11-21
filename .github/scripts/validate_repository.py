"""Validate CloudStream 4.9.1 metadata and this repository's two staged packages."""

import hashlib
import json
import os
import sys
from pathlib import Path
from zipfile import ZipFile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def is_string_list(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def reject_json_constant(value):
    raise ValueError(f"{value} is not a valid JSON value")


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_json_constant)
    except ValueError as exc:
        raise ValueError(f"{path}: {exc}") from exc


def validate_manifest(manifest, base_url):
    require(isinstance(manifest, dict), "repo.json must contain an object")
    name = manifest.get("name")
    require(isinstance(name, str) and name.strip(), "repo.json needs a non-empty name")
    version = manifest.get("manifestVersion")
    require(type(version) is int and version == 1, "Expected manifestVersion 1 in repo.json")
    for field in ("description", "iconUrl"):
        require(
            manifest.get(field) is None or isinstance(manifest[field], str),
            f"repo.json: {field} must be a string or null",
        )
    require(
        manifest.get("pluginLists") == [f"{base_url}/plugins.json"],
        "repo.json must point to the published plugins.json",
    )


def validate_entry(entry, directory, base_url, seen):
    require(isinstance(entry, dict), "plugins.json entries must be objects")
    name = entry.get("internalName")
    require(name in ("SupJav", "SexTB") and name not in seen, f"Unexpected provider: {name!r}")
    seen.add(name)
    display_name = entry.get("name")
    require(isinstance(display_name, str) and display_name.strip(), f"{name}: missing name")
    require(is_string_list(entry.get("authors")), f"{name}: authors must be an array of strings")
    for field in ("description", "repositoryUrl", "language", "iconUrl"):
        require(
            entry.get(field) is None or isinstance(entry[field], str),
            f"{name}: {field} must be a string or null",
        )
    status = entry.get("status")
    require(type(status) is int and 0 <= status <= 3, f"{name}: status must be 0 through 3")
    version = entry.get("version")
    require(type(version) is int and 0 < version <= 2**31 - 1, f"{name}: invalid version")
    api_version = entry.get("apiVersion")
    require(type(api_version) is int and api_version == 1, f"{name}: expected apiVersion 1")
    types = entry.get("tvTypes")
    require(is_string_list(types) and "NSFW" in types, f"{name}: tvTypes must include NSFW")

    package = directory / f"{name}.cs3"
    require(entry.get("url") == f"{base_url}/{package.name}", f"{name}: unexpected download URL")
    content = package.read_bytes()
    size = entry.get("fileSize")
    require(type(size) is int and size == len(content), f"{name}: fileSize mismatch")
    expected_hash = f"sha256-{hashlib.sha256(content).hexdigest()}"
    require(entry.get("fileHash") == expected_hash, f"{name}: fileHash mismatch")

    with ZipFile(package) as archive:
        json.loads(archive.read("manifest.json"))
        require(
            archive.read("classes.dex").startswith(b"dex\n") and archive.testzip() is None,
            f"{name}: invalid CS3 package",
        )


def main():
    directory = Path(sys.argv[1])
    base_url = f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/builds"
    manifest = read_json(directory / "repo.json")
    validate_manifest(manifest, base_url)
    entries = read_json(directory / "plugins.json")
    require(
        isinstance(entries, list) and len(entries) == 2,
        "plugins.json must contain one entry for each provider",
    )
    seen = set()
    for entry in entries:
        validate_entry(entry, directory, base_url, seen)


if __name__ == "__main__":
    main()
