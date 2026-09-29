import sys
import time
import threading
import webbrowser
from pathlib import Path

from streamlit.web import cli as stcli


def mo_trinh_duyet():
    time.sleep(3)
    webbrowser.open("http://localhost:8501")


def main():
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    app_path = base_path / "app.py"

    if not app_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy app.py tại: {app_path}"
        )

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.address",
        "0.0.0.0",
        "--server.port",
        "8501",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
        "--global.developmentMode",
        "false",
    ]

    threading.Thread(
        target=mo_trinh_duyet,
        daemon=True
    ).start()

    stcli.main()


if __name__ == "__main__":
    main()