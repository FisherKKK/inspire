# RSS订阅源分类说明

本文档列出了所有配置的RSS订阅源，方便管理和选择。

## 📊 统计概览

- **总RSS源数**: 60+
- **默认启用**: 40+
- **可选启用**: 20+

## 🎯 按领域分类

### 1. AI/ML (17个源)

#### 顶级研究者和工程师 (8个)
- ✅ Simon Willison - AI工具和实践
- ✅ Eugene Yan - ML工程和MLOps
- ✅ Chip Huyen - 生产环境ML
- ✅ Hamel Husain - AI工程
- ✅ Lilian Weng (OpenAI) - 深度学习研究
- ✅ Sebastian Raschka - ML基础和实践
- ✅ Jay Alammar - ML可视化解释
- ✅ Shreya Shankar - 数据和ML系统

#### 公司博客 (6个)
- ✅ OpenAI Blog - GPT系列和最新研究
- ✅ Anthropic Blog - Claude和AI安全
- ✅ Google AI Blog - Google研究成果
- ⏸️ DeepMind Blog - 前沿AI研究（更新慢）
- ✅ Meta AI Blog - LLaMA等开源模型
- ✅ Hugging Face Blog - 开源ML生态

#### 新闻和聚合 (3个)
- ✅ Smol AI News - AI新闻聚合
- ✅ The Gradient - AI深度文章
- ⏸️ LessWrong AI - AI安全和哲学（内容多）

### 2. LLM Infrastructure & vLLM (3个)

- ✅ **Anyscale Blog** - Ray和分布式推理
- ✅ **Modal Blog** - Serverless GPU
- ✅ **vLLM GitHub Releases** - vLLM版本更新

### 3. 数据库系统 (7个)

- ✅ **Postgres Blog** - PostgreSQL官方博客
- ⏸️ MySQL Server Blog - MySQL更新（较慢）
- ✅ **Redis Blog** - Redis新特性和实践
- ✅ **ClickHouse Blog** - 列式数据库和分析
- ✅ **DuckDB Blog** - 嵌入式分析数据库
- ⏸️ Andy Pavlo (CMU) - 数据库学术研究
- ⏸️ Use The Index, Luke - SQL优化教程

**推荐**: Postgres, Redis, ClickHouse, DuckDB

### 4. 操作系统 & 系统编程 (5个)

- ✅ **LWN.net** - Linux内核和系统新闻
- ✅ **Julia Evans** - 系统知识可视化讲解
- ✅ **Amos (fasterthanlime)** - Rust和系统编程
- ✅ **Brendan Gregg** - 性能分析大师
- ✅ **Cloudflare Blog** - 边缘计算和系统架构

**必读**: LWN.net, Brendan Gregg

### 5. 性能优化 (4个)

- ✅ **Daniel Lemire** - SIMD和底层优化专家
- ✅ **Easyperf** - 性能分析教程
- ⏸️ Travis Downs - 深度性能文章（更新慢但质量高）
- ⏸️ Mechanical Sympathy - 经典性能博客（已停更）

**核心**: Daniel Lemire, Easyperf

### 6. C++ 编程 (6个)

- ✅ **C++ Stories** (Bartłomiej Filipek) - 现代C++技巧
- ✅ **Modernes C++** (Rainer Grimm) - C++并发和现代特性
- ✅ **Fluent C++** (Jonathan Boccara) - C++代码质量
- ✅ **Arthur O'Dwyer** - C++标准和模板
- ⏸️ Sutter's Mill (Herb Sutter) - C++委员会成员（更新少）
- ✅ **ISO C++ Blog** - C++标准和新闻

**推荐**: C++ Stories, Modernes C++, Arthur O'Dwyer

### 7. 通用工程实践 (7个)

