# Nano-vLLM开发

## Week-1

Python会执行vLLM中所有沿路的`__init__.py`文件的代码, 这一步可以理解成事先执行环境准备.

代码运行剖析:

1. 运行vllm serve model
2. 引导程序到vllm.entrypoints.cli.main:main函数, main函数内部进行惰性加载不同的module
3. 进行参数解析, 采用argparse
   1. 我们这里主要关注对serve参数的解析
   2. 因为vllm这里处理的参数非常多, 所以它采用subargparsers进行处理不同的子参数(dest是subparser), 具体的子命令在每个module处理
   3. 每个module会创建对应的command
      1. command负责具体的参数解析逻辑, 增加subparser, 增加对应的参数解析
      2. 执行cmd函数, 执行具体的分发任务
4. 解析完成参数之后, 执行具体的Command的cmd函数, 这里我们关注serve命令
5. serve命令会调用run_server函数
   1. set_server, 进行server相关的配置
      1. 根据host和port获取sock, 接着进行防止资源过载进行的相关配置, 以及SIGTERM相关handler的配置
      2. 构建listen_addr
      3. 将最后的listen_addr和sock都返回出去
   2. await server_worker, 等待worker进行对应的操作
6. 核心在这个run_server_worker
   1. async with build_async_engine_client, async的方式构建engine client (async保证其中的操作是一个异步的操作过程), 那么这个构建过程中发生了什么呢
      1. 首先build_async_engine_client这个函数被asynccontextmanager装饰, 维持一个async的资源上下文环境(构建过程是一个async)
      2. 根据传入的CLI参数, 构建AsyncEngineArgs, 相当于是engine的相关配置数据在这里 (args中的参数进行填充)
      3. 继续调用async的build_async_engine_client_from_engine_args (相当于是根据传入的参数来构建engine)
         1. 这个函数也是一个asynccontextmanager, 真正engine client创建就发生在这里
         2. 首先根据传入的engine_args (engine参数) 创建engine的config
            1. 创建DeviceConfig, 这里应该是要涉及到模型到底载入到CPU还是GPU
            2. 判断模型是否是speculator model (方便后续猜测性采样)
            3. 创建ModelConfig, 模型的配置项害蛮多的, 我感觉这里实现可以先做一个精简的版本
            4. 为V1引擎设置model config (包括默认的config, v1 engine会自动开启chunk_prefill和prefix_caching), 总之这里非常关注chunk_prefill和prefix_caching
            5. 创建CacheConfig (这里的Cache是KV Cache)
            6. 这里可以创建数据并行的相关配置, 但是我们当前只关注local的情况, 这里的配置还挺多的, 后续实现的时候可以具体看一下是否需要舍弃, 创建ParallelConfig. 这里的就是上述的相关操作的配置结果
            7. 创建Speculative Config相关配置
            8. 创建SchedulerConifg的相关配置, 这个应该是决定最后vllm如何调度不同的请求
            9. 创建LoraConfig的相关配置, 但是这个是微调相关的配置啊 (原来是为了方便运行lora微调过后的模型)
            10. 创建LoadConfig的相关配置, 配置模型如何载入权重
            11. 创建结构化输出StructuredOutputsConfig的相关配置, 应该是进行约束性编码, 保证输出格式
            12. 创建ObservabilityConfig的相关配置, 进行metric和tracing
            13. 创建VllmConfig, 是上述所有的Config的合集, 最终返回这个
         3. 从最终创建的config中构建AsyncLLM, 然后yield出去
            1. 加载tokenizer
            2. 创建Processor (可以将Inputs --> EngineCoreRequests)
            3. 创建OutputProcessor(将EngineCoreOutputs --> RequestsOutput)
            4. 创建最核心的EngineCore (在后台进程中启动)
            5. 创建handler和asyncio的eventloop循环
      4. 最后返回构建的engine
   2. 在上述engine_client的上下文中执行如下操作:
      1. 构建前端APP, 这里采用的是FastAPI进行请求的处理, 进行对应的API处理
      2. 最后serve这个server



Nano版本开发剖析:

* 配置项目能够通过命令行进行运行, 这里的本质是告诉python, 命令行的命令应该被转发到哪个入口函数, 核心是在`pyproject.toml`中设置入口:

  ```toml
  [project.scripts]
  nvllm = "nvllm.entrypoints.cli.main:main"
  ```

  接着使用`uv pip install -e .`, 以编辑模式安装这个package

* 接着实现最基本版本的参数解析, 采用自定义的`FlexibleArgumentParser`解析器

  * 添加针对处理不同子命令的`subparsers`, 子命令负责对子解析器进行初始化, 以及核心的运行方法

