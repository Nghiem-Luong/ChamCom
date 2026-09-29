# -*- coding: utf-8 -*-

from datetime import datetime

from Database.database import get_connection


class NguoiAnModel:

    @staticmethod
    def them_nguoi_an(
        ho_ten,
        sdt=None,
        bo_phan_id=None
    ):
        ho_ten = ho_ten.strip()

        if not ho_ten:
            raise ValueError("Họ tên không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO NguoiAn (
                    HoTen,
                    SDT,
                    BoPhanId,
                    DangHoatDong,
                    NgayTao
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                ho_ten,
                sdt,
                bo_phan_id,
                1,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    @staticmethod
    def lay_tat_ca():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    N.Id,
                    N.HoTen,
                    N.SDT,
                    N.BoPhanId,
                    B.TenBoPhan,
                    N.DangHoatDong,
                    N.NgayTao
                FROM NguoiAn N
                LEFT JOIN BoPhan B
                    ON N.BoPhanId = B.Id
                ORDER BY N.HoTen
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_dang_hoat_dong():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    N.Id,
                    N.HoTen,
                    N.SDT,
                    N.BoPhanId,
                    B.TenBoPhan,
                    N.DangHoatDong,
                    N.NgayTao
                FROM NguoiAn N
                LEFT JOIN BoPhan B
                    ON N.BoPhanId = B.Id
                WHERE N.DangHoatDong = 1
                ORDER BY N.HoTen
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_theo_bo_phan(bo_phan_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    N.Id,
                    N.HoTen,
                    N.SDT,
                    N.BoPhanId,
                    B.TenBoPhan,
                    N.DangHoatDong,
                    N.NgayTao
                FROM NguoiAn N
                LEFT JOIN BoPhan B
                    ON N.BoPhanId = B.Id
                WHERE N.BoPhanId = ?
                  AND N.DangHoatDong = 1
                ORDER BY N.HoTen
            """, (bo_phan_id,))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def tim_theo_id(nguoi_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    N.Id,
                    N.HoTen,
                    N.SDT,
                    N.BoPhanId,
                    B.TenBoPhan,
                    N.DangHoatDong,
                    N.NgayTao
                FROM NguoiAn N
                LEFT JOIN BoPhan B
                    ON N.BoPhanId = B.Id
                WHERE N.Id = ?
            """, (nguoi_an_id,))

            return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def tim_theo_ten(ho_ten):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    N.Id,
                    N.HoTen,
                    N.SDT,
                    N.BoPhanId,
                    B.TenBoPhan,
                    N.DangHoatDong,
                    N.NgayTao
                FROM NguoiAn N
                LEFT JOIN BoPhan B
                    ON N.BoPhanId = B.Id
                WHERE N.HoTen LIKE ?
                ORDER BY N.HoTen
            """, (f"%{ho_ten}%",))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def cap_nhat(
        nguoi_an_id,
        ho_ten,
        sdt=None,
        bo_phan_id=None
    ):
        ho_ten = ho_ten.strip()

        if not ho_ten:
            raise ValueError("Họ tên không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NguoiAn
                SET
                    HoTen = ?,
                    SDT = ?,
                    BoPhanId = ?
                WHERE Id = ?
            """, (
                ho_ten,
                sdt,
                bo_phan_id,
                nguoi_an_id
            ))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def ngung_hoat_dong(nguoi_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NguoiAn
                SET DangHoatDong = 0
                WHERE Id = ?
            """, (nguoi_an_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def kich_hoat_lai(nguoi_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NguoiAn
                SET DangHoatDong = 1
                WHERE Id = ?
            """, (nguoi_an_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()