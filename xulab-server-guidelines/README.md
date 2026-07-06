# Xu Lab Server Guidelines Skill 详细介绍

## 概述

**xulab-server-guidelines** 是一个专门为Xu Lab服务器设计的AI行为规范skill。它基于实验室的官方文档和最佳实践，为AI在服务器上的所有操作提供标准化的指导。

### 基本信息

- **Skill名称**: xulab-server-guidelines
- **版本**: 2.0
- **创建日期**: 2026年5月25日
- **适用环境**: Xu Lab服务器集群
- **触发条件**: 当AI进行任何服务器操作时自动触发，尤其包括 SSH 登录、端口转发、Slurm 提交、节点访问和存储清理

## 主要功能

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
- `normal`: 默认分区，用于一般计算任务
- 登陆节点不执行长时间运行任务

#### 分区设置规范
- **重要**: 使用 `--partition=normal`（不是 `cpu`）
- GPU任务使用 `--partition=comput1`
- 测试任务使用 `--partition=test`

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

### 7. SSH会话与自动化连接规范

- SSH 是受控资源，服务器操作必须少连接、合并检查、显式退出。
- 主 agent 同一时间最多保留 1 个交互式 SSH 会话；网页预览最多额外保留 1 个端口转发。
- subagent 默认不得直接 SSH；需要服务器执行时由主 agent 统一提交 Slurm 或统一做一次合并检查。
- 禁止 heartbeat/subagent 高频 SSH 轮询；长任务提交后告诉用户预计唤醒时间。
- 普通交互会话结束必须 `exit`；从登录节点进入计算节点时要逐层 `exit`；端口转发用完必须关闭。
- 如发现 `sshd-session` 异常增多，先停止新连接并列明细，不直接全杀，不误杀 Slurm 作业。

## 文件结构

```
xulab-server-guidelines/
├── SKILL.md                    # 主规范文件
├── references/
│   ├── storage-rules.md        # 存储管理详细规则
│   ├── job-submission.md       # 作业提交规范
│   └── data-cleaning.md        # 数据清理详细指南
└── scripts/
    ├── cleanup_storage.py      # 存储清理脚本
    └── check_resources.sh      # 资源检查脚本
```

### 文件说明

#### SKILL.md
主规范文件，包含所有核心规范和准则。当skill触发时，这是首先加载的文件。

#### references/ 目录
详细的规范文档，提供更深入的信息：

1. **storage-rules.md**
   - 存储管理详细规则
   - 目录结构说明
   - 文件保留策略
   - 常用清理命令

2. **job-submission.md**
   - 作业提交规范
   - 节点使用规则
   - CPU申请最佳实践
   - sbatch脚本模板

3. **data-cleaning.md**
   - 数据清理详细指南
   - 特定软件清理步骤
   - 自动化清理脚本
   - 最佳实践建议

4. **ssh-session-rules.md**
   - SSH会话数量限制
   - 交互会话和端口转发退出规则
   - subagent/heartbeat连接限制
   - `sshd-session` 异常增多后的处理流程

#### scripts/ 目录
实用脚本和工具：

1. **cleanup_storage.py**
   - Python脚本，用于自动化存储清理
   - 查找大文件和多文件目录
   - 清理各种缓存（conda、cpan、pip）

2. **check_resources.sh**
   - Bash脚本，用于检查服务器资源
   - 显示磁盘、内存、CPU使用情况
   - 检查运行中的作业

## 使用场景

### 触发条件
这个skill会在以下情况下自动触发：

1. **编写sbatch脚本时**
   - 确保脚本符合实验室规范
   - 正确设置资源申请参数
   - 使用正确的目录结构

2. **申请计算资源时**
   - 合理分配CPU和内存
   - 选择合适的节点类型
   - 遵循资源使用限制

3. **管理存储空间时**
   - 遵循存储清理原则
   - 正确处理大文件
   - 定期清理不需要的文件

4. **安装软件时**
   - 使用正确的安装目录
   - 遵循环境管理规范
   - 记录软件版本信息

5. **清理数据时**
   - 按照特定软件的清理规则操作
   - 保留必要的文件
   - 删除不需要的中间文件

### 具体示例

#### 示例1：编写sbatch脚本
当AI需要编写一个sbatch脚本时，skill会确保：
- 使用正确的shebang行
- 设置合理的资源申请参数
- 将脚本保存到 `/home1/projects/pipeline/`
- 使用 `/tmp` 目录处理临时文件

#### 示例2：清理分析结果
当AI需要清理一个已完成的分析项目时，skill会：
- 检查项目中的大文件
- 按照特定软件的清理规则操作
- 只保留最终结果和必要文件
- 记录清理过程

