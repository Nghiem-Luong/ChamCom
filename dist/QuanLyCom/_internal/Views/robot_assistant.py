# -*- coding: utf-8 -*-

import streamlit as st
from pathlib import Path

from Utils.ollama_helper import hoi_qwen
from Controllers.AIController import lay_du_lieu_cho_ai


# ============================================================
# THÊM TIN NHẮN
# ============================================================

def them_tin_nhan(vai_tro, noi_dung):

    st.session_state["tro_ly_tin_nhan"].append(
        {
            "vai_tro": vai_tro,
            "noi_dung": noi_dung
        }
    )


# ============================================================
# XÓA LỊCH SỬ CHAT
# ============================================================

def xoa_lich_su_chat():

    st.session_state["tro_ly_tin_nhan"] = [
        {
            "vai_tro": "assistant",
            "noi_dung": (
                "Xin chào chị! 👋\n\n"
                "Em là **Dâu Tây**, trợ lý của "
                "ứng dụng Quản Lý Chấm Cơm.\n\n"
                "Chị muốn em hỗ trợ gì hôm nay?"
            )
        }
    ]


# ============================================================
# XỬ LÝ CÂU HỎI AI + DATABASE
# ============================================================

def xu_ly_cau_hoi_ai(cau_hoi, lich_su=None):

    du_lieu_db = lay_du_lieu_cho_ai(cau_hoi)

    if du_lieu_db:

        cau_hoi_ai = f"""
Bạn là Dâu Tây, trợ lý AI của ứng dụng Quản Lý Chấm Cơm.

Câu hỏi của người dùng:
{cau_hoi}

Dữ liệu chính xác lấy trực tiếp từ hệ thống:
{du_lieu_db}

Hãy trả lời câu hỏi dựa trên dữ liệu hệ thống ở trên.

QUY TẮC BẮT BUỘC:
- Không được thay đổi số liệu.
- Không được tự bịa số liệu.
- Không được suy đoán thêm dữ liệu.
- Nếu dữ liệu đã có câu trả lời, hãy trả lời trực tiếp.
- Trả lời bằng tiếng Việt.
- Trả lời tự nhiên như một trợ lý chat.
- Không cần nói "dữ liệu hệ thống cho biết".
- Nếu có ngày tháng, hiển thị ngày theo dạng DD/MM/YYYY.
"""

    else:

        cau_hoi_ai = f"""
Bạn là Dâu Tây, trợ lý AI của ứng dụng Quản Lý Chấm Cơm.

Người dùng hỏi:
{cau_hoi}

Hãy trả lời câu hỏi một cách tự nhiên bằng tiếng Việt.

Bạn có thể:
- Trò chuyện thông thường.
- Chào hỏi.
- Giải thích cách sử dụng phần mềm.
- Hướng dẫn các chức năng.
- Trả lời câu hỏi kiến thức thông thường.
- Giải thích các khái niệm.

Nếu câu hỏi liên quan đến dữ liệu chấm cơm nhưng hệ thống
không cung cấp dữ liệu cần thiết, hãy nói rõ rằng hiện tại
chưa có dữ liệu phù hợp thay vì tự bịa số liệu.

Không được tự tạo số liệu CSDL.
"""

    return hoi_qwen(
        cau_hoi_ai,
        lich_su
    )


# ============================================================
# GIAO DIỆN ROBOT
# ============================================================

