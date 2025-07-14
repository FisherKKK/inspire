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

  

  

  