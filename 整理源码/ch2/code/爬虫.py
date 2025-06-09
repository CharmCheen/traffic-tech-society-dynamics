import csv
import json
from DrissionPage import ChromiumPage

# 定义每页获取数据的函数
def get_jobs_on_page(dp, page_num):
    url = f"https://www.zhipin.com/web/geek/job?query=交通&city=100010000&page={page_num}"
    dp.get(url)
    resp = dp.listen.wait()
    json_data = resp.response.body
    return json_data['zpData']['jobList']
# 定义总页数
total_pages = 10  # 你可以根据实际情况修改这个值

with open('data.csv', mode='w', encoding='utf-8', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=['职位'])
    csv_writer.writeheader()

    dp = ChromiumPage()
    dp.listen.start("zpgeek/search/joblist.json")

    for page_num in range(1, total_pages + 1):
        jobList = get_jobs_on_page(dp, page_num)
        for index in jobList:
            dit = {
                '职位': index['jobName']
            }
            csv_writer.writerow(dit)
            print(dit)
