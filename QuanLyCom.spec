# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import (
    copy_metadata,
    collect_submodules,
    collect_data_files,
    collect_all,
)


# ============================================================
# 1. STREAMLIT
# ============================================================

streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all(
    "streamlit"
)

datas = []
binaries = []
hiddenimports = []


datas += streamlit_datas
binaries += streamlit_binaries
hiddenimports += streamlit_hiddenimports

datas += copy_metadata("streamlit")


# ============================================================
# 2. OLLAMA
# ============================================================

ollama_datas, ollama_binaries, ollama_hiddenimports = collect_all(
    "ollama"
)

datas += ollama_datas
binaries += ollama_binaries
hiddenimports += ollama_hiddenimports

datas += copy_metadata("ollama")


# ============================================================
# 3. STREAMLIT DATA
# ============================================================

datas += collect_data_files(
    "streamlit",
    include_py_files=False
)


# ============================================================
# 4. OLLAMA DATA
# ============================================================

datas += collect_data_files(
    "ollama",
    include_py_files=False
)


# ============================================================
# 5. PROJECT SOURCE
# ============================================================

project_packages = [
    "Database",
    "Models",
    "Views",
    "Controllers",
    "Utils",
]

for package in project_packages:

    hiddenimports += collect_submodules(package)

    datas += [
        (package, package)
    ]


# ============================================================
# 6. APP.PY
# ============================================================

datas += [
    ("app.py", "."),
]


# ============================================================
# 7. ASSETS + DATABASE
# ============================================================

datas += [
    ("Assets", "Assets"),
    ("Data", "Data"),
]


# ============================================================
# 8. CÁC PACKAGE CHÍNH CỦA ỨNG DỤNG
# ============================================================

main_packages = [
    "pandas",
    "openpyxl",
    "numpy",
    "sqlite3",
]

for package in main_packages:

    try:
        hiddenimports += collect_submodules(package)
    except Exception:
        pass


# ============================================================
# 9. OLLAMA CLIENT
# ============================================================

hiddenimports += [
    "ollama",
]


# ============================================================
# 10. STREAMLIT MODULE QUAN TRỌNG
# ============================================================

hiddenimports += [
    "streamlit",
    "streamlit.web",
    "streamlit.web.cli",
    "streamlit.runtime",
    "streamlit.runtime.scriptrunner",
    "streamlit.runtime.scriptrunner.exec_code",
    "streamlit.runtime.scriptrunner.script_runner",
    "streamlit.runtime.scriptrunner.magic_funcs",
    "streamlit.runtime.state",
    "streamlit.runtime.app_session",
    "streamlit.runtime.runtime",
    "streamlit.web.server",
    "streamlit.web.server.server",
    "streamlit.web.server.starlette",
]


# ============================================================
# 11. PHÂN TÍCH
# ============================================================

a = Analysis(
    ["launcher.py"],

    pathex=[
        r"D:\PyCharm\DuAn\QuanLyCom"
    ],

    binaries=binaries,

    datas=datas,

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,

    optimize=0,
)


# ============================================================
# 12. PYZ
# ============================================================

pyz = PYZ(
    a.pure,
    a.zipped_data,
)


# ============================================================
# 13. EXE
# ============================================================

exe = EXE(
    pyz,

    a.scripts,

    [],

    exclude_binaries=True,

    name="QuanLyCom",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    console=True,

    disable_windowed_traceback=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,
)


# ============================================================
# 14. COLLECT
# ============================================================

coll = COLLECT(
    exe,

    a.binaries,

    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name="QuanLyCom",
)