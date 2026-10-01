# -*- coding: utf-8 -*-

import streamlit as st
from datetime import datetime, date

from Views.layout import (
    hien_thi_header,
    hien_thi_tieu_de_section
)
from Controllers.nguoi_an_controller import NguoiAnController
from Controllers.ngay_an_controller import NgayAnController
from Controllers.chi_tiet_an_controller import ChiTietAnController
from Controllers.suat_an_phat_sinh_controller import SuatAnPhatSinhController
from Controllers.nop_tien_controller import NopTienController
from Database.database import get_connection
from Views.menu_view import chuyen_trang

def _chuyen_trang(menu_key):
    chuyen_trang(menu_key)


def _money(value):
    try:
        return f"{float(value or 0):,.0f} đ"
    except (TypeError, ValueError):
        return "0 đ"


def _safe_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _lay_thong_ke_nguoi():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                COUNT(*) AS TongNguoi,
                COALESCE(
                    SUM(
                        CASE
                            WHEN DangHoatDong = 1
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS DangHoatDong
            FROM NguoiAn
            """
        )

        row = cursor.fetchone()

        tong_nguoi = int(row[0] or 0) if row else 0
        dang_hoat_dong = int(row[1] or 0) if row else 0

        return {
            "tong_nguoi": tong_nguoi,
            "dang_hoat_dong": dang_hoat_dong,
            "da_ngung": max(
                tong_nguoi - dang_hoat_dong,
                0
            )
        }

    except Exception:
        return {
            "tong_nguoi": 0,
            "dang_hoat_dong": 0,
            "da_ngung": 0
        }

    finally:
        connection.close()


@st.fragment(run_every="1s")
def _hien_thi_thoi_gian():
    language = st.session_state.get("language", "vi")

    texts = {
        "vi": {
            "today": "📅 Hôm nay",
            "system_running": "🟢 Hệ thống hoạt động"
        },
        "en": {
            "today": "📅 Today",
            "system_running": "🟢 System is running"
        },
        "zh": {
            "today": "📅 今天",
            "system_running": "🟢 系统运行正常"
        }
    }

    text = texts.get(language, texts["vi"])
    now = datetime.now()

    ngay_hien_tai = now.strftime("%d/%m/%Y")
    gio_hien_tai = now.strftime("%H:%M:%S")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.info(
            f"{text['today']}: **{ngay_hien_tai}**  •  "
            f"🕐 **{gio_hien_tai}**"
        )

    with col2:
        st.success(text["system_running"])


def _lay_du_lieu_hom_nay(ngay_chon, danh_sach):
    ngay_str = ngay_chon.isoformat()

    result_ngay = NgayAnController.tim_theo_ngay(ngay_str)

    if not isinstance(result_ngay, dict):
        return {
            "ngay_an_id": None,
            "registered": 0,
            "eaten": 0,
            "not_eaten": 0,
            "employee_due": 0,
            "guest_count": 0,
            "guest_due": 0,
            "guest_rows": [],
            "error": None
        }

    if not result_ngay.get("success", False):
        return {
            "ngay_an_id": None,
            "registered": 0,
            "eaten": 0,
            "not_eaten": 0,
            "employee_due": 0,
            "guest_count": 0,
            "guest_due": 0,
            "guest_rows": [],
            "error": result_ngay.get(
                "message",
                "Không thể lấy thông tin ngày ăn."
            )
        }

    ngay_an = result_ngay.get("data")

    if not ngay_an:
        return {
            "ngay_an_id": None,
            "registered": 0,
            "eaten": 0,
            "not_eaten": 0,
            "employee_due": 0,
            "guest_count": 0,
            "guest_due": 0,
            "guest_rows": [],
            "error": None
        }

    ngay_an_id = ngay_an[0]

    result_cham = ChiTietAnController.lay_theo_ngay(ngay_an_id)

    rows = []
    if isinstance(result_cham, dict) and result_cham.get("success"):
        rows = result_cham.get("data", []) or []

    registered = len(rows)
    eaten = sum(
        1
        for row in rows
        if len(row) > 5 and bool(row[5])
    )
    not_eaten = max(registered - eaten, 0)

    employee_due = sum(
        _safe_float(row[6])
        for row in rows
        if len(row) > 6 and bool(row[5])
    )

    guest_rows = []
    try:
        guest_rows = (
            SuatAnPhatSinhController
            .lay_theo_ngay(ngay_an_id)
            or []
        )
    except Exception:
        guest_rows = []

    guest_count = sum(
        int(row[4] or 0)
        for row in guest_rows
        if len(row) > 4
    )

    guest_due = sum(
        _safe_float(row[4]) * _safe_float(row[5])
        for row in guest_rows
        if len(row) > 5
    )

    return {
        "ngay_an_id": ngay_an_id,
        "registered": registered,
        "eaten": eaten,
        "not_eaten": not_eaten,
        "employee_due": employee_due,
        "guest_count": guest_count,
        "guest_due": guest_due,
        "guest_rows": guest_rows,
        "error": None
    }


def _lay_du_lieu_cong_no(danh_sach):
    debt_people = 0
    enough_people = 0
    overpaid_people = 0

    total_due = 0.0
    total_paid = 0.0
    total_debt = 0.0
    total_overpaid = 0.0

    for person in danh_sach:
        try:
            if isinstance(person, dict):
                nguoi_id = person.get(
                    "Id",
                    person.get("id")
                )
            else:
                nguoi_id = person[0]

            if nguoi_id is None:
                continue

            result = NopTienController.tinh_so_du(
                nguoi_id
            )

            if not isinstance(result, dict):
                continue

            if not result.get("success", False):
                continue

            due = _safe_float(
                result.get("tong_phai_tra", 0)
            )

            paid = _safe_float(
                result.get("tong_da_nop", 0)
            )

            closing = _safe_float(
                result.get("data", 0)
            )

            total_due += due
            total_paid += paid

            if closing < -0.01:
                debt_people += 1
                total_debt += abs(closing)

            elif closing > 0.01:
                overpaid_people += 1
                total_overpaid += closing

            else:
                enough_people += 1

        except Exception:
            continue

    return {
        "debt_people": debt_people,
        "enough_people": enough_people,
        "overpaid_people": overpaid_people,
        "total_due": total_due,
        "total_paid": total_paid,
        "total_debt": total_debt,
        "total_overpaid": total_overpaid
    }


def hien_thi_trang_chu():
    language = st.session_state.get("language", "vi")

    texts = {
        "vi": {
            "header": "🏠 Trang chủ",
            "header_desc": "Tổng quan nhanh về tình hình chấm cơm và công nợ.",
            "overview": "Tổng quan hôm nay",
            "people": "Người ăn",
            "meals": "Suất ăn",
            "meal_money": "Tiền cơm",
            "need_action": "Cần xử lý",
            "registered": "Đã đăng ký",
            "eaten": "Đã ăn",
            "not_eaten": "Không ăn",
            "guest": "Suất phát sinh",
            "today_status": "Tình hình chấm cơm hôm nay",
            "today_note": "Dữ liệu được lấy trực tiếp từ ngày ăn đang chọn.",
            "debt": "Công nợ",
            "debt_people": "Người còn nợ",
            "enough_people": "Đã đủ",
            "overpaid_people": "Nộp thừa",
            "debt_total": "Tổng còn nợ",
            "overpaid_total": "Tổng nộp thừa",
            "issues": "Cần xử lý",
            "issue_debt": "{} người đang còn công nợ.",
            "issue_guest": "{} suất phát sinh trong ngày.",
            "issue_none": "✅ Hiện không có vấn đề nổi bật cần xử lý.",
            "quick": "Thao tác nhanh",
            "quick_attendance": "🍚 Chấm cơm hôm nay",
            "quick_people": "👥 Quản lý người ăn",
            "quick_payment": "💰 Nộp tiền & công nợ",
            "quick_report": "📑 Xuất báo cáo",
            "date_label": "Ngày xem tổng quan",
            "data_error": "Không thể lấy dữ liệu chấm cơm hôm nay.",
            "no_day": "Ngày này chưa được tạo dữ liệu chấm cơm.",
            "active": "Đang hoạt động",
            "inactive": "Đã ngừng",
            "people_total": "Tổng người ăn",
            "system_note": "Trang chủ chỉ hiển thị tổng quan; dữ liệu chi tiết nằm ở từng chức năng."
        },
        "en": {
            "header": "🏠 Home",
            "header_desc": "Quick overview of meal attendance and payment status.",
            "overview": "Today's Overview",
            "people": "People",
            "meals": "Meals",
            "meal_money": "Meal amount",
            "need_action": "Needs attention",
            "registered": "Registered",
            "eaten": "Eaten",
            "not_eaten": "Not eaten",
            "guest": "Extra meals",
            "today_status": "Today's meal attendance",
            "today_note": "Data is loaded directly from the selected meal date.",
            "debt": "Payments & Debts",
            "debt_people": "People in debt",
            "enough_people": "Paid enough",
            "overpaid_people": "Overpaid",
            "debt_total": "Total debt",
            "overpaid_total": "Total overpaid",
            "issues": "Needs attention",
            "issue_debt": "{} people have outstanding debt.",
            "issue_guest": "{} extra meals recorded today.",
            "issue_none": "✅ No major issue needs attention.",
            "quick": "Quick actions",
            "quick_attendance": "🍚 Meal attendance",
            "quick_people": "👥 People management",
            "quick_payment": "💰 Payments & debts",
            "quick_report": "📑 Export report",
            "date_label": "Overview date",
            "data_error": "Unable to load today's meal data.",
            "no_day": "No meal record has been created for this date.",
            "active": "Active",
            "inactive": "Inactive",
            "people_total": "Total people",
            "system_note": "The home page shows summaries; detailed data remains in each function."
        },
        "zh": {
            "header": "🏠 首页",
            "header_desc": "快速查看用餐记录和缴费情况。",
            "overview": "今日概览",
            "people": "用餐人员",
            "meals": "用餐份数",
            "meal_money": "餐费",
            "need_action": "待处理",
            "registered": "已登记",
            "eaten": "已用餐",
            "not_eaten": "未用餐",
            "guest": "临时餐",
            "today_status": "今日用餐情况",
            "today_note": "数据来自所选用餐日期。",
            "debt": "缴费与欠款",
            "debt_people": "欠款人数",
            "enough_people": "已缴清",
            "overpaid_people": "多缴",
            "debt_total": "欠款总额",
            "overpaid_total": "多缴总额",
            "issues": "待处理",
            "issue_debt": "{} 人存在欠款。",
            "issue_guest": "今日有 {} 份临时餐。",
            "issue_none": "✅ 目前没有明显需要处理的问题。",
            "quick": "快捷操作",
            "quick_attendance": "🍚 用餐记录",
            "quick_people": "👥 人员管理",
            "quick_payment": "💰 缴费与欠款",
            "quick_report": "📑 导出报告",
            "date_label": "概览日期",
            "data_error": "无法获取今日用餐数据。",
            "no_day": "该日期尚未建立用餐记录。",
            "active": "正常使用",
            "inactive": "已停用",
            "people_total": "用餐总人数",
            "system_note": "首页只显示概览，详细数据保留在各个功能页面。"
        }
    }

    text = texts.get(language, texts["vi"])

    hien_thi_header(
        text["header"],
        text["header_desc"]
    )

    _hien_thi_thoi_gian()

    result_people = NguoiAnController.lay_danh_sach()

    if isinstance(result_people, dict) and result_people.get("success"):
        danh_sach = result_people.get("data", []) or []
    else:
        danh_sach = []
        st.warning(
            "⚠️ "
            + (
                result_people.get("message", "Không thể lấy dữ liệu người ăn.")
                if isinstance(result_people, dict)
                else "Không thể lấy dữ liệu người ăn."
            )
        )

    thong_ke_nguoi = _lay_thong_ke_nguoi()

    tong_nguoi = thong_ke_nguoi["tong_nguoi"]
    dang_hoat_dong = thong_ke_nguoi["dang_hoat_dong"]
    da_ngung = thong_ke_nguoi["da_ngung"]

    ngay_xem = st.date_input(
        text["date_label"],
        value=date.today(),
        format="DD/MM/YYYY",
        key="home_overview_date"
    )

    today_data = _lay_du_lieu_hom_nay(
        ngay_xem,
        danh_sach
    )

    debt_data = _lay_du_lieu_cong_no(danh_sach)

    if today_data["error"]:
        st.warning(today_data["error"])

    total_meal_money = (
        today_data["employee_due"]
        + today_data["guest_due"]
    )

    action_count = (
        debt_data["debt_people"]
        + (1 if today_data["guest_count"] > 0 else 0)
    )

    hien_thi_tieu_de_section(
        text["overview"],
        "📊"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            f"👥 {text['people']}",
            tong_nguoi,
            f"{dang_hoat_dong} {text['active']}"
        )

    with c2:
        st.metric(
            f"🍚 {text['meals']}",
            today_data["eaten"],
            f"{today_data['registered']} {text['registered']}"
        )

    with c3:
        st.metric(
            f"💰 {text['meal_money']}",
            _money(total_meal_money),
            f"{today_data['guest_count']} {text['guest']}"
        )

    with c4:
        st.metric(
            f"⚠️ {text['need_action']}",
            action_count,
            f"{debt_data['debt_people']} {text['debt_people']}"
        )

    st.markdown("")

    left, right = st.columns([1.45, 1])

    with left:
        hien_thi_tieu_de_section(
            text["today_status"],
            "🍚"
        )

        st.caption(text["today_note"])

        if today_data["ngay_an_id"] is None:
            st.info(text["no_day"])
        else:
            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    text["registered"],
                    today_data["registered"]
                )

            with m2:
                st.metric(
                    text["eaten"],
                    today_data["eaten"]
                )

            with m3:
                st.metric(
                    text["not_eaten"],
                    today_data["not_eaten"]
                )

            st.progress(
                (
                    today_data["eaten"]
                    / today_data["registered"]
                )
                if today_data["registered"] > 0
                else 0
            )

            st.caption(
                f"💰 Nhân viên: **{_money(today_data['employee_due'])}**  •  "
                f"🍽️ Phát sinh: **{_money(today_data['guest_due'])}**"
            )

    with right:
        hien_thi_tieu_de_section(
            text["debt"],
            "💰"
        )

        d1, d2 = st.columns(2)

        with d1:
            st.metric(
                text["debt_people"],
                debt_data["debt_people"]
            )
            st.metric(
                text["debt_total"],
                _money(debt_data["total_debt"])
            )

        with d2:
            st.metric(
                text["overpaid_people"],
                debt_data["overpaid_people"]
            )
            st.metric(
                text["overpaid_total"],
                _money(debt_data["total_overpaid"])
            )

        st.caption(
            f"Đã đủ: **{debt_data['enough_people']} người**"
        )

    st.markdown("")

    issue_col, people_col = st.columns([1.2, 1])

    with issue_col:
        hien_thi_tieu_de_section(
            text["issues"],
            "⚠️"
        )

        if debt_data["debt_people"] > 0:
            st.warning(
                "• " + text["issue_debt"].format(
                    debt_data["debt_people"]
                )
            )

        if today_data["guest_count"] > 0:
            st.info(
                "• " + text["issue_guest"].format(
                    today_data["guest_count"]
                )
            )

        if (
            debt_data["debt_people"] == 0
            and today_data["guest_count"] == 0
        ):
            st.success(text["issue_none"])

    with people_col:
        hien_thi_tieu_de_section(
            text["people_total"],
            "👥"
        )

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                text["people"],
                tong_nguoi
            )

        with p2:
            st.metric(
                text["active"],
                dang_hoat_dong
            )

        with p3:
            st.metric(
                text["inactive"],
                da_ngung
            )

    st.markdown("")

    hien_thi_tieu_de_section(
        text["quick"],
        "⚡"
    )

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button(
            text["quick_attendance"],
            width="stretch",
            key="home_quick_attendance"
        ):
            _chuyen_trang(
                "🍚 Chấm cơm hôm nay"
            )

    with q2:
        if st.button(
            text["quick_people"],
            width="stretch",
            key="home_quick_people"
        ):
            _chuyen_trang(
                "👩‍🍳 Quản lý người ăn"
            )

    with q3:
        if st.button(
            text["quick_payment"],
            width="stretch",
            key="home_quick_payment"
        ):
            _chuyen_trang(
                "💰 Nộp tiền & công nợ"
            )

    with q4:
        if st.button(
            text["quick_report"],
            width="stretch",
            key="home_quick_report"
        ):
            _chuyen_trang(
                "📑 Xuất báo cáo"
            )

    st.caption(text["system_note"])
