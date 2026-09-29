# -*- coding: utf-8 -*-

import streamlit as st
from datetime import datetime

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
    hien_thi_info_card
)

from Controllers.nguoi_an_controller import NguoiAnController


@st.fragment(run_every="1s")
def _hien_thi_thoi_gian():
    language = st.session_state.get(
        "language",
        "vi"
    )

    texts = {
        "vi": {
            "today": "📅 Hôm nay",
            "system_running": "🟢 Hệ thống hoạt động",
        },
        "en": {
            "today": "📅 Today",
            "system_running": "🟢 System is running",
        },
        "zh": {
            "today": "📅 今天",
            "system_running": "🟢 系统运行正常",
        },
    }

    text = texts.get(
        language,
        texts["vi"]
    )

    now = datetime.now()

    ngay_hien_tai = now.strftime(
        "%d/%m/%Y"
    )

    gio_hien_tai = now.strftime(
        "%H:%M:%S"
    )

    col1, col2 = st.columns(
        [3, 1]
    )

    with col1:
        st.info(
            f"{text['today']}: "
            f"**{ngay_hien_tai}**  •  🕐 **{gio_hien_tai}**"
        )

    with col2:
        st.success(
            text["system_running"]
        )


def hien_thi_trang_chu():

    language = st.session_state.get(
        "language",
        "vi"
    )

    texts = {

        "vi": {
            "header": "🏠 Trang chủ",
            "header_desc": (
                "Tổng quan nhanh về hệ thống Quản lý Chấm Cơm."
            ),

            "overview": "Tổng quan hệ thống",

            "total_people": "Tổng số người ăn",
            "active_people": "Đang hoạt động",
            "inactive_people": "Đã ngừng",

            "people_status": "Tình trạng người ăn",
            "active_desc": (
                "Có {} người đang hoạt động "
                "trên tổng số {} người."
            ),
            "activity_rate": "Tỷ lệ hoạt động: {:.1f}%",

            "main_functions": "Chức năng chính",

            "attendance": "🍚 Chấm cơm",
            "attendance_desc": (
                "Quản lý người ăn, đăng ký suất ăn, "
                "đơn giá và số tiền phải trả theo từng ngày."
            ),

            "people_management": "👩‍🍳 Quản lý người ăn",
            "people_management_desc": (
                "Thêm, chỉnh sửa, tìm kiếm, "
                "ngừng hoạt động hoặc kích hoạt lại người ăn."
            ),

            "payment": "💰 Nộp tiền & công nợ",
            "payment_desc": (
                "Theo dõi tiền đã nộp, tiền phải trả "
                "và tình trạng công nợ của từng người."
            ),

            "statistics": "📊 Thống kê & báo cáo",
            "statistics_desc": (
                "Theo dõi dữ liệu theo thời gian "
                "và xuất báo cáo phục vụ quản lý."
            ),

            "smart_assistant": "Trợ lý thông minh",
            "assistant_title": "🤖 Dâu Tây",
            "assistant_desc": (
                "Trợ lý AI hỗ trợ tra cứu thông tin "
                "và dữ liệu trong hệ thống bằng "
                "câu hỏi tiếng Việt tự nhiên."
            ),
            "assistant_tip": (
                "💡 Bạn có thể sử dụng robot ở góc "
                "màn hình để đặt câu hỏi."
            ),

            "process": "Quy trình sử dụng",

            "step1": "① 👩‍🍳 Quản lý người ăn",
            "step1_desc": (
                "Thêm và quản lý danh sách "
                "người sử dụng suất ăn."
            ),

            "step2": "② 🍚 Chấm cơm",
            "step2_desc": (
                "Ghi nhận người ăn và "
                "số tiền phải trả."
            ),

            "step3": "③ 📊 Theo dõi",
            "step3_desc": (
                "Kiểm tra công nợ, "
                "thống kê và báo cáo."
            ),

            "data_error": (
                "⚠️ Không thể lấy dữ liệu người ăn."
            ),

            "inactive_card": "⚪ Đã ngừng hoạt động",
            "person_unit": "người",
        },

        "en": {
            "header": "🏠 Home",
            "header_desc": (
                "Quick overview of the Meal Management system."
            ),

            "overview": "System Overview",

            "total_people": "Total people",
            "active_people": "Active",
            "inactive_people": "Inactive",

            "people_status": "People Status",
            "active_desc": (
                "{} people are currently active "
                "out of {} people."
            ),
            "activity_rate": "Activity rate: {:.1f}%",

            "main_functions": "Main Functions",

            "attendance": "🍚 Meal Attendance",
            "attendance_desc": (
                "Manage people, meal registration, "
                "prices and daily payable amounts."
            ),

            "people_management": "👩‍🍳 People Management",
            "people_management_desc": (
                "Add, edit, search, deactivate "
                "or reactivate people."
            ),

            "payment": "💰 Payments & Debts",
            "payment_desc": (
                "Track payments, payable amounts "
                "and debt status for each person."
            ),

            "statistics": "📊 Statistics & Reports",
            "statistics_desc": (
                "Monitor data over time "
                "and export management reports."
            ),

            "smart_assistant": "Smart Assistant",
            "assistant_title": "🤖 Dâu Tây",
            "assistant_desc": (
                "AI assistant for searching system information "
                "and data using natural language."
            ),
            "assistant_tip": (
                "💡 Use the robot in the corner "
                "of the screen to ask questions."
            ),

            "process": "Usage Process",

            "step1": "① 👩‍🍳 Manage People",
            "step1_desc": (
                "Add and manage the list "
                "of meal users."
            ),

            "step2": "② 🍚 Meal Attendance",
            "step2_desc": (
                "Record meals and "
                "payable amounts."
            ),

            "step3": "③ 📊 Monitor",
            "step3_desc": (
                "Check debts, "
                "statistics and reports."
            ),

            "data_error": (
                "⚠️ Unable to load people data."
            ),

            "inactive_card": "⚪ Inactive",
            "person_unit": "people",
        },

        "zh": {
            "header": "🏠 首页",
            "header_desc": (
                "快速查看用餐管理系统的整体情况。"
            ),

            "overview": "系统概览",

            "total_people": "用餐总人数",
            "active_people": "正常使用",
            "inactive_people": "已停用",

            "people_status": "人员状态",
            "active_desc": (
                "目前有 {} 人正常使用，"
                "总人数为 {} 人。"
            ),
            "activity_rate": "活跃率：{:.1f}%",

            "main_functions": "主要功能",

            "attendance": "🍚 用餐记录",
            "attendance_desc": (
                "管理用餐人员、用餐登记、"
                "餐费以及每日应付金额。"
            ),

            "people_management": "👩‍🍳 人员管理",
            "people_management_desc": (
                "添加、编辑、搜索、"
                "停用或重新启用人员。"
            ),

            "payment": "💰 缴费与欠款",
            "payment_desc": (
                "查看已缴费用、应付金额 "
                "以及每个人的欠款情况。"
            ),

            "statistics": "📊 统计与报告",
            "statistics_desc": (
                "按时间查看数据 "
                "并生成管理报告。"
            ),

            "smart_assistant": "智能助手",
            "assistant_title": "🤖 Dâu Tây",
            "assistant_desc": (
                "AI 助手可以通过自然语言 "
                "查询系统信息和数据。"
            ),
            "assistant_tip": (
                "💡 可以使用屏幕角落的机器人 "
                "向助手提问。"
            ),

            "process": "使用流程",

            "step1": "① 👩‍🍳 人员管理",
            "step1_desc": (
                "添加并管理 "
                "用餐人员名单。"
            ),

            "step2": "② 🍚 用餐记录",
            "step2_desc": (
                "记录用餐人员 "
                "以及应付金额。"
            ),

            "step3": "③ 📊 数据查看",
            "step3_desc": (
                "查看欠款、"
                "统计数据和报告。"
            ),

            "data_error": (
                "⚠️ 无法获取人员数据。"
            ),

            "inactive_card": "⚪ 已停用",
            "person_unit": "人",
        }
    }

    text = texts.get(
        language,
        texts["vi"]
    )

    hien_thi_header(
        text["header"],
        text["header_desc"]
    )

    _hien_thi_thoi_gian()

    result = (
        NguoiAnController.lay_danh_sach()
    )

    if result["success"]:

        danh_sach = result["data"]

        tong_nguoi = len(
            danh_sach
        )

        dang_hoat_dong = sum(
            1
            for nguoi in danh_sach
            if nguoi[3] == 1
        )

        da_ngung = sum(
            1
            for nguoi in danh_sach
            if nguoi[3] == 0
        )

    else:

        tong_nguoi = 0
        dang_hoat_dong = 0
        da_ngung = 0

        st.warning(
            text["data_error"]
        )

    hien_thi_tieu_de_section(
        text["overview"],
        "📊"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        hien_thi_the(
            text["total_people"],
            tong_nguoi,
            "👥"
        )

    with col2:
        hien_thi_the(
            text["active_people"],
            dang_hoat_dong,
            "🟢"
        )

    with col3:
        hien_thi_the(
            text["inactive_people"],
            da_ngung,
            "⚪"
        )

    st.markdown("")

    hien_thi_tieu_de_section(
        text["people_status"],
        "👥"
    )

    if tong_nguoi > 0:
        ty_le_hoat_dong = (
            dang_hoat_dong
            / tong_nguoi
            * 100
        )
    else:
        ty_le_hoat_dong = 0

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        hien_thi_info_card(
            "🟢 " + text["active_people"],
            text["active_desc"].format(
                dang_hoat_dong,
                tong_nguoi
            )
        )

        st.progress(
            ty_le_hoat_dong / 100,
            text=text["activity_rate"].format(
                ty_le_hoat_dong
            )
        )

    with col2:

        hien_thi_info_card(
            text["inactive_card"],
            f"{da_ngung} "
            f"{text['person_unit']}"
        )

    st.markdown("")

    hien_thi_tieu_de_section(
        text["main_functions"],
        "✨"
    )

    col1, col2 = st.columns(2)

    with col1:

        hien_thi_info_card(
            text["attendance"],
            text["attendance_desc"]
        )

    with col2:

        hien_thi_info_card(
            text["people_management"],
            text["people_management_desc"]
        )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        hien_thi_info_card(
            text["payment"],
            text["payment_desc"]
        )

    with col2:

        hien_thi_info_card(
            text["statistics"],
            text["statistics_desc"]
        )

    st.markdown("")

    hien_thi_tieu_de_section(
        text["smart_assistant"],
        "🤖"
    )

    with st.container(border=True):

        st.markdown(
            f"### {text['assistant_title']}"
        )

        st.write(
            text["assistant_desc"]
        )

        st.info(
            text["assistant_tip"]
        )

    st.markdown("")

    hien_thi_tieu_de_section(
        text["process"],
        "📌"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        hien_thi_info_card(
            text["step1"],
            text["step1_desc"]
        )

    with col2:

        hien_thi_info_card(
            text["step2"],
            text["step2_desc"]
        )

    with col3:

        hien_thi_info_card(
            text["step3"],
            text["step3_desc"]
        )