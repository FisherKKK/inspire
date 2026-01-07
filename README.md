# Inspire - 个人技术知识库

这是一个专注于人工智能、分布式系统和软件工程的个人知识管理仓库，记录学习笔记、研究论文、技术文章和实践总结。

## 📚 仓库结构

| 目录 | 内容简介 | 更新频率 |
|------|---------|---------|
| [HPC](./HPC/) | 高性能计算、CUDA、GPU编程 | ⭐⭐⭐ |
| [LLM](./LLM/) | 大语言模型笔记和研究论文 | ⭐⭐⭐⭐⭐ |
| [os](./os/) | 操作系统相关资料 | ⭐⭐ |
| [talk](./talk/) | 技术访谈和演讲（Ilya Sutskever等） | ⭐⭐⭐ |
| [Timeline](./Timeline/) | **学习时间线** - 追踪AI前沿动态 | ⭐⭐⭐⭐⭐ |
| [vLLM开发](./vLLM开发/) | vLLM架构和开发笔记 | ⭐⭐⭐⭐ |
| [编程语言](./编程语言/) | 现代C++、SIMD、性能优化 | ⭐⭐⭐⭐ |
| [常用](./常用/) | 常用工具和基础技术（Git、UV） | ⭐⭐⭐ |
| [机器学习](./机器学习/) | ML基础：tokenization、embeddings、反向传播 | ⭐⭐⭐⭐ |
| [数据库](./数据库/) | 向量搜索技术 | ⭐⭐⭐⭐ |
| [算法设计](./算法设计/) | 向量搜索算法（Rust实现） | ⭐⭐⭐ |
| [碎碎念](./碎碎念/) | 杂项笔记和思考 | ⭐⭐ |
| [推荐](./推荐/) | 推荐系统研究 | ⭐⭐⭐ |

## 🎯 核心内容

### 📰 [Timeline - 学习时间线](./Timeline/timeline.md)
**最有价值的内容**：追踪最新AI发展、研究论文解读、技术趋势分析。每日更新，包含：
- AI/ML前沿进展
- 优质技术文章链接
- 个人学习思考
- TODO和待深入研究的主题

### 🔧 常用命令和工具
详见 [常用/基础技术.md](./常用/基础技术.md)：
- Git工作流（切换upstream tag、分支管理）
- UV包管理器使用指南

### 💡 技术焦点
- **AI/ML系统**: LLM架构、训练、推理优化
- **向量搜索**: 数据库优化、推荐系统
- **高性能计算**: CUDA、SIMD、CPU优化、并行处理
- **系统编程**: 内存管理、汇编优化、数值计算

## 🚀 快速开始

### 浏览最新内容
```bash
# 查看最新学习动态
cat Timeline/timeline.md | head -100

# 搜索特定主题
grep -r "LLM推理" --include="*.md"
```

### 使用UV管理Python项目
```bash
# 安装UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建新项目
uv init project
uv add <package>
uv run script.py
```

## 📖 学习路径建议

### 入门AI/ML
1. [机器学习/](./机器学习/) - 基础概念
2. [LLM/](./LLM/) - 大语言模型
3. [Timeline/](./Timeline/) - 了解最新趋势

### 深入系统优化
1. [编程语言/](./编程语言/) - 现代C++和SIMD
2. [HPC/](./HPC/) - 高性能计算
3. [vLLM开发/](./vLLM开发/) - 实战项目

### 专注向量搜索
1. [数据库/](./数据库/) - 向量搜索技术
2. [算法设计/](./算法设计/) - Rust实现
3. [推荐/](./推荐/) - 推荐系统应用

## 🔗 参考资源

本仓库引用了众多优质资源，包括：
- **研究人员**: Andrej Karpathy, Ilya Sutskever
- **技术博客**: Simon Willison (simonwillison.net), Eugene Yan, Chip Huyen
- **社区**: Applied LLMs, HackerNews
- **完整列表**: 见 [Timeline/timeline.md](./Timeline/timeline.md)

## 📝 贡献指南

这是个人学习仓库，主要记录：
- 技术文章阅读笔记
- 研究论文总结
- 实践项目经验
- 学习心得和思考

**组织原则**:
- 按技术领域分类
- Markdown为主要格式
- 重视外部链接引用
- 持续更新Timeline

## 📊 统计信息

- **总文件数**: 41
- **Markdown笔记**: 17
- **研究论文(PDF)**: 15
- **最近更新**: 2025年1月

## 🛠️ 使用的工具

- **版本控制**: Git
- **Python管理**: UV
- **AI助手**: Claude Code
- **笔记编辑**: Markdown

## 📮 联系方式

仓库地址: https://gitee.com/FisherKK/inspire

---

> "Self-Taught Engineers Often Outperform"
> 坚持学习，关注基础，追踪前沿
