import requests
import re

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
    id_lists = data.get("idLists", [])[:5]  # 默认只取前 5 个最稳定的账号展示
except Exception as e:
    print(f"抓取账号失败: {e}")
    exit(1)

# 2. 生成 Markdown 表格
table_content = "##### 💡 当前可用共享账号列表（系统自动更新）\n\n"
table_content += "| 序号 | 地区 | 共享 Apple ID 账号 | 解锁密码 | 状态 |\n"
table_content += "| :--- | :---: | :--- | :--- | :---: |\n"
for index, item in enumerate(id_lists):
    # 去除可能夹杂的单双引号
    password = item['password'].replace("'", "").replace('"', "")
    table_content += f"| {index + 1} | 美区 | `{item['email']}` | `{password}` | 🟢 正常 |\n"

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

print("get-apple-id.md 账号列表更新成功！")
