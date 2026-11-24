import streamlit as st
import sqlite3
from pathlib import Path
from datetime import datetime
import math

# ============================================================
# BIDV HOME FINANCE - PERSONAL ADVISOR LANDING PAGE (MVP)
# Run: streamlit run app.py
# ============================================================

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "leads.db"

ADVISOR_NAME = "Mã Văn Duẩn"
PHONE_DISPLAY = "0989 211 684"
PHONE_TEL = "0989211684"
ZALO_URL = "https://zalo.me/0989211684"

# Các thông tin dưới đây được nhập từ poster tham chiếu.
# Xác minh chính sách hiện hành và quyền sử dụng thương hiệu trước khi công bố.
PRODUCTS = {
    "Mua nhà ở": {"ltv": 0.80, "max_years": 30, "grace_months": 36},
    "Mua / đầu tư BĐS kinh doanh": {"ltv": 0.60, "max_years": 20, "grace_months": 36},
}
RATE_PLANS = [
    ("12 tháng đầu", 9.5),
    ("18 tháng đầu", 10.0),
    ("24 tháng đầu", 10.5),
    ("30 tháng đầu", 11.3),
    ("36 tháng đầu", 11.8),
]
PROJECTS = [
    "The Meadow", "Eaton Park", "Elysian", "Artisan Park",
    "Celadon City", "Spring Ville Đồng Nai",
    "Ambience Gamuda Hải Phòng", "Norton Park",
    "Gamuda Central Park Yên Sở",
]

