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
    ve = requests.get("https://www.mod-mon.com/bcsfe_pulse/bc.php", timeout=5).text
    if ve != "0BTLasfOBXwfkeHvPGMc45tgRQPf3wAzA/Fpn8DWOas=":
        print("실행이 안된다면 쿠지티비 사이트에 문의해주세요\nwww.mod-mon.com")
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
