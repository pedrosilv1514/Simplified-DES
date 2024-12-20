from cx_Freeze import setup, Executable

setup(
    name="SDES",
    version="1.0",
    description="SDES Encryption Tool",
    executables=[Executable("main.py", base="Win32GUI")],
)
