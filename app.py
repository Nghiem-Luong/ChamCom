import streamlit as st

from Database.database_initializer import initialize_database
from Views.menu_view import hien_thi_menu

from Views.cham_com_view import hien_thi_cham_com
from Views.nguoi_an_view import hien_thi_nguoi_an
from Views.bo_phan_view import hien_thi_bo_phan
from Views.nop_tien_view import hien_thi_nop_tien
from Views.thong_ke_view import hien_thi_thong_ke
from Views.bao_cao_view import hien_thi_bao_cao
from Views.he_thong_view import hien_thi_he_thong
from Views.trang_chu_view import hien_thi_trang_chu
from Views.robot_assistant import hien_thi_robot

from Views.layout import cai_dat_giao_dien


# ==========================================================
# CẤU HÌNH ỨNG DỤNG
# ==========================================================

st.set_page_config(
    page_title="Quản lý Chấm Cơm",
    page_icon="🍚",
    layout="wide"
)


# ==========================================================
# GIAO DIỆN CHUNG
# ==========================================================

cai_dat_giao_dien()


# ==========================================================
# KHỞI TẠO DATABASE
# ==========================================================

initialize_database()


# ==========================================================
# MENU
# ==========================================================

lua_chon = hien_thi_menu()


# ==========================================================
# TRỢ LÝ AI
# ==========================================================

hien_thi_robot()


# ==========================================================
# ĐIỀU HƯỚNG TRANG
# ==========================================================

if lua_chon == "🏠 Trang chủ":

    hien_thi_trang_chu()


elif lua_chon == "🍚 Chấm cơm hôm nay":

    hien_thi_cham_com()


elif lua_chon == "👩‍🍳 Quản lý người ăn":

    hien_thi_nguoi_an()


elif lua_chon == "🏢 Quản lý bộ phận":

    hien_thi_bo_phan()


elif lua_chon == "💰 Nộp tiền & công nợ":

    hien_thi_nop_tien()


elif lua_chon == "📊 Thống kê":

    hien_thi_thong_ke()


elif lua_chon == "📑 Xuất báo cáo":

    hien_thi_bao_cao()


elif lua_chon == "🤖 Trợ lý & hệ thống":

    hien_thi_he_thong()