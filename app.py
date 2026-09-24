from datetime import date
import streamlit as st

# 1. 頁面基本設定
st.set_page_config(
    page_title="EQ微甜研究所 | 手作烘焙預訂",
    page_icon="🧁",
    layout="centered",
)

# 2. 標題與品牌介紹
st.title("EQ微甜研究所 🧁")
st.caption("手作溫暖 · 微甜無負擔的精緻烘焙")
st.info("💡 工作室為兩人手作生產、產能有限，請先填單私訊確認接單狀況！")

st.divider()

# 3. 第一區塊：選擇商品與數量
st.subheader("1. 選擇品項與數量")

# 使用陣列 + 獨一無二的 id，確保不會重複
products = [
    {"id": "item_1", "name": "莓果燕麥餅", "price": 250, "unit": "盒"},
    {"id": "item_2", "name": "可可燕麥餅", "price": 280, "unit": "盒"},
    {"id": "item_3", "name": "奶油曲奇餅", "price": 220, "unit": "包"},
]

selected_orders = []
total_price = 0

for item in products:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{item['name']}**")
        st.caption(f"NT$ {item['price']} / {item['unit']}")
    with col2:
        # 使用 item['id'] 作為 key，保證獨一無二
        qty = st.number_input(
            "數量",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"qty_{item['id']}",
            label_visibility="collapsed",
        )

    if qty > 0:
        item_total = qty * item["price"]
        selected_orders.append(f"• {item['name']} x {qty} (${item_total})")
        total_price += item_total

st.write(f"### **預估總金額：NT$ {total_price}**")

st.divider()

# 4. 第二區塊：取貨與訂購人資訊
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

# 5. 第三區塊：產生訂單訊息與 IG 私訊跳轉
if st.button("🚀 產生訂單並前往 IG 私訊", type="primary", use_container_width=True):
    if not selected_orders:
        st.error("⚠️ 請至少選擇一項商品！")
    elif not cust_name or not cust_phone:
        st.error("⚠️ 請完整填寫姓名與電話！")
    else:
        items_str = "\n".join(selected_orders)
        note_str = f"\n【備註】：{cust_note}" if cust_note else ""

        order_text = (
            f"你好！我想預訂【EQ微甜研究所】手作點心：\n\n"
            f"{items_str}\n\n"
            f"【預估總金額】：NT$ {total_price}\n"
            f"【預計取貨日】：{pickup_date}\n"
            f"【取貨方式】：{delivery_method}\n"
            f"【訂購人】：{cust_name} ({cust_phone})"
            f"{note_str}\n\n"
            f"請幫我確認是否有產能接單，謝謝！"
        )

        st.success("✅ 訂單內容已順利產生！請點擊上方框內右側按鈕複製訊息：")

        # 顯示可供一鍵複製的文字框
        st.code(order_text, language="text")

        # 提供前往官方 IG 的直接按鈕
        ig_url = "https://www.instagram.com/eq.eqqq/"
        st.link_button(
            "👉 點此前往 @eq.eqqq 官方 IG 貼上私訊",
            ig_url,
            use_container_width=True,
        )
