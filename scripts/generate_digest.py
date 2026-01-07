#!/usr/bin/env python3
"""
每日技术新闻聚合脚本
自动从HackerNews和RSS源抓取内容，使用LLM生成摘要
"""

import os
import sys
import json
import yaml
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import anthropic


class DailyDigestGenerator:
    def __init__(self, config_path: str = "config/sources.yaml"):
        """初始化"""
        self.config = self._load_config(config_path)
        self.articles = []

        # 初始化LLM客户端
        llm_config = self.config.get('llm', {})
        api_key = os.getenv(llm_config.get('api_key_env', 'ANTHROPIC_AUTH_TOKEN'))
        base_url = os.getenv(llm_config.get('base_url_env', 'ANTHROPIC_BASE_URL'))

        if api_key:
            self.llm_client = anthropic.Anthropic(
                api_key=api_key,
                base_url=base_url if base_url else None
            )
        else:
            print("⚠️  警告: 未找到LLM API密钥，将跳过摘要生成")
            self.llm_client = None

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def fetch_hackernews(self) -> List[Dict]:
        """抓取HackerNews热门文章"""
        print("📰 正在抓取 HackerNews...")

        hn_config = self.config.get('hacker_news', {})
        if not hn_config.get('enabled', False):
            print("  ⏭️  HackerNews已禁用，跳过")
            return []

        try:
            # 获取热门文章ID列表
            response = requests.get(hn_config['api_url'], timeout=10)
            story_ids = response.json()[:hn_config.get('max_items', 30)]

            articles = []
            min_score = hn_config.get('min_score', 100)

            for story_id in story_ids:
                # 获取文章详情
                item_url = hn_config['item_url'].format(story_id)
                item_response = requests.get(item_url, timeout=10)
                item = item_response.json()

                # 过滤低分文章
                if item.get('score', 0) < min_score:
                    continue

                # 跳过没有URL的文章（Ask HN等）
                if 'url' not in item:
                    continue

                articles.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'score': item.get('score', 0),
                    'comments': f"https://news.ycombinator.com/item?id={story_id}",
                    'source': 'HackerNews',
                    'category': 'HackerNews'
                })

            print(f"  ✅ 成功抓取 {len(articles)} 篇文章")
            return articles

        except Exception as e:
            print(f"  ❌ 抓取失败: {e}")
            return []

    def fetch_rss_feeds(self) -> List[Dict]:
        """抓取RSS订阅源"""
        print("\n📡 正在抓取 RSS 订阅...")

        all_articles = []
        feeds = self.config.get('rss_feeds', [])

        for feed_config in feeds:
            if not feed_config.get('enabled', True):
                continue

            feed_name = feed_config['name']
            feed_url = feed_config['url']

            print(f"  📥 {feed_name}...")

            try:
                feed = feedparser.parse(feed_url)

                # 只取最近24小时的文章
                cutoff_time = datetime.now() - timedelta(days=1)

                for entry in feed.entries[:10]:  # 每个源最多取10篇
                    # 检查发布时间
                    if hasattr(entry, 'published_parsed'):
                        pub_time = datetime(*entry.published_parsed[:6])
                        if pub_time < cutoff_time:
                            continue

                    all_articles.append({
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'summary': entry.get('summary', ''),
                        'source': feed_name,
                        'category': feed_config.get('category', 'Tech')
                    })

            except Exception as e:
                print(f"    ❌ 失败: {e}")
                continue

        print(f"  ✅ RSS订阅共抓取 {len(all_articles)} 篇文章")
        return all_articles

    def generate_summary(self, article: Dict) -> str:
        """使用LLM生成文章摘要"""
        if not self.llm_client:
            return article.get('summary', '暂无摘要')

        llm_config = self.config.get('llm', {})
        url = article['url']
        title = article['title']

        try:
            # 构造提示词
            prompt = f"""请为以下技术文章生成一个简短的中文摘要（2-3句话），重点说明：
1. 文章的核心主题
2. 关键技术点或创新点
3. 对读者的价值

文章标题: {title}
文章链接: {url}

要求:
- 用简洁的中文表达
- 突出技术要点
- 2-3句话即可
- 不要使用"这篇文章"等开头"""

            message = self.llm_client.messages.create(
                model=llm_config.get('model', 'claude-3-5-haiku-20241022'),
                max_tokens=llm_config.get('max_tokens', 200),
                temperature=llm_config.get('temperature', 0.3),
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return message.content[0].text.strip()

        except Exception as e:
            print(f"    ⚠️  摘要生成失败: {e}")
            return article.get('summary', '暂无摘要')

    def generate_markdown(self, date_str: str) -> str:
        """生成Markdown格式的每日摘要"""
        print("\n📝 正在生成Markdown文档...")

        # 按类别分组
        categorized = {}
        for article in self.articles:
            category = article.get('category', 'Other')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(article)

        # 生成Markdown内容
        md_lines = [
            f"# 每日技术摘要 - {date_str}",
            "",
            f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> 共收集 {len(self.articles)} 篇文章",
            "",
            "## 📑 目录",
            ""
        ]

        # 添加目录
        for category in sorted(categorized.keys()):
            md_lines.append(f"- [{category}](#{category.lower().replace('/', '').replace(' ', '-')}) ({len(categorized[category])}篇)")

        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

        # 添加各类别内容
        for category in sorted(categorized.keys()):
            md_lines.append(f"## {category}")
            md_lines.append("")

            articles = categorized[category]

            # HackerNews特殊处理（显示分数）
            if category == 'HackerNews':
                # 按分数排序
                articles.sort(key=lambda x: x.get('score', 0), reverse=True)

                for article in articles:
                    md_lines.append(f"### [{article['title']}]({article['url']})")
                    md_lines.append(f"")
                    md_lines.append(f"**分数**: {article.get('score', 0)} | [讨论]({article.get('comments', '')})")
                    md_lines.append("")

                    # 生成摘要
                    if self.llm_client:
                        print(f"  🤖 正在为 '{article['title'][:50]}...' 生成摘要")
                        summary = self.generate_summary(article)
                        md_lines.append(f"**摘要**: {summary}")

                    md_lines.append("")
                    md_lines.append("---")
                    md_lines.append("")

            else:
                # 其他RSS源
                for article in articles:
                    md_lines.append(f"### [{article['title']}]({article['url']})")
                    md_lines.append(f"")
                    md_lines.append(f"**来源**: {article.get('source', 'Unknown')}")
                    md_lines.append("")

                    # 生成摘要
                    if self.llm_client:
                        print(f"  🤖 正在为 '{article['title'][:50]}...' 生成摘要")
                        summary = self.generate_summary(article)
                        md_lines.append(f"**摘要**: {summary}")
                    elif article.get('summary'):
                        md_lines.append(f"**摘要**: {article['summary'][:200]}...")

                    md_lines.append("")
                    md_lines.append("---")
                    md_lines.append("")

        # 添加页脚
        md_lines.extend([
            "",
            "---",
            "",
            "## 📚 如何使用",
            "",
            "1. 浏览感兴趣的标题",
            "2. 阅读AI生成的摘要快速了解内容",
            "3. 点击链接深入阅读",
            "4. 有价值的内容可以整理到对应的主题目录",
            "",
            "## 🔧 配置",
            "",
            "修改 `config/sources.yaml` 可以:",
            "- 添加/删除RSS订阅源",
            "- 调整HackerNews最小分数阈值",
            "- 配置内容过滤关键词",
            "",
            f"*本文档由 [daily-digest脚本](../scripts/generate_digest.py) 自动生成*"
        ])

        return "\n".join(md_lines)

    def save_digest(self, content: str, date_str: str):
        """保存每日摘要到文件"""
        output_config = self.config.get('output', {})
        output_dir = Path(output_config.get('directory', 'daily-digest'))
        output_dir.mkdir(exist_ok=True)

        filename = output_config.get('filename_format', 'digest-{date}.md').format(date=date_str)
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✅ 每日摘要已保存到: {filepath}")
        return filepath

    def cleanup_old_files(self):
        """清理旧的摘要文件"""
        output_config = self.config.get('output', {})
        output_dir = Path(output_config.get('directory', 'daily-digest'))
        max_days = output_config.get('max_days_to_keep', 30)

        if not output_dir.exists():
            return

        cutoff_date = datetime.now() - timedelta(days=max_days)
        deleted_count = 0

        for file in output_dir.glob('digest-*.md'):
            # 从文件名提取日期
            try:
                date_str = file.stem.replace('digest-', '')
                file_date = datetime.strptime(date_str, '%Y-%m-%d')

                if file_date < cutoff_date:
                    file.unlink()
                    deleted_count += 1
            except:
                continue

        if deleted_count > 0:
            print(f"🗑️  已清理 {deleted_count} 个旧文件")

    def run(self):
        """主流程"""
        print("🚀 开始生成每日技术摘要\n")
        print("=" * 60)

        # 抓取内容
        hn_articles = self.fetch_hackernews()
        rss_articles = self.fetch_rss_feeds()

        self.articles = hn_articles + rss_articles

        if not self.articles:
            print("\n⚠️  没有抓取到任何文章")
            return

        # 生成摘要文档
        date_str = datetime.now().strftime('%Y-%m-%d')
        markdown_content = self.generate_markdown(date_str)

        # 保存文件
        filepath = self.save_digest(markdown_content, date_str)

        # 清理旧文件
        self.cleanup_old_files()

        print("\n" + "=" * 60)
        print(f"✨ 完成! 共处理 {len(self.articles)} 篇文章")
        print(f"📄 输出文件: {filepath}")


if __name__ == "__main__":
    try:
        generator = DailyDigestGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
