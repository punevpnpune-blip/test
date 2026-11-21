import hashlib
import json
import os
import sys
from pathlib import Path
from zipfile import ZipFile


def main():
    output = Path(sys.argv[1])
    repository = os.environ["GITHUB_REPOSITORY"]
    base_url = f"https://raw.githubusercontent.com/{repository}/builds"
    names = {"SupJav", "SexTB"}
    entries = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in sys.argv[2:]
    ]
    if len(entries) != len(names) or {entry["internalName"] for entry in entries} != names:
        raise ValueError("plugins.json must contain one entry for each provider")

    for entry in entries:
        name = entry["internalName"]
        package = output / f"{name}.cs3"
        content = package.read_bytes()
        expected_hash = f"sha256-{hashlib.sha256(content).hexdigest()}"
        if entry["url"] != f"{base_url}/{package.name}":
            raise ValueError(f"Unexpected download URL for {name}")
        if entry["fileSize"] != len(content) or entry["fileHash"] != expected_hash:
            raise ValueError(f"Package size or hash mismatch for {name}")
        if entry["apiVersion"] != 1 or "NSFW" not in entry["tvTypes"]:
            raise ValueError(f"Unexpected API version or content type for {name}")

        with ZipFile(package) as archive:
            json.loads(archive.read("manifest.json"))
            if not archive.read("classes.dex").startswith(b"dex\n") or archive.testzip():
                raise ValueError(f"Invalid CS3 package for {name}")

    (output / "plugins.json").write_text(
        json.dumps(entries, indent=2) + "\n", encoding="utf-8"
    )
    manifest = json.loads(Path("repo.json").read_text(encoding="utf-8"))
    if manifest["manifestVersion"] != 1:
        raise ValueError("Expected CloudStream repository manifest version 1")
    manifest["pluginLists"] = [f"{base_url}/plugins.json"]
    (output / "repo.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
