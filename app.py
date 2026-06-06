import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

df = pd.read_csv(
    "data.csv",
    parse_dates = ["Date"],
    encoding = "cp932"
)
df_m = pd.melt(
    df,
    id_vars = ['Date', '測定タイミング'],
    var_name = "item",
    value_name = "value"
)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 【修正1】Date列を明示的に日時（datetime）型に変換
df_m["Date"] = pd.to_datetime(df_m["Date"])

st.sidebar.header("時系列グラフ設定")
items = df_m["item"].unique()
y_axis = st.sidebar.selectbox("Y軸", items)

df_g = df_m[df_m["item"] == y_axis]

g1 = px.scatter(
    df_g,
    x="Date",
    y='value',
    color="測定タイミング",
    title="Date vs " + y_axis,
)

fig1 = go.Figure(g1)

# 【修正2】日付の区切りをスラッシュからハイフンに変更
# 縦線とキャプションを追加
fig1.add_vline(
    x="2026-01-15 12:00:00", 
    line_width=2, 
    line_dash="dash", 
    line_color="red",
    annotation_text="ハーフマラソン練習開始",          # 表示するテキスト
    annotation_position="top right",               # テキストの位置 (右上)
    annotation_textangle=-90,                      # テキストの角度 (縦書き)
    annotation_font_color="red"                    # テキストの色
)

st.plotly_chart(fig1)


# 数値型の列名のみを抽出（散布図の軸用）
numeric_columns = df.select_dtypes(include='number').columns.tolist()
# サイドバーにドロップダウンを表示
st.sidebar.header("相関グラフ設定")
corr_x_axis = st.sidebar.selectbox("X", numeric_columns)
corr_y_axis = st.sidebar.selectbox("Y", numeric_columns)

g2 = px.scatter(
    df,
    x = corr_x_axis,
    y = corr_y_axis,
)
fig2 = go.Figure(g2)
st.plotly_chart(fig2)