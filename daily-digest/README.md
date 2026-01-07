# 每日技术摘要 - Daily Tech Digest

每天自动从HackerNews和优质RSS源抓取技术文章，使用AI生成中文摘要。

## 📰 最新摘要

查看 [`daily-digest/`](./daily-digest/) 目录获取每日技术摘要。

## ✨ 功能特性

- 🤖 **自动抓取**: 每天定时抓取HackerNews热门文章和RSS订阅
- 🧠 **AI摘要**: 使用Claude生成简洁的中文摘要
- 📊 **智能分类**: 按主题自动分类文章
- ⚡ **可配置**: 灵活的配置文件，轻松添加/删除订阅源
- 🔄 **自动化**: GitHub Actions定时任务，无需手动操作

## 🚀 快速开始

### 本地运行

1. **安装依赖**

```bash
pip install -r scripts/requirements.txt
```

2. **配置环境变量**

```bash
# Linux/macOS
export ANTHROPIC_AUTH_TOKEN="your-api-key"
export ANTHROPIC_BASE_URL="https://api.anthropic.com"  # 可选

# Windows PowerShell
$env:ANTHROPIC_AUTH_TOKEN = "your-api-key"
$env:ANTHROPIC_BASE_URL = "https://api.anthropic.com"
```

或者直接source你的cc.sh配置:
```bash
source cc.sh
```

3. **运行脚本**

```bash
python scripts/generate_digest.py
```

生成的摘要会保存在 `daily-digest/digest-YYYY-MM-DD.md`

### GitHub Actions 自动化

本仓库已配置GitHub Actions，会自动每天运行。

#### 配置步骤

1. **设置Secrets**

在GitHub仓库设置中添加以下Secrets:
- `ANTHROPIC_AUTH_TOKEN`: 你的Anthropic API密钥
- `ANTHROPIC_BASE_URL`: (可选) 自定义API端点

路径: Settings → Secrets and variables → Actions → New repository secret

2. **启用工作流**

工作流配置在 `.github/workflows/daily-digest.yml`

默认每天UTC 0点 (北京时间早上8点) 运行，你也可以:
- 手动触发: Actions → Daily Tech Digest → Run workflow
- 修改时间: 编辑cron表达式

## ⚙️ 配置说明

### 配置文件: `config/sources.yaml`

#### 1. HackerNews配置

```yaml
hacker_news:
  enabled: true
  max_items: 30        # 最多抓取30篇
  min_score: 100       # 最小分数阈值
```

#### 2. 添加RSS订阅源

```yaml
rss_feeds:
  - name: "博客名称"
    url: "https://example.com/feed.xml"
    category: "AI/ML"
    enabled: true
```

**常用RSS订阅源已预配置**:
- Simon Willison (AI)
- Eugene Yan (ML Engineering)
- Chip Huyen (MLOps)
- Hamel Husain (AI Engineering)
- Vicki Boykis (Engineering)

#### 3. LLM配置

```yaml
llm:
  provider: "anthropic"
  model: "claude-3-5-haiku-20241022"  # 使用Haiku节省成本
  max_tokens: 200                      # 每篇摘要200 tokens
  temperature: 0.3
```

**支持的模型**:
- `claude-3-5-haiku-20241022` (推荐，快速且便宜)
- `claude-3-5-sonnet-20241022` (更高质量)

#### 4. 输出配置

```yaml
output:
  directory: "daily-digest"
  filename_format: "digest-{date}.md"
  max_days_to_keep: 30  # 自动清理30天前的文件
  timezone: "Asia/Shanghai"
```

## 📁 目录结构

```
inspire/
├── daily-digest/           # 每日摘要输出目录
│   ├── digest-2025-01-07.md
│   ├── digest-2025-01-06.md
│   └── ...
├── config/
│   └── sources.yaml        # 配置文件
├── scripts/
│   ├── generate_digest.py  # 主脚本
│   └── requirements.txt    # Python依赖
└── .github/
    └── workflows/
        └── daily-digest.yml  # GitHub Actions配置
```

