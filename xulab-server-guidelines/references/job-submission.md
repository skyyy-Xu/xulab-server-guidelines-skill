# 作业提交规范

## 节点使用规则

### 可用节点
- **comput1**: 有GPU，适合GPU计算任务
- **test**: 测试节点，用于测试脚本和小规模任务
- **normal**: 默认分区，用于一般计算任务

### 分区设置规范
- **重要**: 使用 `--partition=normal`（不是 `cpu`）
- GPU任务使用 `--partition=comput1`
- 测试任务使用 `--partition=test`

### 登陆节点限制
- 登陆节点一般不执行需要长时间运行的任务
- 仅用于文件操作、脚本编辑等轻量级任务

## CPU申请规则

### 基本原则
- 申请CPU数要与实际运算CPU数匹配
- 一般不超过20个CPU

### 最佳实践
1. **评估任务需求**: 根据软件文档和任务规模确定CPU数
2. **避免资源浪费**: 不要申请过多CPU
3. **测试优化**: 先用小规模测试确定最佳CPU数

## sbatch脚本规范

### 脚本存放位置
- 常用软件脚本整理到 `/home1/projects/pipeline/`
- 注意软件版本和参数的选择

### 脚本模板

#### 基本模板
```bash
#!/bin/bash
#SBATCH -J job_name
#SBATCH -o job_name.out
#SBATCH -e job_name.err
#SBATCH -p normal
#SBATCH -n 16
#SBATCH --mem=64G
#SBATCH -t 24:00:00

# 脚本内容
```

#### GPU任务模板
```bash
#!/bin/bash
#SBATCH -J gpu_job
#SBATCH -o gpu_job.out
#SBATCH -e gpu_job.err
#SBATCH -p comput1
#SBATCH -n 4
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH -t 12:00:00

# GPU任务内容
```

### 参数说明

#### 常用参数
- `-J`: 作业名称
- `-o`: 标准输出文件
- `-e`: 标准错误文件
- `-p`: 分区/队列（使用 `normal`，不是 `cpu`）
- `-n`: CPU核心数
- `--mem`: 内存大小
- `-t`: 运行时间限制

#### GPU相关参数
- `--gres=gpu:1`: 申请1个GPU
- `-p comput1`: 使用GPU分区

## 临时文件处理

### /tmp目录使用
- 需要频繁读写文件的操作使用 `/tmp` 目录
- 参考 `/home1/projects/pipeline/repeatmasker.sh`

### 软件特定参数
- 使用 `-tmp` 或 `-working-dir` 参数指定 `/tmp` 目录
- 适用于：mitoZ、trinity等软件

### 数据下载规范
- 下载数据先下载到 `/tmp`，再移动到目标位置
- 适用于：obsutil、ascp、wget等工具

## 流程管理

### 脚本整理
- 常用软件脚本整理到 `/home1/projects/pipeline/`
- 记录软件版本和参数选择
- 便于复用和维护

### 版本控制
- 记录使用的软件版本
- 记录重要的参数设置
- 确保结果可重现

## 常见问题

### 作业提交失败
1. 检查脚本语法
2. 确认资源申请合理
3. 检查分区是否正确

### 作业运行缓慢
1. 检查CPU申请是否匹配
2. 检查内存是否充足
3. 考虑使用 `/tmp` 目录提高I/O性能

### 资源不足
1. 调整CPU和内存申请
2. 考虑分批次运行
3. 使用更高效的算法或工具