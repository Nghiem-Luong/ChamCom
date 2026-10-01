import streamlit as st
from Utils.language import t


# ==========================================================
# DANH SÁCH MENU
# ==========================================================

MENU_ITEMS = {
    "🏠 Trang chủ": "home",
    "🍚 Chấm cơm hôm nay": "attendance",
    "👩‍🍳 Quản lý người ăn": "people",
    "🏢 Quản lý bộ phận": "department",
    "💰 Nộp tiền & công nợ": "payment",
    "📊 Thống kê": "statistics",
    "📑 Xuất báo cáo": "report",
    "⚙️ Hệ thống": "system",
}


# ==========================================================
# CHUYỂN TRANG
# ==========================================================

def chuyen_trang(menu_key):

    if menu_key not in MENU_ITEMS:
        return

    st.session_state["menu_current"] = menu_key

    if "menu_display" in st.session_state:
        del st.session_state["menu_display"]

    st.rerun()


# ==========================================================
# LẤY TRANG HIỆN TẠI
# ==========================================================

def lay_trang_hien_tai():

    return st.session_state.get(
        "menu_current",
        "🏠 Trang chủ"
    )


# ==========================================================
# HIỂN THỊ MENU
# ==========================================================

def hien_thi_menu():

    ngon_ngu_map = {
        "🇻🇳 Tiếng Việt": "vi",
        "🇬🇧 English": "en",
        "🇨🇳 中文": "zh",
    }

    # ======================================================
    # KHỞI TẠO NGÔN NGỮ
    # ======================================================

    if "language" not in st.session_state:
        st.session_state.language = "vi"

    language = st.session_state.language

    # ======================================================
    # CSS SIDEBAR
    # ======================================================

    st.markdown(
        """
        <style>

        section[data-testid="stSidebar"] {

            background: linear-gradient(
                180deg,
                #fffafd 0%,
                #faf7ff 55%,
                #f7fbff 100%
            );

            border-right: 1px solid #eee5ed;
        }


        section[data-testid="stSidebar"] .block-container {

            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }


        div[role="radiogroup"] {

            gap: 5px;
        }


        div[role="radiogroup"] label {

            border-radius: 12px;
            padding: 7px 9px;
        }


        div[role="radiogroup"] label:hover {

            background-color: #f4edf5;
        }


        div[data-baseweb="select"] {

            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ======================================================
    # HEADER SIDEBAR
    # ======================================================

    st.sidebar.markdown(
        "## 🍚 QUẢN LÝ CHẤM CƠM"
    )

    if language == "en":

        st.sidebar.caption(
            "Meal tracking & payment management"
        )

    elif language == "zh":

        st.sidebar.caption(
            "用餐记录与费用管理"
        )

    else:

        st.sidebar.caption(
            "Quản lý ăn uống & công nợ"
        )

    st.sidebar.divider()

    # ======================================================
    # NGÔN NGỮ
    # ======================================================

    st.sidebar.markdown(
        f"**🌐 {t('language', language)}**"
    )

    lua_chon_ngon_ngu = st.sidebar.selectbox(
        "language_selector",
        list(ngon_ngu_map.keys()),
        index=list(ngon_ngu_map.values()).index(
            language
        ),
        label_visibility="collapsed",
        key="language_selector"
    )

    ngon_ngu_moi = ngon_ngu_map[
        lua_chon_ngon_ngu
    ]

    if ngon_ngu_moi != language:

        st.session_state.language = ngon_ngu_moi

        st.rerun()

    language = st.session_state.language

    # ======================================================
    # TIÊU ĐỀ MENU
    # ======================================================

    if language == "en":

        function_title = "FUNCTIONS"
        go_to = "Go to"

    elif language == "zh":

        function_title = "功能"
        go_to = "前往"

    else:

        function_title = "CHỨC NĂNG"
        go_to = "Đi tới"

    st.sidebar.markdown(
        f"### 📌 {function_title}"
    )

    # ======================================================
    # MENU HIỂN THỊ
    # ======================================================

    menu_items = {

        "🏠 Trang chủ":
            f"🏠 {t('home', language)}",

        "🍚 Chấm cơm hôm nay":
            f"🍚 {t('attendance', language)}",

        "👩‍🍳 Quản lý người ăn":
            f"👩‍🍳 {t('people', language)}",

        "🏢 Quản lý bộ phận":
            (
                "🏢 Department Management"
                if language == "en"

                else
                "🏢 部门管理"
                if language == "zh"

                else
                "🏢 Quản lý bộ phận"
            ),

        "💰 Nộp tiền & công nợ":
            f"💰 {t('payment', language)}",

        "📊 Thống kê":
            f"📊 {t('statistics', language)}",

        "📑 Xuất báo cáo":
            f"📑 {t('report', language)}",

        "⚙️ Hệ thống":
            f"⚙️ {t('system', language)}",
    }

    # ======================================================
    # DANH SÁCH MENU
    # ======================================================

    danh_sach_noi_bo = list(
        menu_items.keys()
    )

    danh_sach_hien_thi = list(
        menu_items.values()
    )

    # ======================================================
    # KHỞI TẠO TRANG HIỆN TẠI
    # ======================================================

    if "menu_current" not in st.session_state:

        st.session_state[
            "menu_current"
        ] = danh_sach_noi_bo[0]

    # ======================================================
    # KIỂM TRA TRANG HIỆN TẠI
    # ======================================================

    if (
        st.session_state["menu_current"]
        not in danh_sach_noi_bo
    ):

        st.session_state[
            "menu_current"
        ] = danh_sach_noi_bo[0]

    # ======================================================
    # XÁC ĐỊNH MENU ĐANG CHỌN
    # ======================================================

    current_display = menu_items[
        st.session_state["menu_current"]
    ]

    # ======================================================
    # HIỂN THỊ RADIO MENU
    # ======================================================

    lua_chon_hien_thi = st.sidebar.radio(

        go_to,

        danh_sach_hien_thi,

        index=danh_sach_hien_thi.index(
            current_display
        ),

        label_visibility="collapsed",

        key="menu_display"
    )

    # ======================================================
    # CHUYỂN TỪ TÊN HIỂN THỊ → KEY NỘI BỘ
    # ======================================================

    lua_chon = danh_sach_noi_bo[
        danh_sach_hien_thi.index(
            lua_chon_hien_thi
        )
    ]

    # ======================================================
    # CẬP NHẬT TRANG
    # ======================================================

    if (
        lua_chon
        != st.session_state["menu_current"]
    ):

        st.session_state[
            "menu_current"
        ] = lua_chon

        st.rerun()

    # ======================================================
    # FOOTER SIDEBAR
    # ======================================================

    st.sidebar.divider()

    if language == "en":

        version_text = "Version 3.0.0"
        status_text = "System is running"

    elif language == "zh":

        version_text = "版本 3.0.0"
        status_text = "系统运行正常"

    else:

        version_text = "Phiên bản 3.0.0"
        status_text = "Hệ thống đang hoạt động"

    st.sidebar.caption(
        "🍚 Quản lý Chấm Cơm"
    )

    st.sidebar.caption(
        version_text
    )

    st.sidebar.success(
        f"✓ {status_text}"
    )

    return st.session_state[
        "menu_current"
    ]