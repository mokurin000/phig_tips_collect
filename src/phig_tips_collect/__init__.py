import json
import subprocess

from packaging.version import Version


def collect_tips() -> list[dict[str, str]]:
    old_vers = list(
        filter(
            lambda s: s.startswith("v"),
            map(
                lambda b: b.strip(),
                subprocess.run(["git", "branch"], capture_output=True)
                .stdout.decode(encoding="ascii")
                .split(),
            ),
        )
    )

    new_vers = (
        subprocess.run(["git", "tag"], capture_output=True)
        .stdout.decode(encoding="ascii")
        .split()
    )

    tips = {}

    try:
        for old_ver in old_vers:
            subprocess.run(
                ["git", "checkout", old_ver], check=True, capture_output=True
            )
            with open("MonoBehaviour/ShowTips.json", mode="r", encoding="utf-8") as fp:
                data = json.load(fp)
                if old_ver.startswith("v1"):
                    tips_list = map(lambda t: t.strip(), data["chinese"].split("/"))
                elif old_ver.startswith("v2"):
                    tips_list = map(lambda t: t.strip(), data["chinese"].split("\r\n"))
                else:
                    raise Exception(f"Unsupported old version: {old_ver}")
                for tip in tips_list:
                    ver_list = tips.get(tip, []) + [old_ver]
                    tips[tip] = ver_list

        for new_ver in new_vers:
            subprocess.run(
                ["git", "checkout", new_ver], check=True, capture_output=True
            )
            with open(
                "MonoBehaviour/TipsProvider.json", mode="r", encoding="utf-8"
            ) as fp:
                data = json.load(fp)
                tips_list = map(lambda t: t.strip(), data["tips"][0]["tips"])
                for tip in tips_list:
                    ver_list = tips.get(tip, []) + [new_ver]
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
