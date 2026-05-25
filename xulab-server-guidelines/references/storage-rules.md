# 存储管理详细规则

## 目录结构

### 主要目录
- `/home1/projects` 或 `/home/projects`: 保存原始数据和重要结果文件，定期备份
- `/home1/user/` 或 `/home/user`: 工作目录
- `/tmp`: 临时文件目录，用于频繁读写操作

### 软件安装目录
- `/home/bio_soft/`: 软件安装目录
- `/home/miniconda3/`: Conda环境目录

## 存储清理原则

### 基本原则
1. **只保留必要文件**: 原始数据、脚本和最终结果，以及关键中间结果
2. **确保可重现**: 只要确保能重现分析过程
3. **定期清理**: 未来一年内不会再使用的数据线下保存

### 具体规则

#### 大文件处理
- 用 `du -h` 扫描目录，5G以上的目录需要检查清理
- fastq等大文件用gzip压缩：`sbatch /home/projects/gzip.sh read.fastq`

#### 目录扫描
- 单个目录扫描时间超过15秒，意味着有大量小文件
- 需要清理或tar打包

#### 文件保留规则
- **2年以上的bam文件**: 不保留，有需要重新生成
- **VCF文件**: 只保留1个最终过滤好的
- **1年以上大于2G的文本文件**: 压缩或删除
- **转录组和基因组组装**: 只保留最终fa文件
- **repeat和基因注释**: 只保留最终gff文件

## 特定软件清理规则

### RepeatModeler
- 仅保留 `consensi.fa.classified`
- 不保留 `round-*` 目录

### Juicer
- 仅保留 `aligned/merged_nodup.txt`
- 项目结束后删除

### OrthoFinder
- 删除不需要的版本
- 删除以下目录：
  - `Gene_Trees`
  - `Orthogroup_Sequences`
  - `MultipleSequenceAlignments`

### Maker
- 删除 `*_datastore` 目录

### EVM (EvidenceModeler)
- 删除分染色体跑的临时文件

### BUSCO
- 只保留最终统计结果
- 删除 `hmmer_output` 等目录

### Trinity
- 只保留最终的转录本

## 常用命令

### 查找大文件
```bash
find . -type f -size +5G -printf '%p\t%k KB\n' | awk '{size=$2/1024/1024; printf "%s\t%.2f GB\n", $1, size}'
```

### 查找多文件目录
```bash
find ./ -type d -exec sh -c 'echo -e "{}\t$(find "{}" -maxdepth 1 -type f | wc -l)"' \; | awk '$NF>1000'
```

### 缓存清理
```bash
# Conda缓存清理
conda clean -a

# CPAN缓存清理
rm -rf ~/.cpan/build/*

# pip缓存清理
pip cache purge
```

## 最佳实践

### 项目结束时
1. 清理所有中间文件
2. 只保留最终结果和脚本
3. 记录使用的软件版本和参数
4. 将重要数据备份到 `/home1/projects`

### 定期维护
1. 每月检查存储使用情况
2. 清理过期的临时文件
3. 压缩大文件
4. 删除不再需要的分析结果