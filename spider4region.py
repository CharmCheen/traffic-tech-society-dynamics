# -*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import jieba
import nltk

# Ensure the output directory exists
output_dir = "./data/data2"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set file paths
region_file = "region.txt"
region_file_path = os.path.join(output_dir, region_file)

def spider4region():
    # 启动 Edge 浏览器
    browser = webdriver.Edge()
    # 打开一个文件进行写入
    with open(region_file_path, 'w', encoding='utf-8') as file:
        count = 0
        # 爬取20页数据（20*10）
        for user_page in range(1, 21):
            # 设置要访问的 URL
            url_base = "https://www.zhaopin.com/sou/jl489/kw01GG0Q8/p"
            url = url_base + str(user_page)
            # 打开 URL
            browser.get(url)
            # 等待 5 秒以确保页面加载完成
            time.sleep(5)
            # 使用 BeautifulSoup 解析页面源代码
            soup = BeautifulSoup(browser.page_source, "html.parser")
            # 查找所有 class 为 'jobinfo__other-info' 的 div 标签
            div_tags = soup.find_all("div", class_='jobinfo__other-info')
            # 遍历所有找到的 div 标签
            for i in div_tags:
                print("正在爬取第", count, "条数据")
                # 获取所有子 div 标签的文本内容
                sub_divs = i.find_all("div", class_='jobinfo__other-info-item')
                for sub_div in sub_divs:
                    text_content = sub_div.get_text(strip=True)
                    # 将文本内容写入文件
                    file.write(text_content + '\n')
                count += 1
        print("共爬取到", count, "条数据")
    # 关闭浏览器
    browser.quit()

def clean_text(text):
    # Tokenization
    tokens_zh = jieba.lcut(text)  # Chinese tokenization
    tokens_en = word_tokenize(text)  # English tokenization

    # Normalization
    tokens_zh = [token.lower() for token in tokens_zh if token.isalnum()]
    tokens_en = [token.lower() for token in tokens_en if token.isalnum()]

    # Stop Words Removal
    stop_words_zh = {
        '经验','学历', '不限','-','',''   }
    stop_words_en = set(nltk.corpus.stopwords.words('english'))

    tokens_zh = [token for token in tokens_zh if token not in stop_words_zh and token not in regions]
    tokens_en = [token for token in tokens_en if token not in stop_words_en]

    # Remove Meaningless Words
    meaningless_words = re.compile(r'\b\d+\b|\b[a-zA-Z]{5,}\b')
    tokens_zh = [token for token in tokens_zh if not meaningless_words.match(token)]
    tokens_en = [token for token in tokens_en if not meaningless_words.match(token)]

    # Combine tokens
    cleaned_text = ' '.join(tokens_zh + tokens_en)
    return cleaned_text


def main():
    #爬取 URL 并保存到文件
    #已完成，暂时注释
    spider4region()
    #词频统计

    

if __name__ == "__main__":
    main()