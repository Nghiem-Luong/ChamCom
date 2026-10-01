# -*- coding: utf-8 -*-

import streamlit as st
import os
import shutil
import sys
from pathlib import Path

from Models.audit_log_model import AuditLogModel
from Views.tra_cuu_view import hien_thi_tra_cuu


# =========================================================
# XÁC ĐỊNH THƯ MỤC ỨNG DỤNG
# =========================================================

def lay_thu_muc_ung_dung():
    """
    Xác định thư mục gốc của ứng dụng.

    Khi chạy .py:
        D:\\PyCharm\\DuAn\\QuanLyCom

    Khi chạy .exe:
        D:\\PyCharm\\DuAn\\QuanLyCom\\dist\\QuanLyCom
    """

    try:
        if getattr(sys, "frozen", False):
            # Đang chạy bằng file .exe
            return Path(sys.executable).resolve().parent

        # Đang chạy bằng Python
        return Path(__file__).resolve().parent.parent

    except Exception:
        return Path.cwd()


# =========================================================
# TÌM DATABASE
# =========================================================

def tim_database():
    """
    Tìm file QuanLyCom.db thực tế.

    Ưu tiên:
    1. Data/QuanLyCom.db trong thư mục ứng dụng
    2. Data/QuanLyCom.db trong thư mục hiện tại
    3. Data/QuanLyCom.db ở thư mục cha

    Trả về Path nếu tìm thấy.
    Trả về None nếu không tìm thấy.
    """

    thu_muc_ung_dung = lay_thu_muc_ung_dung()
    thu_muc_hien_tai = Path.cwd()

    cac_duong_dan = [
        thu_muc_ung_dung / "Data" / "QuanLyCom.db",
        thu_muc_hien_tai / "Data" / "QuanLyCom.db",
        thu_muc_ung_dung.parent / "Data" / "QuanLyCom.db",
    ]

    da_kiem_tra = set()

    for duong_dan in cac_duong_dan:

        try:
            duong_dan = duong_dan.resolve()

            if str(duong_dan) in da_kiem_tra:
                continue

            da_kiem_tra.add(str(duong_dan))

            if duong_dan.exists() and duong_dan.is_file():
                return duong_dan

        except Exception:
            continue

    return None


# =========================================================
# ĐƯỜNG DẪN DATABASE VÀ BACKUP
# =========================================================

def lay_duong_dan_database():
    """
    Lấy đường dẫn database thực tế.
    """

    database = tim_database()

    if database:
        return database

    # Nếu chưa tìm thấy thì trả về vị trí mặc định
    return (
        lay_thu_muc_ung_dung()
        / "Data"
        / "QuanLyCom.db"
    )


def lay_thu_muc_backup():
    """
    Thư mục backup nằm cạnh database.
    """

    database = lay_duong_dan_database()

    return database.parent / "Backups"


DATABASE_FILE = lay_duong_dan_database()
BACKUP_DIR = lay_thu_muc_backup()


# =========================================================
# TẠO THƯ MỤC BACKUP
# =========================================================

def tao_thu_muc_backup():
    """Tạo thư mục backup nếu chưa tồn tại."""

    backup_dir = lay_thu_muc_backup()

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return backup_dir


# =========================================================
# SAO LƯU DATABASE
# =========================================================

def sao_luu_database():
    """Sao lưu database hiện tại."""

    try:

        database_file = tim_database()

        if database_file is None:

            thu_muc_ung_dung = lay_thu_muc_ung_dung()

            return (
                False,
                "Không tìm thấy file cơ sở dữ liệu.\n\n"
                f"Thư mục ứng dụng đang được xác định là:\n"
                f"{thu_muc_ung_dung}\n\n"
                "Hãy kiểm tra xem có thư mục:\n"
                f"{thu_muc_ung_dung / 'Data'}\n\n"
                "và file:\n"
                "QuanLyCom.db"
            )

        backup_dir = database_file.parent / "Backups"

        backup_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        ten_file = "QuanLyCom_backup.db"

        duong_dan_backup = backup_dir / ten_file

        # Sao lưu database
        shutil.copy2(
            str(database_file),
            str(duong_dan_backup)
        )

        # Kiểm tra lại file backup
        if not duong_dan_backup.exists():

            return (
                False,
                "Đã thực hiện sao lưu nhưng không tìm thấy "
                "file backup sau khi sao chép."
            )

        kich_thuoc = duong_dan_backup.stat().st_size

        if kich_thuoc <= 0:

            return (
                False,
                "File backup được tạo nhưng có kích thước 0 KB."
            )

        return (
            True,
            "Đã sao lưu dữ liệu thành công.\n\n"
            f"CSDL nguồn:\n"
            f"{database_file}\n\n"
            f"File backup:\n"
            f"{duong_dan_backup}\n\n"
            f"Kích thước backup: "
            f"{kich_thuoc / 1024:.1f} KB"
        )

    except Exception as e:

        return (
            False,
            f"Lỗi sao lưu: {e}"
        )


# =========================================================
# KHÔI PHỤC DATABASE
# =========================================================

def khoi_phuc_database(duong_dan_backup):
    """Khôi phục database từ file backup."""

    try:

        database_file = tim_database()

        if not os.path.exists(duong_dan_backup):

            return (
                False,
                "Không tìm thấy file backup."
            )

        if database_file is None:

            return (
                False,
                "Không tìm thấy database hiện tại."
            )

        # Đảm bảo đường dẫn là Path
        duong_dan_backup = Path(
            duong_dan_backup
        )

        # Sao lưu database hiện tại trước khi khôi phục
        backup_truoc_khi_khoi_phuc = (
            database_file.parent
            / "Backups"
            / "QuanLyCom_before_restore.db"
        )

        try:

            shutil.copy2(
                str(database_file),
                str(backup_truoc_khi_khoi_phuc)
            )

        except Exception:
            pass

        # Khôi phục
        shutil.copy2(
            str(duong_dan_backup),
            str(database_file)
        )

        return (
            True,
            "Khôi phục cơ sở dữ liệu thành công.\n\n"
            f"Database hiện tại:\n"
            f"{database_file}"
        )

    except Exception as e:

        return (
            False,
            f"Lỗi khôi phục: {e}"
        )


