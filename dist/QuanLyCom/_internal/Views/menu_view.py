import streamlit as st


def hien_thi_menu():

    # ==========================================================
    # THƯƠNG HIỆU
    # ==========================================================

    st.sidebar.markdown(
        """
        <div style="
            text-align:center;
            padding:18px 12px;
            border-radius:18px;
            background:linear-gradient(145deg,#fff0f5,#f6f1ff);
            border:1px solid #eadde6;
            margin-bottom:18px;
        ">
            <div style="font-size:36px;">🍚</div>
            <div style="
                font-size:17px;
                font-weight:800;
                color:#493640;
                margin-top:7px;
            ">
                QUẢN LÝ CHẤM CƠM
            </div>
            <div style="
                font-size:12px;
                color:#82747d;
                margin-top:5px;
            ">
                Quản lý ăn uống & công nợ
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==========================================================
    # CHỨC NĂNG
    # ==========================================================

    st.sidebar.markdown(
        "### 📌 CHỨC NĂNG"
    )

    lua_chon = st.sidebar.radio(
        "Đi tới",
        [
            "🏠 Trang chủ",
            "🍚 Chấm cơm hôm nay",
            "👩‍🍳 Quản lý người ăn",
            "💰 Nộp tiền & công nợ",
            "📊 Thống kê",
            "📑 Xuất báo cáo",
            "🤖 Trợ lý & hệ thống"
        ],
        label_visibility="collapsed"
    )

    # ==========================================================
    # PHÂN CÁCH
    # ==========================================================

    st.sidebar.divider()

    # ==========================================================
    # TRẠNG THÁI HỆ THỐNG
    # ==========================================================

    st.sidebar.caption(
        "🍚 Quản lý Chấm Cơm"
    )

    st.sidebar.caption(
        "Phiên bản 1.0.0"
    )

    st.sidebar.success(
        "Hệ thống đang hoạt động"
    )

    return lua_chon