import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="SMARTSAVE 360",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CSS GIAO DIỆN
# =========================================================
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }

    .main-title {
        background: white;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .main-title h1 {
        color: #0b7a3b;
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }

    .control-title {
        background: #0b7a3b;
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .smart-box {
        background: white;
        border: 2px solid #0b7a3b;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
    }

    .smart-title {
        color: #0b7a3b;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .selected-box {
        background: #e8f5e9;
        border-left: 6px solid #0b7a3b;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 10px 0 15px 0;
    }

    .result-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .result-main {
        font-size: 30px;
        font-weight: bold;
        color: #0b7a3b;
    }

    .money {
        font-weight: bold;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================================================
# HÀM TÍNH NGÀY ĐÁO HẠN
# =========================================================
def tinh_ngay_dao_han(ngay_gui, ky_han_thang):
    return ngay_gui + relativedelta(months=ky_han_thang)


# =========================================================
# HÀM TÍNH LÃI THEO SỐ NGÀY
# =========================================================
def tinh_lai_theo_ngay(tien_goc, lai_suat, so_ngay):
    return tien_goc * (lai_suat / 100) * so_ngay / 365


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown("""
<div class="main-title">
    <h1>Số tiền gửi</h1>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SMARTSAVE 360
# =========================================================
st.markdown("""
<div class="smart-box">
    <div class="smart-title">SMARTSAVE 360</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# BẢNG ĐIỀU KHIỂN
# =========================================================
st.markdown("""
<div class="control-title">
    BẢNG ĐIỀU KHIỂN
</div>
""", unsafe_allow_html=True)


# =========================================================
# ĐANG CHỌN
# =========================================================
st.markdown("""
<div class="selected-box">
    <b>Đang chọn:</b> Tiết kiệm
</div>
""", unsafe_allow_html=True)


# =========================================================
# CHỌN NHANH
# =========================================================
st.button("Chọn nhanh")


# =========================================================
# NHẬP THÔNG TIN
# =========================================================
col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=0,
        value=500_000_000,
        step=1_000_000,
        format="%d"
    )

    lai_suat_co_han = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

    lai_suat_khong_ky_han = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1,
        format="%.2f"
    )

with col2:
    ngay_gui = st.date_input(
        "Ngày gửi tiền",
        value=date(2026, 8, 23)
    )

    ngay_rut = st.date_input(
        "Ngày rút tiền",
        value=date(2026, 11, 23)
    )

    ky_han = st.selectbox(
        "Kỳ hạn gửi tiền",
        options=[1, 2, 3, 6, 9, 12, 18, 24, 36],
        index=2,
        format_func=lambda x: f"{x} tháng"
    )


# =========================================================
# NGÀY ĐÁO HẠN
# =========================================================
ngay_dao_han = tinh_ngay_dao_han(ngay_gui, ky_han)

st.info(
    f"Ngày đáo hạn theo kỳ hạn đã chọn: **{ngay_dao_han.strftime('%d/%m/%Y')}**"
)


# =========================================================
# CÁCH NHẬN LÃI
# =========================================================
st.markdown("### Cách nhận tiền lãi")

cach_nhan_lai = st.radio(
    "Chọn phương thức nhận lãi",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ],
    horizontal=True
)


# =========================================================
# TÍNH TOÁN
# =========================================================
if st.button("TÍNH TOÁN", type="primary"):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif ngay_rut < ngay_gui:
        st.error("Ngày rút tiền không được nhỏ hơn ngày gửi tiền.")

    else:

        # -------------------------------------------------
        # TRƯỜNG HỢP 1: RÚT TRƯỚC HẠN
        # -------------------------------------------------
        if ngay_rut < ngay_dao_han:

            so_ngay = (ngay_rut - ngay_gui).days

            lai = tinh_lai_theo_ngay(
                tien_gui,
                lai_suat_khong_ky_han,
                so_ngay
            )

            tong_tien = tien_gui + lai

            trang_thai = "Rút trước hạn"

            lai_ap_dung = lai_suat_khong_ky_han

            st.warning(
                "Khách hàng rút trước hạn nên toàn bộ thời gian gửi "
                "được tính theo lãi suất không kỳ hạn."
            )

        # -------------------------------------------------
        # TRƯỜNG HỢP 2: RÚT ĐÚNG NGÀY ĐÁO HẠN
        # -------------------------------------------------
        elif ngay_rut == ngay_dao_han:

            so_ngay = (ngay_dao_han - ngay_gui).days

            lai = tinh_lai_theo_ngay(
                tien_gui,
                lai_suat_co_han,
                so_ngay
            )

            tong_tien = tien_gui + lai

            trang_thai = "Rút đúng hạn"

            lai_ap_dung = lai_suat_co_han

        # -------------------------------------------------
        # TRƯỜNG HỢP 3: RÚT SAU NGÀY ĐÁO HẠN
        # -------------------------------------------------
        else:

            # Số kỳ hạn đã hoàn thành
            so_ky_da_gia_han = 0
            moc_dao_han = ngay_dao_han

            while ngay_rut > moc_dao_han:
                so_ky_da_gia_han += 1
                moc_dao_han = moc_dao_han + relativedelta(months=ky_han)

            # Ngày bắt đầu của kỳ hiện tại
            ngay_bat_dau_ky = moc_dao_han - relativedelta(months=ky_han)

            # Lãi của các kỳ đã hoàn thành
            lai_moi_ky = tinh_lai_theo_ngay(
                tien_gui,
                lai_suat_co_han,
                (ngay_bat_dau_ky - ngay_gui).days
            )

            # Lãi kỳ hiện tại
            so_ngay_ky_hien_tai = (ngay_rut - ngay_bat_dau_ky).days

            lai_ky_hien_tai = tinh_lai_theo_ngay(
                tien_gui,
                lai_suat_co_han,
                so_ngay_ky_hien_tai
            )

            # Tổng lãi
            lai = lai_moi_ky * so_ky_da_gia_han + lai_ky_hien_tai

            tong_tien = tien_gui + lai

            trang_thai = "Đã tự động gia hạn"

            lai_ap_dung = lai_suat_co_han


        # =================================================
        # HIỂN THỊ KẾT QUẢ
        # =================================================
        st.markdown("## KẾT QUẢ")

        r1, r2 = st.columns(2)

        with r1:
            st.markdown(
                f"""
                <div class="result-box">
                    <p>Trạng thái</p>
                    <h3>{trang_thai}</h3>
                    <p>Phương thức nhận lãi</p>
                    <h3>{cach_nhan_lai}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with r2:
            st.markdown(
                f"""
                <div class="result-box">
                    <p>Tổng số tiền khách hàng nhận được</p>
                    <div class="result-main">
                        {format_money(tong_tien)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =================================================
        # CHI TIẾT
        # =================================================
        st.markdown("### Chi tiết tiền nhận")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Tiền gốc",
                format_money(tien_gui)
            )

        with c2:
            st.metric(
                "Tiền lãi",
                format_money(lai)
            )

        with c3:
            st.metric(
                "Lãi suất áp dụng",
                f"{lai_ap_dung:.2f}%/năm"
            )

        with c4:
            st.metric(
                "Số ngày tính lãi",
                f"{so_ngay} ngày"
            )


        # =================================================
        # XỬ LÝ 3 PHƯƠNG THỨC NHẬN LÃI
        # =================================================
        st.markdown("### Phân tích phương thức nhận lãi")

        if cach_nhan_lai == "Nhận lãi trước":

            lai_truoc = tinh_lai_theo_ngay(
                tien_gui,
                lai_ap_dung,
                so_ngay
            )

            tien_thuc_nhan = tien_gui

            st.write(
                f"Tiền lãi nhận trước: **{format_money(lai_truoc)}**"
            )

            st.write(
                f"Tiền gốc nhận khi rút: **{format_money(tien_thuc_nhan)}**"
            )

            st.write(
                f"Tổng giá trị khách hàng nhận: "
                f"**{format_money(lai_truoc + tien_thuc_nhan)}**"
            )

        elif cach_nhan_lai == "Nhận lãi hàng kỳ":

            # Với kỳ hạn tháng, ước tính lãi mỗi tháng
            lai_moi_thang = tien_gui * (lai_ap_dung / 100) / 12

            so_thang = max(1, so_ngay // 30)

            tong_lai_hang_ky = lai_moi_thang * so_thang

            st.write(
                f"Lãi dự kiến mỗi tháng: "
                f"**{format_money(lai_moi_thang)}**"
            )

            st.write(
                f"Tổng lãi đã tính: "
                f"**{format_money(tong_lai_hang_ky)}**"
            )

            st.write(
                f"Tổng gốc + lãi: "
                f"**{format_money(tien_gui + tong_lai_hang_ky)}**"
            )

        else:

            st.write(
                f"Tiền gốc: **{format_money(tien_gui)}**"
            )

            st.write(
                f"Tiền lãi cuối kỳ: **{format_money(lai)}**"
            )

            st.write(
                f"Tổng tiền nhận cuối kỳ: "
                f"**{format_money(tien_gui + lai)}**"
            )
