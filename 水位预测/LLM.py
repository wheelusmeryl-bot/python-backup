import os
import requests
import json
import time

# Dify 的 API Key 不再写死在代码里，从环境变量读取。
# 运行前先设置：
#   Windows CMD        set DIFY_API_KEY=app-xxxxxxxx
#   PowerShell         $env:DIFY_API_KEY="app-xxxxxxxx"
DIFY_API_KEY = os.environ.get("DIFY_API_KEY", "")


def call_dify_api():
    URL = "https://api.dify.ai/v1/chat-messages"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + DIFY_API_KEY
    }

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




    def call_api(url, method='get', data=None, headers=None, timeout=30, stream=False):

        try:

            headers = headers or {'Content-Type': 'application/json'}


            if method.lower() == 'get':
                resp = requests.get(url, params=data, headers=headers, timeout=timeout, stream=stream)
            else:
                resp = requests.post(url, json=data, headers=headers, timeout=timeout, stream=stream)

            resp.raise_for_status()
            return resp

        except Exception as e:
            print(f"请求失败: {str(e)}")
            return None


    file_path = r"C:/Users/29120/Desktop/学习/预演预案.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print("问题的答案:")


            for char in file.read():
                print(char, end='', flush=True)

                if char in ['.', '!', '?', '\n']:
                    time.sleep(0.1)
                else:
                    time.sleep(0.01)
            print()
        return True

    except FileNotFoundError:
        print(f"错误：未找到文件 '{file_path}'")
        return False
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
        return False


if __name__ == "__main__":
    call_dify_api()
