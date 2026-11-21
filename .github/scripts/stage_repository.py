import json
import os
import sys
from pathlib import Path


def main():
    output = Path(sys.argv[1])
    repository = os.environ["GITHUB_REPOSITORY"]
    base_url = f"https://raw.githubusercontent.com/{repository}/builds"
    entries = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in sys.argv[2:]
    ]

    (output / "plugins.json").write_text(
        json.dumps(entries, indent=2) + "\n", encoding="utf-8"
    )
    manifest = json.loads(Path("repo.json").read_text(encoding="utf-8"))
    manifest["pluginLists"] = [f"{base_url}/plugins.json"]
    (output / "repo.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
