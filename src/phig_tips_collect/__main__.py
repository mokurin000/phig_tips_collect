import os
import sys
import json

from phig_tips_collect import collect_tips


def main():
    os.chdir("./Phigdata")
    d = collect_tips()
    d = sorted(d, key=lambda e: e["text"])

    sys.stdout.reconfigure(encoding="utf-8")
    json.dump(d, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