- ✅ **Vicki Boykis** - 数据和工程
- ✅ **High Scalability** - 大规模系统架构
- ⏸️ The Morning Paper - 论文解读（已停更，但经典）
- ⏸️ InfoQ - 技术新闻（内容多）
- ✅ **ACM Queue** - 学术和工程结合
- ✅ **Martin Fowler** - 软件架构大师
- ✅ **Netflix Tech Blog** - Netflix工程实践
- ✅ **Uber Engineering Blog** - Uber技术分享

**必读**: Martin Fowler, Netflix/Uber Tech Blog

### 8. Rust (2个)

- ✅ **Rust Blog** - Rust官方博客
- ✅ **This Week in Rust** - Rust周报

### 9. 技术新闻 & 开源 (3个)

- ✅ **Lobsters** - 技术新闻聚合（类似HN但更专注）
- ⏸️ Dev.to AI/ML - 社区文章（质量参差）
- ⏸️ Medium TDS - 需订阅
- ✅ **Papers With Code** - 最新ML论文+代码
- ✅ **GitHub Engineering** - GitHub工程实践

### 10. 学术研究 (3个)

- ⏸️ arXiv AI - AI论文（每天100+篇，慎用）
- ⏸️ arXiv ML - ML论文（每天200+篇，慎用）
- ✅ **Papers With Code** - 精选有代码的论文

## 🔧 使用建议

### 初始配置（精简版，约20个源）

如果你第一次使用，建议只启用以下核心源：

```yaml
# AI/ML核心
- Simon Willison, Eugene Yan, Chip Huyen
- OpenAI, Anthropic, Hugging Face
- Smol AI News

# Infrastructure
- Anyscale, Modal, vLLM

# 数据库
- Postgres, Redis, ClickHouse

# 系统和性能
- LWN.net, Brendan Gregg, Daniel Lemire

# C++
- C++ Stories, Modernes C++

# 工程实践
- Martin Fowler, Netflix Tech Blog
```

### 完整配置（推荐，约40个源）

当前配置已经是推荐的完整配置，所有标记✅的源都已启用。

### 高级配置（可选）

如果你需要更全面的覆盖，可以启用：
- Travis Downs（深度性能文章）
- Andy Pavlo（数据库学术）
- arXiv feeds（论文每日更新）
- InfoQ（技术新闻）

## 📝 管理建议

### 1. 定期调整

每月查看 `daily-digest/` 中的内容，评估各源的质量：
- 如果某个源持续提供高价值内容 → 保持启用
- 如果某个源内容重复或质量下降 → 禁用
- 发现新的优质源 → 添加到配置

### 2. 控制数量

建议同时启用的源数量：
- **最少**: 15-20个（核心源）
- **推荐**: 30-40个（当前配置）
- **最多**: 50-60个（完整配置）

超过60个源会导致每日摘要过长，难以阅读。

### 3. 分类管理

当某个领域的文章过多时：
- 考虑创建专门的主题摘要
- 或者提高该领域源的筛选标准
- 使用关键词过滤

### 4. 质量 vs 数量

优先考虑：
- ✅ 更新频率适中（每周1-3篇）
- ✅ 内容深度足够
- ✅ 与你的研究方向相关
- ❌ 避免日更但质量低的源
- ❌ 避免很少更新的源

## 🎯 特别推荐（必读源）

基于你的兴趣领域，强烈推荐以下10个核心源：

1. **Brendan Gregg** - 性能优化必读
2. **Daniel Lemire** - SIMD和底层优化
3. **LWN.net** - Linux和系统编程
4. **vLLM Releases** - 直接追踪vLLM更新
5. **C++ Stories** - 现代C++实践
6. **Eugene Yan** - ML工程和系统设计
7. **Anyscale Blog** - 分布式ML推理
8. **ClickHouse Blog** - 高性能数据库
9. **Netflix Tech Blog** - 大规模系统实践
10. **Papers With Code** - 前沿ML研究

## 📊 更新频率参考

- **日更**: HackerNews, Smol AI News
- **周更**: Most engineering blogs, Papers With Code
- **月更**: 学术博客, ISO C++
- **不定期**: 公司博客（发布新产品时）

---

最后更新: 2026-01-07
