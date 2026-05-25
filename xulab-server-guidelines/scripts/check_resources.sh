#!/bin/bash
# 资源检查脚本
# 用于检查服务器资源使用情况

echo "=============================================="
echo "服务器资源检查"
echo "=============================================="

# 检查磁盘使用情况
echo -e "\n1. 磁盘使用情况:"
df -h | grep -E "(Filesystem|/home|/tmp)"

# 检查当前目录大小
echo -e "\n2. 当前目录大小:"
du -sh . 2>/dev/null || echo "无法获取目录大小"

# 检查大文件
echo -e "\n3. 查找大于5G的文件:"
find . -type f -size +5G -printf '%p\t%k KB\n' 2>/dev/null | awk '{size=$2/1024/1024; printf "%s\t%.2f GB\n", $1, size}' | head -10

# 检查多文件目录
echo -e "\n4. 查找包含超过1000个文件的目录:"
find ./ -type d -exec sh -c 'echo -e "{}\t$(find "{}" -maxdepth 1 -type f | wc -l)"' \; 2>/dev/null | awk '$NF>1000' | head -10

# 检查内存使用
echo -e "\n5. 内存使用情况:"
free -h

# 检查CPU使用
echo -e "\n6. CPU使用情况:"
top -bn1 | head -5

# 检查运行中的作业
echo -e "\n7. 运行中的作业:"
squeue -u $USER 2>/dev/null || echo "无法获取作业信息"

# 检查conda环境
echo -e "\n8. Conda环境:"
conda env list 2>/dev/null || echo "无法获取conda环境信息"

echo -e "\n=============================================="
echo "检查完成"
echo "=============================================="