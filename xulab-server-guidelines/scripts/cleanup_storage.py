#!/usr/bin/env python3
"""
存储清理脚本
用于检查和清理服务器存储空间
"""

import os
import subprocess
import sys
from pathlib import Path

def find_large_files(directory=".", size_limit="5G"):
    """查找大文件"""
    print(f"\n查找大于 {size_limit} 的文件...")
    cmd = f"find {directory} -type f -size +{size_limit} -printf '%p\\t%k KB\\n' | awk '{{size=$2/1024/1024; printf \"%s\\t%.2f GB\\n\", $1, size}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    else:
        print("未找到大文件")

def find_many_files_directories(directory=".", threshold=1000):
    """查找包含大量文件的目录"""
    print(f"\n查找包含超过 {threshold} 个文件的目录...")
    cmd = f"find {directory} -type d -exec sh -c 'echo -e \"{{}}\\t$(find \"{{}}\" -maxdepth 1 -type f | wc -l)\"' \\; | awk '$NF>{threshold}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    else:
        print("未找到多文件目录")

def clean_conda_cache():
    """清理Conda缓存"""
    print("\n清理Conda缓存...")
    try:
        subprocess.run(["conda", "clean", "-a"], check=True)
        print("Conda缓存清理完成")
    except subprocess.CalledProcessError:
        print("Conda缓存清理失败")

def clean_cpan_cache():
    """清理CPAN缓存"""
    print("\n清理CPAN缓存...")
    cpan_build = Path.home() / ".cpan" / "build"
    if cpan_build.exists():
        try:
            subprocess.run(["rm", "-rf", str(cpan_build)], check=True)
            print("CPAN缓存清理完成")
        except subprocess.CalledProcessError:
            print("CPAN缓存清理失败")
    else:
        print("CPAN缓存目录不存在")

def clean_pip_cache():
    """清理pip缓存"""
    print("\n清理pip缓存...")
    try:
        subprocess.run(["pip", "cache", "purge"], check=True)
        print("pip缓存清理完成")
    except subprocess.CalledProcessError:
        print("pip缓存清理失败")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."

    print("=" * 60)
    print("存储清理脚本")
    print("=" * 60)

    # 查找大文件
    find_large_files(directory)

    # 查找多文件目录
    find_many_files_directories(directory)

    # 清理缓存
    clean_conda_cache()
    clean_cpan_cache()
    clean_pip_cache()

    print("\n" + "=" * 60)
    print("清理完成")
    print("=" * 60)

if __name__ == "__main__":
    main()