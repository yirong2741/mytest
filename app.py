import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import pandas as pd
import plotly.express as px
from pyecharts.charts import WordCloud, Radar
from pyecharts import options as opts
from streamlit.components.v1 import html
import altair as alt
import re

# 设计文本输入框
url = st.text_input("请输入文章的URL")

# 如果用户输入了URL
if url:
    # 抓取文本内容
    response = requests.get(url)
    text = response.text

    # 使用BeautifulSoup去除HTML标签
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()

    # 分词
    words = jieba.cut(text)

    # 去除标点符号
    words = [word for word in words if word.strip() and not re.match(r'[^\w]', word)]

    word_counts = Counter(words)

    # 交互过滤低频词
    min_frequency = st.sidebar.slider("设置最低词频", 1, 100, 10)
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= min_frequency}

    # 展示词频排名前20的词汇
    top_20_words = Counter(filtered_word_counts).most_common(20)

    # 将词频排名转为 DataFrame
    df_top_20 = pd.DataFrame(top_20_words, columns=['词汇', '频次'])

    # 在表格中展示
    st.write("词频排名前20的词汇（表格展示）:")
    st.table(df_top_20)

    # 图型筛选
    chart_type = st.sidebar.selectbox("选择图表类型", ["词云", "饼图", "折线图", "散点图", "雷达图", "面积图", "树状图",
                                                       "Altair条形图"])

    # 根据选择的图表类型显示不同的图表
    if chart_type == "词云":
        # 生成词云
        wordcloud = WordCloud()
        wordcloud.add("", top_20_words, word_size_range=[20, 100])
        wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="词云"))
        # 显示词云
        wordcloud_html = wordcloud.render_embed()
        html(wordcloud_html, height=800)
    elif chart_type == "饼图":
        # 使用饼图展示词频
        fig_pie = px.pie(df_top_20, values='频次', names='词汇', title='饼图')
        st.plotly_chart(fig_pie)
    elif chart_type == "折线图":
        # 使用折线图展示词频
        fig_line = px.line(df_top_20, x='词汇', y='频次', title='折线图')
        st.plotly_chart(fig_line)
    elif chart_type == "散点图":
        # 使用散点图展示词频
        fig_scatter = px.scatter(df_top_20, x='词汇', y='频次', title='散点图')
        st.plotly_chart(fig_scatter)
    elif chart_type == "雷达图":
        # 使用雷达图展示词频
        words, frequencies = zip(*top_20_words)
        radar_schema = [
            opts.RadarIndicatorItem(name=word, max_=max(frequencies)) for word in words
        ]
        radar = Radar()
        radar.add_schema(schema=radar_schema)
        radar.add('', [list(frequencies)], color='#f9713c')
        radar.set_global_opts(title_opts=opts.TitleOpts(title='雷达图'))
        radar_html = radar.render_embed()
        html(radar_html, height=500)
    elif chart_type == "面积图":
        # 使用面积图展示词频
        fig_area = px.area(df_top_20, x='词汇', y='频次', title='面积图')
        st.plotly_chart(fig_area)
    elif chart_type == "树状图":
        # 使用树形图展示词频
        fig_treemap = px.treemap(df_top_20, path=['词汇'], values='频次', title='树状图')
        st.plotly_chart(fig_treemap)
    elif chart_type == "Altair条形图":
        chart = alt.Chart(df_top_20).mark_bar().encode(
            x=alt.X('词汇:N', sort='-y'),
            y='频次:Q',
            color=alt.Color('频次:Q', scale=alt.Scale(scheme='viridis')),
            tooltip=['词汇', '频次']
        ).properties(
            width=600,
            height=400,
            title='词频分析条形图 (Altair版本)'
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
