# -*- coding: utf-8 -*-

from datetime import datetime

from Database.database import get_connection


class BoPhanModel:

    @staticmethod
    def them_bo_phan(ten_bo_phan):
        ten_bo_phan = ten_bo_phan.strip()

        if not ten_bo_phan:
            raise ValueError("Tên bộ phận không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO BoPhan (
                    TenBoPhan,
                    DangHoatDong,
                    NgayTao
                )
                VALUES (?, ?, ?)
            """, (
                ten_bo_phan,
                1,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                    Id,
                    TenBoPhan,
                    DangHoatDong,
                    NgayTao
                FROM BoPhan
                ORDER BY TenBoPhan
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
                    Id,
                    TenBoPhan,
                    DangHoatDong,
                    NgayTao
                FROM BoPhan
                WHERE DangHoatDong = 1
                ORDER BY TenBoPhan
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def tim_theo_id(bo_phan_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    TenBoPhan,
                    DangHoatDong,
                    NgayTao
                FROM BoPhan
                WHERE Id = ?
            """, (bo_phan_id,))

            return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def tim_theo_ten(ten_bo_phan):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    TenBoPhan,
                    DangHoatDong,
                    NgayTao
                FROM BoPhan
                WHERE TenBoPhan LIKE ?
                ORDER BY TenBoPhan
            """, (f"%{ten_bo_phan}%",))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def cap_nhat(bo_phan_id, ten_bo_phan):
        ten_bo_phan = ten_bo_phan.strip()

        if not ten_bo_phan:
            raise ValueError("Tên bộ phận không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE BoPhan
                SET TenBoPhan = ?
                WHERE Id = ?
            """, (
                ten_bo_phan,
                bo_phan_id
            ))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def ngung_hoat_dong(bo_phan_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE BoPhan
                SET DangHoatDong = 0
                WHERE Id = ?
            """, (bo_phan_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def kich_hoat_lai(bo_phan_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE BoPhan
                SET DangHoatDong = 1
                WHERE Id = ?
            """, (bo_phan_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()