st.set_page_config(
    page_title="Giải pháp tài chính cho tổ ấm tương lai",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------- CSS -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root { --green:#006b68; --dark:#064b49; --gold:#c58a24; --cream:#fbf7ee; --ink:#183536; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
.stApp { background:#fff; }
.block-container { max-width:1120px; padding-top:1rem; padding-bottom:5rem; }
.brand {font-size:32px;font-weight:800;letter-spacing:-1.5px;color:var(--green);margin:0;}
.brand span {color:#e3a627;}
.eyebrow {color:var(--green);font-weight:800;letter-spacing:2px;font-size:12px;text-transform:uppercase;}
.hero {padding:3.2rem 2.6rem;border-radius:24px;background:linear-gradient(90deg,rgba(255,251,242,.97),rgba(255,251,242,.84),rgba(255,251,242,.35)),url('https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1800&q=85');background-size:cover;background-position:center;border:1px solid #eee4d3;}
.hero h1 {font-family:'Playfair Display',serif;font-size:clamp(34px,5vw,58px);line-height:1.08;color:#123738;margin:.6rem 0;}
.hero h1 span {color:#b67b22;}
.hero p {font-size:17px;max-width:600px;color:#526360;}
.section-title {font-family:'Playfair Display',serif;font-size:32px;font-weight:700;color:#173c3b;margin-bottom:.2rem;}
.subtle {color:#687672;font-size:14px;}
.product-card {background:#fff;border:1px solid #e9e1d2;border-radius:18px;padding:20px;box-shadow:0 8px 28px rgba(33,52,47,.07);height:100%;}
.metric {background:#fffcf6;border:1px solid #f0e8d9;border-radius:12px;padding:12px 8px;text-align:center;}
.metric strong {display:block;color:#a66c1d;font-family:'Playfair Display',serif;font-size:25px;}
.metric small {color:#667575;font-size:11px;}
.rate-card {background:#fffcf6;border:1px solid #f0e8d9;border-radius:12px;padding:14px;text-align:center;height:100%;}
.rate-card strong {display:block;color:#a66c1d;font-family:'Playfair Display',serif;font-size:25px;}
.result-card {background:linear-gradient(145deg,#075f5c,#003f40);color:white;border-radius:18px;padding:22px;}
.result-card .amount {font-family:'Playfair Display',serif;font-size:34px;color:#f6d58c;font-weight:700;}
.result-card small {color:#d1e4df;}
.contact-card {background:linear-gradient(145deg,#075f5c,#003f40);color:white;border-radius:20px;padding:25px;}
div.stButton > button, div.stLinkButton > a {border-radius:999px;font-weight:700;}
div.stButton > button[kind="primary"] {background:#006b68;border-color:#006b68;}
a {color:#006b68;}
footer {visibility:hidden;}
@media(max-width:700px) {
 .block-container {padding-left:1rem;padding-right:1rem;}
 .hero {padding:2rem 1.2rem;background-position:62% center;}
 .hero h1 {font-size:36px;}
 .section-title {font-size:27px;}
}
</style>
""", unsafe_allow_html=True)

# ----------------------- Utilities ----------------------------
def money_vnd(value: float) -> str:
    return f"{max(0, value):,.0f}".replace(",", ".") + " đ"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                need TEXT NOT NULL,
                project TEXT,
                message TEXT
            )
        """)
        conn.commit()

def save_lead(full_name, phone, need, project, message):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO leads (created_at, full_name, phone, need, project, message)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(timespec="seconds"), full_name, phone, need, project, message)
        )
        conn.commit()

def simulate_loan(principal, annual_rate_pct, years, method, grace_months):
    """Mô phỏng dư nợ giảm dần; trong ân hạn chỉ trả lãi, gốc chia cho kỳ còn lại."""
    principal = max(0.0, float(principal))
    months = max(1, int(years) * 12)
    grace = min(max(0, int(grace_months)), months - 1)
    monthly_rate = max(0.0, float(annual_rate_pct)) / 100 / 12
    repay_months = months - grace
    fixed_principal = principal / repay_months if repay_months else principal
    if monthly_rate == 0:
        annuity_payment = principal / repay_months if repay_months else principal
    else:
        annuity_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-repay_months))

    balance = principal
    total_interest = 0.0
    schedule = []
    for month in range(1, months + 1):
        interest = balance * monthly_rate
        if month <= grace:
            principal_payment = 0.0
        elif method == "Gốc đều, lãi giảm dần":
            principal_payment = min(balance, fixed_principal)
        else:
            principal_payment = min(balance, max(0.0, annuity_payment - interest))
        payment = principal_payment + interest
        total_interest += interest
        schedule.append({
            "month": month,
            "opening_balance": balance,
            "principal": principal_payment,
            "interest": interest,
            "payment": payment,
            "closing_balance": max(0.0, balance - principal_payment),
        })
        balance = max(0.0, balance - principal_payment)

    return schedule, total_interest

def clean_phone(phone):
    return "".join(ch for ch in phone if ch.isdigit() or ch == "+")

init_db()

# -------------------------- Header ----------------------------
header_left, header_right = st.columns([2, 1])
with header_left:
    st.markdown('<p class="brand">BIDV<span> ✳</span></p>', unsafe_allow_html=True)
with header_right:
    st.markdown("<div style='text-align:right;padding-top:9px;color:#687672;font-size:13px'>CHUYÊN VIÊN TƯ VẤN TÍN DỤNG</div>", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Giải pháp tài chính bất động sản</div>
  <h1>GIẢI PHÁP TÀI CHÍNH<br><span>CHO TỔ ẤM TƯƠNG LAI</span></h1>
  <p>Đồng hành cùng bạn lựa chọn phương án tài chính phù hợp cho kế hoạch an cư và đầu tư bất động sản.</p>
</div>
""", unsafe_allow_html=True)

cta1, cta2, cta3 = st.columns([1, 1, 1])
with cta1:
    st.link_button("☎ Gọi tư vấn", f"tel:{PHONE_TEL}", use_container_width=True)
with cta2:
    st.link_button("◉ Tư vấn ngay qua Zalo", ZALO_URL, use_container_width=True)
with cta3:
    st.button("↓ Tính khoản vay", on_click=lambda: st.session_state.update({"jump_calculator": True}), use_container_width=True)

if st.session_state.pop("jump_calculator", False):
    st.markdown('<div id="calculator"></div>', unsafe_allow_html=True)

st.divider()

# -------------------------- Products --------------------------
st.markdown('<div class="eyebrow">Giải pháp theo nhu cầu</div><div class="section-title">Lựa chọn phương án phù hợp</div>', unsafe_allow_html=True)
st.markdown('<p class="subtle">Thông tin tham khảo theo tài liệu đầu vào; điều kiện thực tế phụ thuộc hồ sơ và phê duyệt tín dụng.</p>', unsafe_allow_html=True)
p1, p2 = st.columns(2)
for col, (name, info) in zip([p1, p2], PRODUCTS.items()):
    with col:
        with st.container(border=True):
            st.subheader(name)
            m1, m2, m3 = st.columns(3)
            m1.markdown(f'<div class="metric"><small>Vay tối đa</small><strong>{info["ltv"]*100:.0f}%</strong></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric"><small>Thời hạn</small><strong>{info["max_years"]} năm</strong></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="metric"><small>Ân hạn gốc</small><strong>{info["grace_months"]} tháng</strong></div>', unsafe_allow_html=True)

st.caption("Các tỷ lệ, thời hạn và thời gian ân hạn là thông tin tham khảo tối đa, không phải cam kết cấp tín dụng.")

# --------------------------- Rates ----------------------------
st.divider()
st.markdown('<div class="eyebrow">Chương trình lãi suất tham khảo</div><div class="section-title">Lựa chọn thời gian ưu đãi</div>', unsafe_allow_html=True)
rate_cols = st.columns(5)
for col, (period, rate) in zip(rate_cols, RATE_PLANS):
    with col:
        st.markdown(f'<div class="rate-card"><small>Từ</small><strong>{rate:.1f}%</strong><small>/năm</small><p style="font-size:12px;margin-bottom:0">{period}</p></div>', unsafe_allow_html=True)
st.caption("Lãi suất và điều kiện áp dụng phải được xác nhận tại thời điểm tư vấn. Lãi suất sau ưu đãi có thể thay đổi theo thỏa thuận và chính sách ngân hàng.")

# ------------------------ Calculator --------------------------
st.divider()
st.markdown('<div id="calculator"></div><div class="eyebrow">Công cụ mô phỏng</div><div class="section-title">Tính khoản vay dự kiến</div>', unsafe_allow_html=True)
st.markdown('<p class="subtle">Điều chỉnh thông tin để ước tính vốn tự có và nghĩa vụ trả nợ hàng tháng.</p>', unsafe_allow_html=True)

with st.container(border=True):
    c_input, c_result = st.columns([1.05, 0.95], gap="large")
    with c_input:
        purpose = st.selectbox("Nhu cầu vay", list(PRODUCTS.keys()))
        product = PRODUCTS[purpose]
        property_value = st.number_input("Giá trị bất động sản (VNĐ)", min_value=100_000_000, max_value=100_000_000_000, value=3_000_000_000, step=100_000_000, format="%d")
        max_loan = int(property_value * product["ltv"])
        loan_amount = st.number_input("Số tiền vay mong muốn (VNĐ)", min_value=0, max_value=max_loan, value=min(2_100_000_000, max_loan), step=50_000_000, format="%d")
        default_rate = 9.5
        rate = st.number_input("Lãi suất năm (%)", min_value=0.0, max_value=30.0, value=default_rate, step=0.1)
        years = st.slider("Thời hạn vay (năm)", min_value=1, max_value=product["max_years"], value=min(25, product["max_years"]))
        method = st.selectbox("Phương thức trả nợ", ["Gốc đều, lãi giảm dần", "Trả góp đều hàng tháng"])
        grace = st.selectbox("Thời gian ân hạn gốc", [0, 12, 24, 36], index=3, format_func=lambda x: f"{x} tháng" if x else "Không ân hạn")
        st.caption(f"Tỷ lệ vay tối đa tham khảo: {product['ltv']*100:.0f}% · Hạn mức theo giá trị tài sản: {money_vnd(max_loan)}")

    schedule, total_interest = simulate_loan(loan_amount, rate, years, method, grace)
    first = schedule[0] if schedule else {"payment": 0, "principal": 0, "interest": 0}
    max_payment = max((row["payment"] for row in schedule), default=0)
    equity = max(0, property_value - loan_amount)
    ltv_actual = (loan_amount / property_value * 100) if property_value else 0

    with c_result:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("<small>Khoản trả dự kiến tháng đầu tiên</small>", unsafe_allow_html=True)
        st.markdown(f'<div class="amount">{money_vnd(first["payment"])}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
          <div><small>Số tiền vay</small><br><b>{money_vnd(loan_amount)}</b></div>
          <div><small>Vốn tự có</small><br><b>{money_vnd(equity)}</b></div>
          <div><small>Tỷ lệ vay thực tế</small><br><b>{ltv_actual:.1f}%</b></div>
          <div><small>Tổng lãi mô phỏng</small><br><b>{money_vnd(total_interest)}</b></div>
        </div></div>
        """, unsafe_allow_html=True)
        st.markdown("**Chi tiết tháng đầu**")
        st.write(f"- Gốc: **{money_vnd(first['principal'])}**")
        st.write(f"- Lãi: **{money_vnd(first['interest'])}**")
        st.write(f"- Khoản trả cao nhất mô phỏng: **{money_vnd(max_payment)}**")
        st.write(f"- Thời hạn: **{years} năm**")
        st.write(f"- Ân hạn gốc: **{grace} tháng**")
        st.caption("Mô phỏng giả định lãi suất không đổi trong toàn kỳ. Trong thời gian ân hạn chỉ trả lãi, gốc được phân bổ vào thời gian còn lại. Chưa bao gồm phí, bảo hiểm và nghĩa vụ khác.")

    with st.expander("Xem 12 kỳ trả nợ đầu tiên"):
        st.dataframe(
            [{
                "Kỳ": row["month"],
                "Dư nợ đầu kỳ": round(row["opening_balance"]),
                "Gốc": round(row["principal"]),
                "Lãi": round(row["interest"]),
                "Tổng trả": round(row["payment"]),
                "Dư nợ cuối kỳ": round(row["closing_balance"]),
            } for row in schedule[:12]],
            use_container_width=True,
            hide_index=True,
        )

# --------------------------- Projects -------------------------
st.divider()
st.markdown('<div class="eyebrow">Danh sách tham khảo</div><div class="section-title">Các dự án áp dụng</div>', unsafe_allow_html=True)
st.markdown('<p class="subtle">Tên dự án theo tài liệu người dùng cung cấp; cần xác nhận điều kiện áp dụng thực tế.</p>', unsafe_allow_html=True)
project_cols = st.columns(3)
for i, project_name in enumerate(PROJECTS):
    with project_cols[i % 3]:
        st.markdown(f"**{project_name}**")
        st.caption("Dự án tham khảo")

# -------------------------- Contact ---------------------------
st.divider()
st.markdown('<div class="eyebrow">Kết nối chuyên viên tư vấn</div><div class="section-title">Bắt đầu kế hoạch tài chính của bạn</div>', unsafe_allow_html=True)
contact_left, contact_right = st.columns([0.85, 1.15], gap="large")
with contact_left:
    st.markdown(f"""
    <div class="contact-card">
      <div style="color:#f4d48b;font-size:12px;font-weight:800;letter-spacing:1px">CHUYÊN VIÊN TƯ VẤN</div>
      <h2 style="font-family:'Playfair Display',serif;margin-bottom:4px">{ADVISOR_NAME}</h2>
      <p style="color:#c9ded8">Tư vấn giải pháp vay mua nhà và bất động sản</p>
      <p style="font-size:17px">☎ &nbsp; <b>{PHONE_DISPLAY}</b></p>
      <p style="color:#c9ded8;font-size:13px">Zalo: {PHONE_DISPLAY}</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("☎ GỌI TƯ VẤN NGAY", f"tel:{PHONE_TEL}", use_container_width=True)
    st.link_button("◉ TƯ VẤN NGAY QUA ZALO", ZALO_URL, use_container_width=True)

with contact_right:
    st.subheader("Đăng ký tư vấn")
    st.caption("Thông tin có dấu * là bắt buộc.")
    with st.form("lead_form", clear_on_submit=True):
        full_name = st.text_input("Họ và tên *", max_chars=100, placeholder="Nguyễn Văn A")
        phone = st.text_input("Số điện thoại *", max_chars=20, placeholder="09xxxxxxxx")
        need = st.selectbox("Nhu cầu *", ["Chọn nhu cầu", "Mua nhà ở", "Đầu tư bất động sản", "Tư vấn khoản vay"])
        project = st.selectbox("Dự án quan tâm", ["Chưa xác định"] + PROJECTS)
        message = st.text_area("Thông tin thêm", max_chars=500, placeholder="Giá trị bất động sản, số tiền dự kiến vay...")
        consent = st.checkbox("Tôi đồng ý để chuyên viên liên hệ nhằm phản hồi yêu cầu tư vấn này.")
        submitted = st.form_submit_button("GỬI YÊU CẦU TƯ VẤN", use_container_width=True, type="primary")
        if submitted:
            phone_clean = clean_phone(phone)
            digits = "".join(ch for ch in phone_clean if ch.isdigit())
            if not full_name.strip():
                st.error("Vui lòng nhập họ và tên.")
            elif len(digits) < 9 or len(digits) > 11:
                st.error("Vui lòng kiểm tra số điện thoại (9–11 chữ số).")
            elif need == "Chọn nhu cầu":
                st.error("Vui lòng chọn nhu cầu vay.")
            elif not consent:
                st.error("Bạn cần xác nhận đồng ý để được liên hệ tư vấn.")
            else:
                save_lead(full_name.strip(), phone_clean, need, "" if project == "Chưa xác định" else project, message.strip())
                st.success("Đã lưu yêu cầu tư vấn trên máy chủ đang chạy ứng dụng. Chuyên viên có thể liên hệ theo số điện thoại đã cung cấp.")
                st.info("Lưu ý: Bản MVP này lưu dữ liệu vào SQLite trên máy chạy ứng dụng; cần cấu hình máy chủ bảo mật và quy trình quản lý dữ liệu trước khi dùng thật.")

# --------------------------- Footer ---------------------------
st.divider()
st.markdown("""
**Lưu ý về thông tin và nhận diện:** Đây là bản MVP minh họa cho landing page cá nhân, không mặc nhiên là website chính thức của BIDV. Tên thương hiệu, logo, thông tin sản phẩm, lãi suất, dự án và nội dung quảng bá phải được kiểm tra và có chấp thuận cần thiết trước khi công bố. Mọi khoản vay phụ thuộc hồ sơ, tài sản bảo đảm, điều kiện tín dụng và phê duyệt của ngân hàng. Công cụ tính toán chỉ mang tính tham khảo.
""")
st.caption("© Landing page tư vấn cá nhân · Không nhập CCCD, tài khoản ngân hàng hoặc dữ liệu nhạy cảm vào biểu mẫu.")