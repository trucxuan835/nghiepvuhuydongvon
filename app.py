import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

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
    .main-title {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .smart-box {
        border: 2px solid #198754;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        background-color: #ffffff;
    }

    .smart-title {
        font-size: 25px;
        font-weight: 800;
        color: #198754;
        text-align: center;
        margin-bottom: 15px;
    }

    .green-box {
        background-color: #198754;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .selected-box {
        background-color: #198754;
        color: white;
        padding: 8px 14px;
        border-radius: 7px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .result-box {
        border: 2px solid #198754;
        border-radius: 10px;
        padding: 18px;
        background-color: #f8fff9;
        margin-top: 15px;
    }

    .money {
        font-size: 25px;
        font-weight: 800;
        color: #198754;
    }

    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffecb5;
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
    }

    .info-box {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG
# =========================================================
def vnd(value):
    return f"{value:,.0f} VNĐ"


def percent(value):
    return f"{value:.2f}%"


def add_months(d, months):
    return d + relativedelta(months=months)


# =========================================================
# HÀM TÍNH LÃI
# =========================================================
def tinh_lai(
    tien_goc,
    lai_co_ky_han,
    lai_khong_ky_han,
    ngay_gui,
    ngay_rut,
    ky_han_thang,
    phuong_thuc
):
    """
    Quy ước:
    - Ngày bắt đầu tính lãi: ngày gửi.
    - Ngày kết thúc tính lãi: trước ngày rút.
    - Số ngày = ngày_rút - ngày_gửi.
    - Mỗi kỳ đúng bằng kỳ hạn đã chọn.
    - Nếu đã hết kỳ hạn mà chưa rút -> tự động gia hạn cùng kỳ hạn.
    - Phần thời gian chưa đủ một kỳ được tính lãi không kỳ hạn.
    """

    if ngay_rut <= ngay_gui:
        return None, "Ngày rút tiền phải sau ngày gửi tiền."

    if tien_goc <= 0:
        return None, "Số tiền gửi phải lớn hơn 0."

    if ky_han_thang <= 0:
        return None, "Kỳ hạn phải lớn hơn 0."

    # Tổng số ngày thực tế
    tong_so_ngay = (ngay_rut - ngay_gui).days

    # Ngày đáo hạn ban đầu
    ngay_dao_han_dau = add_months(ngay_gui, ky_han_thang)

    # =====================================================
    # RÚT TRƯỚC HẠN
    # =====================================================
    if ngay_rut < ngay_dao_han_dau:
        lai = tien_goc * lai_khong_ky_han / 100 * tong_so_ngay / 365

        chi_tiet = [{
            "Kỳ": "Kỳ 1",
            "Loại kỳ tính lãi": "Lãi không kỳ hạn – rút trước hạn",
            "Từ ngày": ngay_gui.strftime("%d/%m/%Y"),
            "Đến trước ngày": ngay_rut.strftime("%d/%m/%Y"),
            "Số ngày": tong_so_ngay,
            "Lãi suất": lai_khong_ky_han,
            "Tiền lãi": lai
        }]

        tong_nhan = tien_goc + lai

        return {
            "loai": "Rút trước hạn",
            "tong_ngay": tong_so_ngay,
            "lai": lai,
            "tong_nhan": tong_nhan,
            "chi_tiet": chi_tiet,
            "ngay_dao_han_dau": ngay_dao_han_dau
        }, None

    # =====================================================
    # ĐÃ ĐẾN HẠN / TỰ ĐỘNG GIA HẠN
    # =====================================================
    chi_tiet = []

    ngay_bat_dau_ky = ngay_gui
    tong_lai_co_ky_han = 0
    tong_lai_khong_ky_han = 0
    ky = 1

    while True:

        ngay_ket_thuc_ky = add_months(ngay_bat_dau_ky, ky_han_thang)

        # Trường hợp rút đúng ngày kết thúc kỳ
        if ngay_rut == ngay_ket_thuc_ky:
            so_ngay = (ngay_rut - ngay_bat_dau_ky).days

            lai_ky = (
                tien_goc
                * lai_co_ky_han / 100
                * so_ngay / 365
            )

            tong_lai_co_ky_han += lai_ky

            chi_tiet.append({
                "Kỳ": f"Kỳ {ky}",
                "Loại kỳ tính lãi": f"Lãi có kỳ hạn – Kỳ {ky}",
                "Từ ngày": ngay_bat_dau_ky.strftime("%d/%m/%Y"),
                "Đến trước ngày": ngay_rut.strftime("%d/%m/%Y"),
                "Số ngày": so_ngay,
                "Lãi suất": lai_co_ky_han,
                "Tiền lãi": lai_ky
            })

            break

        # Trường hợp chưa đủ hết kỳ
        if ngay_rut < ngay_ket_thuc_ky:
            so_ngay = (ngay_rut - ngay_bat_dau_ky).days

            lai_khong_han = (
                tien_goc
                * lai_khong_ky_han / 100
                * so_ngay / 365
            )

            tong_lai_khong_ky_han += lai_khong_han

            chi_tiet.append({
                "Kỳ": f"Kỳ {ky}",
                "Loại kỳ tính lãi": f"Lãi không kỳ hạn – phần dư Kỳ {ky}",
                "Từ ngày": ngay_bat_dau_ky.strftime("%d/%m/%Y"),
                "Đến trước ngày": ngay_rut.strftime("%d/%m/%Y"),
                "Số ngày": so_ngay,
                "Lãi suất": lai_khong_ky_han,
                "Tiền lãi": lai_khong_han
            })

            break

        # Đã hoàn thành một kỳ
        so_ngay = (ngay_ket_thuc_ky - ngay_bat_dau_ky).days

        lai_ky = (
            tien_goc
            * lai_co_ky_han / 100
            * so_ngay / 365
        )

        tong_lai_co_ky_han += lai_ky

        chi_tiet.append({
            "Kỳ": f"Kỳ {ky}",
            "Loại kỳ tính lãi": f"Lãi có kỳ hạn – Kỳ {ky}",
            "Từ ngày": ngay_bat_dau_ky.strftime("%d/%m/%Y"),
            "Đến trước ngày": ngay_ket_thuc_ky.strftime("%d/%m/%Y"),
            "Số ngày": so_ngay,
            "Lãi suất": lai_co_ky_han,
            "Tiền lãi": lai_ky
        })

        # Sang kỳ tiếp theo -> tự động gia hạn
        ngay_bat_dau_ky = ngay_ket_thuc_ky
        ky += 1

    tong_lai = tong_lai_co_ky_han + tong_lai_khong_ky_han

    # =====================================================
    # TÍNH THEO PHƯƠNG THỨC NHẬN LÃI
    # =====================================================

    # Nhận lãi cuối kỳ:
    # Gốc + toàn bộ lãi được nhận tại ngày rút.
    if phuong_thuc == "Nhận lãi cuối kỳ":
        tong_nhan = tien_goc + tong_lai

    # Nhận lãi hàng kỳ:
    # Lãi của mỗi kỳ hoàn thành được trả từng kỳ.
    # Phần dư cuối cùng nếu chưa đủ kỳ -> lãi không kỳ hạn.
    elif phuong_thuc == "Nhận lãi hàng kỳ":
        tong_nhan = tien_goc + tong_lai

    # Nhận lãi trước:
    # Lãi của từng kỳ được nhận đầu mỗi kỳ.
    # Tổng dòng tiền nhận = gốc cuối kỳ + toàn bộ lãi.
    elif phuong_thuc == "Nhận lãi trước":
        tong_nhan = tien_goc + tong_lai

    else:
        tong_nhan = tien_goc + tong_lai

    return {
        "loai": "Đáo hạn / tự động gia hạn",
        "tong_ngay": tong_so_ngay,
        "lai": tong_lai,
        "lai_co_ky_han": tong_lai_co_ky_han,
        "lai_khong_ky_han": tong_lai_khong_ky_han,
        "tong_nhan": tong_nhan,
        "chi_tiet": chi_tiet,
        "ngay_dao_han_dau": ngay_dao_han_dau
    }, None


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown(
    '<div class="main-title">Số tiền gửi</div>',
    unsafe_allow_html=True
)

# =========================================================
# KHUNG SMARTSAVE 360
# =========================================================
st.markdown("""
<div class="smart-box">
    <div class="smart-title">SMARTSAVE 360</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# BẢNG ĐIỀU KHIỂN
# =========================================================
st.markdown(
    '<div class="green-box">BẢNG ĐIỀU KHIỂN</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown(
        '<div class="selected-box">Đang chọn</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### Chọn nhanh")


# =========================================================
# NÚT CHỌN NHANH
# =========================================================
if "so_tien" not in st.session_state:
    st.session_state.so_tien = 500_000_000
    st.session_state.lai_co_ky_han = 5.0
    st.session_state.lai_khong_ky_han = 0.2
    st.session_state.ngay_gui = date(2026, 8, 23)
    st.session_state.ngay_rut = date(2026, 11, 23)
    st.session_state.ky_han = 3
    st.session_state.phuong_thuc = "Nhận lãi cuối kỳ"

quick = st.button("Chọn nhanh", use_container_width=True)

if quick:
    st.session_state.so_tien = 500_000_000
    st.session_state.lai_co_ky_han = 5.0
    st.session_state.lai_khong_ky_han = 0.2
    st.session_state.ngay_gui = date(2026, 8, 23)
    st.session_state.ngay_rut = date(2026, 11, 23)
    st.session_state.ky_han = 3
    st.session_state.phuong_thuc = "Nhận lãi cuối kỳ"
    st.rerun()


# =========================================================
# NHẬP THÔNG TIN
# =========================================================
st.markdown("### Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=0,
        step=1_000_000,
        value=st.session_state.so_tien
    )

    lai_co_ky_han = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        max_value=100.0,
        step=0.01,
        value=st.session_state.lai_co_ky_han
    )

    lai_khong_ky_han = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        max_value=100.0,
        step=0.01,
        value=st.session_state.lai_khong_ky_han
    )

with col2:
    ngay_gui = st.date_input(
        "Ngày gửi tiền",
        value=st.session_state.ngay_gui,
        format="DD/MM/YYYY"
    )

    ngay_rut = st.date_input(
        "Ngày rút tiền",
        value=st.session_state.ngay_rut,
        format="DD/MM/YYYY"
    )

    ky_han = st.selectbox(
        "Kỳ hạn gửi tiền",
        options=[1, 2, 3, 6, 9, 12, 18, 24, 36],
        index=[1, 2, 3, 6, 9, 12, 18, 24, 36].index(
            st.session_state.ky_han
        ),
        format_func=lambda x: f"{x} tháng"
    )


# =========================================================
# PHƯƠNG THỨC NHẬN LÃI
# =========================================================
st.markdown("### Phương thức nhận tiền lãi")

phuong_thuc = st.radio(
    "Khách hàng lựa chọn:",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ],
    index=[
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ].index(st.session_state.phuong_thuc),
    horizontal=True
)


# =========================================================
# THÔNG TIN TỰ ĐỘNG
# =========================================================
ngay_dao_han = add_months(ngay_gui, ky_han)

st.markdown(
    f"""
    <div class="info-box">
    <b>Ngày đáo hạn kỳ đầu:</b> {ngay_dao_han.strftime("%d/%m/%Y")}
    <br>
    <b>Nguyên tắc:</b> Nếu chưa rút khi đến hạn, tiền gửi sẽ tự động
    gia hạn thêm đúng {ky_han} tháng.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NÚT TÍNH TOÁN
# =========================================================
st.markdown("")

tinh = st.button(
    "TÍNH TOÁN",
    type="primary",
    use_container_width=True
)


# =========================================================
# KẾT QUẢ
# =========================================================
if tinh:

    ket_qua, loi = tinh_lai(
        so_tien,
        lai_co_ky_han,
        lai_khong_ky_han,
        ngay_gui,
        ngay_rut,
        ky_han,
        phuong_thuc
    )

    if loi:
        st.error(loi)

    else:

        # -------------------------------------------------
        # THÔNG BÁO TRẠNG THÁI
        # -------------------------------------------------
        if ket_qua["loai"] == "Rút trước hạn":
            st.warning(
                "Khách hàng rút trước hạn. Toàn bộ thời gian gửi "
                "được tính theo lãi suất không kỳ hạn."
            )
        else:
            st.success(
                "Khoản tiền đã đến hạn hoặc đã hoàn thành một hoặc "
                "nhiều kỳ. Hệ thống tự động tính các kỳ gia hạn."
            )

        # -------------------------------------------------
        # TỔNG QUAN
        # -------------------------------------------------
        st.markdown("## Kết quả tính tiền")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Tiền gốc",
                vnd(so_tien)
            )

        with c2:
            st.metric(
                "Tổng tiền lãi",
                vnd(ket_qua["lai"])
            )

        with c3:
            st.metric(
                "Tổng tiền khách nhận",
                vnd(ket_qua["tong_nhan"])
            )

        # -------------------------------------------------
        # CHI TIẾT PHÂN LOẠI LÃI
        # -------------------------------------------------
        if ket_qua["loai"] != "Rút trước hạn":

            c1, c2 = st.columns(2)

            with c1:
                st.markdown(
                    f"""
                    <div class="result-box">
                    <b>Lãi có kỳ hạn</b>
                    <div class="money">
                    {vnd(ket_qua["lai_co_ky_han"])}
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"""
                    <div class="result-box">
                    <b>Lãi không kỳ hạn</b>
                    <div class="money">
                    {vnd(ket_qua["lai_khong_ky_han"])}
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -------------------------------------------------
        # PHƯƠNG THỨC NHẬN LÃI
        # -------------------------------------------------
        st.markdown("### Phương thức nhận lãi")

        if phuong_thuc == "Nhận lãi trước":
            st.info(
                "Khách hàng nhận tiền lãi của kỳ ngay từ đầu kỳ. "
                "Kết quả tổng dòng tiền gồm tiền lãi đã nhận "
                "và tiền gốc nhận khi rút."
            )

        elif phuong_thuc == "Nhận lãi hàng kỳ":
            st.info(
                "Khách hàng nhận tiền lãi sau mỗi kỳ hoàn thành. "
                "Các kỳ được thể hiện riêng tại bảng chi tiết."
            )

        else:
            st.info(
                "Khách hàng nhận toàn bộ tiền lãi cùng tiền gốc "
                "khi rút tiền."
            )

        # -------------------------------------------------
        # BẢNG CHI TIẾT
        # -------------------------------------------------
        st.markdown("### Chi tiết kỳ tính lãi")

        df = pd.DataFrame(ket_qua["chi_tiet"])

        if not df.empty:

            df["Lãi suất"] = df["Lãi suất"].apply(
                lambda x: f"{x:.2f}%/năm"
            )

            df["Tiền lãi"] = df["Tiền lãi"].apply(
                lambda x: f"{x:,.0f} VNĐ"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        # -------------------------------------------------
        # GIẢI THÍCH
        # -------------------------------------------------
        st.markdown("### Tổng hợp")

        st.write(
            f"**Số ngày tính lãi:** {ket_qua['tong_ngay']} ngày"
        )

        st.write(
            f"**Ngày gửi:** {ngay_gui.strftime('%d/%m/%Y')}"
        )

        st.write(
            f"**Ngày rút:** {ngay_rut.strftime('%d/%m/%Y')}"
        )

        st.write(
            f"**Kỳ hạn:** {ky_han} tháng"
        )

        st.write(
            f"**Lãi suất có kỳ hạn:** "
            f"{lai_co_ky_han:.2f}%/năm"
        )

        st.write(
            f"**Lãi suất không kỳ hạn:** "
            f"{lai_khong_ky_han:.2f}%/năm"
        )

        st.markdown(
            f"""
            <div class="result-box">
                <div><b>TIỀN GỐC:</b> {vnd(so_tien)}</div>
                <div><b>TỔNG TIỀN LÃI:</b> {vnd(ket_qua['lai'])}</div>
                <hr>
                <div class="money">
                    TỔNG TIỀN KHÁCH HÀNG NHẬN:
                    {vnd(ket_qua['tong_nhan'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # LƯU Ý
        # -------------------------------------------------
        st.markdown(
            """
            <div class="warning-box">
            <b>Quy ước tính của SMARTSAVE 360:</b><br>
            • Ngày gửi được tính là ngày bắt đầu tính lãi.<br>
            • Ngày rút không tính lãi, tức tính đến trước 1 ngày rút.<br>
            • Rút trước hạn: tính lãi không kỳ hạn cho toàn bộ số ngày thực gửi.<br>
            • Đủ một kỳ hạn: tính theo lãi suất có kỳ hạn của kỳ đó.<br>
            • Nếu không rút khi đến hạn: tự động gia hạn đúng kỳ hạn ban đầu.<br>
            • Phần thời gian chưa đủ một kỳ sau khi gia hạn được tính theo lãi suất không kỳ hạn.<br>
            • Mỗi kỳ được ghi rõ Kỳ 1, Kỳ 2, Kỳ 3... trong bảng chi tiết.
            </div>
            """,
            unsafe_allow_html=True
        )