#### 示例3：安装新软件
当AI需要安装一个新软件时，skill会：
- 使用share账号进行安装
- 优先选择 `bio_soft` 目录
- 创建独立的conda环境（如需要）
- 记录安装过程和版本信息

## 包含的脚本和工具

### cleanup_storage.py

#### 功能
- 查找大于指定大小的文件
- 识别包含大量文件的目录
- 清理conda、cpan、pip缓存
- 提供存储使用报告

#### 使用方法
```bash
# 检查当前目录
python3 cleanup_storage.py

# 检查指定目录
python3 cleanup_storage.py /path/to/directory
```

#### 输出示例
```
============================================================
存储清理脚本
============================================================

查找大于 5G 的文件...
/home/user/large_file.fastq	6.50 GB

查找包含超过 1000 个文件的目录...
/home/user/analysis/results	1523

清理Conda缓存...
Conda缓存清理完成

清理CPAN缓存...
CPAN缓存清理完成

清理pip缓存...
pip缓存清理完成

============================================================
清理完成
============================================================
```

### check_resources.sh

#### 功能
- 检查磁盘使用情况
- 显示内存和CPU使用
- 查找大文件和多文件目录
- 检查运行中的作业

#### 使用方法
```bash
# 运行资源检查
bash check_resources.sh
```

#### 输出示例
```
==============================================
服务器资源检查
==============================================

1. 磁盘使用情况:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       500G  350G  150G  70% /home

2. 当前目录大小:
2.5G	.

3. 查找大于5G的文件:
./data/raw_sequences.fastq	6.50 GB

4. 查找包含超过1000个文件的目录:
./analysis/results	1523

5. 内存使用情况:
              total        used        free      shared  buff/cache   available
Mem:           62Gi        45Gi       8.5Gi       1.2Gi       8.2Gi        15Gi

6. CPU使用情况:
top - 14:30:25 up 45 days,  5:23,  2 users,  load average: 2.15, 1.89, 1.67

7. 运行中的作业:
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
            123456    comput1  analysis   xiaotian  R    2:15:03      1 comput1-01

8. Conda环境:
# conda environments:
#
base                  *  /home/miniconda3
rnabloom                 /home/miniconda3/envs/rnabloom

==============================================
检查完成
==============================================
```

## 最佳实践

### 1. 定期检查存储
- 每月运行一次 `check_resources.sh`
- 及时清理大文件和多文件目录
- 监控存储使用趋势

### 2. 遵循清理规范
- 按照特定软件的清理规则操作
- 保留必要的中间结果
- 记录清理过程和原因

### 3. 合理申请资源
- 根据实际需求申请CPU和内存
- 避免资源浪费
- 测试确定最佳资源配置

### 4. 规范脚本管理
- 将常用脚本整理到 `/home1/projects/pipeline/`
- 记录软件版本和参数
- 确保脚本可重现

### 5. 团队协作
- 遵循实验室规范
- 分享有用的脚本和工具
- 及时沟通资源使用情况

## 常见问题

### Q1: 如何处理大文件？
A: 使用gzip压缩fastq等大文件，命令：`sbatch /home/projects/gzip.sh read.fastq`

### Q2: 如何查找包含大量文件的目录？
A: 使用命令：`find ./ -type d -exec sh -c 'echo -e "{}\t$(find "{}" -maxdepth 1 -type f | wc -l)"' \; | awk '$NF>1000'`

### Q3: 如何清理conda缓存？
A: 运行命令：`conda clean -a`

### Q4: 应该保留哪些中间结果？
A: 只保留能确保分析可重现的关键中间结果，其他中间文件应该清理。

### Q5: 如何正确申请计算资源？
A: 根据软件文档和任务规模确定CPU数，一般不超过20个CPU，申请数要与实际运算数匹配。

## 更新和维护

### 版本更新
- 定期根据实验室最新规范更新skill
- 添加新的软件清理规则
- 优化脚本功能

### 反馈和改进
- 收集使用反馈
- 根据实际需求调整规范
- 持续改进skill内容

## 相关资源

### 实验室文档
- Xulab须知.docx
- Xulab server guideline.docx
- Data cleaning guideline.docx
- Storage rules.docx
- storage usage.xlsx

### 参考链接
- 实验室Google Drive: [链接]
- 软件安装目录: `/home/bio_soft/`
- 常用脚本目录: `/home1/projects/pipeline/`

## 总结

**xulab-server-guidelines** skill是Xu Lab服务器使用的重要规范工具。它通过标准化AI的行为，确保所有服务器操作都符合实验室的最佳实践，从而提高资源使用效率，减少错误，并促进团队协作。

通过遵循这个skill中的规范，AI可以：
1. 正确管理存储空间
2. 合理申请计算资源
3. 编写规范的脚本
4. 有效清理数据
5. 规范安装和使用软件

这个skill是动态的，会根据实验室的发展和需求不断更新和完善。
