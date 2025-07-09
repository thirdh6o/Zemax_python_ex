import os
import clr
from pathlib import Path

zemaxRoot = os.environ.get("ZEMAX_ROOT")

if zemaxRoot is None:
    # 通过注册表获取
    import winreg
    aKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Zemax")
    zemaxRoot = winreg.QueryValueEx(aKey, 'ZemaxRoot')[0]
    winreg.CloseKey(aKey)

print("ZemaxRoot =", zemaxRoot)

dll_path = Path(zemaxRoot) / "ZOS-API" / "Libraries" / "ZOSAPI_NetHelper.dll"
print("NetHelper 路径：", dll_path)

clr.AddReference(str(dll_path))

import ZOSAPI_NetHelper
ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()

zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
print("ZemaxDir =", zemaxDir)

if zemaxDir is None:
    raise Exception('Cannot find OpticStudio')
