from datetime import date
import streamlit as st

# 1. 頁面基本設定
st.set_page_config(
    page_title="EQ微甜研究所 | 手作雪花酥預訂",
    page_icon="❄️",
    layout="centered",
)

# 自訂背景顏色（經典米色）與字體顏色（黑色）
st.markdown(
    """
    <style>
    /* 全域頁面背景改為米色，文字改為黑色 */
    .stApp {
        background-color: #F5F5DC;
        color: #000000;
    }
    
    /* 確保所有標題、段落、副標題與標籤文字皆為黑色 */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #000000 !important;
    }

    /* 調整輸入框與選單背景與文字顏色 */
    .stTextInput input, .stSelectbox select, .stTextArea textarea, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. 進網頁自動跳出的兩頁圖片公告對話框
# ---------------------------------------------------------
if "announcement_page" not in st.session_state:
    st.session_state.announcement_page = 1
if "show_announcement" not in st.session_state:
    st.session_state.show_announcement = True


@st.dialog("📢 EQ微甜研究所 最新公告")
def show_announcement_dialog():
    if st.session_state.announcement_page == 1:
        st.markdown("### 📋 訂購須知 (1/2)")
        # 顯示訂購須知圖片 KNOW.jpg
        st.image("KNOW.jpg", use_container_width=True)

        if st.button("下一頁：買二送一優惠 (2/2) ➡️", type="primary", use_container_width=True):
            st.session_state.announcement_page = 2
            st.rerun()

    elif st.session_state.announcement_page == 2:
        st.markdown("### 🎉 買二送一限時活動 (2/2)")
        # 顯示買二送一活動圖片 event.jpg
        st.image("event.jpg", use_container_width=True)

        if st.button("我已知悉，開始選購 🛒", type="primary", use_container_width=True):
            st.session_state.show_announcement = False
            st.rerun()


# 進入網站時跳出彈窗
if st.session_state.show_announcement:
    show_announcement_dialog()

# ---------------------------------------------------------
# 3. 主頁面內容
# ---------------------------------------------------------
st.title("EQ微甜研究所 ❄️")
st.caption("手作溫暖 · 濃郁Q彈不黏牙的精緻雪花酥")
st.info("💡 一人手作產能有限！目前享【買二送一】優惠（贈送原味），請填單私訊確認接單狀況！")

st.divider()

# 第一區塊：選擇雪花酥口味與數量
st.subheader("1. 選擇雪花酥口味與數量")

products = [
    {
        "id": "original",
        "name": "原味雪花酥",
        "desc": "一包 150g（約 10-12塊）。濃郁奶香結合酥脆餅乾與酸甜蔓越莓，口感Q彈不黏牙。",
        "price": 180,
        "image": "no.jpg",
    },
    {
        "id": "cocoa",
        "name": "可可雪花酥",
        "desc": "一包 150g（約 10-12塊）。微苦香醇的苦甜可可風味，層次豐富、大人小孩都愛。",
        "price": 190,
        "image": "Coco.jpg",
    },
    {
        "id": "mango",
        "name": "芒果雪花酥",
        "desc": "一包 150g（約 10-12塊）。香甜芒果風味，帶有夏日清爽果香，口感Q彈不黏牙。",
        "price": 190,
        "image": "m.jpg",
    },
]

selected_orders = []
total_price = 0
total_packs = 0  # 統計購買總包數以計算贈送數量

for prod in products:
    col_img, col_info = st.columns([1, 2])

    with col_img:
        st.image(prod["image"], use_container_width=True)

    with col_info:
        st.markdown(f"### {prod['name']}")
        st.caption(prod["desc"])
        st.write(f"**NT$ {prod['price']} / 包 (150g)**")

        qty = st.number_input(
            "數量 (包)",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"qty_{prod['id']}",
        )

        if qty > 0:
            item_total = qty * prod["price"]
            item_name = f"{prod['name']} (150g)"
            selected_orders.append(f"• {item_name} x {qty}包 (${item_total})")
            total_price += item_total
            total_packs += qty

    st.markdown("---")

# 計算買二送一贈送數量
free_packs = total_packs // 2
if free_packs > 0:
    st.success(f"🎁 **【買二送一優惠套用】買滿 {total_packs} 包，自動贈送：原味雪花酥 x {free_packs} 包（$0）**")

st.markdown(f"### **預估總金額：NT$ {total_price}**")

st.divider()

# 第二區塊：取貨與訂購人資訊
st.subheader("2. 取貨與訂購人資訊")

pickup_date = st.date_input("希望取貨/出貨日期 *", min_value=date.today())
cust_name = st.text_input("訂購人姓名 *", placeholder="例如：王小美")
cust_phone = st.text_input("聯絡電話 *", placeholder="例如：0912345678")
delivery_method = st.selectbox(
    "取貨方式 *", ["工作室自取", "黑貓宅配 (+運費)", "7-11 店到店 (+運費)"]
)
cust_note = st.text_area(
    "備註說明（選填）", placeholder="如有特殊需求或贈禮卡片需求請註明"
)

st.divider()

# 第三區塊：產生訂單訊息與 IG 私訊跳轉
if st.button("🚀 產生訂單並前往 IG 私訊", type="primary", use_container_width=True):
    if not selected_orders:
        st.error("⚠️ 請至少選擇一項商品！")
    elif not cust_name or not cust_phone:
        st.error("⚠️ 請完整填寫姓名與電話！")
    else:
        # 如果有符合買二送一，將贈品資訊加入訂單文字明細
        order_list = selected_orders.copy()
        if free_packs > 0:
            order_list.append(f"• 🎁 買二送一贈品：原味雪花酥 x {free_packs}包 ($0)")

        items_str = "\n".join(order_list)
        note_str = f"\n【備註】：{cust_note}" if cust_note else ""

        order_text = (
            f"你好！我想預訂【EQ微甜研究所】手作雪花酥：\n\n"
            f"{items_str}\n\n"
            f"【預估總金額】：NT$ {total_price}\n"
            f"【預計取貨日】：{pickup_date}\n"
            f"【取貨方式】：{delivery_method}\n"
            f"【訂購人】：{cust_name} ({cust_phone})"
            f"{note_str}\n\n"
            f"請問何時方便出貨，謝謝！"
        )

        st.success("✅ 訂單內容已順利產生！請點擊上方框內右側按鈕複製訊息：")

        st.code(order_text, language="text")

        ig_url = "https://www.instagram.com/eq.eqqq/"
        st.link_button(
            "👉 點此前往 @eq.eqqq 官方 IG 貼上私訊",
            ig_url,
            use_container_width=True,
        )