def hien_thi_robot():

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "tro_ly_mo" not in st.session_state:
        st.session_state["tro_ly_mo"] = False

    if "tro_ly_phong_to" not in st.session_state:
        st.session_state["tro_ly_phong_to"] = False

    if "tro_ly_tin_nhan" not in st.session_state:

        st.session_state["tro_ly_tin_nhan"] = [
            {
                "vai_tro": "assistant",
                "noi_dung": (
                    "Xin chào chị! 👋\n\n"
                    "Em là **Dâu Tây**, trợ lý của "
                    "ứng dụng Quản Lý Chấm Cơm.\n\n"
                    "Chị muốn em hỗ trợ gì hôm nay?"
                )
            }
        ]

    # ========================================================
    # AVATAR
    # ========================================================

    base_dir = Path(__file__).resolve().parent.parent

    avatar_path = (
        base_dir
        / "Assets"
        / "tro_ly_avatar.png"
    )

    # ========================================================
    # CSS
    #
    # Không dùng HTML div tự tạo.
    # Chỉ style các component Streamlit.
    # ========================================================

    st.markdown(
        """
        <style>

        /* =====================================================
           ROBOT ĐÓNG
           ===================================================== */

        .st-key-tro-ly-closed {

            position: fixed !important;

            right: 20px !important;
            bottom: 20px !important;

            z-index: 999999 !important;

            width: 66px !important;
            height: 66px !important;

            padding: 0 !important;
            margin: 0 !important;

            pointer-events: none !important;

            animation: troLyFloat 3s ease-in-out infinite;
        }


        .st-key-tro-ly-closed [data-testid="stImage"] {

            display: none !important;
        }


        .st-key-tro-ly-closed button {

            width: 62px !important;
            height: 62px !important;

            min-width: 62px !important;
            min-height: 62px !important;

            padding: 0 !important;

            border-radius: 50% !important;

            border: 3px solid white !important;

            background:
                linear-gradient(
                    135deg,
                    #ff79a8 0%,
                    #ff4f81 55%,
                    #ff3d72 100%
                ) !important;

            color: white !important;

            font-size: 25px !important;

            box-shadow:
                0 8px 28px rgba(255, 79, 129, 0.35),
                0 4px 12px rgba(0, 0, 0, 0.18) !important;

            pointer-events: auto !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        .st-key-tro-ly-closed button:hover {

            transform: scale(1.08) !important;

            box-shadow:
                0 12px 34px rgba(255, 79, 129, 0.42),
                0 5px 14px rgba(0, 0, 0, 0.20) !important;
        }


        .st-key-tro-ly-closed button:active {

            transform: scale(0.94) !important;
        }


        /* =====================================================
           CHATBOX THƯỜNG
           ===================================================== */

        .st-key-tro-ly-chat {

            position: fixed !important;

            right: 20px !important;
            bottom: 20px !important;

            width: 410px !important;
            height: 650px !important;

            z-index: 999998 !important;

            padding: 0 !important;
            margin: 0 !important;

            background: #ffffff !important;

            border-radius: 24px !important;

            border: 1px solid #eeeeee !important;

            overflow: hidden !important;

            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.18),
                0 8px 25px rgba(255, 79, 129, 0.12) !important;

            animation:
                troLyOpen 0.25s ease-out !important;
        }


        /* =====================================================
           CHATBOX FULLSCREEN
           ===================================================== */

        .st-key-tro-ly-full {

            position: fixed !important;

            left: 6vw !important;
            right: 6vw !important;

            top: 4vh !important;
            bottom: 4vh !important;

            z-index: 999998 !important;

            padding: 0 !important;
            margin: 0 !important;

            background: #ffffff !important;

            border-radius: 24px !important;

            border: 1px solid #eeeeee !important;

            overflow: hidden !important;

            box-shadow:
                0 25px 80px rgba(0, 0, 0, 0.22) !important;

            animation:
                troLyOpen 0.25s ease-out !important;
        }


        /* =====================================================
           HEADER
           ===================================================== */

        .st-key-tro-ly-chat
        [data-testid="stHorizontalBlock"]:first-child,

        .st-key-tro-ly-full
        [data-testid="stHorizontalBlock"]:first-child {

            background:
                linear-gradient(
                    135deg,
                    #ff72a4 0%,
                    #ff4f81 50%,
                    #ff3d72 100%
                ) !important;

            padding:
                10px 12px 10px 12px !important;

            margin: 0 !important;

            border-radius: 24px 24px 0 0 !important;
        }


        /* =====================================================
           HEADER AVATAR
           ===================================================== */

        .st-key-tro-ly-chat
        [data-testid="stHorizontalBlock"]:first-child
        [data-testid="stImage"] img,

        .st-key-tro-ly-full
        [data-testid="stHorizontalBlock"]:first-child
        [data-testid="stImage"] img {

            width: 44px !important;
            height: 44px !important;

            object-fit: cover !important;

            border-radius: 50% !important;

            border: 2px solid white !important;

            background: white !important;

            box-shadow:
                0 2px 8px rgba(0, 0, 0, 0.12) !important;
        }


        /* =====================================================
           HEADER BUTTON
           ===================================================== */

        .st-key-tro-ly-chat
        [data-testid="stHorizontalBlock"]:first-child button,

        .st-key-tro-ly-full
        [data-testid="stHorizontalBlock"]:first-child button {

            min-width: 34px !important;
            min-height: 34px !important;

            width: 34px !important;
            height: 34px !important;

            padding: 0 !important;

            border-radius: 50% !important;

            border: none !important;

            background:
                rgba(255, 255, 255, 0.18) !important;

            color: white !important;

            font-size: 15px !important;

            box-shadow: none !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stHorizontalBlock"]:first-child button:hover,

        .st-key-tro-ly-full
        [data-testid="stHorizontalBlock"]:first-child button:hover {

            background:
                rgba(255, 255, 255, 0.30) !important;

            transform: scale(1.05) !important;
        }


        /* =====================================================
           NỘI DUNG CHAT
           ===================================================== */

        .st-key-tro-ly-lich-su {

            background:
                linear-gradient(
                    180deg,
                    #fffafd 0%,
                    #f9f9fc 45%,
                    #f6f7fa 100%
                ) !important;

            border-radius: 0 !important;

            padding:
                12px 12px 8px 12px !important;

            overflow-y: auto !important;

            scrollbar-width: thin !important;

            scrollbar-color:
                #d8d8dc
                transparent !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar {

            width: 5px !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar-track {

            background: transparent !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar-thumb {

            background: #d7d7dc !important;

            border-radius: 10px !important;
        }


        /* =====================================================
           CHAT MESSAGE
           ===================================================== */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessage"] {

            background: transparent !important;

            border: none !important;

            padding: 2px 0 !important;

            margin:
                7px 0 !important;

            box-shadow: none !important;
        }


        /* =====================================================
           AVATAR MESSAGE
           ===================================================== */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageAvatar"] {

            width: 32px !important;
            height: 32px !important;

            min-width: 32px !important;

            border-radius: 50% !important;
        }


        /* =====================================================
           NỘI DUNG MESSAGE
           ===================================================== */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] {

            max-width: 78% !important;

            padding: 0 !important;

            background: transparent !important;
        }


        /* =====================================================
           TEXT MESSAGE
           ===================================================== */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] p {

            font-size: 14px !important;

            line-height: 1.5 !important;

            margin-top: 0 !important;

            margin-bottom: 5px !important;

            word-break: break-word !important;

            overflow-wrap: anywhere !important;
        }


        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] p:last-child {

            margin-bottom: 0 !important;
        }


        /* =====================================================
           CAPTION TÊN NGƯỜI GỬI
           ===================================================== */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"]
        [data-testid="stCaptionContainer"] {

            font-size: 10px !important;

            font-weight: 600 !important;

            color: #9a9aa2 !important;

            margin-bottom: 3px !important;
        }


        /* =====================================================
           CODE
           ===================================================== */

        .st-key-tro-ly-lich-su code {

            background: #f0f0f3 !important;

            border-radius: 5px !important;

            padding: 2px 5px !important;

            font-size: 12px !important;
        }


        /* =====================================================
           GỢI Ý
           ===================================================== */

        .st-key-tro-ly-chat
        [data-testid="stCaptionContainer"],

        .st-key-tro-ly-full
        [data-testid="stCaptionContainer"] {

            color: #9999a2 !important;

            font-size: 11px !important;
        }


        /* =====================================================
           NÚT GỢI Ý
           ===================================================== */

        .st-key-tro-ly-chat
        [data-testid="stHorizontalBlock"]:not(:first-child)
        button,

        .st-key-tro-ly-full
        [data-testid="stHorizontalBlock"]:not(:first-child)
        button {

            border-radius: 14px !important;

            border: 1px solid #ececef !important;

            background: white !important;

            color: #55555d !important;

            min-height: 34px !important;

            font-size: 12px !important;

            transition:
                all 0.18s ease !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stHorizontalBlock"]:not(:first-child)
        button:hover,

        .st-key-tro-ly-full
        [data-testid="stHorizontalBlock"]:not(:first-child)
        button:hover {

            background: #fff2f6 !important;

            border-color: #ff9cba !important;

            color: #ff4779 !important;

            transform: translateY(-1px) !important;
        }


        /* =====================================================
           CHAT INPUT
           ===================================================== */

        .st-key-tro-ly-chat
        [data-testid="stChatInput"],

        .st-key-tro-ly-full
        [data-testid="stChatInput"] {

            background:
                rgba(248, 249, 251, 0.96) !important;

            padding:
                7px 12px 12px 12px !important;

            border-top:
                1px solid #eeeeef !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stChatInput"] textarea,

        .st-key-tro-ly-full
        [data-testid="stChatInput"] textarea {

            min-height: 44px !important;

            max-height: 100px !important;

            border-radius: 24px !important;

            border:
                1px solid #dedee3 !important;

            background: white !important;

            color: #222 !important;

            font-size: 14px !important;

            padding:
                11px 48px 11px 16px !important;

            box-shadow:
                0 2px 8px rgba(0, 0, 0, 0.04) !important;

            resize: none !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stChatInput"] textarea:focus,

        .st-key-tro-ly-full
        [data-testid="stChatInput"] textarea:focus {

            border-color:
                #ff80a5 !important;

            box-shadow:
                0 0 0 3px
                rgba(255, 79, 129, 0.10) !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stChatInput"] button,

        .st-key-tro-ly-full
        [data-testid="stChatInput"] button {

            width: 34px !important;
            height: 34px !important;

            min-width: 34px !important;
            min-height: 34px !important;

            border-radius: 50% !important;

            background:
                #ff4f81 !important;

            color: white !important;

            border: none !important;
        }


        /* =====================================================
           DIVIDER
           ===================================================== */

        .st-key-tro-ly-chat hr,

        .st-key-tro-ly-full hr {

            margin:
                0 !important;

            border-color:
                rgba(255,255,255,0.15) !important;
        }


        /* =====================================================
           ANIMATION
           ===================================================== */

        @keyframes troLyOpen {

            from {

                opacity: 0;

                transform:
                    translateY(14px)
                    scale(0.97);
            }

            to {

                opacity: 1;

                transform:
                    translateY(0)
                    scale(1);
            }
        }


        @keyframes troLyFloat {

            0%,
            100% {

                transform:
                    translateY(0);
            }

            50% {

                transform:
                    translateY(-5px);
            }
        }


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 700px) {

            .st-key-tro-ly-chat {

                left: 8px !important;
                right: 8px !important;

                bottom: 8px !important;

                width:
                    calc(100vw - 16px) !important;

                height:
                    calc(100vh - 16px) !important;

                border-radius: 20px !important;
            }


            .st-key-tro-ly-full {

                left: 4px !important;
                right: 4px !important;

                top: 4px !important;
                bottom: 4px !important;

                border-radius: 18px !important;
            }


            .st-key-tro-ly-closed {

                right: 14px !important;
                bottom: 14px !important;
            }


            .st-key-tro-ly-closed button {

                width: 58px !important;
                height: 58px !important;

                min-width: 58px !important;
                min-height: 58px !important;

                font-size: 23px !important;
            }


            .st-key-tro-ly-lich-su
            [data-testid="stChatMessageContent"] {

                max-width: 84% !important;
            }


            .st-key-tro-ly-chat
            [data-testid="stChatInput"] textarea,

            .st-key-tro-ly-full
            [data-testid="stChatInput"] textarea {

                font-size: 16px !important;
            }
        }


        /* =====================================================
           DARK MODE
           ===================================================== */

        @media (prefers-color-scheme: dark) {

            .st-key-tro-ly-chat,

            .st-key-tro-ly-full {

                background: #191a1f !important;

                border-color: #303138 !important;
            }


            .st-key-tro-ly-lich-su {

                background:
                    linear-gradient(
                        180deg,
                        #202126 0%,
                        #191a1f 100%
                    ) !important;
            }


            .st-key-tro-ly-lich-su
            [data-testid="stChatMessageContent"] p {

                color: #f1f2f4 !important;
            }


            .st-key-tro-ly-chat
            [data-testid="stChatInput"],

            .st-key-tro-ly-full
            [data-testid="stChatInput"] {

                background: #191a1f !important;

                border-color: #303138 !important;
            }


            .st-key-tro-ly-chat
            [data-testid="stChatInput"] textarea,

            .st-key-tro-ly-full
            [data-testid="stChatInput"] textarea {

                background: #292a30 !important;

                color: white !important;

                border-color: #414249 !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # TRỢ LÝ ĐANG ĐÓNG
    # ========================================================

    if not st.session_state["tro_ly_mo"]:

        with st.container(key="tro-ly-closed"):

            if st.button(
                "🍓",
                key="mo_tro_ly",
                help="Mở trợ lý Dâu Tây"
            ):

                st.session_state["tro_ly_mo"] = True

                st.rerun()

        return

    # ========================================================
    # KÍCH THƯỚC CHATBOX
    # ========================================================

    if st.session_state["tro_ly_phong_to"]:

        chat_container = st.container(
            key="tro-ly-full"
        )

        chieu_cao_lich_su = 500

    else:

        chat_container = st.container(
            key="tro-ly-chat"
        )

        chieu_cao_lich_su = 330

    # ========================================================
    # CHATBOX
    # ========================================================

    with chat_container:

        # ====================================================
        # HEADER
        # ====================================================

        (
            col_avatar,
            col_title,
            col_clear,
            col_expand,
            col_close
        ) = st.columns(
            [0.8, 4.3, 0.7, 0.7, 0.7],
            vertical_alignment="center"
        )

        # ====================================================
        # AVATAR
        # ====================================================

        with col_avatar:

            if avatar_path.exists():

                st.image(
                    str(avatar_path),
                    width=42
                )

            else:

                st.markdown("🍓")

        # ====================================================
        # TÊN
        # ====================================================

        with col_title:

            st.markdown(
                "**🍓 Dâu Tây**"
            )

            st.caption(
                "● Đang hoạt động · Qwen 2.5 3B"
            )

        # ====================================================
        # XÓA
        # ====================================================

        with col_clear:

            if st.button(
                "🗑",
                key="xoa_tro_ly",
                help="Xóa lịch sử trò chuyện"
            ):

                xoa_lich_su_chat()

                st.rerun()

        # ====================================================
        # PHÓNG TO
        # ====================================================

        with col_expand:

            if st.button(
                "↗",
                key="phong_to_tro_ly",
                help="Phóng to / thu nhỏ"
            ):

                st.session_state[
                    "tro_ly_phong_to"
                ] = not st.session_state[
                    "tro_ly_phong_to"
                ]

                st.rerun()

        # ====================================================
        # ĐÓNG
        # ====================================================

        with col_close:

            if st.button(
                "✕",
                key="dong_tro_ly",
                help="Đóng trợ lý"
            ):

                st.session_state[
                    "tro_ly_mo"
                ] = False

                st.session_state[
                    "tro_ly_phong_to"
                ] = False

                st.rerun()

        st.divider()

        # ====================================================
        # LỊCH SỬ CHAT
        # ====================================================

        with st.container(
            height=chieu_cao_lich_su,
            border=False,
            key="tro-ly-lich-su",
            autoscroll=True
        ):

            for tin_nhan in st.session_state[
                "tro_ly_tin_nhan"
            ]:

                vai_tro = tin_nhan["vai_tro"]

                noi_dung = tin_nhan["noi_dung"]

                if vai_tro == "assistant":

                    with st.chat_message(
                        "assistant",
                        avatar="🍓"
                    ):

                        st.caption("DÂU TÂY")

                        st.markdown(
                            noi_dung
                        )

                elif vai_tro == "user":

                    with st.chat_message(
                        "user",
                        avatar="👤"
                    ):

                        st.caption("BẠN")

                        st.markdown(
                            noi_dung
                        )

        # ====================================================
        # GỢI Ý
        # ====================================================

        st.caption(
            "💡 Bạn có thể hỏi Dâu Tây bất cứ điều gì."
        )

        # ====================================================
        # CÂU HỎI NHANH
        # ====================================================

        col1, col2, col3 = st.columns(
            3,
            gap="small"
        )

        # ====================================================
        # CÔNG NỢ
        # ====================================================

        with col1:

            if st.button(
                "💰 Công nợ",
                key="goi_y_cong_no",
                width="stretch"
            ):

                cau_hoi = (
                    "Tôi muốn xem thông tin công nợ."
                )

                lich_su = list(
                    st.session_state[
                        "tro_ly_tin_nhan"
                    ]
                )

                them_tin_nhan(
                    "user",
                    cau_hoi
                )

                with st.spinner(
                    "🍓 Dâu Tây đang suy nghĩ..."
                ):

                    tra_loi = xu_ly_cau_hoi_ai(
                        cau_hoi,
                        lich_su
                    )

                them_tin_nhan(
                    "assistant",
                    tra_loi
                )

                st.rerun()

        # ====================================================
        # THỐNG KÊ
        # ====================================================

        with col2:

            if st.button(
                "📊 Thống kê",
                key="goi_y_thong_ke",
                width="stretch"
            ):

                cau_hoi = (
                    "Tôi muốn xem thông tin thống kê."
                )

                lich_su = list(
                    st.session_state[
                        "tro_ly_tin_nhan"
                    ]
                )

                them_tin_nhan(
                    "user",
                    cau_hoi
                )

                with st.spinner(
                    "🍓 Dâu Tây đang suy nghĩ..."
                ):

                    tra_loi = xu_ly_cau_hoi_ai(
                        cau_hoi,
                        lich_su
                    )

                them_tin_nhan(
                    "assistant",
                    tra_loi
                )

                st.rerun()

        # ====================================================
        # TRỢ GIÚP
        # ====================================================

        with col3:

            if st.button(
                "❓ Trợ giúp",
                key="goi_y_tro_giup",
                width="stretch"
            ):

                cau_hoi = (
                    "Bạn có thể giúp tôi những gì "
                    "trong ứng dụng Quản Lý Chấm Cơm?"
                )

                lich_su = list(
                    st.session_state[
                        "tro_ly_tin_nhan"
                    ]
                )

                them_tin_nhan(
                    "user",
                    cau_hoi
                )

                with st.spinner(
                    "🍓 Dâu Tây đang suy nghĩ..."
                ):

                    tra_loi = xu_ly_cau_hoi_ai(
                        cau_hoi,
                        lich_su
                    )

                them_tin_nhan(
                    "assistant",
                    tra_loi
                )

                st.rerun()

        # ====================================================
        # Ô NHẬP CHAT
        # ====================================================

        cau_hoi = st.chat_input(
            "Nhập câu hỏi cho Dâu Tây...",
            key="tro_ly_input"
        )

        # ====================================================
        # XỬ LÝ CÂU HỎI
        # ====================================================

        if cau_hoi:

            cau_hoi = cau_hoi.strip()

            if cau_hoi:

                lich_su = list(
                    st.session_state[
                        "tro_ly_tin_nhan"
                    ]
                )

                them_tin_nhan(
                    "user",
                    cau_hoi
                )

                with st.spinner(
                    "🍓 Dâu Tây đang suy nghĩ..."
                ):

                    tra_loi = xu_ly_cau_hoi_ai(
                        cau_hoi,
                        lich_su
                    )

                them_tin_nhan(
                    "assistant",
                    tra_loi
                )

                st.rerun()