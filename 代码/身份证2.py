with open(r"C:\Users\29120\Downloads\CTF4\数据校验\data.csv", 'r', encoding='utf-8') as f1:
    for line in f1:
        # 按逗号分割行数据
        a = line.split(',')
        # 确保每行有5个字段（避免索引越界错误）
        if len(a) < 5:
            continue

        # 提取各字段
        id = a[0]  # 序号
        id_card = a[1].strip()  # 身份证号（修正：统一用id_card变量）
        gender = a[3].strip()  # 性别
        phone = a[4].strip()  # 手机号

        # 校验条件（修正了变量名错误，将b改为id_card）
        if (
                len(id_card) == 18 and  # 身份证18位
                # 前17位是数字，最后一位是数字或X/x
                id_card[:17].isdigit() and (id_card[17].isdigit() or id_card[17].upper() == 'X') and
                len(phone) == 11 and  # 手机号11位
                phone[0] == '1' and  # 手机号以1开头
                3 <= int(phone[1]) <= 9 and  # 手机号第二位3-9
                # 性别与身份证第17位奇偶一致（假设性别是"男"/"女"，如果是0/1请修改这里）
                ((int(id_card[16]) % 2 == 1 and gender == '男') or
                 (int(id_card[16]) % 2 == 0 and gender == '女')) and
                1900 <= int(id_card[6:10]) <= 2025 and  # 年份合理
                1 <= int(id_card[10:12]) <= 12  # 月份有效
        ):
            print(f"符合条件的序号: {id}")