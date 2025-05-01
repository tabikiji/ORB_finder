import re

from collections import defaultdict

import streamlit as st



# 都道府県名を取り出す関数

def extract_prefecture(address):

    pattern = r"(東京都|北海道|(?:京都|大阪)府|[^\s,、]{2,3}県)"

    match = re.search(pattern, address)

    if match:

        return match.group()

    else:

        return None



# ファイルから住所リスト読み込み

with open("addresses.txt", "r", encoding="utf-8") as f:

    addresses = [line.strip() for line in f if line.strip()]



# 都道府県別にまとめる

prefecture_map = defaultdict(list)



for addr in addresses:

    prefecture = extract_prefecture(addr)

    if prefecture:

        prefecture_map[prefecture].append(addr)

    else:

        prefecture_map["不明"].append(addr)



# ----------------- ここからStreamlit -----------------



st.title("Worldcoin ORB設置場所検索ツール")

# 招待コード表示セクション

st.markdown("## 📢 招待コード")



invite_code = "K4M7NYJ"

st.code(invite_code, language='text')



# コピー用の説明（streamlit標準では自動コピー不可）

st.button("📋 このコードをコピーしました！", on_click=lambda: st.toast("コピーしました（Ctrl+Cで手動）"))

# 都道府県選択

prefecture_list = sorted(prefecture_map.keys())

selected_prefecture = st.selectbox("都道府県を選択してください", prefecture_list)



# 住所一覧表示

if selected_prefecture:

    st.write(f"### {selected_prefecture} の住所一覧（{len(prefecture_map[selected_prefecture])}件）")

    for addr in prefecture_map[selected_prefecture]:

        st.write(f"- {addr}")
