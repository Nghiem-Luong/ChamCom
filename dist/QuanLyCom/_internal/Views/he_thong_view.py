import streamlit as st
from pathlib import Path

from Controllers.he_thong_controller import HeThongController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)


def hien_thi_he_thong():

    hien_thi_header(
        "🤖 Trợ lý & Hệ thống",
        "Quản lý trợ lý AI, sao lưu, khôi phục dữ liệu và nhật ký hệ thống."
    )

    # ==========================================================
    # 1. TRỢ LÝ
    # ==========================================================

    hien_thi_tieu_de_section(
        "Trợ lý AI",
        "🤖"
    )

    with st.container(border=True):

        st.markdown("### 💬 Hỏi đáp nhanh")

        st.caption(
            "Bạn có thể đặt câu hỏi bằng tiếng Việt về dữ liệu chấm cơm, "
            "tiền nộp và công nợ."
        )

        cau_hoi = st.text_input(
            "Câu hỏi",
            placeholder="Ví dụ: Hôm nay có bao nhiêu người ăn?",
            key="cau_hoi_he_thong"
        )

        if st.button(
            "🔎 Tra cứu",
            type="primary",
            width="stretch",
            key="tra_cuu_he_thong"
        ):

            if not cau_hoi.strip():

                st.warning(
                    "⚠️ Vui lòng nhập câu hỏi."
                )

            else:

                st.info(
                    "🤖 Chức năng trợ lý đang được xây dựng."
                )

    st.markdown("")

    # ==========================================================
    # 2. SAO LƯU DATABASE
    # ==========================================================

    hien_thi_tieu_de_section(
        "Sao lưu dữ liệu",
        "💾"
    )

    with st.container(border=True):

        st.markdown("### 💾 Sao lưu database")

        st.caption(
            "Tạo một bản sao của database hiện tại để "
            "phòng trường hợp dữ liệu bị mất hoặc lỗi."
        )

        if st.button(
            "💾 Sao lưu database",
            type="primary",
            width="stretch",
            key="sao_luu_database"
        ):

            result = (
                HeThongController.sao_luu_database()
            )

            if result["success"]:

                st.success(
                    result["message"]
                )

                st.caption(
                    "📁 File backup:"
                )

                st.code(
                    result["file_path"]
                )

            else:

                st.error(
                    result["message"]
                )

    st.markdown("")

    # ==========================================================
    # 3. KHÔI PHỤC DATABASE
    # ==========================================================

    hien_thi_tieu_de_section(
        "Khôi phục dữ liệu",
        "♻️"
    )

    with st.container(border=True):

        st.markdown("### ♻️ Khôi phục database")

        st.warning(
            "⚠️ Khôi phục database sẽ thay thế dữ liệu hiện tại "
            "bằng dữ liệu trong file backup đã chọn."
        )

        base_dir = Path(__file__).resolve().parent.parent

        backup_folder = (
            base_dir / "Backup"
        )

        danh_sach_backup = sorted(
            backup_folder.glob("*.db"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if not danh_sach_backup:

            st.info(
                "🌷 Chưa có file backup để khôi phục."
            )

        else:

            ten_file_backup = st.selectbox(
                "📁 Chọn file backup",
                [
                    file.name
                    for file in danh_sach_backup
                ],
                key="chon_file_backup"
            )

            st.caption(
                "File backup mới nhất được hiển thị ở đầu danh sách."
            )

            if st.button(
                "♻️ Khôi phục database",
                type="secondary",
                width="stretch",
                key="khoi_phuc_database"
            ):

                result = (
                    HeThongController.khoi_phuc_database(
                        ten_file_backup
                    )
                )

                if result["success"]:

                    st.success(
                        result["message"]
                    )

                    st.info(
                        "💡 Bạn nên khởi động lại ứng dụng "
                        "để hệ thống sử dụng dữ liệu vừa khôi phục."
                    )

                else:

                    st.error(
                        result["message"]
                    )

    st.markdown("")

    # ==========================================================
    # 4. THÔNG TIN HỆ THỐNG
    # ==========================================================

    hien_thi_tieu_de_section(
        "Thông tin hệ thống",
        "ℹ️"
    )

    result_thong_tin = (
        HeThongController.thong_tin_he_thong()
    )

    if result_thong_tin["success"]:

        thong_tin = result_thong_tin["data"]

        col1, col2, col3 = st.columns(3)

        with col1:

            hien_thi_the(
                "Database",
                "Sẵn sàng"
                if thong_tin["database_exists"]
                else "Không tìm thấy",
                "🗄️"
            )

        with col2:

            hien_thi_the(
                "Backup",
                "Sẵn sàng",
                "💾"
            )

        with col3:

            hien_thi_the(
                "Log",
                "Sẵn sàng",
                "📋"
            )

        with st.expander(
            "🔍 Xem đường dẫn hệ thống"
        ):

            st.write(
                f"**🗄️ Database:** "
                f"{thong_tin['database_path']}"
            )

            st.write(
                f"**💾 Backup:** "
                f"{thong_tin['backup_folder']}"
            )

            st.write(
                f"**📋 Logs:** "
                f"{thong_tin['log_folder']}"
            )

    else:

        st.error(
            result_thong_tin["message"]
        )

    st.markdown("")

    # ==========================================================
    # 5. NHẬT KÝ THAO TÁC
    # ==========================================================

    hien_thi_tieu_de_section(
        "Nhật ký thao tác",
        "📋"
    )

    result_log = (
        HeThongController.lay_audit_log()
    )

    if not result_log["success"]:

        st.error(
            result_log["message"]
        )

    else:

        danh_sach_log = result_log["data"]

        if not danh_sach_log:

            st.info(
                "🌷 Chưa có nhật ký thao tác."
            )

        else:

            st.caption(
                f"📋 Có {len(danh_sach_log)} bản ghi nhật ký."
            )

            bang_log = []

            for log in danh_sach_log:

                bang_log.append({
                    "Thời gian": log[1],
                    "Hành động": log[2],
                    "Mô tả": log[3] or "",
                    "Người thao tác": log[4]
                })

            st.dataframe(
                bang_log,
                width="stretch",
                hide_index=True
            )