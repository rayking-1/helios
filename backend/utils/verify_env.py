#!/usr/bin/env python
"""
环境变量验证工具

用于检查和修复Helios Adaptive Planner所需的环境变量配置。
"""

import os
import sys
import json
from pathlib import Path
import platform


REQUIRED_ENV_VARS = {
    # LLM API 相关
    'OPENAI_API_KEY': {
        'description': 'OpenAI API密钥，用于智能体调用LLM',
        'example': 'sk-abcdefg123456789',
        'default': None  # 没有默认值，必须手动设置
    },
    'DASHSCOPE_API_KEY': {
        'description': '通义千问/灵积API密钥',
        'example': 'sk-abcdefg123456789',
        'default': None
    },
    
    # 数据库相关
    'DATABASE_URL': {
        'description': '数据库连接URL',
        'example': 'postgresql://user:password@localhost:5432/helios',
        'default': 'sqlite:///./helios.db'  # SQLite作为默认值
    },
    
    # 安全与认证相关
    'JWT_SECRET_KEY': {
        'description': 'JWT令牌签名密钥',
        'example': 'a-very-long-and-secure-random-string',
        'default': 'helios-development-secret-key'  # 仅用于开发环境
    },
    'JWT_ALGORITHM': {
        'description': 'JWT加密算法',
        'example': 'HS256',
        'default': 'HS256'
    },
    
    # 应用配置
    'ENVIRONMENT': {
        'description': '当前运行环境（development, testing, production）',
        'example': 'development',
        'default': 'development'
    },
    'LOG_LEVEL': {
        'description': '日志级别',
        'example': 'INFO',
        'default': 'INFO'
    },
    'PYTHONPATH': {
        'description': 'Python模块搜索路径',
        'example': '/path/to/helios_adaptive_planner',
        'default': None  # 自动设置
    }
}


def get_project_root() -> Path:
    """获取项目根目录的路径"""
    # 从当前文件开始，向上查找项目根目录
    current = Path(__file__).resolve()
    for _ in range(10):  # 限制最大向上查找层数
        current = current.parent
        if (current / 'pyproject.toml').exists() or (current / 'setup.py').exists():
            return current
        if current.parent == current:  # 已经到达文件系统根目录
            break
    
    # 如果找不到明确的项目标记，默认使用backend的父目录
    return Path(__file__).resolve().parent.parent.parent


def check_env_vars() -> dict:
    """检查所有必需的环境变量"""
    results = {}
    project_root = get_project_root()
    
    for var_name, config in REQUIRED_ENV_VARS.items():
        value = os.environ.get(var_name)
        if var_name == 'PYTHONPATH' and value is None:
            # 特殊处理PYTHONPATH
            if platform.system() == 'Windows':
                value = str(project_root).replace('\\', '\\\\')
            else:
                value = str(project_root)
        
        status = 'ok' if value else ('default' if config['default'] else 'missing')
        
        results[var_name] = {
            'value': value if value else config['default'],
            'status': status,
            'description': config['description'],
        }
        
    return results


def print_status(results: dict) -> bool:
    """打印环境变量检查结果，返回是否所有变量都已设置"""
    print("\n环境变量检查结果:")
    print("=" * 80)
    print(f"{'变量名':<20} {'状态':<10} {'值':<30} {'说明'}")
    print("-" * 80)
    
    all_set = True
    
    for var_name, info in results.items():
        status_display = {
            'ok': '✅ 已设置',
            'default': '⚠️ 使用默认值',
            'missing': '❌ 缺失'
        }.get(info['status'], info['status'])
        
        value_display = info['value'] if info['value'] else 'N/A'
        # 对API密钥进行脱敏处理
        if 'API_KEY' in var_name and value_display and value_display != 'N/A':
            value_display = value_display[:4] + '****' + value_display[-4:] if len(value_display) > 8 else '****'
            
        print(f"{var_name:<20} {status_display:<10} {value_display:<30} {info['description']}")
        
        if info['status'] == 'missing':
            all_set = False
            
    print("=" * 80)
    return all_set


