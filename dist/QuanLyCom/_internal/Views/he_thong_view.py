# -*- coding: utf-8 -*-

import streamlit as st
from pathlib import Path

from Controllers.he_thong_controller import HeThongController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)

from Utils.ollama_helper import hoi_qwen
from Controllers.AIController import lay_du_lieu_cho_ai


# ==========================================================
# TRỢ LÝ AI - XỬ LÝ CÂU HỎI
# ==========================================================

def xu_ly_cau_hoi_he_thong(cau_hoi):

    du_lieu_db = lay_du_lieu_cho_ai(cau_hoi)

    if du_lieu_db:

        prompt = f"""
Bạn là Dâu Tây, trợ lý AI của ứng dụng Quản Lý Chấm Cơm.

Câu hỏi của người dùng:
{cau_hoi}

Dữ liệu chính xác lấy trực tiếp từ hệ thống:
{du_lieu_db}

Hãy trả lời câu hỏi dựa trên dữ liệu hệ thống ở trên.

QUY TẮC:
- Không được thay đổi số liệu.
- Không được tự bịa số liệu.
- Không được suy đoán thêm dữ liệu.
- Trả lời trực tiếp, ngắn gọn, dễ hiểu.
- Trả lời bằng tiếng Việt.
- Nếu có ngày tháng, hiển thị dạng DD/MM/YYYY.
"""

    else:

        prompt = f"""
Bạn là Dâu Tây, trợ lý AI của ứng dụng Quản Lý Chấm Cơm.

Người dùng hỏi:
{cau_hoi}

Hãy trả lời bằng tiếng Việt một cách tự nhiên.

Bạn có thể:
- Hướng dẫn sử dụng phần mềm.
- Giải thích chức năng.
- Trò chuyện thông thường.
- Giải thích các khái niệm.

Nếu câu hỏi yêu cầu dữ liệu CSDL nhưng hệ thống
không cung cấp dữ liệu phù hợp, hãy nói rõ rằng
chưa có dữ liệu phù hợp.

Không được tự tạo số liệu CSDL.
"""

    return hoi_qwen(prompt, None)


# ==========================================================
# HÀM CHÍNH
# ==========================================================

