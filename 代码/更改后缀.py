import os


def batch_rename_txt_to_md(directory):
    """
    将指定目录中的所有 .txt 文件重命名为 .md 文件

    参数:
    directory (str): 要处理的目录路径
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return

    # 遍历目录中的所有文件和文件夹
    for filename in os.listdir(directory):
        # 构建完整路径
        full_path = os.path.join(directory, filename)

        # 检查是否为文件且是 .txt 文件
        if os.path.isfile(full_path) and filename.lower().endswith('.txt'):
            # 获取不带扩展名的文件名
            base_name = os.path.splitext(filename)[0]

            # 构建新的文件名
            new_filename = base_name + '.md'
            new_full_path = os.path.join(directory, new_filename)

            # 重命名文件
            try:
                os.rename(full_path, new_full_path)
                print(f"已将 '{filename}' 重命名为 '{new_filename}'")
            except Exception as e:
                print(f"无法重命名文件 '{filename}': {str(e)}")


if __name__ == "__main__":
    # 直接指定要处理的目录路径
    directory = r"F:\python\知识库文件"

    # 调用重命名函数
    batch_rename_txt_to_md(directory)