def generate_env_file(results: dict) -> None:
    """根据检查结果生成.env文件"""
    project_root = get_project_root()
    env_file = project_root / '.env'
    
    if env_file.exists():
        print(f"\n⚠️ .env文件已存在: {env_file}")
        overwrite = input("是否覆盖? (y/N): ").strip().lower() == 'y'
        if not overwrite:
            print("已取消创建.env文件")
            return
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# Helios Adaptive Planner 环境变量配置\n")
        f.write("# 自动生成于 " + str(import_module('datetime').datetime.now()) + "\n\n")
        
        for var_name, config in REQUIRED_ENV_VARS.items():
            value = results[var_name]['value']
            if not value and config['default']:
                value = config['default']
                
            f.write(f"# {config['description']}\n")
            f.write(f"# 示例: {config['example']}\n")
            
            if value:
                f.write(f"{var_name}={value}\n")
            else:
                f.write(f"# {var_name}=\n")
            
            f.write("\n")
    
    print(f"\n✅ 已创建.env文件: {env_file}")


def fix_pythonpath() -> None:
    """修复PYTHONPATH环境变量"""
    project_root = get_project_root()
    
    if platform.system() == 'Windows':
        print("\n在Windows上设置PYTHONPATH:")
        print(f"  $env:PYTHONPATH = \"{project_root}\"")
        
        # 检查是否在PowerShell中运行
        if os.environ.get('PSModulePath'):
            # 提供PowerShell设置命令
            print("\n要在当前PowerShell会话中设置，请运行:")
            print(f"  $env:PYTHONPATH = \"{project_root}\"")
            print("\n要永久设置(需要管理员权限)，请运行:")
            print(f"  [Environment]::SetEnvironmentVariable('PYTHONPATH', \"{project_root}\", 'User')")
        else:
            # 提供CMD设置命令
            print("\n要在当前CMD会话中设置，请运行:")
            print(f"  set PYTHONPATH={project_root}")
            print("\n要永久设置，请运行:")
            print(f"  setx PYTHONPATH \"{project_root}\"")
    else:
        # Linux/Mac设置
        print("\n在Linux/Mac上设置PYTHONPATH:")
        print(f"  export PYTHONPATH=\"{project_root}\"")
        print("\n要永久设置，请添加到~/.bashrc或~/.zshrc:")
        print(f"  echo 'export PYTHONPATH=\"{project_root}\"' >> ~/.bashrc")


