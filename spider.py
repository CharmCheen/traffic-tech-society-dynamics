from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Ensure the output directory exists
output_dir = "./data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set file paths
urls_file = "urls_list.txt"
urls_file_path = os.path.join(output_dir, urls_file)

job_descriptions_file = "job_descriptions.txt"
job_descriptions_path = os.path.join(output_dir, job_descriptions_file)

cleaned_text_file = "cleaned_text.txt"
cleaned_text_path = os.path.join(output_dir, cleaned_text_file)

keywords_file = "keywords.txt"
keywords_file_path = os.path.join(output_dir, keywords_file)

wordcloud_image_file = "wordcloud.png"
wordcloud_image_path = os.path.join(output_dir, wordcloud_image_file)

def spider4url():
    # 启动 Edge 浏览器
    browser = webdriver.Edge()
    # 打开一个文件进行写入
    with open(urls_file_path, 'w', encoding='utf-8') as file:
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
            # 查找所有 class 为 'jobinfo__top' 的 div 标签
            div_tags = soup.find_all("div", class_='jobinfo__top')
            # 遍历所有找到的 div 标签
            for i in div_tags:
                print("正在爬取第", count, "条数据")
                # 获取第一个 a 标签的 href 属性
                href = i.find_all("a")[0]["href"]
                # 将 href 写入文件
                file.write(href + '\n')
                count += 1
        print("共爬取到", count, "条数据")
    # 关闭浏览器
    browser.quit()

def read_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def fetch_text_from_url(url, index):
    # 启动 Edge 浏览器
    browser = webdriver.Edge()
    # 打开 URL
    browser.get(url)
    try:
        # 定义可能的选择器列表
        selectors = [
            (By.CLASS_NAME, "describtion__detail-content"),
            (By.CSS_SELECTOR, ".main-body__block.main-body__block--pb32")
        ]

        job_description = None

        for selector in selectors:
            try:
                # 等待特定的<div>标签加载完成
                description_content = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located(selector)
                )
                # 获取文本内容
                job_description = description_content.text
                break  # 如果找到内容，跳出循环
            except:
                # 如果未找到当前选择器的元素，继续尝试下一个
                continue

        if job_description:
            return job_description
        else:
            print(f"处理URL失败: {url}\n错误信息: 未找到指定的元素。")
            # 保存出错时的页面截图，方便调试
            browser.save_screenshot(f'screenshot_{index}.png')
            return None
    except Exception as e:
        print(f"处理URL失败: {url}\n错误信息: {e}")
        # 保存出错时的页面截图，方便调试
        browser.save_screenshot(f'screenshot_{index}.png')
        return None
    finally:
        # 关闭浏览器
        browser.quit()

def main():
    # 爬取 URL 并保存到文件
    spider4url()
    
    # 读取保存的 URL
    urls = read_urls(urls_file_path)
    
    # 爬取每个 URL 的文本内容
    for index, url in enumerate(urls):
        job_description = fetch_text_from_url(url, index)
        if job_description:
            with open(job_descriptions_path, 'a', encoding='utf-8') as file:
                file.write(job_description + '\n')

if __name__ == "__main__":
    main()