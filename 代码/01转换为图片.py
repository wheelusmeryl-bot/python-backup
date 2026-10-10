def process_text_file(input_file: str, output_file: str) -> None:
    """
    处理文本文件：删除换行和空格，字符逆序后保存到新文件

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    try:
        # 读取输入文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 删除所有换行符和空格（包括普通空格、制表符等空白字符）
        cleaned_content = content.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')

        # 2. 字符逆序
        reversed_content = cleaned_content[::-1]

        # 3. 将结果写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(reversed_content)

        print(f"处理完成！")
        print(f"原始文件：{input_file}")
        print(f"处理后文件：{output_file}")
        print(f"原始字符数（含空白）：{len(content)}")
        print(f"清理后字符数：{len(cleaned_content)}")

    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except PermissionError:
        print(f"错误：没有权限访问文件 {input_file} 或 {output_file}")
    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


# 主程序执行
if __name__ == "__main__":
    # 定义输入输出文件路径
    INPUT_FILE = "1.txt"
    OUTPUT_FILE = "2.txt"

    # 调用处理函数
    process_text_file(INPUT_FILE, OUTPUT_FILE)