# =========================================================
# TRA CỨU
# =========================================================

def hien_thi_tra_cuu_tab():
    """Hiển thị chức năng hỗ trợ và tra cứu."""

    hien_thi_tra_cuu()


# =========================================================
# GIAO DIỆN SAO LƯU
# =========================================================

def hien_thi_sao_luu():
    """Hiển thị chức năng sao lưu và khôi phục dữ liệu."""

    st.subheader("💾 Sao lưu & khôi phục dữ liệu")

    st.info(
        "Sử dụng chức năng này để sao lưu dữ liệu trước khi thực hiện "
        "các thao tác quan trọng với hệ thống."
    )

    col1, col2 = st.columns(2)

    # =========================================================
    # SAO LƯU
    # =========================================================

    with col1:

        st.markdown("### 💾 Sao lưu dữ liệu")

        if st.button(
            "💾 Sao lưu ngay",
            width="stretch",
            type="primary"
        ):

            thanh_cong, thong_bao = sao_luu_database()

            if thanh_cong:

                st.success(thong_bao)

            else:

                st.error(thong_bao)

    # =========================================================
    # KHÔI PHỤC
    # =========================================================

    with col2:

        st.markdown("### 📂 File backup hiện có")

        try:

            backup_dir = tao_thu_muc_backup()

            danh_sach_backup = []

            for ten_file in os.listdir(backup_dir):

                duong_dan = backup_dir / ten_file

                if (
                    duong_dan.is_file()
                    and ten_file.lower().endswith(".db")
                ):
                    danh_sach_backup.append(ten_file)

            danh_sach_backup.sort(
                reverse=True
            )

        except Exception as e:

            danh_sach_backup = []

            st.error(
                f"Không thể đọc thư mục backup: {e}"
            )

        if danh_sach_backup:

            file_backup = st.selectbox(
                "Chọn file backup",
                danh_sach_backup,
                key="chon_file_backup"
            )

            duong_dan_backup = (
                backup_dir / file_backup
            )

            if st.button(
                "🔄 Khôi phục dữ liệu",
                width="stretch"
            ):

                thanh_cong, thong_bao = (
                    khoi_phuc_database(
                        duong_dan_backup
                    )
                )

                if thanh_cong:

                    st.success(thong_bao)

                    st.warning(
                        "Bạn nên tải lại trang ứng dụng để hệ thống "
                        "đọc lại dữ liệu."
                    )

                else:

                    st.error(thong_bao)

        else:

            st.caption(
                "Chưa có file backup."
            )


# =========================================================
# NHẬT KÝ HOẠT ĐỘNG
# =========================================================

def hien_thi_log():
    """Hiển thị nhật ký hoạt động."""

    st.subheader("📋 Nhật ký hoạt động")

    try:

        logs = AuditLogModel.lay_tat_ca()

        if not logs:

            st.info(
                "Chưa có dữ liệu nhật ký."
            )

            return

        # =====================================================
        # CHUYỂN DỮ LIỆU SANG DẠNG BẢNG
        # =====================================================

        du_lieu = []

        for log in logs:

            du_lieu.append({
                "ID": log[0],
                "Thời gian": log[1],
                "Hành động": log[2],
                "Mô tả": log[3],
                "Người thao tác": log[4],
            })

        st.dataframe(
            du_lieu,
            width="stretch",
            hide_index=True
        )

        st.divider()

        # =====================================================
        # XÓA NHẬT KÝ
        # =====================================================

        st.markdown("### 🗑️ Xóa nhật ký")

        log_id = st.number_input(
            "Nhập ID nhật ký cần xóa",
            min_value=1,
            step=1,
            value=1,
            key="log_id_xoa"
        )

        if st.button(
            "🗑️ Xóa nhật ký",
            width="stretch"
        ):

            try:

                so_luong = AuditLogModel.xoa_log(
                    int(log_id)
                )

                if so_luong > 0:

                    st.success(
                        f"Đã xóa nhật ký có ID = "
                        f"{int(log_id)}."
                    )

                    st.rerun()

                else:

                    st.warning(
                        f"Không tìm thấy nhật ký có ID = "
                        f"{int(log_id)}."
                    )

            except Exception as e:

                st.error(
                    f"Lỗi khi xóa nhật ký: {e}"
                )

    except Exception as e:

        st.error(
            f"Không thể tải nhật ký: {e}"
        )


# =========================================================
# MÀN HÌNH HỆ THỐNG
# =========================================================

def hien_thi_he_thong(language="vi"):
    """
    Màn hình Hệ thống.

    Gồm:
    1. Hỗ trợ & Tra cứu
    2. Sao lưu & Khôi phục
    3. Ghi log
    """

    st.title("⚙️ Hệ thống")

    tab_ho_tro, tab_sao_luu, tab_log = st.tabs([
        "🆘 Hỗ trợ",
        "💾 Sao lưu & khôi phục",
        "📋 Ghi log"
    ])

    # =========================================================
    # TAB HỖ TRỢ
    # =========================================================

    with tab_ho_tro:
        hien_thi_tra_cuu_tab()

    # =========================================================
    # TAB SAO LƯU
    # =========================================================

    with tab_sao_luu:
        hien_thi_sao_luu()

    # =========================================================
    # TAB LOG
    # =========================================================

    with tab_log:
        hien_thi_log()