# -*- coding: utf-8 -*-

import streamlit as st


_NOTIFICATION_KEY = "_qlc_pending_notification"


def _hien_thi_thong_bao(message, icon=None, loai="success"):
    """
    Hiển thị thông báo có animation.

    Không sử dụng HTML <div> tự tạo.
    """

    if not message:
        return

    cau_hinh = {
        "success": {
            "icon": "✅",
        },
        "error": {
            "icon": "❌",
        },
        "warning": {
            "icon": "⚠️",
        },
        "info": {
            "icon": "ℹ️",
        },
    }

    config = cau_hinh.get(
        loai,
        cau_hinh["info"],
    )

    st.markdown(
        """
        <style>
        @keyframes qlc_notification_in {
            0% {
                opacity: 0;
                transform: translateY(-12px) scale(0.98);
            }

            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        @keyframes qlc_notification_glow {
            0% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.02);
            }

            100% {
                transform: scale(1);
            }
        }

        [class*="stAlert"] {
            animation:
                qlc_notification_in 0.35s ease-out,
                qlc_notification_glow 0.8s ease-in-out 0.35s;
            border-radius: 14px !important;
        }

        @media (prefers-reduced-motion: reduce) {
            [class*="stAlert"] {
                animation: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    noi_dung = f"{config['icon']} {message}"

    if loai == "success":

        st.success(
            noi_dung,
            icon="✅",
        )

    elif loai == "error":

        st.error(
            noi_dung,
            icon="❌",
        )

    elif loai == "warning":

        st.warning(
            noi_dung,
            icon="⚠️",
        )

    else:

        st.info(
            noi_dung,
            icon="ℹ️",
        )


def thong_bao_thanh_cong(message):
    """
    Hiển thị thông báo thành công ngay lập tức.
    """

    _hien_thi_thong_bao(
        message,
        "✅",
        "success",
    )


def thong_bao_loi(message):
    """
    Hiển thị thông báo lỗi.
    """

    _hien_thi_thong_bao(
        message,
        "❌",
        "error",
    )


def thong_bao_canh_bao(message):
    """
    Hiển thị cảnh báo.
    """

    _hien_thi_thong_bao(
        message,
        "⚠️",
        "warning",
    )


def thong_bao_thong_tin(message):
    """
    Hiển thị thông tin.
    """

    _hien_thi_thong_bao(
        message,
        "ℹ️",
        "info",
    )


def luu_thong_bao(message, loai="success"):
    """
    Lưu thông báo để hiển thị sau khi st.rerun().
    """

    st.session_state[_NOTIFICATION_KEY] = {
        "message": message,
        "loai": loai,
    }


def hien_thi_thong_bao_da_luu():
    """
    Hiển thị thông báo đã lưu sau khi trang được rerun.
    """

    notification = st.session_state.pop(
        _NOTIFICATION_KEY,
        None,
    )

    if not notification:
        return

    message = notification.get(
        "message",
        "",
    )

    loai = notification.get(
        "loai",
        "success",
    )

    if loai == "success":

        thong_bao_thanh_cong(message)

    elif loai == "error":

        thong_bao_loi(message)

    elif loai == "warning":

        thong_bao_canh_bao(message)

    else:

        thong_bao_thong_tin(message)