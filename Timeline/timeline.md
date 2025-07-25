# TimeLine

## 2025-07-06 AI Search

Google CLI相关内容：

* `GEMINI.md`类似于现在DeepWiki正在做的事情，AI时代，everything都要为AI服务。类似Github这种网站，LLM往往无法访问总结，需要将仓库中的内容扁平化处理才能方便LLM进行使用。这个类似的思路在Cursor等都有应用。
* TODO

Code agent和RAG相关简介：

* 类似Claude Code和Gemini CLI现在都是惰性加载code file, 我理解当用户发出一个task或者query之后:
  * 初始化的时候, 两者会获取代码库的目录结构

## 2025-07-13 Small Stuff

* Google foundation models for relational data

  * 相当于使用Graph模型为关系型数据建模
  * 针对于数据库中的关系型数据，将每个表看作是同一种节点类型，将表中的外键视为边，将表中其它数据看作节点特征，从而对关系型数据建模 https://storage.googleapis.com/gweb-research2023-media/media/GFM4RelationalData-2.mp4
  * 来源: [关系数据图基础模型 --- Graph foundation models for relational data](https://research.google/blog/graph-foundation-models-for-relational-data/)

* Gemini 2.5 将文字内容映射回到PDF中

  * 本质上就是一个对指定文本找锚框的一个操作，据说Gemini对YOLO这种锚框操作（Boundary Box）做了Post train操作
  * 这个操作比较适合RAG中对原文的citation，增强结果的可靠性
  * 来源：[《Sergey 的博客》 --- Sergey's Blog](https://www.sergey.fyi/articles/using-gemini-for-precise-citations)

* How I use Claude Code

  * 通过VS Code的扩展使用Claude Code
  * `/install-github-app`命令能够让Claude自动审查PR
  * Claude Code在处理大型代码库的时候更出色, 主要和底层的运行模式息息相关. 这里大概率也是采用和Gemini-CLI一样的操作
  * 消息排队也是有用的功能, Claude code相当于会智能调度排队系统中的人物
  * Claude Code支持多样的custom hooks, slash commands, project-specific configuration. `CLAUDE.md`中包含对项目的概述
  * Memory system, `#`会快速添加记忆, `CLAUDE.md`文件可以分层

* 反向代理Reverse proxy deep dive

  * 隐藏内部复杂网络的proxy, 通常主要在service mesh, load balancer
  * 对于service mesh来说, Envoy/Linkerd比较常见. Edge proxy中Nginx/HAProxy比较多
  * 反向代理流程:
    * client连接反向代理
    * client发起请求
    * proxy转发到origin
    * proxy等待origin响应
    * proxy将响应转发给客户端
    * proxy/client/origin关闭连接
  * 主要的复杂之处在于并发:
    * 默认的socket/network io是阻塞的. 也可以采用none-block io, 但是这样需要轮询每个fd是否准备好了
    * 采用I/O multiplex: select, poll, epoll:
      * 最原始的I/O包括阻塞和非阻塞, 阻塞需要进程卡住不停等待, 非阻塞需要不断轮询
      * select
        * 固定大小的fd数组告诉内核监控, 内核检查完毕后返回到用户空间. 但是需要用户空间进行轮询检查. 中间会发生内核拷贝
      * poll
        * 非固定数组大小, 仍然需要用户-内核空间拷贝, 仍然需要轮询
      * epoll
        * 事件驱动(回调函数), 通过共享mmap来避免数据拷贝, 调用wait函数等待I/O事件完成.  采用红黑树.
  * C10K问题处理(从同一主机处理10k个并发连接)
    * event-driven programming
    * multiplexing I/O operations
    * Thread pooling
    * Networking and OS optimization
  * Socket Sharding 套接字分片
    * 允许多个监听绑定到同一个端口, 利用内核提供的负载均衡功能
  * 来源: [Reverse proxy deep dive. This post was originally published on… | by mitendra mahto | Jun, 2025 | Medium](https://medium.com/@mitendra_mahto/cross-posted-from-https-startwithawhy-com-reverseproxy-2024-01-15-reverseproxy-deep-dive-html-c3443dc3e0e5)


## 2025-07-14 Sleepy

* 如何跟紧最近AI的进展:
  * 一手信息永远都是最准确的; 关注值得信赖的人的comment和summary
    * https://simonwillison.net/tags/ai/, Simon的Blog
    * Andrej Karpathy
    * https://every.to/chain-of-thought?sort=newest, 前沿AI的能力
    * 各家公司的最新进展, blog, guides, cookbooks
    * AI工程相关工程师
      * https://hamel.dev/
      * https://www.sh-reya.com/
      * https://jxnl.co/
      * https://eugeneyan.com/
      * https://applied-llms.org/
      * https://huyenchip.com/
      * https://omarkhattab.com/, https://x.com/lateinteraction
      * https://www.daily.co/blog/author/kwindla-hultman-kramer/, https://x.com/kwindla
      * https://leehanchung.github.io/
      * https://x.com/jobergum
      * https://crawshaw.io/
      * https://vintagedata.org/blog/
      * https://www.interconnects.ai/
      * https://www.oneusefulthing.org/
      * https://www.aisnakeoil.com/
    * 新闻或者媒体
      * https://x.com/swyx, https://news.smol.ai/
      * https://www.dwarkesh.com/
      * https://www.lesswrong.com/w/ai?sortedBy=magic, https://www.alignmentforum.org/
      * https://gwern.net/
  * 来源: [《我如何跟上 AI 进展（以及为什么你也必须这样做）- nilenso 博客》 --- How I keep up with AI progress (and why you must too) - nilenso blog](https://blog.nilenso.com/blog/2025/06/23/how-i-keep-up-with-ai-progress/)
* MoonShot-K2
  * MoonCake发布了新的K2-MOE模型, 总共1T参数, 实际激活32B, 采用Muon优化器训练
  * **TODO:** 可以看一下这个模型的具体细节
  * 来源: [Kimi K2 是一种最先进的专家混合（MoE）语言模型 | Hacker News --- Kimi K2 is a state-of-the-art mixture-of-experts (MoE) language model | Hacker News](https://news.ycombinator.com/item?id=44533403)

## 2025-07-17 Very Sleepy

* 机械臂相关更进，这里应该是开源的 [pollen-robotics/AmazingHand: 控制 AH!的代码和模型 --- pollen-robotics/AmazingHand: Code and model to control the AH!](https://github.com/pollen-robotics/AmazingHand)
* 美国智能建筑 [《Bedrock Robotics》 --- Bedrock Robotics](https://bedrockrobotics.com/news/introducing-bedrock-robotics)
* 将ELO分数加入到RAG的Ranker中 
  * 看思路的话可能是类似于去学偏好，对query以及召回中采样的两个doc进行对比打分，最后形成ELO得分
  * 核心在于逆分差得胜会让你的分剧烈变化，反之不然
  * 为了解决召回质量低，但整体分偏高的问题，引入全局bias。
  * 来源：[Show HN：使用国际象棋 Elo 分数改进搜索排名 | Hacker News --- Show HN: Improving search ranking with chess Elo scores | Hacker News](https://news.ycombinator.com/item?id=44582662)

## 2025-07-18 Binary Search

* Self-Taught Engineers Often Outperform
    * 有师傅指路固然重要，但是带有明确目标的探索和坚韧不拔才能锻炼出优秀的工程师。也就是说要尝试从头到尾去做一个你没接触过的东西，在这个过程中你会学到很多。
    * 总的来说就是我们需要带有目的性的钻研，去挑战自己不懂的东西，自己尝试理解解决，而不是依靠教程，博客。不停地探索和试错，这种方式是学习地最好方式，去创造而不是依赖别人。
    * 有点费米的那个味道
    * 来源：[Self-Taught Engineers Often Outperform | michaelbastos.com](https://michaelbastos.com/blog/why-self-taught-engineers-often-outperform)
    

## 2025-07-19 U can U up

* Favorite use case is writing log
  * 讨论也很有意思。有些人觉得AI就应该替人类完成编程中琐碎的事情，避免人类进行频繁的上下文切换，方便人类更集中精力去做有创造力的事情；但是也有人觉得这种琐碎的事情也是编程的一部分，如果因为这样就感到烦为什么要编程。
  * 另外一点就是说在AI时代，经验丰富程序员的意义在哪里？世界的价值观正在从know-how向know-what-you-need转变。你能实现的东西AI也能实现，关键在于你得指导AI你需要什么。同样的对于经验丰富的程序员，他们能凭借直觉（psychic way）发现问题的根源，并且有效的指导AI。但是我觉得新手也能通过询问AI解决方案一步一步到这个地步，虽然会慢一点，但是也能达到。
  * 总结起来现在的AI就像是一个从来不会跟人沟通，从来不会说不的外包团队，具体的实现如何，目前有好有坏；同样的计算机领域在不断的抽象，并且提高抽象，AI将抽象带到了一个更新的高度。然而重要的警示是高级的抽象不能消除对底层原理理解的需求。越是高级复杂的抽象，越需要底层基础来支撑。**但是现在的自我反思发现错误的能力也很强，对外行人来说这是一个黑盒，除非能够保证100%可靠？**
  * 回到这篇文章，文章很大一部分在探讨Jetbrain Python的Full Line Code Completition。PyCharm团队相当于为Python定制了一个专用的LLM，包括：
    * 核心思路
      * 使用llama.cpp以及llama架构训练1b模型，数据采用stack数据集，一个代码模型，剔除了注释（因为只想要模型去生成代码而不是注释，补全性质）
      * 根据python的特性重新设计BPE tokenizer
      * 移除了import语句（因为开发者经常在写代码的最后写import语句）
    * 实际推理过程
      * FP32到INT8量化
      * Cache策略：在preload code的50%中载入代码，剩余的50%留给随处可能出来的代码
  * 来源：[我最喜欢的 AI 应用场景是写日志 | Hacker News --- My favorite use-case for AI is writing logs | Hacker News](https://news.ycombinator.com/item?id=44599549)
  * 这个作者的其它blog也值得一看：[存档 • 常规科技 • 衬衫 --- Archive • Normcore Tech • Buttondown](https://newsletter.vickiboykis.com/archive/)

## 2025-07-22 Coincidence

* Log by time, not by count
  * 主要说的是如何记录log, 因为我不怎么打日志, 所以这边他的意见是
    * 按照固定时间间隔打log. 原因是如果按照数量打印日志, 那么:
      * 如果日志记录过多: 降低系统性能, 冗余日志不利于观测, 日志保存昂贵
      * 如果日志记录过少: 不知道是否程序在运行, 降低观察性
  * 讨论区意见: 要区分log和metric
    * log指的是系统中重要的时间发生的时间点, 例如错误, 警告
    * metric则是捕捉可量化的数据, 例如函数调用时间, 队列长度等等
    * 同样的也有的人认为log和metric之间的界限再逐渐模糊, 存在互相转换工具
    * Log: search, get context, read; Metric: measure, plot dashboards, define alerts
  * 来源: [按时间记录，而非按数量记录 | Hacker News --- Log by time, not by count | Hacker News](https://news.ycombinator.com/item?id=44630927)

## 2025-07-23 Two clock

* Qwen-Code3
  * 主要是为了赶这一波Code Agent的潮流，后端模型是Aliyun自己训练的，前端基于Gemini-CLI改造
  * 针对Development环境进行训练：
    * 训练数据70%来自代码，原生256K上下文，借助YaRN扩展到1M上下文，这些都是code必备的操作。合成数据扩展，通过利用coder2.5对低质数据进行清洗和重写
  * 评论区主要再说对于MOE架构和本地LLM，DRAM的带宽和单卡的性能（两块3090的提高微乎其微，内存带宽受限）是模型推理的瓶颈
  * 另外一点就是动态量化技术，为重要的层分配更多的位，不那么重要的层分配少一点的位数
  * 来源：[Qwen3-Coder: 如何本地运行 | Unsloth 文档 --- Qwen3-Coder: How to Run Locally | Unsloth Documentation](https://docs.unsloth.ai/basics/qwen3-coder-how-to-run-locally)，[Qwen3-Coder: 在世界中的自主编程 | Hacker News --- Qwen3-Coder: Agentic coding in the world | Hacker News](https://news.ycombinator.com/item?id=44653072)

## 2025-07-26 Green bean coffe

* AI搜索降低了搜索界面的点击量
  * 搜索引擎现在的策略是生成搜索结果的overview，那么很多用户基本上就不再会去点击真正的网站
  * 这样的话将会导致所有的广告的收益都将被搜索引擎垄断。在传统搜索时代已经有了很多ad block插件，那么在大模型时代我们应该如何做这个ad block呢？
    * 最简单的也是通过AI来检测是否出现软广，然后AI rewrite
  * 同样的我感觉GEO（又叫AIO和传统SEO技术相对）的技术也应该要进行了解**TODO**
  
* Kagi搜索

  * 开源了自己的vector search
    * 添加了diverse特性（使搜索的结果diverse）
    * 看他们的测试结果bge embedding model确实还是最好用的

* Maven Vector Search

  * 这个公司的主要业务看起来是一个在线教育
    * 搜索：课程名称 + 课程描述 --> Embedding (这里是否AI生成描述扩展 + 可能query会更好呢)
    * 分类：手动分类形成Topic + AI生成Topic描述（感觉这一步AI可以全自动）--> Embedding，为课程推荐主题或者查找主题相关的课程
    * 个性化（推荐）：AI描述用户（职位 + 学习过的课程 + 点击过的课程 + 相关信息）--> Embedding 

  * 来源：[Maven: Search, categorization, and personalization, all in a week with embeddings](https://maven.com/blog/embeddings)
  * Embedding质量的榜单：[MTEB Leaderboard - a Hugging Face Space by mteb](https://huggingface.co/spaces/mteb/leaderboard)

  