## 🎯 使用工作流

### 每日阅读流程

1. **早上8点** - 自动生成新的摘要文档
2. **快速浏览** - 查看标题和AI摘要
3. **深入阅读** - 点击链接阅读感兴趣的文章
4. **归档整理** - 有价值的内容整理到对应主题目录

### 与Timeline结合使用

在Timeline中引用每日摘要的精华内容:

```markdown
## 2025-01-07

* 今日技术亮点
  * 文章标题和核心观点
  * 来源: [每日摘要](../daily-digest/digest-2025-01-07.md#具体章节)
  * TODO: 深入研究某个主题
```

## 🔧 高级配置

### 添加Twitter/X订阅 (通过RSS Bridge)

Twitter不提供官方RSS，需要使用第三方服务如Nitter:

```yaml
rss_feeds:
  - name: "Andrej Karpathy (via Nitter)"
    url: "https://nitter.net/karpathy/rss"
    category: "AI/ML"
    enabled: true
```

注意: Nitter实例可能不稳定，建议使用自建实例。

### 内容过滤

```yaml
filter_keywords:
  include: ["LLM", "向量搜索", "HPC", "性能优化"]  # 只保留包含这些词的文章
  exclude: ["cryptocurrency", "NFT"]              # 排除这些主题
```

### 切换到OpenAI

```yaml
llm:
  provider: "openai"
  model: "gpt-4o-mini"
  api_key_env: "OPENAI_API_KEY"
```

## 📊 成本估算

使用Claude 3.5 Haiku:
- 输入: ~$0.80 / MTok
- 输出: ~$4.00 / MTok

每天30篇文章，每篇摘要200 tokens:
- 每天成本: < $0.10
- 每月成本: < $3.00

非常经济实惠！

## 🐛 故障排查

### 脚本运行失败

```bash
# 检查依赖
pip install -r scripts/requirements.txt

# 检查环境变量
echo $ANTHROPIC_AUTH_TOKEN

# 查看详细错误
python scripts/generate_digest.py
```

### GitHub Actions失败

1. 检查Secrets是否正确配置
2. 查看Actions日志: Actions → Daily Tech Digest → 最新运行
3. 确认有足够的API额度

### RSS源无法访问

某些RSS源可能需要代理或有地区限制:
- 尝试使用代理
- 查找RSS源的镜像
- 禁用该源: `enabled: false`

## 🔄 更新和维护

### 添加新的RSS源

1. 找到RSS feed URL (通常是 `/feed`, `/rss`, `/feed.xml`)
2. 编辑 `config/sources.yaml`
3. 测试: `python scripts/generate_digest.py`
4. 提交配置

### 调整抓取时间

编辑 `.github/workflows/daily-digest.yml`:

```yaml
schedule:
  # 每天北京时间早上8点
  - cron: '0 0 * * *'

  # 改为每天早上6点
  - cron: '0 22 * * *'  # UTC 22:00 = 北京时间 6:00
```

## 💡 使用技巧

1. **快速扫描**: 先看摘要，节省时间
2. **标记重要**: 复制精华到Timeline
3. **定期回顾**: 每周回顾本周摘要
4. **主题归档**: 重要内容整理到专题目录
5. **调整阈值**: HackerNews分数阈值可以提高(如200+)减少噪音

## 📝 TODO

- [ ] 支持多语言摘要
- [ ] 添加内容去重功能
- [ ] 支持周报生成(汇总本周精华)
- [ ] 添加关键词趋势分析
- [ ] 集成更多RSS源(Reddit, Dev.to等)

## 🤝 贡献

发现好的技术博客或RSS源？欢迎通过PR添加到配置文件！

## 📄 许可

本项目仅供个人学习使用。

---

**提示**: 第一次运行建议手动测试，确认配置正确后再启用自动化。
