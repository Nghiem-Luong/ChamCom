# -*- coding: utf-8 -*-

import streamlit as st
from pathlib import Path

from Utils.ollama_helper import hoi_qwen
from Controllers.AIController import lay_du_lieu_cho_ai


# ============================================================
# HÀM THÊM TIN NHẮN
# ============================================================

def them_tin_nhan(vai_tro, noi_dung):

    st.session_state["tro_ly_tin_nhan"].append(
        {
            "vai_tro": vai_tro,
            "noi_dung": noi_dung
        }
    )


# ============================================================
# HÀM XÓA LỊCH SỬ
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
# HÀM XỬ LÝ CÂU HỎI VỚI AI + DATABASE
# ============================================================

def xu_ly_cau_hoi_ai(cau_hoi, lich_su=None):
    """
    Xử lý câu hỏi:
    1. Python kiểm tra CSDL.
    2. Nếu có dữ liệu liên quan -> đưa dữ liệu chính xác cho Qwen.
    3. Nếu không liên quan CSDL -> cho Qwen trả lời bình thường.
    """

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
# HÀM HIỂN THỊ ROBOT
# ============================================================

def hien_thi_robot():

    # ========================================================
    # KHỞI TẠO SESSION STATE
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
    # ĐƯỜNG DẪN AVATAR
    # ========================================================

    base_dir = Path(__file__).resolve().parent.parent

    avatar_path = (
        base_dir
        / "Assets"
        / "tro_ly_avatar.png"
    )

    # ========================================================
    # CSS
    # ========================================================

    st.markdown(
        """
        <style>

        /* =====================================================
           DÂU TÂY AI
           ===================================================== */

        /* -----------------------------------------------------
           1. NÚT ROBOT KHI ĐÓNG
           ----------------------------------------------------- */

        .st-key-tro-ly-closed {

            position: fixed !important;

            right: 24px !important;
            bottom: 24px !important;

            z-index: 999999 !important;

            pointer-events: none !important;
        }


        .st-key-tro-ly-closed button {

            width: 64px !important;
            height: 64px !important;

            min-width: 64px !important;
            min-height: 64px !important;

            padding: 0 !important;

            border-radius: 50% !important;

            border: 3px solid white !important;

            background: linear-gradient(
                135deg,
                #ff6b9d 0%,
                #ff4f81 100%
            ) !important;

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.20),
                0 3px 8px rgba(255, 79, 129, 0.30) !important;

            transition: all 0.2s ease !important;

            pointer-events: auto !important;
        }


        .st-key-tro-ly-closed button:hover {

            transform: scale(1.08) !important;

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.25),
                0 4px 12px rgba(255, 79, 129, 0.35) !important;
        }


        .st-key-tro-ly-closed button:active {

            transform: scale(0.96) !important;
        }


        /* -----------------------------------------------------
           2. KHUNG CHAT
           ----------------------------------------------------- */

        .st-key-tro-ly-chat {

            position: fixed !important;

            right: 24px !important;
            bottom: 20px !important;

            width: 430px !important;
            height: 680px !important;

            z-index: 999998 !important;

            background: #ffffff !important;

            border-radius: 20px !important;

            overflow: hidden !important;

            box-shadow:
                0 18px 55px rgba(0, 0, 0, 0.22),
                0 4px 14px rgba(0, 0, 0, 0.10) !important;

            border: 1px solid #e7e7e7 !important;

            /*
             * Quan trọng:
             * Container ngoài không bắt sự kiện click.
             */

            pointer-events: none !important;
        }


        /*
         * Các thành phần thực sự của chat vẫn nhận click.
         */

        .st-key-tro-ly-chat button,
        .st-key-tro-ly-chat input,
        .st-key-tro-ly-chat textarea,
        .st-key-tro-ly-chat [role="button"],
        .st-key-tro-ly-chat [data-testid="stChatInput"],
        .st-key-tro-ly-chat [data-testid="stChatMessage"],
        .st-key-tro-ly-chat [data-testid="stChatMessageContent"],
        .st-key-tro-ly-chat img {

            pointer-events: auto !important;
        }


        /* -----------------------------------------------------
           3. HEADER CHAT
           ----------------------------------------------------- */

        .st-key-tro-ly-chat .dau-tay-title {

            display: flex !important;

            align-items: center !important;

            gap: 11px !important;

            padding: 14px 16px !important;

            margin: 0 !important;

            background: linear-gradient(
                135deg,
                #ff6b9d 0%,
                #ff4f81 100%
            ) !important;

            color: white !important;

            border-radius: 0 !important;
        }


        .st-key-tro-ly-chat .dau-tay-title img {

            width: 44px !important;
            height: 44px !important;

            min-width: 44px !important;

            object-fit: cover !important;

            border-radius: 50% !important;

            border: 2px solid rgba(
                255,
                255,
                255,
                0.9
            ) !important;

            background: white !important;
        }


        .st-key-tro-ly-chat .dau-tay-title strong {

            display: block !important;

            font-size: 16px !important;

            line-height: 20px !important;

            font-weight: 700 !important;

            color: white !important;
        }


        .st-key-tro-ly-chat .dau-tay-status {

            display: block !important;

            margin-top: 2px !important;

            font-size: 12px !important;

            line-height: 16px !important;

            color: rgba(
                255,
                255,
                255,
                0.90
            ) !important;
        }


        /* -----------------------------------------------------
           4. LỊCH SỬ CHAT
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su {

            padding: 12px 12px 8px 12px !important;

            background:
                linear-gradient(
                    rgba(248, 249, 251, 0.92),
                    rgba(248, 249, 251, 0.92)
                ) !important;

            border-radius: 0 !important;

            overflow-y: auto !important;

            pointer-events: auto !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar {

            width: 6px !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar-track {

            background: transparent !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar-thumb {

            background: #d2d5da !important;

            border-radius: 10px !important;
        }


        .st-key-tro-ly-lich-su::-webkit-scrollbar-thumb:hover {

            background: #b8bbc0 !important;
        }


        /* -----------------------------------------------------
           5. TIN NHẮN STREAMLIT
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessage"] {

            display: flex !important;

            width: 100% !important;

            margin-top: 7px !important;
            margin-bottom: 7px !important;

            padding: 0 !important;

            background: transparent !important;

            border: none !important;

            box-shadow: none !important;

            pointer-events: auto !important;
        }


        /* -----------------------------------------------------
           6. AVATAR TIN NHẮN
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageAvatar"] {

            width: 32px !important;
            height: 32px !important;

            min-width: 32px !important;

            margin-top: 2px !important;

            border-radius: 50% !important;
        }


        /* -----------------------------------------------------
           7. NỘI DUNG TIN NHẮN
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] {

            max-width: 78% !important;

            padding: 0 !important;

            background: transparent !important;

            pointer-events: auto !important;
        }


        /* -----------------------------------------------------
           8. BUBBLE
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] > div {

            width: fit-content !important;

            max-width: 100% !important;

            padding: 9px 13px !important;

            border-radius: 17px !important;

            font-size: 14px !important;

            line-height: 1.45 !important;

            word-break: break-word !important;

            overflow-wrap: anywhere !important;
        }


        /* -----------------------------------------------------
           9. TIN NHẮN DÂU TÂY
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessage"][data-testid*="assistant"]
        [data-testid="stChatMessageContent"] > div {

            background: white !important;

            color: #202124 !important;

            border: 1px solid #e7e7e7 !important;

            border-top-left-radius: 5px !important;

            box-shadow:
                0 1px 2px rgba(0, 0, 0, 0.06) !important;
        }


        /* -----------------------------------------------------
           10. TIN NHẮN NGƯỜI DÙNG
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessage"][data-testid*="user"]
        [data-testid="stChatMessageContent"] > div {

            background: #ff4f81 !important;

            color: white !important;

            border: none !important;

            border-top-right-radius: 5px !important;

            box-shadow:
                0 1px 2px rgba(
                    255,
                    79,
                    129,
                    0.20
                ) !important;
        }


        /* -----------------------------------------------------
           11. TEXT
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] p {

            margin-top: 0 !important;

            margin-bottom: 4px !important;
        }


        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] p:last-child {

            margin-bottom: 0 !important;
        }


        /* -----------------------------------------------------
           12. CODE
           ----------------------------------------------------- */

        .st-key-tro-ly-lich-su
        [data-testid="stChatMessageContent"] code {

            background: rgba(
                0,
                0,
                0,
                0.06
            ) !important;

            padding: 2px 5px !important;

            border-radius: 5px !important;

            font-size: 12px !important;
        }


        /* -----------------------------------------------------
           13. BUTTON CHAT
           ----------------------------------------------------- */

        .st-key-tro-ly-chat button {

            font-family: inherit !important;

            pointer-events: auto !important;

            border-radius: 12px !important;

            transition:
                background 0.15s ease,
                transform 0.15s ease !important;
        }


        .st-key-tro-ly-chat button[kind="secondary"] {

            min-height: 34px !important;

            padding: 5px 10px !important;

            border: 1px solid #e4e5e7 !important;

            background: #ffffff !important;

            color: #444 !important;

            font-size: 12px !important;

            font-weight: 500 !important;
        }


        .st-key-tro-ly-chat button[kind="secondary"]:hover {

            background: #fff0f4 !important;

            border-color: #ff9cba !important;

            color: #ff3f76 !important;

            transform: translateY(-1px) !important;
        }


        /* -----------------------------------------------------
           14. Ô NHẬP CHAT
           ----------------------------------------------------- */

        .st-key-tro-ly-chat
        [data-testid="stChatInput"] {

            padding: 6px 12px 12px 12px !important;

            background: #f8f9fb !important;

            pointer-events: auto !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stChatInput"] textarea {

            min-height: 42px !important;

            max-height: 100px !important;

            padding: 11px 46px 11px 15px !important;

            border-radius: 22px !important;

            border: 1px solid #dedfe3 !important;

            background: white !important;

            color: #202124 !important;

            font-size: 14px !important;

            box-shadow: none !important;

            resize: none !important;

            pointer-events: auto !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stChatInput"] textarea:focus {

            border-color: #ff7da2 !important;

            box-shadow:
                0 0 0 2px rgba(
                    255,
                    79,
                    129,
                    0.10
                ) !important;
        }


        .st-key-tro-ly-chat
        [data-testid="stChatInput"] button {

            border-radius: 50% !important;

            width: 34px !important;

            height: 34px !important;

            min-width: 34px !important;

            min-height: 34px !important;

            margin-right: 5px !important;

            pointer-events: auto !important;
        }


        /* -----------------------------------------------------
           15. FULLSCREEN CHAT
           ----------------------------------------------------- */

        .st-key-tro-ly-full {

            position: fixed !important;

            left: 7vw !important;
            right: 7vw !important;

            top: 5vh !important;
            bottom: 5vh !important;

            z-index: 999999 !important;

            background: white !important;

            border-radius: 22px !important;

            overflow: hidden !important;

            border: 1px solid #e5e5e5 !important;

            box-shadow:
                0 20px 70px rgba(
                    0,
                    0,
                    0,
                    0.25
                ) !important;

            pointer-events: none !important;
        }


        .st-key-tro-ly-full button,
        .st-key-tro-ly-full input,
        .st-key-tro-ly-full textarea,
        .st-key-tro-ly-full [role="button"],
        .st-key-tro-ly-full [data-testid="stChatInput"],
        .st-key-tro-ly-full [data-testid="stChatMessage"] {

            pointer-events: auto !important;
        }


        .st-key-tro-ly-full .dau-tay-title {

            display: flex !important;

            align-items: center !important;

            gap: 12px !important;

            padding: 16px 20px !important;

            background: linear-gradient(
                135deg,
                #ff6b9d 0%,
                #ff4f81 100%
            ) !important;

            color: white !important;
        }


        .st-key-tro-ly-full .dau-tay-title img {

            width: 48px !important;
            height: 48px !important;

            border-radius: 50% !important;

            border: 2px solid white !important;
        }


        /* -----------------------------------------------------
           16. RESPONSIVE
           ----------------------------------------------------- */

        @media (max-width: 700px) {

            .st-key-tro-ly-chat {

                right: 10px !important;
                bottom: 10px !important;

                width: calc(100vw - 20px) !important;

                height: calc(100vh - 20px) !important;

                border-radius: 18px !important;
            }


            .st-key-tro-ly-closed {

                right: 16px !important;
                bottom: 16px !important;
            }


            .st-key-tro-ly-closed button {

                width: 58px !important;
                height: 58px !important;

                min-width: 58px !important;
                min-height: 58px !important;
            }


            .st-key-tro-ly-lich-su
            [data-testid="stChatMessageContent"] {

                max-width: 82% !important;
            }


            .st-key-tro-ly-chat
            [data-testid="stChatInput"] textarea {

                font-size: 16px !important;
            }
        }


        /* -----------------------------------------------------
           17. DARK MODE
           ----------------------------------------------------- */

        @media (prefers-color-scheme: dark) {

            .st-key-tro-ly-chat {

                background: #18191d !important;

                border-color: #303136 !important;
            }


            .st-key-tro-ly-lich-su {

                background: #202124 !important;
            }


            .st-key-tro-ly-lich-su
            [data-testid="stChatMessage"]
            [data-testid="stChatMessageContent"] > div {

                background: #303136 !important;

                color: #f1f3f4 !important;

                border-color: #3b3c40 !important;
            }


            .st-key-tro-ly-chat
            [data-testid="stChatInput"] {

                background: #18191d !important;
            }


            .st-key-tro-ly-chat
            [data-testid="stChatInput"] textarea {

                background: #303136 !important;

                color: white !important;

                border-color: #45464b !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # ROBOT ĐANG ĐÓNG
    # ========================================================

    if not st.session_state["tro_ly_mo"]:

        with st.container(
            key="tro-ly-closed"
        ):

            if avatar_path.exists():

                st.image(
                    str(avatar_path),
                    width=100
                )

            if st.button(
                "💬 Trợ lý",
                key="mo_tro_ly",
                width="stretch"
            ):

                st.session_state[
                    "tro_ly_mo"
                ] = True

                st.rerun()

        return

    # ========================================================
    # KÍCH THƯỚC CHATBOX
    # ========================================================

    if st.session_state["tro_ly_phong_to"]:

        chat_container = st.container(
            key="tro-ly-full"
        )

        chieu_cao_lich_su = 430

    else:

        chat_container = st.container(
            key="tro-ly-chat"
        )

        chieu_cao_lich_su = 360

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
            [0.9, 4.5, 0.8, 0.8, 0.8],
            vertical_alignment="center"
        )

        # ====================================================
        # AVATAR
        # ====================================================

        with col_avatar:

            if avatar_path.exists():

                st.image(
                    str(avatar_path),
                    width=45
                )

        # ====================================================
        # TÊN DÂU TÂY
        # ====================================================

        with col_title:

            st.markdown(
                '<div class="dau-tay-title">'
                '🍓 Dâu Tây'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="dau-tay-status">'
                '● Đang hoạt động • Qwen 2.5 3B'
                '</div>',
                unsafe_allow_html=True
            )

        # ====================================================
        # XÓA CHAT
        # ====================================================

        with col_clear:

            if st.button(
                "🗑️",
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

                        st.caption(
                            "🤖 DÂU TÂY"
                        )

                        st.markdown(
                            noi_dung
                        )

                elif vai_tro == "user":

                    with st.chat_message(
                        "user",
                        avatar="👤"
                    ):

                        st.caption(
                            "👤 BẠN"
                        )

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
        # Ô NHẬP
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