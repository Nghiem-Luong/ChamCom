import streamlit as st
from datetime import date, timedelta

from Controllers.thong_ke_controller import ThongKeController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)


def hien_thi_thong_ke():

    # ==========================================================
    # NGÔN NGỮ
    # ==========================================================

    language = st.session_state.get("language", "vi")

    texts = {
        "vi": {
            "header": "📊 Thống kê",
            "header_desc": (
                "Theo dõi tình hình ăn uống và chi phí theo thời gian."
            ),

            "period": "Khoảng thời gian thống kê",
            "stat_type": "Kiểu thống kê",

            "today": "Hôm nay",
            "last_7_days": "7 ngày gần nhất",
            "this_month": "Tháng này",
            "custom": "Tùy chọn",

            "from_date": "Từ ngày",
            "to_date": "Đến ngày",

            "date_error": (
                "⚠️ Ngày bắt đầu không được lớn hơn ngày kết thúc."
            ),

            "statistics_from": "📌 Đang thống kê từ",
            "to": "đến",

            "overview": "Tổng quan",
            "days": "Số ngày",
            "total_meals": "Tổng lượt ăn",
            "total_money": "Tổng tiền",
            "average_per_meal": "Trung bình / lượt",

            "daily_statistics": "Thống kê từng ngày",
            "no_data_period": (
                "🌷 Chưa có dữ liệu trong khoảng thời gian này."
            ),

            "date": "Ngày",
            "people_eating": "Số người ăn",
            "total_money_column": "Tổng tiền",

            "charts": "Biểu đồ theo ngày",
            "people_chart": "#### 👥 Số người ăn theo ngày",
            "money_chart": "#### 💰 Tổng tiền theo ngày",

            "by_person": "Thống kê theo người",
            "name": "Họ tên",
            "meal_count": "Số lần ăn",
            "no_person_data": (
                "🌷 Chưa có dữ liệu theo người."
            ),
        },

        "en": {
            "header": "📊 Statistics",
            "header_desc": (
                "Track meal activity and costs over time."
            ),

            "period": "Statistics Period",
            "stat_type": "Statistics Type",

            "today": "Today",
            "last_7_days": "Last 7 days",
            "this_month": "This month",
            "custom": "Custom",

            "from_date": "From date",
            "to_date": "To date",

            "date_error": (
                "⚠️ The start date cannot be later than the end date."
            ),

            "statistics_from": "📌 Statistics from",
            "to": "to",

            "overview": "Overview",
            "days": "Number of days",
            "total_meals": "Total meals",
            "total_money": "Total amount",
            "average_per_meal": "Average / meal",

            "daily_statistics": "Daily Statistics",
            "no_data_period": (
                "🌷 No data available for this period."
            ),

            "date": "Date",
            "people_eating": "People eating",
            "total_money_column": "Total amount",

            "charts": "Daily Charts",
            "people_chart": "#### 👥 People eating per day",
            "money_chart": "#### 💰 Total amount per day",

            "by_person": "Statistics by Person",
            "name": "Name",
            "meal_count": "Number of meals",
            "no_person_data": (
                "🌷 No data available by person."
            ),
        },

        "zh": {
            "header": "📊 统计",
            "header_desc": (
                "按时间查看用餐情况和费用。"
            ),

            "period": "统计时间范围",
            "stat_type": "统计类型",

            "today": "今天",
            "last_7_days": "最近7天",
            "this_month": "本月",
            "custom": "自定义",

            "from_date": "开始日期",
            "to_date": "结束日期",

            "date_error": (
                "⚠️ 开始日期不能晚于结束日期。"
            ),

            "statistics_from": "📌 统计时间",
            "to": "至",

            "overview": "概览",
            "days": "天数",
            "total_meals": "用餐总次数",
            "total_money": "总金额",
            "average_per_meal": "平均 / 次",

            "daily_statistics": "每日统计",
            "no_data_period": (
                "🌷 此时间范围内暂无数据。"
            ),

            "date": "日期",
            "people_eating": "用餐人数",
            "total_money_column": "总金额",

            "charts": "每日图表",
            "people_chart": "#### 👥 每日用餐人数",
            "money_chart": "#### 💰 每日总金额",

            "by_person": "按人员统计",
            "name": "姓名",
            "meal_count": "用餐次数",
            "no_person_data": (
                "🌷 暂无人员统计数据。"
            ),
        }
    }

    text = texts.get(language, texts["vi"])

    # ==========================================================
    # 1. HEADER
    # ==========================================================

    hien_thi_header(
        text["header"],
        text["header_desc"]
    )

    # ==========================================================
    # 2. CHỌN KHOẢNG THỜI GIAN
    # ==========================================================

    hien_thi_tieu_de_section(
        text["period"],
        "📅"
    )

    with st.container(border=True):

        che_do = st.selectbox(
            text["stat_type"],
            [
                text["today"],
                text["last_7_days"],
                text["this_month"],
                text["custom"]
            ]
        )

        hom_nay = date.today()

        if che_do == text["today"]:

            tu_ngay = hom_nay
            den_ngay = hom_nay

        elif che_do == text["last_7_days"]:

            tu_ngay = hom_nay - timedelta(days=6)
            den_ngay = hom_nay

        elif che_do == text["this_month"]:

            tu_ngay = hom_nay.replace(day=1)
            den_ngay = hom_nay

        else:

            col1, col2 = st.columns(2)

            with col1:

                tu_ngay = st.date_input(
                    text["from_date"],
                    value=hom_nay.replace(day=1),
                    format="DD/MM/YYYY"
                )

            with col2:

                den_ngay = st.date_input(
                    text["to_date"],
                    value=hom_nay,
                    format="DD/MM/YYYY"
                )

        if tu_ngay > den_ngay:

            st.error(
                text["date_error"]
            )

            return

    tu_ngay_str = tu_ngay.strftime(
        "%Y-%m-%d"
    )

    den_ngay_str = den_ngay.strftime(
        "%Y-%m-%d"
    )

    st.caption(
        f"{text['statistics_from']} "
        f"**{tu_ngay.strftime('%d/%m/%Y')}** "
        f"{text['to']} "
        f"**{den_ngay.strftime('%d/%m/%Y')}**"
    )

    # ==========================================================
    # 3. LẤY THỐNG KÊ TỔNG QUAN
    # ==========================================================

    result = (
        ThongKeController.thong_ke_theo_khoang_ngay(
            tu_ngay_str,
            den_ngay_str
        )
    )

    if not result["success"]:

        st.error(
            result["message"]
        )

        return

    data = result["data"]

    # ==========================================================
    # 4. TỔNG QUAN
    # ==========================================================

    hien_thi_tieu_de_section(
        text["overview"],
        "📌"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        hien_thi_the(
            text["days"],
            data["so_ngay"],
            "📅"
        )

    with col2:

        hien_thi_the(
            text["total_meals"],
            data["tong_luot_an"],
            "👥"
        )

    with col3:

        hien_thi_the(
            text["total_money"],
            f"{data['tong_tien']:,.0f} đ",
            "💰"
        )

    with col4:

        hien_thi_the(
            text["average_per_meal"],
            f"{data['trung_binh']:,.0f} đ",
            "📌"
        )

    st.markdown("")

    # ==========================================================
    # 5. THỐNG KÊ TỪNG NGÀY
    # ==========================================================

    hien_thi_tieu_de_section(
        text["daily_statistics"],
        "📈"
    )

    result_ngay = (
        ThongKeController.thong_ke_tung_ngay(
            tu_ngay_str,
            den_ngay_str
        )
    )

    if not result_ngay["success"]:

        st.error(
            result_ngay["message"]
        )

    else:

        du_lieu_ngay = result_ngay["data"]

        if not du_lieu_ngay:

            st.info(
                text["no_data_period"]
            )

        else:

            bang_ngay = []

            for row in du_lieu_ngay:

                ngay = row[0]
                so_nguoi = row[1]
                tong_tien = row[2]

                bang_ngay.append({
                    text["date"]: ngay,
                    text["people_eating"]: so_nguoi,
                    text["total_money_column"]: tong_tien
                })

            st.dataframe(
                bang_ngay,
                width="stretch",
                hide_index=True,
                column_config={
                    text["total_money_column"]:
                        st.column_config.NumberColumn(
                            text["total_money_column"],
                            format="%,.0f đ"
                        )
                }
            )

    # ==========================================================
    # 6. BIỂU ĐỒ
    # ==========================================================

    if (
        result_ngay["success"]
        and result_ngay["data"]
    ):

        hien_thi_tieu_de_section(
            text["charts"],
            "📊"
        )

        # ------------------------------------------------------
        # BIỂU ĐỒ SỐ NGƯỜI ĂN
        # ------------------------------------------------------

        st.markdown(
            text["people_chart"]
        )

        du_lieu_bieu_do = {
            text["date"]: [],
            text["people_eating"]: []
        }

        for row in result_ngay["data"]:

            du_lieu_bieu_do[
                text["date"]
            ].append(
                row[0]
            )

            du_lieu_bieu_do[
                text["people_eating"]
            ].append(
                row[1]
            )

        st.line_chart(
            du_lieu_bieu_do,
            x=text["date"],
            y=text["people_eating"]
        )

        # ------------------------------------------------------
        # BIỂU ĐỒ TIỀN
        # ------------------------------------------------------

        st.markdown(
            text["money_chart"]
        )

        du_lieu_tien = {
            text["date"]: [],
            text["total_money_column"]: []
        }

        for row in result_ngay["data"]:

            du_lieu_tien[
                text["date"]
            ].append(
                row[0]
            )

            du_lieu_tien[
                text["total_money_column"]
            ].append(
                row[2]
            )

        st.line_chart(
            du_lieu_tien,
            x=text["date"],
            y=text["total_money_column"]
        )

    # ==========================================================
    # 7. THỐNG KÊ THEO NGƯỜI
    # ==========================================================

    hien_thi_tieu_de_section(
        text["by_person"],
        "👩‍🍳"
    )

    result_nguoi = (
        ThongKeController.thong_ke_theo_nguoi(
            tu_ngay_str,
            den_ngay_str
        )
    )

    if not result_nguoi["success"]:

        st.error(
            result_nguoi["message"]
        )

    else:

        du_lieu_nguoi = result_nguoi["data"]

        bang_nguoi = []

        for row in du_lieu_nguoi:

            bang_nguoi.append({
                text["name"]: row[1],
                text["meal_count"]: row[2],
                text["total_money_column"]: row[3]
            })

        if bang_nguoi:

            st.dataframe(
                bang_nguoi,
                width="stretch",
                hide_index=True,
                column_config={
                    text["total_money_column"]:
                        st.column_config.NumberColumn(
                            text["total_money_column"],
                            format="%,.0f đ"
                        )
                }
            )

        else:

            st.info(
                text["no_person_data"]
            )