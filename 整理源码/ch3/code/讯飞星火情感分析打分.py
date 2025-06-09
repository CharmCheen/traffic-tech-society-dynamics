import sys
import os
import json
import requests
import pandas as pd
import re
import time

def get_policy_sentiment_from_file(file_path):
    # 读取文件内容
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        print(f"读取文件 {file_path} 失败: {e}")
        return None

    # API 配置
    API_URL = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    APIPASSWORD = "GzZnwmtaBaxwWPwvZrpR:SShqObedaeuLMCJrZHUT"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APIPASSWORD}"
    }

    # 构建请求参数，确保返回固定格式：
    # {"quarterly_scores": [{"quarter": "YYYY-Q", "sentiment": 0.xxxxxx}, ...]}
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个政策分析专家，请对给定的中文文本计算政策导向情感得分，"
                "并将结果以 JSON 格式严格返回，格式如下：\n"
                "{\"quarterly_scores\": [{\"quarter\": \"YYYY-Q\", \"sentiment\": 0.xxxxxx}, ...]}\n"
                "其中 sentiment 的取值范围为 0 到 1，保留六位小数，结果需按照时间顺序排列。"
            )
        },
        {
            "role": "user",
            "content": f"请阅读下面的文本，基于内容分析这几年来逐季度的政策情感得分：\n{file_content}"
        }
    ]

    data = {
        "model": "4.0Ultra",
        "user": "user_123456",
        "messages": messages,
        "temperature": 0.5,
        "top_k": 4,
        "stream": False,
        "max_tokens": 150,
        "presence_penalty": 1,
        "frequency_penalty": 1,
        "response_format": {"type": "json_object"}
    }

    # 增加重试机制，最多重试3次
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"文件 {file_path} 请求网络错误: {e} (尝试 {attempt+1}/{max_retries})")
            time.sleep(2)
            if attempt == max_retries - 1:
                return None

    # 解析返回结果
    try:
        result = response.json()
        if result.get("code") == 0:
            choices = result.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "").strip()
                # 去除 markdown 包裹符号
                if content.startswith("```"):
                    content = re.sub(r"^```(?:json)?", "", content)
                    content = re.sub(r"```$", "", content).strip()
                try:
                    data_obj = json.loads(content)
                    return data_obj.get("quarterly_scores")
                except Exception as e:
                    print(f"文件 {file_path} 返回的 JSON 格式错误: {e}\n内容: {content}")
                    return None
            else:
                print(f"文件 {file_path} 未返回任何有效结果")
                return None
        else:
            error = result.get("error")
            if error:
                print(f"文件 {file_path} 请求出错: {error.get('message')}")
            else:
                print(f"文件 {file_path} 请求出错，未获得错误信息")
            return None
    except json.JSONDecodeError as e:
        print(f"文件 {file_path} 解析 JSON 时出错: {e}")
        return None

def process_folder(folder_path):
    records = []
    # 遍历文件夹中所有 .txt 文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            print(f"正在处理文件: {file_name}")
            quarterly_scores = get_policy_sentiment_from_file(file_path)
            if quarterly_scores:
                for entry in quarterly_scores:
                    quarter = entry.get("quarter")
                    sentiment = entry.get("sentiment")
                    records.append({
                        "file_name": file_name,
                        "quarter": quarter,
                        "sentiment": sentiment
                    })
                print(f"{file_name} 成功获得逐季度情感得分")
            else:
                print(f"{file_name} 未获得有效的情感得分序列")
    return records

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_policy_sentiment_quarterly.py <文件夹路径>")
    else:
        folder_path = sys.argv[1]
        if not os.path.isdir(folder_path):
            print(f"{folder_path} 不是一个有效的文件夹路径")
            sys.exit(1)
        records = process_folder(folder_path)
        if records:
            df = pd.DataFrame(records, columns=["file_name", "quarter", "sentiment"])
            output_csv = os.path.join(folder_path, "policy_sentiment_quarterly.csv")
            df.to_csv(output_csv, index=False, encoding="utf-8-sig")
            print(f"所有文件逐季度情感得分已保存到: {output_csv}")
        else:
            print("没有获得任何有效的情感得分记录。")