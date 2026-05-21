import requests
import re
from datetime import datetime, timezone, timedelta

# 1. 获取最新账号
url = "https://ali.wangdu.site/apple/idlists"
headers = {
    "Referer": "https://ios.wwkejishe.top/",
    "Origin": "https://ios.wwkejishe.top",
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    id_lists = data.get("idLists", [])
except Exception as e:
    print(f"抓取账号失败: {e}")
    exit(1)

# 获取当前的北京时间（UTC+8）
beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)
last_update_time = now_beijing.strftime("%Y-%m-%d %H:%M:%S")

# 2. 生成 Markdown 表格
table_content = "##### 💡 当前可用共享账号列表（系统自动更新）\n\n"
table_content += f"> 🕒 **上次刷新时间**：`{last_update_time}` (北京时间，系统每 6 小时检测一次)\n\n"

table_content += "| 序号 | 地区 | 共享 Apple ID 账号 (双击全选) | 解锁密码 (点击展开) | 状态 |\n"
table_content += "| :--- | :---: | :--- | :--- | :---: |\n"

for index, item in enumerate(id_lists):
    # 格式化账号单元格，使用 code 标签方便读者双击复制
    email_cell = f"<code>{item['email']}</code>"
    
    # 清理密码中夹杂的引号
    raw_pw = item['password'].replace("'", "").replace('"', "")
    
    # 自动生成掩码（保留前2位，后面全部替换为黑色圆点）
    if len(raw_pw) > 2:
        masked_pw = raw_pw[:2] + "•" * (len(raw_pw) - 2)
    else:
        # 密码极短时的安全兜底
        masked_pw = raw_pw[:1] + "•" * (len(raw_pw) - 1) if raw_pw else "••"
    
    # 利用 HTML details 标签在表格内实现安全的“折叠/展开密码”
    password_cell = f"<details><summary>🔑 <code>{masked_pw}</code></summary><code>{raw_pw}</code></details>"
    
    # 追加到表格行（保持单行写入以防 Markdown 表格语法破裂）
    table_content += f"| {index + 1} | 美区 | {email_cell} | {password_cell} | 🟢 正常 |\n"

# 3. 读取并更新 get-apple-id.md
file_path = "get-apple-id.md"
with open(file_path, "r", encoding="utf-8") as f:
    file_data = f.read()

# 定位占位符并替换
pattern = r"<!-- ACCOUNTS_START -->.*?<!-- ACCOUNTS_END -->"
replacement = f"<!-- ACCOUNTS_START -->\n{table_content}\n<!-- ACCOUNTS_END -->"
new_file_data = re.sub(pattern, replacement, file_data, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_file_data)

print(f"get-apple-id.md 账号列表（共 {len(id_lists)} 个）已于 {last_update_time} 成功生成！")
