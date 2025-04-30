import re
from collections import defaultdict
import streamlit as st
from geopy.geocoders import Nominatim
import pandas as pd
import time

# ----------------- 住所処理 -----------------

def extract_prefecture(address):
    pattern = r"(東京都|北海道|(?:京都|大阪)府|[^　\s,、]{2,3}県)"
    match = re.search(pattern, address)
    if match:
        return match.group()
    return None

with open("addresses.txt", "r", encoding="utf-8") as f:
    addresses = [line.strip() for line in f if line.strip()]

prefecture_map = defaultdict(list)
for addr in addresses:
    pref = extract_prefecture(addr)
    if pref:
        prefecture_map[pref].append(addr)
    else:
        prefecture_map["不明"].append(addr)

# ----------------- 緯度経度取得 -----------------
geolocator = Nominatim(user_agent="orb_finder_app")
geo_data = []

with st.spinner("位置情報を取得中..."):
    for addr in addresses:
        try:
            location = geolocator.geocode(addr)
            if location:
                geo_data.append({
                    "address": addr,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
            time.sleep(1)  # レート制限対策
        except:
            continue

df_geo = pd.DataFrame(geo_data)

# ----------------- Streamlit UI -----------------
st.title("Worldcoin ORB設置場所検索ツール")

# 招待コード表示
st.markdown("## 📢 招待コード")
invite_code = "K4M7NYJ"
st.code(invite_code, language='text')
st.button("\ud83d\udccb このコードをコピーしました！", on_click=lambda: st.toast("コピーしました（Ctrl+Cで手動）"))

# 都道府県選択
target_pref = st.selectbox("都道府県を選択してください", sorted(prefecture_map.keys()))

# 住所リスト
data = prefecture_map[target_pref]
st.markdown(f"### {target_pref} の住所一覧（{len(data)}件）")
for addr in data:
    st.write(f"- {addr}")

# 地図表示
st.markdown("---")
st.subheader("🌍 地図表示")

if not df_geo.empty:
    st.map(df_geo[["latitude", "longitude"]])
else:
    st.warning("マップに表示できる位置情報がありません。")
