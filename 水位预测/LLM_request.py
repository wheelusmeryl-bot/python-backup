import os
import requests
import json

# Dify 的 API Key 不再写死在代码里，从环境变量读取。
# 运行前先设置：
#   Windows CMD        set DIFY_API_KEY=app-xxxxxxxx
#   PowerShell         $env:DIFY_API_KEY="app-xxxxxxxx"
DIFY_API_KEY = os.environ.get("DIFY_API_KEY", "")


def call_dify_api():

    #URL
    URL= "https://api.dify.ai/v1/chat-messages"

    #请求头
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + DIFY_API_KEY
    }

    # 请求数据
    DATA = {
        "inputs": {"location": "X市T河流"},
        "query": "蓝色预警",
        "user": "AI application engineer",
        "response_mode": "streaming",
        "model":"qwen2.5:7b",
        "temperature":0.1,
        "max_tokens":8192
    }
    response = requests.post(
        url=URL,
        headers=HEADERS,
        data=json.dumps(DATA),
        stream=True
    )

    # 检查响应状态
    if response.status_code == 200:
        # 检查响应内容类型
        content_type = response.headers.get('Content-Type', '')
        if 'text/event-stream' in content_type:
            # 处理流式响应，逐字输出答案
            print("问题的答案:")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        json_str = decoded_line[6:]  # 移除 'data: ' 前缀
                        try:
                            json_data = json.loads(json_str)
                            if json_data.get('event') == 'message' and 'answer' in json_data:
                                print(json_data['answer'], end='', flush=True)
                            elif json_data.get('event') == 'message_end':
                                print()  # 输出换行
                        except json.JSONDecodeError as e:
                            print(f"JSON解析错误: {e}")
                            print(f"原始数据: {json_str}")
            return True
        else:
            # 如果不是流式响应，打印响应内容类型和内容
            print(f"响应内容类型: {content_type}")
            print("响应内容(前500字符):")
            print(response.text[:500])
            return False
    else:
        print(f"API调用失败，状态码: {response.status_code}")
        print(response.text)
        return None
def call_dify_api1():

    #URL
    URL= "https://api.dify.ai/v1/chat-messages"

    #请求头
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + DIFY_API_KEY
    }

    # 请求数据
    DATA = {
        "inputs": {"location": "X市T河流"},
        "query": "蓝色预警",
        "user": "AI application engineer",
        "response_mode": "streaming",
        "model":"qwen2.5:7b",
        "temperature":0.1,
        "max_tokens":8192

    }
    response = requests.post(
        url=URL,
        headers=HEADERS,
        data=json.dumps(DATA),
        stream=True
    )

if __name__ == "__main__":
    # 调用Dify API
    call_dify_api()