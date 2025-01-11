import os
import sys
import json

from phig_tips_collect import collect_tips


def main():
    os.chdir("./Phigdata")
    d = collect_tips()
    json.dump(d, sys.stdout, ensure_ascii=True)


if __name__ == "__main__":
    main()
