import os
import re


def sanitize_filename(filename):
    """清理文件名，移除不合法字符"""
    # 替换或移除不合法字符
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # 限制文件名长度（Windows最大255字符）
    return filename[:250] + '.txt' if len(filename) > 250 else filename + '.txt'


def create_knowledge_base_files(names, output_dir='./知识库文件'):
    """为每个知识库名称创建对应的txt文件"""
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    for name in names:
        # 清理文件名
        safe_filename = sanitize_filename(name)
        file_path = os.path.join(output_dir, safe_filename)

        try:
            # 写入文件内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"知识库名称：{name}\n\n")
                file.write(f"关于{name}的详细内容。\n")
                file.write("=" * 50 + "\n")
                file.write("说明：\n")
                file.write("- 本文件为水利安全知识库的一部分\n")
                file.write("- 内容可根据实际需求扩展\n")

            print(f"✅ 已创建文件：{file_path}")
        except Exception as e:
            print(f"❌ 创建文件 {safe_filename} 时出错：{e}")


if __name__ == "__main__":
    # 水利安全知识库名称列表（保持与原问题一致）
    knowledge_base_names = [
        "水利工程安全预警监测库",
        "水利建设安全风险评估库",
        "水环境安全防护技术库",
        "水利工程抗震安全知识库",
        "水利设备安全检修指南库",
        "流域水资源安全调配智库",
        "水利工程安全验收标准库",
        "城市水利系统安全运行库",
        "水利安全应急物资储备库",
        "水利工程耐久性安全智库",
        "中小河流安全治理知识库",
        "水利工程安全监理规范库",
        "水利行业网络安全防护库",
        "农田水利设施安全管护库",
        "水利工程安全事故处理库",
        "水利工程安全责任体系库",
        "极端天气水利安全应对库",
        "水利工程安全成本核算库",
        "水利安全公众教育知识库",
        "国际水利安全合作案例库"
    ]

    # 创建所有知识库文件（默认在当前目录下的"知识库文件"文件夹）
    create_knowledge_base_files(knowledge_base_names)