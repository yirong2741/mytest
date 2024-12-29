import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import plotly.express as px
import pandas as pd
from pyecharts.charts import WordCloud, Bar, Line, Scatter, Radar
from pyecharts import options as opts
from streamlit.components.v1 import html

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
    word_counts = Counter(words)

    # 交互过滤低频词
    min_frequency = st.sidebar.slider("设置最低词频", 1, 100, 10)
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= min_frequency}

    # 展示词频排名前20的词汇
    top_20_words = Counter(filtered_word_counts).most_common(20)
    st.write("词频排名前20的词汇:", top_20_words)

    # 图型筛选
    chart_type = st.sidebar.selectbox("选择图表类型", ["词云", "柱状图", "饼图", "折线图", "散点图", "雷达图", "箱形图", "面积图", "树形图"])

    # 根据选择的图表类型显示不同的图表
    if chart_type == "词云":
        # 生成词云
        wordcloud = WordCloud()
        wordcloud.add("", top_20_words, word_size_range=[20, 100])
        wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="词云"))
        # 显示词云
        wordcloud_html = wordcloud.render_embed()
        html(wordcloud_html, height=800)
    elif chart_type == "柱状图":
        # 使用柱状图展示词频
        df_bar = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_bar = px.bar(df_bar, x='词汇', y='频次', title='柱状图')
        st.plotly_chart(fig_bar)
    elif chart_type == "饼图":
        # 使用饼图展示词频
        df_pie = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_pie = px.pie(df_pie, values='频次', names='词汇', title='饼图')
        st.plotly_chart(fig_pie)
    elif chart_type == "折线图":
        # 使用折线图展示词频
        df_line = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_line = px.line(df_line, x='词汇', y='频次', title='折线图')
        st.plotly_chart(fig_line)
    elif chart_type == "散点图":
        # 使用散点图展示词频
        df_scatter = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_scatter = px.scatter(df_scatter, x='词汇', y='频次', title='散点图')
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
    elif chart_type == "箱形图":
        # 使用箱形图展示词频
        df_box = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_box = px.box(df_box, x='词汇', y='频次', title='箱形图')
        st.plotly_chart(fig_box)
    elif chart_type == "面积图":
        # 使用面积图展示词频
        df_area = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_area = px.area(df_area, x='词汇', y='频次', title='面积图')
        st.plotly_chart(fig_area)
    elif chart_type == "树形图":
        # 使用树形图展示词频
        df_treemap = pd.DataFrame(top_20_words, columns=['词汇', '频次'])
        fig_treemap = px.treemap(df_treemap, path=['词汇'], values='频次', title='树形图')
        st.plotly_chart(fig_treemap)
