# -*- coding: utf-8 -*-

import streamlit as st


# ==========================================================
# CẤU HÌNH GIAO DIỆN CHUNG
# ==========================================================

def cai_dat_giao_dien():

    st.markdown(
        """
        <style>

        /* ==================================================
           ANIMATION
           ================================================== */

        @keyframes qlc_fade_up {
            0% {
                opacity: 0;
                transform: translateY(7px);
            }

            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes qlc_fade_in {
            0% {
                opacity: 0;
            }

            100% {
                opacity: 1;
            }
        }

        @keyframes qlc_soft_scale {
            0% {
                opacity: 0;
                transform: scale(0.99);
            }

            100% {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes qlc_pulse {
            0% {
                box-shadow:
                    0 0 0 0
                    rgba(205, 125, 155, 0.18);
            }

            70% {
                box-shadow:
                    0 0 0 6px
                    rgba(205, 125, 155, 0);
            }

            100% {
                box-shadow:
                    0 0 0 0
                    rgba(205, 125, 155, 0);
            }
        }


        /* ==================================================
           TOÀN ỨNG DỤNG
           ================================================== */

        .stApp {
            background:
                linear-gradient(
                    180deg,
                    #fffafb 0%,
                    #f9fafc 45%,
                    #f5f7fb 100%
                );
        }

        .block-container {
            max-width: 1120px;
            padding-top: 1.25rem;
            padding-bottom: 2rem;

            animation:
                qlc_fade_in
                0.3s
                ease-out;
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

            border-right:
                1px solid #ebe4e9;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarContent"] {

            padding-top: 0.8rem;
        }

        section[data-testid="stSidebar"]
        [role="radiogroup"] {

            gap: 3px;
        }

        /* VÙNG MENU */

        section[data-testid="stSidebar"]
        [role="radiogroup"] label {

            padding: 8px 10px;

            border-radius: 9px;

            border:
                1px solid transparent;

            background:
                transparent !important;

            transition:
                background 0.18s ease,
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
        }

        /* ==================================================
           HOVER MENU
           ÉP MÀU SÁNG, KHÔNG CHO STREAMLIT HIỆN XÁM
           ================================================== */

        section[data-testid="stSidebar"]
        [role="radiogroup"] label:hover {

            background:
                linear-gradient(
                    90deg,
                    #ffeaf3 0%,
                    #f4eaff 100%
                ) !important;

            border-color:
                #edc9da !important;

            transform:
                translateX(2px);

            box-shadow:
                0 3px 10px
                rgba(
                    190,
                    125,
                    160,
                    0.12
                );
        }

        /* Các thành phần bên trong label */

        section[data-testid="stSidebar"]
        [role="radiogroup"]
        label:hover > div {

            background:
                transparent !important;
        }

        section[data-testid="stSidebar"]
        [role="radiogroup"]
        label:hover > div > div {

            background:
                transparent !important;
        }

        section[data-testid="stSidebar"]
        [role="radiogroup"]
        label:hover p {

            color:
                #984d72 !important;
        }

        /* ==================================================
           MỤC ĐANG CHỌN
           ================================================== */

        section[data-testid="stSidebar"]
        [role="radiogroup"]
        label[data-checked="true"] {

            background:
                linear-gradient(
                    90deg,
                    #fbdfea 0%,
                    #eee5ff 100%
                ) !important;

            border:
                1px solid #e5c4d5 !important;

            box-shadow:
                0 3px 10px
                rgba(
                    190,
                    125,
                    160,
                    0.10
                );
        }

        section[data-testid="stSidebar"]
        [role="radiogroup"]
        label[data-checked="true"] > div {

            background:
                transparent !important;
        }

        section[data-testid="stSidebar"]
        [role="radiogroup"]
        label[data-checked="true"] p {

            color:
                #8f486b !important;

            font-weight:
                700;
        }

        section[data-testid="stSidebar"]
        [role="radiogroup"] label p {

            font-size:
                14px;

            font-weight:
                600;

            color:
                #51434b;

            transition:
                color 0.18s ease;
        }


        /* ==================================================
           HEADER
           ================================================== */

        [class*="st-key-qlc-page-header-"] {

            padding:
                18px 22px;

            margin-bottom:
                16px;

            border-radius:
                16px;

            background:
                linear-gradient(
                    135deg,
                    #fff1f5 0%,
                    #f7f2ff 52%,
                    #eef7ff 100%
                );

            border:
                1px solid #eadde5;

            box-shadow:
                0 5px 18px
                rgba(
                    80,
                    55,
                    70,
                    0.055
                );

            animation:
                qlc_fade_up
                0.35s
                ease-out;
        }

        [class*="st-key-qlc-page-header-"]
        [data-testid="stMarkdownContainer"] h1 {

            color:
                #463640;

            font-size:
                26px;

            font-weight:
                750;

            letter-spacing:
                -0.35px;

            margin-top:
                0;

            margin-bottom:
                4px;
        }

        [class*="st-key-qlc-page-header-"]
        [data-testid="stCaptionContainer"] {

            color:
                #766872;

            font-size:
                14px;

            line-height:
                1.45;
        }


        /* ==================================================
           SECTION TITLE
           ================================================== */

        [class*="st-key-qlc-section-title-"] {

            margin-top:
                8px;

            margin-bottom:
                9px;

            padding:
                1px;

            animation:
                qlc_fade_up
                0.3s
                ease-out;
        }

        [class*="st-key-qlc-section-title-"]
        [data-testid="stMarkdownContainer"] h3 {

            color:
                #463740;

            font-size:
                18px;

            font-weight:
                700;

            margin:
                0;
        }


        /* ==================================================
           STAT CARD
           ================================================== */

        [class*="st-key-qlc-stat-card-"] {

            min-height:
                88px;

            padding:
                12px 16px;

            border-radius:
                13px;

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.96
                );

            border:
                1px solid #ebe4e8;

            box-shadow:
                0 3px 12px
                rgba(
                    60,
                    45,
                    55,
                    0.045
                );

            transition:
                transform 0.16s ease,
                box-shadow 0.16s ease,
                border-color 0.16s ease;

            animation:
                qlc_soft_scale
                0.32s
                ease-out;
        }

        [class*="st-key-qlc-stat-card-"]:hover {

            transform:
                translateY(-2px);

            border-color:
                #dfc4d2;

            box-shadow:
                0 7px 18px
                rgba(
                    60,
                    45,
                    55,
                    0.075
                );
        }

        [class*="st-key-qlc-stat-card-"]
        [data-testid="stMarkdownContainer"] p {

            margin-top:
                0;

            margin-bottom:
                2px;
        }

        [class*="st-key-qlc-stat-card-"]
        [data-testid="stMarkdownContainer"] h4 {

            color:
                #81747b;

            font-size:
                12px;

            font-weight:
                600;

            margin-top:
                0;

            margin-bottom:
                2px;
        }

        [class*="st-key-qlc-stat-card-"]
        [data-testid="stMarkdownContainer"] h2 {

            color:
                #41343c;

            font-size:
                23px;

            font-weight:
                750;

            line-height:
                1.15;

            margin-top:
                0;

            margin-bottom:
                0;
        }


        /* ==================================================
           INFO CARD
           ================================================== */

        [class*="st-key-qlc-info-card-"] {

            padding:
                13px 16px;

            border-radius:
                13px;

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.96
                );

            border:
                1px solid #ebe5e9;

            box-shadow:
                0 3px 12px
                rgba(
                    60,
                    45,
                    55,
                    0.04
                );

            transition:
                transform 0.16s ease,
                box-shadow 0.16s ease,
                border-color 0.16s ease;

            animation:
                qlc_fade_up
                0.32s
                ease-out;
        }

        [class*="st-key-qlc-info-card-"]:hover {

            transform:
                translateY(-1px);

            border-color:
                #dfcbd6;

            box-shadow:
                0 6px 17px
                rgba(
                    60,
                    45,
                    55,
                    0.065
                );
        }

        [class*="st-key-qlc-info-card-"]
        [data-testid="stMarkdownContainer"] h4 {

            color:
                #51434b;

            font-size:
                14px;

            font-weight:
                700;

            margin-top:
                0;

            margin-bottom:
                3px;
        }

        [class*="st-key-qlc-info-card-"]
        [data-testid="stMarkdownContainer"] p {

            color:
                #81747b;

            font-size:
                13px;

            line-height:
                1.45;

            margin-bottom:
                0;
        }


        /* ==================================================
           BUTTON
           ================================================== */

        .stButton > button {

            min-height:
                38px !important;

            padding:
                5px 13px !important;

            border-radius:
                9px !important;

            border:
                1px solid #e3d8de !important;

            font-weight:
                600 !important;

            transition:
                transform 0.14s ease,
                box-shadow 0.14s ease,
                background 0.14s ease,
                border-color 0.14s ease;
        }

        .stButton > button:hover {

            transform:
                translateY(-1px);

            background:
                #fff3f7 !important;

            border-color:
                #e1b9ca !important;

            box-shadow:
                0 4px 12px
                rgba(
                    190,
                    125,
                    160,
                    0.10
                );
        }

        .stButton > button:active {

            transform:
                translateY(1px)
                scale(0.985);
        }

        .stButton > button:focus {

            outline:
                none !important;
        }


        /* ==================================================
           INPUT
           ================================================== */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input,
        .stTextArea textarea {

            border-radius:
                9px !important;

            transition:
                border-color 0.15s ease,
                box-shadow 0.15s ease;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus,
        .stTimeInput input:focus,
        .stTextArea textarea:focus {

            border-color:
                #d9a9bd !important;

            box-shadow:
                0 0 0 3px
                rgba(
                    217,
                    169,
                    189,
                    0.13
                ) !important;
        }


        /* ==================================================
           SELECTBOX
           ================================================== */

        [data-baseweb="select"] {

            border-radius:
                9px !important;
        }

        [data-baseweb="select"] > div {

            border-radius:
                9px !important;
        }


        /* ==================================================
           CHECKBOX / RADIO
           ================================================== */

        [data-testid="stCheckbox"] label,
        [data-testid="stRadio"] label {

            transition:
                opacity 0.15s ease,
                background 0.15s ease;
        }

        [data-testid="stCheckbox"] label:hover,
        [data-testid="stRadio"] label:hover {

            opacity:
                1;

            background:
                #fff1f6;

            border-radius:
                7px;
        }


        /* ==================================================
           EXPANDER
           ================================================== */

        [data-testid="stExpander"] {

            border-radius:
                10px !important;

            border-color:
                #ebe5e9 !important;

            transition:
                box-shadow 0.18s ease,
                border-color 0.18s ease,
                background 0.18s ease;
        }

        [data-testid="stExpander"]:hover {

            border-color:
                #dfcbd6 !important;

            background:
                #fffafd !important;

            box-shadow:
                0 3px 12px
                rgba(
                    60,
                    45,
                    55,
                    0.045
                );
        }

        [data-testid="stExpander"] summary {

            font-weight:
                600 !important;
        }


        /* ==================================================
           DATAFRAME
           ================================================== */

        [data-testid="stDataFrame"] {

            border-radius:
                11px;

            overflow:
                hidden;

            border:
                1px solid #e7dfe4;

            animation:
                qlc_fade_up
                0.35s
                ease-out;

            box-shadow:
                0 3px 12px
                rgba(
                    60,
                    45,
                    55,
                    0.035
                );
        }


        /* ==================================================
           TABLE
           ================================================== */

        [data-testid="stTable"] {

            border-radius:
                11px;

            overflow:
                hidden;

            border:
                1px solid #e7dfe4;

            animation:
                qlc_fade_up
                0.35s
                ease-out;
        }


        /* ==================================================
           ALERT
           ================================================== */

        [data-testid="stAlert"] {

            border-radius:
                10px;

            animation:
                qlc_fade_up
                0.3s
                ease-out;

            box-shadow:
                0 3px 12px
                rgba(
                    60,
                    45,
                    55,
                    0.04
                );
        }


        /* ==================================================
           METRIC
           ================================================== */

        [data-testid="stMetric"] {

            padding:
                11px 14px;

            border-radius:
                12px;

            background:
                #ffffff;

            border:
                1px solid #ebe5e9;

            box-shadow:
                0 3px 11px
                rgba(
                    60,
                    45,
                    55,
                    0.035
                );

            animation:
                qlc_soft_scale
                0.3s
                ease-out;
        }


        /* ==================================================
           DIVIDER
           ================================================== */

        hr {

            border-color:
                #ebe5e9 !important;

            margin-top:
                0.7rem !important;

            margin-bottom:
                0.7rem !important;
        }


        /* ==================================================
           TAB
           ================================================== */

        [data-baseweb="tab"] {

            font-weight:
                600;

            transition:
                color 0.15s ease,
                transform 0.15s ease;
        }

        [data-baseweb="tab"]:hover {

            transform:
                translateY(-1px);

            color:
                #a65379;
        }


        /* ==================================================
           FOOTER
           ================================================== */

        [class*="st-key-qlc-footer-"] {

            margin-top:
                24px;

            padding-top:
                12px;

            border-top:
                1px solid #ebe5e9;

            text-align:
                center;

            color:
                #988b92;

            font-size:
                12px;

            animation:
                qlc_fade_in
                0.45s
                ease-out;
        }


        /* ==================================================
           RESPONSIVE
           ================================================== */

        @media (max-width: 768px) {

            .block-container {

                padding-top:
                    0.8rem;

                padding-left:
                    0.8rem;

                padding-right:
                    0.8rem;

                padding-bottom:
                    1.5rem;
            }

            [class*="st-key-qlc-page-header-"] {

                padding:
                    16px;

                margin-bottom:
                    12px;

                border-radius:
                    13px;
            }

            [class*="st-key-qlc-page-header-"]
            [data-testid="stMarkdownContainer"] h1 {

                font-size:
                    22px;
            }

            [class*="st-key-qlc-stat-card-"] {

                min-height:
                    78px;

                padding:
                    10px 13px;
            }

            [class*="st-key-qlc-stat-card-"]
            [data-testid="stMarkdownContainer"] h2 {

                font-size:
                    20px;
            }

            [class*="st-key-qlc-info-card-"] {

                padding:
                    12px 13px;
            }

            .stButton > button {

                min-height:
                    42px !important;
            }
        }


        /* ==================================================
           GIẢM ANIMATION
           ================================================== */

        @media (prefers-reduced-motion: reduce) {

            *,
            *::before,
            *::after {

                animation-duration:
                    0.01ms !important;

                animation-iteration-count:
                    1 !important;

                transition-duration:
                    0.01ms !important;
            }
        }


        /* ==================================================
           DARK MODE
           ================================================== */

        @media (prefers-color-scheme: dark) {

            .stApp {

                background:
                    linear-gradient(
                        180deg,
                        #17171a 0%,
                        #191a1e 50%,
                        #16181c 100%
                    );
            }

            section[data-testid="stSidebar"] {

                background:
                    linear-gradient(
                        180deg,
                        #1d1b1f 0%,
                        #1b1b20 55%,
                        #181a1f 100%
                    );

                border-color:
                    #303038;
            }

            section[data-testid="stSidebar"]
            [role="radiogroup"] label p {

                color:
                    #d8ced4;
            }

            /* DARK MODE - HOVER SÁNG */

            section[data-testid="stSidebar"]
            [role="radiogroup"] label:hover {

                background:
                    linear-gradient(
                        90deg,
                        #49333e,
                        #3d354e
                    ) !important;

                border-color:
                    #6b4d5d !important;

                box-shadow:
                    0 3px 12px
                    rgba(
                        210,
                        130,
                        170,
                        0.13
                    );
            }

            section[data-testid="stSidebar"]
            [role="radiogroup"] label:hover > div,
            section[data-testid="stSidebar"]
            [role="radiogroup"] label:hover > div > div {

                background:
                    transparent !important;
            }

            section[data-testid="stSidebar"]
            [role="radiogroup"] label:hover p {

                color:
                    #ffd8e8 !important;
            }

            section[data-testid="stSidebar"]
            [role="radiogroup"]
            label[data-checked="true"] {

                background:
                    linear-gradient(
                        90deg,
                        #503540,
                        #403750
                    ) !important;

                border-color:
                    #725266 !important;
            }

            [class*="st-key-qlc-page-header-"] {

                background:
                    linear-gradient(
                        135deg,
                        #30252c 0%,
                        #282530 52%,
                        #222b33 100%
                    );

                border-color:
                    #403942;
            }

            [class*="st-key-qlc-page-header-"]
            [data-testid="stMarkdownContainer"] h1 {

                color:
                    #f4eaf0;
            }

            [class*="st-key-qlc-page-header-"]
            [data-testid="stCaptionContainer"] {

                color:
                    #c1b5bc;
            }

            [class*="st-key-qlc-section-title-"]
            [data-testid="stMarkdownContainer"] h3 {

                color:
                    #f0e6eb;
            }

            [class*="st-key-qlc-stat-card-"],
            [class*="st-key-qlc-info-card-"] {

                background:
                    #202126;

                border-color:
                    #36373d;
            }

            [class*="st-key-qlc-stat-card-"]
            [data-testid="stMarkdownContainer"] h4 {

                color:
                    #b9adb4;
            }

            [class*="st-key-qlc-stat-card-"]
            [data-testid="stMarkdownContainer"] h2 {

                color:
                    #f1ebee;
            }

            [class*="st-key-qlc-info-card-"]
            [data-testid="stMarkdownContainer"] h4 {

                color:
                    #eee5e9;
            }

            [class*="st-key-qlc-info-card-"]
            [data-testid="stMarkdownContainer"] p {

                color:
                    #b8adb3;
            }

            [data-testid="stMetric"] {

                background:
                    #202126;

                border-color:
                    #36373d;
            }

            [class*="st-key-qlc-footer-"] {

                border-color:
                    #36373d;

                color:
                    #9e959a;
            }

            [data-testid="stExpander"] {

                border-color:
                    #36373d !important;
            }

            .stButton > button:hover {

                background:
                    #3b2933 !important;

                border-color:
                    #704c5e !important;
            }

            [data-testid="stCheckbox"] label:hover,
            [data-testid="stRadio"] label:hover {

                background:
                    #342a30;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# BỘ ĐẾM KEY
# ==========================================================

def _next_key(prefix):

    key_name = (
        f"_qlc_counter_{prefix}"
    )

    if key_name not in st.session_state:

        st.session_state[key_name] = 0

    st.session_state[key_name] += 1

    return (
        f"qlc-{prefix}-"
        f"{st.session_state[key_name]}"
    )


# ==========================================================
# HEADER
# ==========================================================

def hien_thi_header(
    tieu_de,
    mo_ta=None
):

    key_header = _next_key(
        "page-header"
    )

    with st.container(
        key=key_header
    ):

        st.markdown(
            f"# {tieu_de}"
        )

        if mo_ta:

            st.caption(
                mo_ta
            )


# ==========================================================
# THẺ THỐNG KÊ
# ==========================================================

def hien_thi_the(
    tieu_de,
    gia_tri,
    bieu_tuong=""
):

    key_card = _next_key(
        "stat-card"
    )

    with st.container(
        border=True,
        key=key_card
    ):

        if bieu_tuong:

            st.markdown(
                f"### {bieu_tuong}"
            )

        st.markdown(
            f"#### {tieu_de}"
        )

        st.markdown(
            f"## {gia_tri}"
        )


# ==========================================================
# TIÊU ĐỀ SECTION
# ==========================================================

def hien_thi_tieu_de_section(
    tieu_de,
    bieu_tuong=""
):

    key_section = _next_key(
        "section-title"
    )

    with st.container(
        key=key_section
    ):

        if bieu_tuong:

            st.markdown(
                f"### {bieu_tuong}  {tieu_de}"
            )

        else:

            st.markdown(
                f"### {tieu_de}"
            )


# ==========================================================
# INFO CARD
# ==========================================================

def hien_thi_info_card(
    tieu_de,
    noi_dung
):

    key_card = _next_key(
        "info-card"
    )

    with st.container(
        border=True,
        key=key_card
    ):

        st.markdown(
            f"#### {tieu_de}"
        )

        st.write(
            noi_dung
        )


# ==========================================================
# FOOTER
# ==========================================================

def hien_thi_footer():

    key_footer = _next_key(
        "footer"
    )

    with st.container(
        key=key_footer
    ):

        st.caption(
            "🍚 Quản Lý Chấm Cơm  •  "
            "Hệ thống quản lý suất ăn"
        )