def create_local_config(results: dict) -> None:
    """创建本地配置文件"""
    project_root = get_project_root()
    config_dir = project_root / 'backend' / 'config'
    config_file = config_dir / 'local_config.py'
    
    os.makedirs(config_dir, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("# 本地配置文件 - 不要提交到版本控制系统\n")
        f.write("# 自动生成于 " + str(import_module('datetime').datetime.now()) + "\n\n")
        
        f.write("# 环境变量配置\n")
        f.write("ENV_VARS = {\n")
        
        for var_name, info in results.items():
            value = info['value']
            if value:
                if isinstance(value, str):
                    f.write(f"    '{var_name}': '{value}',\n")
                else:
                    f.write(f"    '{var_name}': {value},\n")
            else:
                f.write(f"    # '{var_name}': None,\n")
                
        f.write("}\n\n")
        
        f.write("# LLM配置\n")
        f.write("LLM_CONFIG = {\n")
        f.write("    'model': 'gpt-3.5-turbo',\n")
        f.write("    'temperature': 0.7,\n")
        f.write("    'config_list': [\n")
        
        # 添加OpenAI配置
        openai_key = results.get('OPENAI_API_KEY', {}).get('value')
        if openai_key:
            f.write("        {\n")
            f.write("            'model': 'gpt-3.5-turbo',\n")
            f.write(f"            'api_key': '{openai_key}',\n")
            f.write("        },\n")
            
        # 添加DashScope配置
        dashscope_key = results.get('DASHSCOPE_API_KEY', {}).get('value')
        if dashscope_key:
            f.write("        {\n")
            f.write("            'model': 'qwen-max',\n")
            f.write(f"            'api_key': '{dashscope_key}',\n")
            f.write("            'api_type': 'dashscope',\n")
            f.write("        },\n")
            
        f.write("    ],\n")
        f.write("}\n")
    
    print(f"\n✅ 已创建本地配置文件: {config_file}")
    print("   该文件包含LLM配置和环境变量，不会被提交到版本控制系统")


def import_module(module_name: str):
    """动态导入模块，用于避免引入不必要的依赖"""
    return __import__(module_name)


def main() -> None:
    """主函数"""
    print("Helios Adaptive Planner 环境验证工具")
    print("-" * 40)
    
    results = check_env_vars()
    all_set = print_status(results)
    
    if not all_set:
        print("\n❗ 检测到缺少必需的环境变量")
        print("请选择要执行的操作:")
        print("1. 生成.env文件")
        print("2. 查看如何设置PYTHONPATH")
        print("3. 创建本地配置文件")
        print("q. 退出")
        
        choice = input("\n请输入选项 (1-3 或 q): ").strip()
        
        if choice == '1':
            generate_env_file(results)
        elif choice == '2':
            fix_pythonpath()
        elif choice == '3':
            create_local_config(results)
        else:
            print("已退出")
            return
    else:
        print("\n✅ 所有环境变量检查通过")
        
        print("\n可选操作:")
        print("1. 生成.env文件")
        print("2. 创建本地配置文件")
        print("q. 退出")
        
        choice = input("\n请输入选项 (1-2 或 q): ").strip()
        
        if choice == '1':
            generate_env_file(results)
        elif choice == '2':
            create_local_config(results)
        else:
            print("已退出")
            return


if __name__ == "__main__":
    main() 
 
"""
环境变量验证工具

用于检查和修复Helios Adaptive Planner所需的环境变量配置。
"""

import os
import sys
import json
from pathlib import Path
import platform


REQUIRED_ENV_VARS = {
    # LLM API 相关
    'OPENAI_API_KEY': {
        'description': 'OpenAI API密钥，用于智能体调用LLM',
        'example': 'sk-abcdefg123456789',
        'default': None  # 没有默认值，必须手动设置
    },
    'DASHSCOPE_API_KEY': {
        'description': '通义千问/灵积API密钥',
        'example': 'sk-abcdefg123456789',
        'default': None
    },
    
    # 数据库相关
    'DATABASE_URL': {
        'description': '数据库连接URL',
        'example': 'postgresql://user:password@localhost:5432/helios',
        'default': 'sqlite:///./helios.db'  # SQLite作为默认值
    },
    
    # 安全与认证相关
    'JWT_SECRET_KEY': {
        'description': 'JWT令牌签名密钥',
        'example': 'a-very-long-and-secure-random-string',
        'default': 'helios-development-secret-key'  # 仅用于开发环境
    },
    'JWT_ALGORITHM': {
        'description': 'JWT加密算法',
        'example': 'HS256',
        'default': 'HS256'
    },
    
    # 应用配置
    'ENVIRONMENT': {
        'description': '当前运行环境（development, testing, production）',
        'example': 'development',
        'default': 'development'
    },
    'LOG_LEVEL': {
        'description': '日志级别',
        'example': 'INFO',
        'default': 'INFO'
    },
    'PYTHONPATH': {
        'description': 'Python模块搜索路径',
        'example': '/path/to/helios_adaptive_planner',
        'default': None  # 自动设置
    }
}


def get_project_root() -> Path:
    """获取项目根目录的路径"""
    # 从当前文件开始，向上查找项目根目录
    current = Path(__file__).resolve()
    for _ in range(10):  # 限制最大向上查找层数
        current = current.parent
        if (current / 'pyproject.toml').exists() or (current / 'setup.py').exists():
            return current
        if current.parent == current:  # 已经到达文件系统根目录
            break
    
    # 如果找不到明确的项目标记，默认使用backend的父目录
    return Path(__file__).resolve().parent.parent.parent


def check_env_vars() -> dict:
    """检查所有必需的环境变量"""
    results = {}
    project_root = get_project_root()
    
    for var_name, config in REQUIRED_ENV_VARS.items():
        value = os.environ.get(var_name)
        if var_name == 'PYTHONPATH' and value is None:
            # 特殊处理PYTHONPATH
            if platform.system() == 'Windows':
                value = str(project_root).replace('\\', '\\\\')
            else:
                value = str(project_root)
        
        status = 'ok' if value else ('default' if config['default'] else 'missing')
        
        results[var_name] = {
            'value': value if value else config['default'],
            'status': status,
            'description': config['description'],
        }
        
    return results


def print_status(results: dict) -> bool:
    """打印环境变量检查结果，返回是否所有变量都已设置"""
    print("\n环境变量检查结果:")
    print("=" * 80)
    print(f"{'变量名':<20} {'状态':<10} {'值':<30} {'说明'}")
    print("-" * 80)
    
    all_set = True
    
    for var_name, info in results.items():
        status_display = {
            'ok': '✅ 已设置',
            'default': '⚠️ 使用默认值',
            'missing': '❌ 缺失'
        }.get(info['status'], info['status'])
        
        value_display = info['value'] if info['value'] else 'N/A'
        # 对API密钥进行脱敏处理
        if 'API_KEY' in var_name and value_display and value_display != 'N/A':
            value_display = value_display[:4] + '****' + value_display[-4:] if len(value_display) > 8 else '****'
            
        print(f"{var_name:<20} {status_display:<10} {value_display:<30} {info['description']}")
        
        if info['status'] == 'missing':
            all_set = False
            
    print("=" * 80)
    return all_set


def generate_env_file(results: dict) -> None:
    """根据检查结果生成.env文件"""
    project_root = get_project_root()
    env_file = project_root / '.env'
    
    if env_file.exists():
        print(f"\n⚠️ .env文件已存在: {env_file}")
        overwrite = input("是否覆盖? (y/N): ").strip().lower() == 'y'
        if not overwrite:
            print("已取消创建.env文件")
            return
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# Helios Adaptive Planner 环境变量配置\n")
        f.write("# 自动生成于 " + str(import_module('datetime').datetime.now()) + "\n\n")
        
        for var_name, config in REQUIRED_ENV_VARS.items():
            value = results[var_name]['value']
            if not value and config['default']:
                value = config['default']
                
            f.write(f"# {config['description']}\n")
            f.write(f"# 示例: {config['example']}\n")
            
            if value:
                f.write(f"{var_name}={value}\n")
            else:
                f.write(f"# {var_name}=\n")
            
            f.write("\n")
    
    print(f"\n✅ 已创建.env文件: {env_file}")


def fix_pythonpath() -> None:
    """修复PYTHONPATH环境变量"""
    project_root = get_project_root()
    
    if platform.system() == 'Windows':
        print("\n在Windows上设置PYTHONPATH:")
        print(f"  $env:PYTHONPATH = \"{project_root}\"")
        
        # 检查是否在PowerShell中运行
        if os.environ.get('PSModulePath'):
            # 提供PowerShell设置命令
            print("\n要在当前PowerShell会话中设置，请运行:")
            print(f"  $env:PYTHONPATH = \"{project_root}\"")
            print("\n要永久设置(需要管理员权限)，请运行:")
            print(f"  [Environment]::SetEnvironmentVariable('PYTHONPATH', \"{project_root}\", 'User')")
        else:
            # 提供CMD设置命令
            print("\n要在当前CMD会话中设置，请运行:")
            print(f"  set PYTHONPATH={project_root}")
            print("\n要永久设置，请运行:")
            print(f"  setx PYTHONPATH \"{project_root}\"")
    else:
        # Linux/Mac设置
        print("\n在Linux/Mac上设置PYTHONPATH:")
        print(f"  export PYTHONPATH=\"{project_root}\"")
        print("\n要永久设置，请添加到~/.bashrc或~/.zshrc:")
        print(f"  echo 'export PYTHONPATH=\"{project_root}\"' >> ~/.bashrc")


def create_local_config(results: dict) -> None:
    """创建本地配置文件"""
    project_root = get_project_root()
    config_dir = project_root / 'backend' / 'config'
    config_file = config_dir / 'local_config.py'
    
    os.makedirs(config_dir, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("# 本地配置文件 - 不要提交到版本控制系统\n")
        f.write("# 自动生成于 " + str(import_module('datetime').datetime.now()) + "\n\n")
        
        f.write("# 环境变量配置\n")
        f.write("ENV_VARS = {\n")
        
        for var_name, info in results.items():
            value = info['value']
            if value:
                if isinstance(value, str):
                    f.write(f"    '{var_name}': '{value}',\n")
                else:
                    f.write(f"    '{var_name}': {value},\n")
            else:
                f.write(f"    # '{var_name}': None,\n")
                
        f.write("}\n\n")
        
        f.write("# LLM配置\n")
        f.write("LLM_CONFIG = {\n")
        f.write("    'model': 'gpt-3.5-turbo',\n")
        f.write("    'temperature': 0.7,\n")
        f.write("    'config_list': [\n")
        
        # 添加OpenAI配置
        openai_key = results.get('OPENAI_API_KEY', {}).get('value')
        if openai_key:
            f.write("        {\n")
            f.write("            'model': 'gpt-3.5-turbo',\n")
            f.write(f"            'api_key': '{openai_key}',\n")
            f.write("        },\n")
            
        # 添加DashScope配置
        dashscope_key = results.get('DASHSCOPE_API_KEY', {}).get('value')
        if dashscope_key:
            f.write("        {\n")
            f.write("            'model': 'qwen-max',\n")
            f.write(f"            'api_key': '{dashscope_key}',\n")
            f.write("            'api_type': 'dashscope',\n")
            f.write("        },\n")
            
        f.write("    ],\n")
        f.write("}\n")
    
    print(f"\n✅ 已创建本地配置文件: {config_file}")
    print("   该文件包含LLM配置和环境变量，不会被提交到版本控制系统")


def import_module(module_name: str):
    """动态导入模块，用于避免引入不必要的依赖"""
    return __import__(module_name)


def main() -> None:
    """主函数"""
    print("Helios Adaptive Planner 环境验证工具")
    print("-" * 40)
    
    results = check_env_vars()
    all_set = print_status(results)
    
    if not all_set:
        print("\n❗ 检测到缺少必需的环境变量")
        print("请选择要执行的操作:")
        print("1. 生成.env文件")
        print("2. 查看如何设置PYTHONPATH")
        print("3. 创建本地配置文件")
        print("q. 退出")
        
        choice = input("\n请输入选项 (1-3 或 q): ").strip()
        
        if choice == '1':
            generate_env_file(results)
        elif choice == '2':
            fix_pythonpath()
        elif choice == '3':
            create_local_config(results)
        else:
            print("已退出")
            return
    else:
        print("\n✅ 所有环境变量检查通过")
        
        print("\n可选操作:")
        print("1. 生成.env文件")
        print("2. 创建本地配置文件")
        print("q. 退出")
        
        choice = input("\n请输入选项 (1-2 或 q): ").strip()
        
        if choice == '1':
            generate_env_file(results)
        elif choice == '2':
            create_local_config(results)
        else:
            print("已退出")
            return


if __name__ == "__main__":
    main() 
 
 