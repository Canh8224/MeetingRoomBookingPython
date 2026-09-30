import streamlit as st
from datetime import date, time, datetime
from database import SessionLocal
from models.room import Room
from models.user import User
from models.room_booking import RoomBooking

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Danh sách phòng họp - CMC ATI",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Tùy chỉnh triệt để giao diện
st.markdown("""
    <style>
    /* Bỏ Header/Footer mặc định của Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Navbar Trên Cùng */
    .navbar {
        background-color: #c2d6f6;
        padding: 12px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .logo-box {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .logo-title {
        color: #0052cc;
        font-weight: 800;
        font-size: 20px;
        line-height: 1;
    }
    .logo-sub {
        color: #0052cc;
        font-size: 8px;
        text-transform: uppercase;
        font-weight: 600;
    }
    .menu-links {
        display: flex;
        gap: 35px;
        font-weight: 500;
        color: #333;
        font-size: 14px;
    }
    .menu-item {
        color: #4b5563;
        text-decoration: none;
    }
    .menu-item.active {
        color: #111827;
        font-weight: 700;
    }
    .user-icon {
        background: white;
        padding: 4px 10px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        font-size: 14px;
    }

    /* Đổi màu Nút Streamlit chính chủ từ Đỏ -> Xanh Lam chuẩn */
    div.stButton > button {
        background-color: #1b64f2 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #114ec3 !important;
        color: white !important;
    }
    div.stButton > button:disabled {
        background-color: #e5e7eb !important;
        color: #9ca3af !important;
        border: none !important;
        cursor: not-allowed !important;
    }

    /* Style Thẻ Phòng (Card) */
    .card-container {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .card-img {
        width: 100%;
        height: 130px;
        object-fit: cover;
    }
    .card-content {
        padding: 12px;
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    .room-title {
        font-weight: 700;
        font-size: 14px;
        color: #1f2937;
        line-height: 1.2;
    }
    .status-badge-green {
        color: #10b981;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }
    .status-badge-red {
        color: #ef4444;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }
    .room-detail {
        color: #6b7280;
        font-size: 12px;
        margin-bottom: 3px;
    }
    .card-footer {
        padding: 0 12px 12px 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .link-detail {
        font-size: 12px;
        color: #1b64f2;
        text-decoration: none;
        font-weight: 500;
    }
    .link-detail:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Top Navigation Bar chuẩn
st.markdown("""
    <div class="navbar">
        <div class="logo-box">
            <span style="font-size: 26px; color: #0066cc;">☁️</span>
            <div>
                <div class="logo-title">CMC ATI</div>
                <div class="logo-sub">KHÁT KHAO CHINH PHỤC THẾ GIỚI</div>
            </div>
        </div>
        <div class="menu-links">
            <span class="menu-item">Quản lý người dùng</span>
            <span class="menu-item">Quản lý phòng</span>
            <span class="menu-item active">Danh sách phòng</span>
        </div>
        <div class="user-icon">
            <span>☰</span>
            <span style="font-size: 16px; color: #9ca3af;">👤</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Tiêu đề danh sách & Nút Đặt phòng mới
head_left, head_right = st.columns([8, 2])
with head_left:
    st.markdown("<h3 style='margin:0; font-size: 20px; font-weight:700;'>Danh sách phòng họp</h3>",
                unsafe_allow_html=True)
with head_right:
    if st.button("➕ Đặt phòng mới", key="add_new_room"):
        st.toast("Mở form đặt phòng mới!")

st.write("")  # Khoảng trống nhỏ



# 5. Lấy danh sách phòng từ MySQL
db = SessionLocal()

try:
    db_rooms = db.query(Room).all()

    rooms = []

    for room in db_rooms:
        if room.available:
            status = "Trống"
        else:
            status = "Đang sử dụng"

        rooms.append({
            "id": room.room_id,
            "name": room.room_name,
            "status": status,
            "location": room.location,
            "capacity": f"{room.capacity} người",
            "img": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=500&q=80"
        })
        if "selected_room_id" not in st.session_state:
            st.session_state.selected_room_id = None

finally:
    db.close()

# 6. Chia 5 Cột phẳng chuẩn kích thước
cols = st.columns(len(rooms))

for i, room in enumerate(rooms):
    with cols[i]:
        # Xử lý badge
        if room["status"] == "Trống":
            badge_html = '<span class="status-badge-green">✔ Trống</span>'
        else:
            badge_html = '<span class="status-badge-red">✖ Đang sử dụng</span>'

        # Thẻ Card thông tin
        st.markdown(f"""
            <div class="card-container">
                <div>
                    <img src="{room['img']}" class="card-img"/>
                    <div class="card-content">
                        <div class="card-header">
                            <div class="room-title">{room['name']}</div>
                            {badge_html}
                        </div>
                        <div class="room-detail">{room['location']}</div>
                        <div class="room-detail">👥 {room['capacity']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Nút hành động & Link ở dưới card
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            st.markdown(f"<div style='padding-top:6px;'><a href='#' class='link-detail'>Xem chi tiết</a></div>",
                        unsafe_allow_html=True)
        with btn_col2:
            is_disabled = (room["status"] != "Trống")
            if st.button("Đặt phòng", key=f"btn_room_{room['id']}", disabled=is_disabled):
                st.toast(f"Đã đăng ký {room['name']} thành công!", icon="✅")