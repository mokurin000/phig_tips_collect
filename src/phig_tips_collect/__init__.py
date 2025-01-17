import json
import subprocess

from packaging.version import Version


def collect_tips(version_range: str = None) -> list[dict[str, str]]:
    vers = (
        subprocess.run(["git", "tag"], capture_output=True)
        .stdout.decode(encoding="ascii")
        .split()
    )

    tips = {}

    try:
        if version_range is not None:
            minv, maxv = map(lambda v: Version(v), version_range.split(".."))

            def filter_version(version: str) -> bool:
                v = Version(version)
                return v < minv or v > maxv
        else:

            def filter_version(_: str) -> bool:
                return False

        for version in vers:
            if filter_version(version):
                continue

            subprocess.run(
                ["git", "checkout", version], check=True, capture_output=True
            )

            match version[1]:
                case "1":
                    path = "MonoBehaviour/ShowTips.json"

                    def get_list(data: dict):
                        return map(lambda t: t.strip(), data["chinese"].split("/"))
                case "2" if Version(version) < Version("v2.2"):
                    path = "MonoBehaviour/ShowTips.json"

                    def get_list(data: dict):
                        return map(lambda t: t.strip(), data["chinese"].split("\r\n"))
                case "2" | "3":
                    path = "MonoBehaviour/TipsProvider.json"

                    def get_list(data: dict):
                        return map(lambda t: t.strip(), data["tips"][0]["tips"])
                case _:
                    raise Exception(f"Unsupported version: {version}")

            with open(path, mode="r", encoding="utf-8") as fp:
                data = json.load(fp)
                for tip in get_list(data):
                    ver_list = tips.get(tip, []) + [version]
                    tips[tip] = ver_list

    finally:
        subprocess.run(["git", "checkout", "main"], capture_output=True)

    results = []

    for tip, versions in tips.items():
        versions: list
        versions.sort(key=Version)
        first, last = versions[0], versions[-1]

        results.append(
            {
                "text": tip,
                "min_ver": first,
                "max_ver": last,
            }
        )

    return results
