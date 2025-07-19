# fix_environment.py
# 目的：自动化创建和修复项目环境配置文件

import os

# 定义项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# --- 1. 创建或覆盖 .env 文件 ---
# 关键：使用 'utf-8' 编码，这在Python中默认不带BOM，从而解决编码问题。
env_content = "DATABASE_URL=postgresql://postgres:Lzhlzh985@localhost/helios"
env_file_path = os.path.join(project_root, '.env')

try:
    with open(env_file_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f"✅ 成功创建/覆盖 .env 文件于: {env_file_path}")
    print(f"   - 编码: UTF-8 (无BOM)")
    print(f"   - 内容: {env_content}")
except Exception as e:
    print(f"❌ 创建 .env 文件失败: {e}")


# --- 2. 创建或覆盖 requirements.txt 文件 ---
# 列出所有已知的、必要的依赖
requirements_content = """
fastapi
uvicorn[standard]
python-dotenv
psycopg2-binary
sqlalchemy
alembic
python-jose[cryptography]
python-multipart
pydantic
pydantic-settings
"""
req_file_path = os.path.join(project_root, 'requirements.txt')

try:
    with open(req_file_path, 'w', encoding='utf-8') as f:
        f.write(requirements_content.strip())
    print(f"\n✅ 成功创建/覆盖 requirements.txt 文件于: {req_file_path}")
except Exception as e:
    print(f"❌ 创建 requirements.txt 文件失败: {e}")

print("\n自动化环境修复脚本执行完毕。") 