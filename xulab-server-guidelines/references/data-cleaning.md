# 数据清理详细指南

## 清理原则

### 基本原则
1. **只保留必要文件**: 原始数据、脚本和最终结果
2. **确保可重现**: 保留关键中间结果
3. **定期清理**: 及时清理不再需要的文件

### 清理频率
- 每月进行一次全面清理
- 项目结束后立即清理
- 存储空间不足时及时清理

## 大文件处理

### 识别大文件
```bash
# 查找大于5G的文件
find . -type f -size +5G -printf '%p\t%k KB\n' | awk '{size=$2/1024/1024; printf "%s\t%.2f GB\n", $1, size}'
```

### 压缩大文件
```bash
# 压缩fastq文件
sbatch /home/projects/gzip.sh read.fastq

# 手动压缩
gzip large_file.txt
```

### 删除大文件
```bash
# 删除大于5G的文件（谨慎使用）
find . -type f -size +5G -delete
```

## 多文件目录处理

### 识别多文件目录
```bash
# 查找包含超过1000个文件的目录
find ./ -type d -exec sh -c 'echo -e "{}\t$(find "{}" -maxdepth 1 -type f | wc -l)"' \; | awk '$NF>1000'
```

### 打包多文件目录
```bash
# tar打包目录
tar -czf directory_name.tar.gz directory_name/

# 打包后删除原目录
tar -czf directory_name.tar.gz directory_name/ && rm -rf directory_name/
```

## 特定软件清理

### RepeatModeler
**保留文件**: `consensi.fa.classified`

**删除内容**:
- `round-*` 目录
- 其他中间文件

**清理命令**:
```bash
# 保留classified文件，删除其他
mv consensi.fa.classified ../
rm -rf round-*
```

### Juicer
**保留文件**: `aligned/merged_nodup.txt`

**删除内容**:
- 其他中间文件
- 项目结束后全部删除

**清理命令**:
```bash
# 保留merged_nodup.txt
mv aligned/merged_nodup.txt ../
rm -rf aligned/
```

### OrthoFinder
**删除目录**:
- `Gene_Trees`
- `Orthogroup_Sequences`
- `MultipleSequenceAlignments`

**清理命令**:
```bash
rm -rf Gene_Trees/
rm -rf Orthogroup_Sequences/
rm -rf MultipleSequenceAlignments/
```

### Maker
**删除目录**: `*_datastore`

**清理命令**:
```bash
rm -rf *_datastore/
```

### EVM (EvidenceModeler)
**删除内容**: 分染色体跑的临时文件

**清理命令**:
```bash
# 删除临时文件
rm -rf *.tmp
rm -rf temp_*
```

### BUSCO
**保留文件**: 最终统计结果

**删除内容**:
- `hmmer_output` 目录
- 其他中间文件

**清理命令**:
```bash
# 保留最终结果
mv full_table.tsv ../
rm -rf hmmer_output/
```

### Trinity
**保留文件**: 最终的转录本

**删除内容**: 其他中间文件

**清理命令**:
```bash
# 保留最终转录本
mv Trinity.fasta ../
rm -rf tmp/
```

## 文件保留规则

### 时间相关规则
- **2年以上的bam文件**: 不保留，需要时重新生成
- **1年以上大于2G的文本文件**: 压缩或删除

### 文件类型规则
- **VCF文件**: 只保留1个最终过滤好的
- **转录组和基因组组装**: 只保留最终fa文件
- **repeat和基因注释**: 只保留最终gff文件

## 缓存清理

### Conda缓存
```bash
conda clean -a
```

### CPAN缓存
```bash
rm -rf ~/.cpan/build/*
```

### pip缓存
```bash
pip cache purge
```

## 自动化清理脚本

### 基本清理脚本
```bash
#!/bin/bash
# 自动清理脚本

echo "开始清理..."

# 查找大文件
echo "查找大于5G的文件..."
find . -type f -size +5G -printf '%p\t%k KB\n' | awk '{size=$2/1024/1024; printf "%s\t%.2f GB\n", $1, size}'

# 查找多文件目录
echo "查找包含超过1000个文件的目录..."
find ./ -type d -exec sh -c 'echo -e "{}\t$(find "{}" -maxdepth 1 -type f | wc -l)"' \; | awk '$NF>1000'

# 清理缓存
echo "清理缓存..."
conda clean -a
rm -rf ~/.cpan/build/*
pip cache purge

echo "清理完成"
```

### 定期清理建议
1. **每月检查**: 运行清理脚本检查存储使用
2. **项目结束**: 立即清理中间文件
3. **存储不足**: 及时清理大文件和缓存

## 最佳实践

### 清理前准备
1. **备份重要数据**: 确保重要文件已备份
2. **记录清理内容**: 记录删除的文件和原因
3. **测试清理命令**: 先用小范围测试

### 清理后验证
1. **检查关键文件**: 确保重要文件未误删
2. **验证分析结果**: 确保分析结果完整
3. **更新文档**: 记录清理后的目录结构

### 长期维护
1. **定期检查**: 每月检查存储使用情况
2. **优化流程**: 建立自动清理流程
3. **培训团队**: 确保团队成员了解清理规范