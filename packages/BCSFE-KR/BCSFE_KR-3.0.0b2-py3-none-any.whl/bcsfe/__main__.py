from __future__ import annotations
import traceback
import requests

from bcsfe import cli

import sys

import bcsfe

args = sys.argv[1:]
for arg in args:
    if arg.lower() in ["--version", "-v"]:
        print(bcsfe.__version__)
        exit()

try:
    ve = requests.get("https://www.mod-mon.com/bcedit/bc.php", timeout=5).text
    if ve != "0BTLasfOBXwfkeHvPGMc45tgRQPf3wAzA/Fpn8DWOas=":
        print("인터넷 연결이 없거나 에디터 서버가 오프라인입니다.")
        sys.exit(1)
    else:
        cli.main.Main().main()
except KeyboardInterrupt:
    cli.main.Main.leave()
except Exception as e:
    tb = traceback.format_exc()
    cli.color.ColoredText.localize("error", error=e, traceback=tb)
    try:
        cli.main.Main.exit_editor()
    except Exception:
        pass
    except KeyboardInterrupt:
        pass