def hien_thi_he_thong():

    language = st.session_state.get(
        "language",
        "vi"
    )

    # ======================================================
    # NGÔN NGỮ
    # ======================================================

    texts = {

        "vi": {
            "header": "🤖 Trợ lý & Hệ thống",
            "header_desc": (
                "Quản lý trợ lý AI, sao lưu, khôi phục "
                "dữ liệu và nhật ký hệ thống."
            ),

            "assistant": "Trợ lý AI",
            "assistant_desc": (
                "Trợ lý Dâu Tây có thể hỗ trợ tra cứu dữ liệu "
                "chấm cơm, tiền nộp và công nợ."
            ),

            "quick_question": "💬 Hỏi đáp nhanh",
            "question": "Câu hỏi",
            "placeholder": (
                "Ví dụ: Hôm nay có bao nhiêu người ăn?"
            ),
            "search": "🔎 Tra cứu",
            "empty_question": "⚠️ Vui lòng nhập câu hỏi.",
            "thinking": "🤖 Dâu Tây đang suy nghĩ...",

            "backup_title": "Sao lưu dữ liệu",
            "backup_subtitle": "💾 Sao lưu database",
            "backup_desc": (
                "Tạo một bản sao của database hiện tại "
                "để phòng trường hợp dữ liệu bị mất hoặc lỗi."
            ),
            "backup_button": "💾 Sao lưu database",
            "backup_file": "📁 File backup:",

            "restore_title": "Khôi phục dữ liệu",
            "restore_subtitle": "♻️ Khôi phục database",
            "restore_warning": (
                "⚠️ Khôi phục database sẽ thay thế dữ liệu "
                "hiện tại bằng dữ liệu trong file backup đã chọn."
            ),
            "no_backup": "🌷 Chưa có file backup để khôi phục.",
            "choose_backup": "📁 Chọn file backup",
            "backup_latest": (
                "File backup mới nhất được hiển thị ở đầu danh sách."
            ),
            "restore_button": "♻️ Khôi phục database",
            "restart": (
                "💡 Bạn nên khởi động lại ứng dụng "
                "để hệ thống sử dụng dữ liệu vừa khôi phục."
            ),

            "system_info": "Thông tin hệ thống",
            "database": "Database",
            "ready": "Sẵn sàng",
            "not_found": "Không tìm thấy",
            "backup": "Backup",
            "log": "Log",
            "paths": "🔍 Xem đường dẫn hệ thống",
            "database_path": "🗄️ Database",
            "backup_path": "💾 Backup",
            "log_path": "📋 Logs",

            "audit": "Nhật ký thao tác",
            "no_log": "🌷 Chưa có nhật ký thao tác.",
            "log_count": "📋 Có {} bản ghi nhật ký.",
            "time": "Thời gian",
            "action": "Hành động",
            "description": "Mô tả",
            "operator": "Người thao tác",
        },

        "en": {
            "header": "🤖 Assistant & System",
            "header_desc": (
                "Manage the AI assistant, backup, restore "
                "and system activity logs."
            ),

            "assistant": "AI Assistant",
            "assistant_desc": (
                "Dâu Tây can help you check meal attendance, "
                "payments and debts."
            ),

            "quick_question": "💬 Quick Q&A",
            "question": "Question",
            "placeholder": (
                "Example: How many people ate today?"
            ),
            "search": "🔎 Search",
            "empty_question": "⚠️ Please enter a question.",
            "thinking": "🤖 Dâu Tây is thinking...",

            "backup_title": "Data Backup",
            "backup_subtitle": "💾 Database Backup",
            "backup_desc": (
                "Create a copy of the current database "
                "to protect against data loss or errors."
            ),
            "backup_button": "💾 Backup database",
            "backup_file": "📁 Backup file:",

            "restore_title": "Data Restore",
            "restore_subtitle": "♻️ Restore Database",
            "restore_warning": (
                "⚠️ Restoring the database will replace the "
                "current data with the selected backup."
            ),
            "no_backup": "🌷 No backup file is available.",
            "choose_backup": "📁 Select backup file",
            "backup_latest": (
                "The newest backup file is shown first."
            ),
            "restore_button": "♻️ Restore database",
            "restart": (
                "💡 You should restart the application "
                "after restoring the database."
            ),

            "system_info": "System Information",
            "database": "Database",
            "ready": "Ready",
            "not_found": "Not found",
            "backup": "Backup",
            "log": "Log",
            "paths": "🔍 View system paths",
            "database_path": "🗄️ Database",
            "backup_path": "💾 Backup",
            "log_path": "📋 Logs",

            "audit": "Activity Log",
            "no_log": "🌷 No activity logs yet.",
            "log_count": "📋 {} log records.",
            "time": "Time",
            "action": "Action",
            "description": "Description",
            "operator": "Operator",
        },

        "zh": {
            "header": "🤖 助手与系统",
            "header_desc": (
                "管理 AI 助手、数据库备份、恢复 "
                "以及系统操作日志。"
            ),

            "assistant": "AI 助手",
            "assistant_desc": (
                "Dâu Tây 可以帮助查询用餐记录、"
                "缴费信息和欠款。"
            ),

            "quick_question": "💬 快速问答",
            "question": "问题",
            "placeholder": (
                "例如：今天有多少人用餐？"
            ),
            "search": "🔎 查询",
            "empty_question": "⚠️ 请输入问题。",
            "thinking": "🤖 Dâu Tây 正在思考...",

            "backup_title": "数据备份",
            "backup_subtitle": "💾 数据库备份",
            "backup_desc": (
                "创建当前数据库副本，"
                "防止数据丢失或出现错误。"
            ),
            "backup_button": "💾 备份数据库",
            "backup_file": "📁 备份文件：",

            "restore_title": "数据恢复",
            "restore_subtitle": "♻️ 恢复数据库",
            "restore_warning": (
                "⚠️ 恢复数据库将使用所选备份文件 "
                "替换当前数据。"
            ),
            "no_backup": "🌷 暂无可恢复的备份文件。",
            "choose_backup": "📁 选择备份文件",
            "backup_latest": (
                "最新的备份文件显示在列表顶部。"
            ),
            "restore_button": "♻️ 恢复数据库",
            "restart": (
                "💡 恢复数据库后，建议重新启动应用程序。"
            ),

            "system_info": "系统信息",
            "database": "数据库",
            "ready": "正常",
            "not_found": "未找到",
            "backup": "备份",
            "log": "日志",
            "paths": "🔍 查看系统路径",
            "database_path": "🗄️ 数据库",
            "backup_path": "💾 备份",
            "log_path": "📋 日志",

            "audit": "操作日志",
            "no_log": "🌷 暂无操作日志。",
            "log_count": "📋 共 {} 条日志记录。",
            "time": "时间",
            "action": "操作",
            "description": "说明",
            "operator": "操作人员",
        }
    }

    text = texts.get(
        language,
        texts["vi"]
    )

    # ======================================================
    # HEADER
    # ======================================================

    hien_thi_header(
        text["header"],
        text["header_desc"]
    )

    # ======================================================
    # 1. TRỢ LÝ AI
    # ======================================================

    hien_thi_tieu_de_section(
        text["assistant"],
        "🤖"
    )

    with st.container(border=True):

        st.markdown(
            f"### {text['quick_question']}"
        )

        st.caption(
            text["assistant_desc"]
        )

        cau_hoi = st.text_input(
            text["question"],
            placeholder=text["placeholder"],
            key="cau_hoi_he_thong"
        )

        if st.button(
            text["search"],
            type="primary",
            width="stretch",
            key="tra_cuu_he_thong"
        ):

            if not cau_hoi.strip():

                st.warning(
                    text["empty_question"]
                )

            else:

                with st.spinner(
                    text["thinking"]
                ):

                    try:

                        tra_loi = xu_ly_cau_hoi_he_thong(
                            cau_hoi.strip()
                        )

                        if tra_loi:

                            st.success(
                                "🍓 Dâu Tây"
                            )

                            st.markdown(
                                tra_loi
                            )

                        else:

                            st.warning(
                                "Không nhận được câu trả lời từ AI."
                                if language == "vi"
                                else
                                "No response received from AI."
                                if language == "en"
                                else
                                "未收到 AI 的回复。"
                            )

                    except Exception as e:

                        if language == "vi":

                            st.error(
                                f"❌ Không thể kết nối với trợ lý AI: {e}"
                            )

                        elif language == "en":

                            st.error(
                                f"❌ Unable to connect to AI assistant: {e}"
                            )

                        else:

                            st.error(
                                f"❌ 无法连接 AI 助手：{e}"
                            )

    st.markdown("")

    # ======================================================
    # 2. SAO LƯU DATABASE
    # ======================================================

    hien_thi_tieu_de_section(
        text["backup_title"],
        "💾"
    )

    with st.container(border=True):

        st.markdown(
            f"### {text['backup_subtitle']}"
        )

        st.caption(
            text["backup_desc"]
        )

        if st.button(
            text["backup_button"],
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
                    text["backup_file"]
                )

                st.code(
                    result["file_path"]
                )

            else:

                st.error(
                    result["message"]
                )

    st.markdown("")

    # ======================================================
    # 3. KHÔI PHỤC DATABASE
    # ======================================================

    hien_thi_tieu_de_section(
        text["restore_title"],
        "♻️"
    )

    with st.container(border=True):

        st.markdown(
            f"### {text['restore_subtitle']}"
        )

        st.warning(
            text["restore_warning"]
        )

        base_dir = (
            Path(__file__).resolve().parent.parent
        )

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
                text["no_backup"]
            )

        else:

            ten_file_backup = st.selectbox(
                text["choose_backup"],
                [
                    file.name
                    for file in danh_sach_backup
                ],
                key="chon_file_backup"
            )

            st.caption(
                text["backup_latest"]
            )

            if st.button(
                text["restore_button"],
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
                        text["restart"]
                    )

                else:

                    st.error(
                        result["message"]
                    )

    st.markdown("")

    # ======================================================
    # 4. THÔNG TIN HỆ THỐNG
    # ======================================================

    hien_thi_tieu_de_section(
        text["system_info"],
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
                text["database"],
                (
                    text["ready"]
                    if thong_tin["database_exists"]
                    else text["not_found"]
                ),
                "🗄️"
            )

        with col2:

            hien_thi_the(
                text["backup"],
                text["ready"],
                "💾"
            )

        with col3:

            hien_thi_the(
                text["log"],
                text["ready"],
                "📋"
            )

        with st.expander(
            text["paths"]
        ):

            st.write(
                f"**{text['database_path']}:** "
                f"{thong_tin['database_path']}"
            )

            st.write(
                f"**{text['backup_path']}:** "
                f"{thong_tin['backup_folder']}"
            )

            st.write(
                f"**{text['log_path']}:** "
                f"{thong_tin['log_folder']}"
            )

    else:

        st.error(
            result_thong_tin["message"]
        )

    st.markdown("")

    # ======================================================
    # 5. NHẬT KÝ THAO TÁC
    # ======================================================

    hien_thi_tieu_de_section(
        text["audit"],
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
                text["no_log"]
            )

        else:

            st.caption(
                text["log_count"].format(
                    len(danh_sach_log)
                )
            )

            bang_log = []

            for log in danh_sach_log:

                bang_log.append(
                    {
                        text["time"]: log[1],
                        text["action"]: log[2],
                        text["description"]: log[3] or "",
                        text["operator"]: log[4]
                    }
                )

            st.dataframe(
                bang_log,
                width="stretch",
                hide_index=True
            )