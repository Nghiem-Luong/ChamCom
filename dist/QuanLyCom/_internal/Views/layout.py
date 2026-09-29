import streamlit as st
import html


# ==========================================================
# CẤU HÌNH GIAO DIỆN CHUNG
# ==========================================================

def cai_dat_giao_dien():

    st.markdown(
        """
        <style>

        /* ==================================================
           TOÀN ỨNG DỤNG
           ================================================== */

        .stApp {
            background:
                linear-gradient(
                    180deg,
                    #fffafb 0%,
                    #f8f9fc 45%,
                    #f5f7fb 100%
                );
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }


        /* ==================================================
           SIDEBAR
           ================================================== */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #fffafd 0%,
                    #faf8fc 55%,
                    #f7f8fc 100%
                );

            border-right: 1px solid #ebe4e9;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.2rem;
        }


        /* ---------- Logo ---------- */

        .qlc-sidebar-brand {
            padding: 22px 16px;

            border-radius: 18px;

            background:
                linear-gradient(
                    145deg,
                    #fff0f5,
                    #f6f1ff
                );

            border: 1px solid #eadde6;

            text-align: center;

            box-shadow:
                0 5px 18px rgba(70, 50, 65, 0.055);
        }

        .qlc-sidebar-logo {
            font-size: 38px;
            line-height: 1;

            margin-bottom: 10px;
        }

        .qlc-sidebar-title {
            color: #493640;

            font-size: 17px;
            font-weight: 800;

            letter-spacing: 0.3px;
        }

        .qlc-sidebar-subtitle {
            margin-top: 5px;

            color: #82747d;

            font-size: 12px;
        }


        /* ---------- Tiêu đề menu ---------- */

        .qlc-sidebar-section {
            margin: 8px 4px 8px 4px;

            color: #756770;

            font-size: 12px;
            font-weight: 750;

            letter-spacing: 0.5px;
        }


        /* ---------- Radio menu ---------- */

        section[data-testid="stSidebar"]
        div[role="radiogroup"] {
            gap: 5px;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"] > label {
            padding: 10px 12px;

            border-radius: 11px;

            transition:
                background 0.15s ease,
                transform 0.15s ease;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"] > label:hover {
            background: #f4edf2;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"]
        > label[data-checked="true"] {
            background:
                linear-gradient(
                    90deg,
                    #f8e8ef,
                    #f3eef9
                );

            border: 1px solid #eadce5;
        }

        section[data-testid="stSidebar"]
        div[role="radiogroup"]
        > label p {
            font-size: 14px;

            font-weight: 600;

            color: #51434b;
        }


        /* ---------- Footer sidebar ---------- */

        .qlc-sidebar-footer {
            padding: 12px 8px;
        }

        .qlc-sidebar-footer-title {
            color: #5d4d56;

            font-size: 13px;
            font-weight: 700;
        }

        .qlc-sidebar-footer-version {
            margin-top: 3px;

            color: #968991;

            font-size: 11px;
        }

        .qlc-sidebar-status {
            display: flex;
            align-items: center;

            gap: 6px;

            margin-top: 9px;

            color: #7c7177;

            font-size: 11px;
        }

        .qlc-status-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #62b77a;

            display: inline-block;
        }


        /* ==================================================
           HEADER TRANG
           ================================================== */

        .qlc-header {
            position: relative;

            overflow: hidden;

            padding: 28px 32px;

            margin-bottom: 24px;

            border-radius: 22px;

            background:
                linear-gradient(
                    135deg,
                    #fff1f5 0%,
                    #f7f2ff 52%,
                    #eef7ff 100%
                );

            border: 1px solid #eadde5;

            box-shadow:
                0 8px 28px rgba(
                    80,
                    55,
                    70,
                    0.07
                );
        }

        .qlc-header::before {
            content: "";

            position: absolute;

            width: 180px;
            height: 180px;

            right: -60px;
            top: -90px;

            border-radius: 50%;

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.55
                );
        }

        .qlc-header-title {
            position: relative;

            margin: 0;

            color: #463640;

            font-size: 30px;

            font-weight: 750;

            letter-spacing: -0.4px;
        }

        .qlc-header-description {
            position: relative;

            margin: 8px 0 0 0;

            color: #766872;

            font-size: 15px;

            line-height: 1.6;
        }


        /* ==================================================
           SECTION TITLE
           ================================================== */

        .qlc-section-title {
            display: flex;

            align-items: center;

            gap: 10px;

            margin-top: 12px;

            margin-bottom: 14px;

            color: #463740;

            font-size: 20px;

            font-weight: 700;
        }


        /* ==================================================
           CARD THỐNG KÊ
           ================================================== */

        .qlc-stat-card {
            min-height: 118px;

            padding: 20px 22px;

            border-radius: 18px;

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.92
                );

            border: 1px solid #ebe4e8;

            box-shadow:
                0 5px 18px rgba(
                    60,
                    45,
                    55,
                    0.055
                );

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        .qlc-stat-card:hover {
            transform: translateY(-2px);

            box-shadow:
                0 8px 22px rgba(
                    60,
                    45,
                    55,
                    0.08
                );
        }

        .qlc-stat-icon {
            font-size: 22px;

            margin-bottom: 8px;
        }

        .qlc-stat-title {
            color: #81747b;

            font-size: 13px;

            font-weight: 600;

            margin-bottom: 5px;
        }

        .qlc-stat-value {
            color: #41343c;

            font-size: 26px;

            font-weight: 750;

            line-height: 1.2;
        }


        /* ==================================================
           INFO CARD
           ================================================== */

        .qlc-info-card {
            padding: 18px 20px;

            border-radius: 16px;

            background: #ffffff;

            border: 1px solid #ebe5e9;

            box-shadow:
                0 4px 15px rgba(
                    60,
                    45,
                    55,
                    0.045
                );
        }

        .qlc-info-title {
            color: #51434b;

            font-size: 15px;

            font-weight: 700;

            margin-bottom: 5px;
        }

        .qlc-info-text {
            color: #81747b;

            font-size: 14px;

            line-height: 1.55;
        }


        /* ==================================================
           BUTTON
           ================================================== */

        .stButton > button {
            min-height: 42px !important;

            border-radius: 11px !important;

            border: 1px solid #e5dce1 !important;

            font-weight: 600 !important;

            transition:
                transform 0.12s ease,
                box-shadow 0.12s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);

            box-shadow:
                0 5px 14px rgba(
                    70,
                    50,
                    65,
                    0.09
                );
        }


        /* ==================================================
           INPUT
           ================================================== */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input,
        .stTextArea textarea {

            border-radius: 11px !important;
        }


        /* ==================================================
           SELECTBOX
           ================================================== */

        div[data-baseweb="select"] > div {
            border-radius: 11px !important;
        }


        /* ==================================================
           EXPANDER
           ================================================== */

        .streamlit-expanderHeader {
            border-radius: 12px !important;

            font-weight: 600 !important;
        }


        /* ==================================================
           DATAFRAME
           ================================================== */

        div[data-testid="stDataFrame"] {
            border-radius: 14px;

            overflow: hidden;

            border: 1px solid #ebe5e9;
        }


        /* ==================================================
           ALERT
           ================================================== */

        div[data-testid="stAlert"] {
            border-radius: 13px;
        }


        /* ==================================================
           METRIC STREAMLIT
           ================================================== */

        div[data-testid="stMetric"] {

            padding: 15px 17px;

            border-radius: 15px;

            background: #ffffff;

            border: 1px solid #ebe5e9;

            box-shadow:
                0 4px 14px rgba(
                    60,
                    45,
                    55,
                    0.04
                );
        }


        /* ==================================================
           DIVIDER
           ================================================== */

        hr {
            border-color: #ebe5e9 !important;
        }


        /* ==================================================
           TAB
           ================================================== */

        button[data-baseweb="tab"] {
            font-weight: 600;
        }


        /* ==================================================
           FOOTER
           ================================================== */

        .qlc-footer {
            margin-top: 35px;

            padding-top: 18px;

            border-top: 1px solid #ebe5e9;

            text-align: center;

            color: #988b92;

            font-size: 13px;
        }


        /* ==================================================
           RESPONSIVE
           ================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .qlc-header {
                padding: 22px;
            }

            .qlc-header-title {
                font-size: 24px;
            }

            .qlc-header-description {
                font-size: 14px;
            }

            .qlc-stat-card {
                min-height: 105px;

                padding: 16px;
            }

            .qlc-stat-value {
                font-size: 22px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# HEADER
# ==========================================================

def hien_thi_header(
    tieu_de,
    mo_ta=None
):

    tieu_de_an_toan = html.escape(
        str(tieu_de)
    )

    html_header = (
        '<div class="qlc-header">'

        '<h1 class="qlc-header-title">'
        f'{tieu_de_an_toan}'
        '</h1>'
    )

    if mo_ta:

        mo_ta_an_toan = html.escape(
            str(mo_ta)
        )

        html_header += (
            '<p class="qlc-header-description">'
            f'{mo_ta_an_toan}'
            '</p>'
        )

    html_header += '</div>'

    st.markdown(
        html_header,
        unsafe_allow_html=True
    )


# ==========================================================
# THẺ THỐNG KÊ
# ==========================================================

def hien_thi_the(
    tieu_de,
    gia_tri,
    bieu_tuong=""
):

    tieu_de_an_toan = html.escape(
        str(tieu_de)
    )

    gia_tri_an_toan = html.escape(
        str(gia_tri)
    )

    bieu_tuong_an_toan = html.escape(
        str(bieu_tuong)
    )

    html_card = (
        '<div class="qlc-stat-card">'

        '<div class="qlc-stat-icon">'
        f'{bieu_tuong_an_toan}'
        '</div>'

        '<div class="qlc-stat-title">'
        f'{tieu_de_an_toan}'
        '</div>'

        '<div class="qlc-stat-value">'
        f'{gia_tri_an_toan}'
        '</div>'

        '</div>'
    )

    st.markdown(
        html_card,
        unsafe_allow_html=True
    )


# ==========================================================
# TIÊU ĐỀ SECTION
# ==========================================================

def hien_thi_tieu_de_section(
    tieu_de,
    bieu_tuong=""
):

    tieu_de_an_toan = html.escape(
        str(tieu_de)
    )

    bieu_tuong_an_toan = html.escape(
        str(bieu_tuong)
    )

    st.markdown(
        (
            '<div class="qlc-section-title">'

            f'<span>{bieu_tuong_an_toan}</span>'

            f'<span>{tieu_de_an_toan}</span>'

            '</div>'
        ),
        unsafe_allow_html=True
    )


# ==========================================================
# INFO CARD
# ==========================================================

def hien_thi_info_card(
    tieu_de,
    noi_dung
):

    tieu_de_an_toan = html.escape(
        str(tieu_de)
    )

    noi_dung_an_toan = html.escape(
        str(noi_dung)
    )

    st.markdown(
        (
            '<div class="qlc-info-card">'

            '<div class="qlc-info-title">'
            f'{tieu_de_an_toan}'
            '</div>'

            '<div class="qlc-info-text">'
            f'{noi_dung_an_toan}'
            '</div>'

            '</div>'
        ),
        unsafe_allow_html=True
    )


# ==========================================================
# FOOTER
# ==========================================================

def hien_thi_footer():

    st.markdown(
        """
        <div class="qlc-footer">

            🍚 Quản Lý Chấm Cơm

            &nbsp;•&nbsp;

            Hệ thống quản lý suất ăn

        </div>
        """,
        unsafe_allow_html=True
    )