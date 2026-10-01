# -*- coding: utf-8 -*-

import streamlit as st
import os
import shutil

from Models.audit_log_model import AuditLogModel
from Views.tra_cuu_view import hien_thi_tra_cuu


DATABASE_FILE = os.path.join("Data", "QuanLyCom.db")
BACKUP_DIR = os.path.join("Data", "Backups")


def tao_thu_muc_backup():
    """Tạo thư mục backup nếu chưa tồn tại."""
    os.makedirs(BACKUP_DIR, exist_ok=True)


def sao_luu_database():
    """Sao lưu database hiện tại."""
    if not os.path.exists(DATABASE_FILE):
        return False, "Không tìm thấy file cơ sở dữ liệu."

    try:
        tao_thu_muc_backup()

        ten_file = "QuanLyCom_backup.db"
        duong_dan_backup = os.path.join(
            BACKUP_DIR,
            ten_file
        )

        shutil.copy2(
            DATABASE_FILE,
            duong_dan_backup
        )

        return (
            True,
            f"Đã sao lưu dữ liệu vào: {duong_dan_backup}"
        )

    except Exception as e:
        return False, f"Lỗi sao lưu: {e}"


def khoi_phuc_database(duong_dan_backup):
    """Khôi phục database từ file backup."""
    if not os.path.exists(duong_dan_backup):
        return False, "Không tìm thấy file backup."

    if not os.path.exists(DATABASE_FILE):
        return False, "Không tìm thấy database hiện tại."

    try:
        shutil.copy2(
            duong_dan_backup,
            DATABASE_FILE
        )

        return (
            True,
            "Khôi phục cơ sở dữ liệu thành công."
        )

    except Exception as e:
        return False, f"Lỗi khôi phục: {e}"


def hien_thi_tra_cuu_tab():
    """Hiển thị chức năng hỗ trợ và tra cứu."""
    hien_thi_tra_cuu()


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

        tao_thu_muc_backup()

        danh_sach_backup = []

        for ten_file in os.listdir(BACKUP_DIR):

            duong_dan = os.path.join(
                BACKUP_DIR,
                ten_file
            )

            if (
                os.path.isfile(duong_dan)
                and ten_file.endswith(".db")
            ):
                danh_sach_backup.append(ten_file)

        danh_sach_backup.sort(reverse=True)

        if danh_sach_backup:

            file_backup = st.selectbox(
                "Chọn file backup",
                danh_sach_backup,
                key="chon_file_backup"
            )

            duong_dan_backup = os.path.join(
                BACKUP_DIR,
                file_backup
            )

            if st.button(
                "🔄 Khôi phục dữ liệu",
                width="stretch"
            ):
                thanh_cong, thong_bao = khoi_phuc_database(
                    duong_dan_backup
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
            st.caption("Chưa có file backup.")


def hien_thi_log():
    """Hiển thị nhật ký hoạt động."""

    st.subheader("📋 Nhật ký hoạt động")

    try:

        logs = AuditLogModel.lay_tat_ca()

        if not logs:
            st.info("Chưa có dữ liệu nhật ký.")
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
                        f"Đã xóa nhật ký có ID = {int(log_id)}."
                    )

                    st.rerun()

                else:

                    st.warning(
                        f"Không tìm thấy nhật ký có ID = {int(log_id)}."
                    )

            except Exception as e:

                st.error(
                    f"Lỗi khi xóa nhật ký: {e}"
                )

    except Exception as e:

        st.error(
            f"Không thể tải nhật ký: {e}"
        )


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