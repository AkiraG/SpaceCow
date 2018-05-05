import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("SPACECOW.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = [],
        include_files = [('/images','images'),'images/caipira.png','images/ship.png',('/sound','sound')],
        excludes = []
)




setup(
    name = "COWLEN",
    version = "2.0",
    description = "VACA ALIEN",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
