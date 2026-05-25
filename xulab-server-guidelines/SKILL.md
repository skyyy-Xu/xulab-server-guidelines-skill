---
name: xulab-server-guidelines
description: Xu Lab服务器使用规范和准则。当AI在服务器上进行任何操作时触发，包括：编写sbatch脚本、申请计算资源、管理存储空间、安装软件、清理数据等。确保所有操作符合实验室规范，提高资源使用效率。
---

# Xu Lab Server Guidelines

## Overview

本skill提供Xu Lab服务器的使用规范，确保AI在服务器上的所有操作都符合实验室标准。当进行服务器操作时，必须遵循这些准则。

## Core Guidelines

### 1. 存储管理规范

#### 目录使用规则
- `/home1/projects` 或 `/home/projects`: 保存原始数据和重要结果文件，定期备份
- `/home1/user/` 或 `/home/user`: 工作目录
- `/tmp`: 需要频繁读写文件的操作（如repeatmodeler、busco等）

#### 存储清理原则
- 只保留原始数据、脚本和最终结果，以及关键中间结果
- 未来一年内不会再使用的数据线下保存
- 5G以上的目录需要检查清理
- 扫描时间超过15秒的目录有大量小文件，需清理或tar打包

### 2. 计算资源规范

#### 节点使用
- `comput1`: 有GPU，适合GPU计算任务
- `test`: 测试节点
- 登陆节点不执行长时间运行任务

#### CPU申请规则
- 申请CPU数与实际运算CPU数匹配
- 一般不超过20个CPU

### 3. 脚本编写规范

#### sbatch脚本要求
- 常用软件脚本整理到 `/home1/projects/pipeline/`
- 注意软件版本和参数选择
- 使用 `/tmp` 目录处理频繁读写操作
- **分区设置**: 使用 `--partition=normal`（不是 `cpu`）

#### 临时文件处理
- 下载数据先下载到 `/tmp`，再移动到目标位置
- 使用 `-tmp` 或 `-working-dir` 参数指定 `/tmp` 目录

### 4. 软件安装规范

#### 安装规则
- 使用share账号安装软件
- 优先在 `bio_soft` 自行安装
- 复杂环境变量时创建env（如 `conda create -p /home1/miniconda3/envs/rnabloom`）
- 避免过分依赖conda
- 安装失败可在学校集群安装

### 5. 数据清理规范

#### 大文件处理
- fastq等大文件用gzip压缩：`sbatch /home/projects/gzip.sh read.fastq`
- 用 `du -h` 扫描目录，重点检查大于5G的文件

#### 特定软件清理规则
- **RepeatModeler**: 仅保留 `consensi.fa.classified`
- **Juicer**: 仅保留 `aligned/merged_nodup.txt`
- **OrthoFinder**: 删除不需要的版本；删除 `Gene_Trees`、`Orthogroup_Sequence` 等目录
- **Maker**: 删除 `*_datastore` 目录
- **EVM**: 删除分染色体跑的临时文件
- **BUSCO**: 只保留最终统计结果
- **Trinity**: 只保留最终的转录本

#### 文件保留规则
- 2年以上的bam不保留
- VCF文件只保留1个最终过滤好的
- 1年以上大于2G的文本文件压缩或删除
- 转录组和基因组组装只保留最终fa文件
- repeat和基因注释只保留最终gff文件

### 6. 工具使用规范

#### 必备工具
熟练掌握以下工具，避免用excel分析处理数据：
- `bedtools`, `seqkit`, `csvtk`, `samtools`, `bcftools`
- `awk`, `sed`, `grep`, `sort`, `uniq`, `perl`

#### 其他规范
- 搜索用Google，禁止用百度
- 谨慎使用AI生成的内容
- 邮箱使用学校官方域名或个人常用邮箱，禁止用qq邮箱
- 文献管理推荐使用Zotero、EndNote等工具
- 尽可能使用在线文档，推荐用Google Drive客户端同步文件

## Quick Reference

### 常用命令

#### 查找大文件
```bash
find . -type f -size +5G -printf '%p\t%k KB\n' | awk '{size=$2/1024/1024; printf "%s\t%.2f GB\n", $1, size}'
```

#### 查找多文件目录
```bash
find ./ -type d -exec sh -c 'echo -e "{}\t$(find "{}" -maxdepth 1 -type f | wc -l)"' \; | awk '$NF>1000'
```

#### 缓存清理
```bash
conda clean -a
rm -rf ~/.cpan/build/*
pip cache purge
```

## Resources

### references/
详细的规范文档和参考资料。

- `storage-rules.md`: 存储管理详细规则
- `job-submission.md`: 作业提交规范
- `data-cleaning.md`: 数据清理详细指南

### scripts/
常用脚本和工具。

- `cleanup_storage.py`: 存储清理脚本
- `check_resources.sh`: 资源检查脚本