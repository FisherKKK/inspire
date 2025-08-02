# Modern CPP

> 核心主要是记录看到CPP的一些简单内容

## 1. 对象的生命周期

普通对象的生命周期例子:

```cpp
auto& GetData(){
   const int i = 5;
   return i;
 }

auto* GetData(){
   const char* i = "Hello";
   return i;
 } 

auto* GetData(){
   const char[] i = "Hello";
   return i;
}
```

复杂对象的生命周期例子:

```cpp
struct S {
 S(int a){
   a = new MyWidgetNothrow(a);
   b = new MyWidgetThrows(a);
 }
 ~S(){
  delete a;
  delete b;
 }

MyWidget* a;
 MyWidget* b;
 };

int main(){S s;}
// 由于S在构造函数中抛出异常, 析构函数不会执行, 导致内存泄漏
```

 一个可行的方式:

```cpp
struct S {
 S() = default;
 S(int a):S{} {
 a = new MyWidgetNothrow;
 b = new MyWidgetThrows;
 }
 ~S(){
 delete a;
 delete b;
 }

MyWidget* a = nullptr;
 MyWidget* b = nullptr;
 };

int main(){S s;}

// 但是采用委派构造函数就能解决内存泄露问题. 一个更好的方式是采用智能指针! 因此避免在代码中直接出线new运算符
```

因此要记住: **对象生命周期从构造函数执行结束开始, 构造函数没有成功执行就无法正常执行析构函数**, 并且尽可能少使用`new`运算符, 而是使用智能指针.

## 2. Make you program run faster

原文: [Make your programs run faster by better using the data cache - Johnny's Software Lab (johnnysswlab.com)](https://johnnysswlab.com/make-your-programs-run-faster-by-better-using-the-data-cache/)



在无法改善算法复杂度的情况下, 充分利用计算机体系架构带来的好处: 缓存, 如下是一些Tips:

* 线性访问数据的时候, 使用vector或者array. 或者使用缓存友好的数据结构, 例如Judy数组等等

* Access together should be close to each other

* 使用value数组而非pointer数组

* 优化对类的访问

  * 本质上就是说对于类的数组, 我们希望缓存的时候同一个元素在同一个缓冲行, 因此我们想要类是64位对齐的, 即添加`__attribute__((aligned (64)))`

    ```cpp
    my_class* array_of_my_class;
    posix_memalign((void**)array_of_my_class, 64, SIZE * sizeof(my_class));
    for (size_t i = 0; i < SIZE; i++) {
        ::new (&array_of_my_class[i]) my_class(i);
    }
    ```

* 有效访问矩阵中的数据

* 避免在类和结构体中进行padding

  * 结构体在定义过程会按照最大的进行对齐(起始地址和终止地址), 因此声明变量的时候最好先大后小.
  * 尽可能使用较小的类型

* 避免使用heap分配

* 避免写入内存

* 使用软件预取

  ```cpp
  int binarySearch(int *array, int number_of_elements, int key) {
      int low = 0, high = number_of_elements-1, mid;
      while(low <= high) {
          mid = (low + high)/2;
  #ifdef DO_PREFETCH
          // low path
          __builtin_prefetch (&array[(mid + 1 + high)/2], 0, 1);
          // high path
          __builtin_prefetch (&array[(low + mid - 1)/2], 0, 1);
  #endif
  
          if(array[mid] < key)
              low = mid + 1; 
          else if(array[mid] == key)
               return mid;
          else if(array[mid] > key)
               high = mid-1;
          }
  }
  ```

  ## 3. C语言中的对齐和填充

  [Structures in C: From Basics to Memory Alignment – Abstract Expression --- C 中的结构：从基础知识到内存对齐 – 抽象表达式](https://abstractexpr.com/2023/06/29/structures-in-c-from-basics-to-memory-alignment/)

  一般来说结构体中的结构并非是packed结构, 其中是存在填充的, 并进行了如下的布局规定:

  * 第一个成员的地址和结构体的起始地址相同

  * 每一个成员之前都有可能存在内存对齐

  * 结构体末端也会存在填充

  * 每个类型必须位于其类型大小的倍数

  * 结构必须获得足够的尾部填充以与其最大的数据类型对齐

  * 如果需要一个绝对的打包结构可以进行如下的操作:

    ```c
    struct s {
        char a;
        int b;
        double c;
        char d[10];
    } __attribute__((packed));
    ```

C语言结构体中另外一个非常有意思的就是Flexible Array Member, 它的结构如下:

```c
struct DynamicString {
    int len;
    char str[];
};
```

这和`Redis`中`sds`的设计是一样的, 本质上`str`这个成员是不占据结构的大小, 即**结构体大小将如同最后一个成员不存在一样**



## 3. SmartPDF中的CallBack

[Simplest C++ callback, from SumatraPDF](https://blog.kowalczyk.info/a-stsj/simplest-c-callback-from-sumatrapdf.html)

 SumatraPDF 中一种简单的 C++ 回调实现，该方法使用自定义的 `Func0` 和 `Func1` 结构体，作为`std::function<>` 和 lambda 表达式的替代方案。作者选择这种自定义方法的原因是，与使用 lambda 表达式时**编译器自动生成的函数名相比，自定义方法生成的名称更具描述性，有助于调试崩溃报告**。

`Func0` 和 `Func1` 结构体通过结合函数指针和数据来实现回调，并支持有参数和无参数的函数，同时保持类型安全。

```c++
// 最简单的闭包
using func0Ptr = void (*)(void*);
struct Func0 {
  func0Ptr fn;
  void* data;
  void Call() { fn(data); }
};

// 采用模板进行处理
template <typename T>
Func0 MkFunc0(void (*fn)(T*), T* d) {
    auto res = Func0{};
    res.fn = (func0Ptr)fn;
    res.userData = (void*)d;
    return res;
}

void MyFunc(MyFuncData* data) { }

auto data = new MyFuncData;
auto fn = MkFunc0(MyFunc, data);


// 如下本质上是判断这是否是一个带有状态捕获的闭包

using func0Ptr = void (*)(void*);
using funcVoidPtr = void (*)();

#define kVoidFunc0 (void*)-1

// the simplest possible function that ties a function and a single argument to it
// we get type safety and convenience with mkFunc()
struct Func0 {
    void* fn = nullptr;
    void* userData = nullptr;

    Func0() = default;
    Func0(const Func0& that) {
        this->fn = that.fn;
        this->userData = that.userData;
    }
    ~Func0() = default;

    bool IsEmpty() const {
        return fn == nullptr;
    }
    void Call() const {
        if (!fn) {
            return;
        }
        if (userData == kVoidFunc0) {
            auto func = (funcVoidPtr)fn;
            func();
            return;
        }
        auto func = (func0Ptr)fn;
        func(userData);
    }
};

template <typename T>
Func0 MkFunc0(void (*fn)(T*), T* d) {
    auto res = Func0{};
    res.fn = (func0Ptr)fn;
    res.userData = (void*)d;
    return res;
}

Func0 MkFuncVoid(funcVoidPtr fn) {
    auto res = Func0{};
    res.fn = (void*)fn;
    res.userData = kVoidFunc0;
    return res;
}


// 这里本质上是允许传递额外参数的闭包
template <typename T>
struct Func1 {
    void (*fn)(void*, T) = nullptr;
    void* userData = nullptr;

    Func1() = default;
    ~Func1() = default;

    bool IsEmpty() const {
        return fn == nullptr;
    }
    void Call(T arg) const {
        if (fn) {
            fn(userData, arg);
        }
    }
};

template <typename T1, typename T2>
Func1<T2> MkFunc1(void (*fn)(T1*, T2), T1* d) {
    auto res = Func1<T2>{};
    using fptr = void (*)(void*, T2);
    res.fn = (fptr)fn;
    res.userData = (void*)d;
    return res;
}
```



尽管承认 `std::function<>` 更具灵活性，作者认为其自定义方案更小巧、更快、更易于理解，并避免了**模板可能导致的额外代码和编译速度下降问题**。

> comments: 主要的一个说法就是自定义的closure能够避免模板编程带来的编译开销和无法维护的问题(例如闭包名)
>
> 这个哥们的blog也值得一看: [所有文章 --- All articles](https://blog.kowalczyk.info/tag/programming)

## 4. CPP中关于Latecy的优化内容

1. [C++ 用于低延迟应用程序（包括高频交易）的模式 | Hacker News --- C++ patterns for low-latency applications inmemeding high-frequency trading | Hacker News](https://news.ycombinator.com/item?id=40908273)，因为高频交易对延迟的需求非常严格
   1. 知识点
      1. CRTP动态多态 --> 静态多态
      2. inline函数，避免寻址带来的损耗
      3. constexpr编译时计算评估
      4. CPP代码优化策略：
         1. Cache Warm
         2. Compile-time dispatch，通过模板实例化，函数重载优化编译时代码路径选择。避免运行时派发
         3. Constexpr，编译时表达式评估，允许常量折叠和编译时计算
         4. Loop unrolling：编译时循环展开，减少循环控制开销
         5. 类型一致性：保持sign，float类型的一致性
         6. 分支预测/减少：Likely或者Unlikely优化代码
         7. Slowpath Removal：优化很少执行的代码
         8. SIMD
         9. Prefetching
         10. Lock-free Programming：使用原子操作，避免死锁和潜在的性能开销
         11. Inline：减少函数调用开销，热代码直接inline
   2. 工具使用
      1. [Compiler Explorer](https://godbolt.org/)探测编译后的代码
2. [CppCon](https://github.com/CppCon)，每年的CppCon的会议内容也值得一看，会有一些比较好的设计模式
3. [Computer, Enhance! | Casey Muratori | Substack](https://www.computerenhance.com/?sort=top)，性能相关的代码设计
4. [The LMAX Architecture](https://martinfowler.com/articles/lmax.html)高频交易的设计模式
5. [Notes on running Redis with HPC techniques](https://gist.github.com/neomantra/3c9b89887d19be6fa5708bf4017c0ecd)，高性能Redis的运行介绍
6. [Software optimization resources. C++ and assembly. Windows, Linux, BSD, Mac OS X](https://www.agner.org/optimize/)，软件运行优化指南
7. [realtimecollisiondetection.net](https://realtimecollisiondetection.net/)，实时音频处理，也是一个性能要求严格的领域
8. [(17) Signals & Threads Podcast - YouTube](https://www.youtube.com/playlist?list=PLCiAikFFaMJouorRXDSfS2UoKV4BfKyQm)信号量和线程的一个podcast
9. [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)，CPP核心指南

## 5. CPU绑定和亲和性

CPU绑定的本质是将一个进程绑定到某个固定的CPU核心，这样的话就能带来的好处：

* 减少上下文切换的开销
* 避免该进程调度到其他核心，从而导致缓存刷新的问题
* 避免NUMA跨界点访问

CPU隔离是避免将一个进程调度到某些CPU核心：

* 能够保证这些核心能够被独享，而不需要和其它进程竞争
* 修改引导程序（如 /etc/default/grub）的配置。
* 在 GRUB_CMDLINE_LINUX 这一行里，加入 isolcpus=2,3 （假设你想隔离CPU 2和3）。

特性	CPU 绑定 (Pinning)	CPU 隔离 (Isolation)
控制级别	建议性：告诉调度器在哪运行特定进程	强制性：命令调度器不许使用某些核心
隔离程度	部分隔离：应用进程固定，但OS仍可使用该核心	完全隔离：OS通用调度器被禁止使用该核心
主要目标	提高缓存效率，减少进程迁移	消除系统抖动，获得极致、确定的低延迟
对OS的影响	对OS调度影响小	从OS可用的通用核心池中移除了核心
实现方式	运行时命令 (taskset, numactl)	内核启动参数 (isolcpus)，需要重启
适用场景	大多数对性能敏感的应用（如数据库、Web服务器）	极端低延迟应用（如高频交易、科学计算、电信）

对于很多网络应用，每次网络数据包到来的时候都会发生中断。频繁的中断产生上下文切换开销，缓存刷新等性能开销问题。因此我们可以让固定和进程的同一NUMA的CPU专门负责中断处理。

taskset只能pin cpu，numactl不仅能pin cpu，还能pin内存。先在调度器那边隔离某些核，然后在把进程pin到对应的核上

那么如下就是一个最简单的运行例子：

```sh
export REDIS_CPUS=1
numactl --all --physcpubind=$REDIS_CPUS --localalloc redis-server
```

## 6. 常用的Profile命令和工具

一个常用的bash脚本，观测程序的主要卡点

```sh
perf stat -e task-clock,cycles,instructions,cache-references,cache-misses,branches,branch-misses,faults,minor-faults,cs,migrations -r 3 nice taskset 0x01 ./xxx
```

## 7. 一些有用的C++资源

1. [More C++ Idioms - Wikibooks, open books for an open world](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms)
2. [Introduction 2016 NUMA Deep Dive Series - frankdenneman.nl](https://frankdenneman.nl/2016/07/06/introduction-2016-numa-deep-dive-series/)
3. [High Performance Browser Networking (O'Reilly)](https://hpbn.co/)
4. [Linux Performance](https://www.brendangregg.com/linuxperf.html)
5. [向量集合是 Redis 的一部分 -  --- Vector Sets are part of Redis - ](https://antirez.com/news/149)
6. [neomantra/presentations: Presentations I have given](https://github.com/neomantra/presentations)
7. [优化 Web 服务器以实现高吞吐量和低延迟 - Dropbox --- Optimizing web servers for high throughput and low latency - Dropbox](https://dropbox.tech/infrastructure/optimizing-web-servers-for-high-throughput-and-low-latency)
8. [Optimizing Nginx for High Traffic Loads](https://blog.martinfjordvald.com/optimizing-nginx-for-high-traffic-loads/)

## 8. 可以后续阅读的内容

- [ ] [Bjarne Stroustrup's Homepage](https://www.stroustrup.com/)
- [ ] [C 和 C++编译器选项强化指南 | Hacker News --- Compiler Options Hardening Guide for C and C++ | Hacker News](https://news.ycombinator.com/item?id=43533516)
- [ ] [C++绝对超棒 | Hacker News --- C++ is an absolute blast | Hacker News](https://news.ycombinator.com/item?id=42495135)
- [ ] [C++的两个派系 | Hacker News --- The two factions of C++ | Hacker News](https://news.ycombinator.com/item?id=42231489)
- [ ] [Matt Godbolt 通过向我展示 C++让我对 Rust 产生了兴趣 | Hacker News --- Matt Godbolt sold me on Rust by showing me C++ | Hacker News](https://news.ycombinator.com/item?id=43907820)
- [ ] [《初始化在 C++中真疯狂（2017）| Hacker News》 --- Initialization in C++ is bonkers (2017) | Hacker News](https://news.ycombinator.com/item?id=43999492)
- [ ] [0+0 > 0: C++线程本地存储性能 | Hacker News --- 0+0 > 0: C++ thread-local storage performance | Hacker News](https://news.ycombinator.com/item?id=43077675)
- [ ] [我最喜欢的 C++模式：X 宏 (2023) | Hacker News --- My Favorite C++ Pattern: X Macros (2023) | Hacker News](https://news.ycombinator.com/item?id=43472143)
- [ ] [C++模板宏编程与 Lisp 宏 | Hacker News --- C++ template macroprogramming versus Lisp macros | Hacker News](https://news.ycombinator.com/item?id=42150206)
- [ ] [C 和 C++优先考虑性能而非正确性（2023）| Hacker News --- C and C++ prioritize performance over correctness (2023) | Hacker News](https://news.ycombinator.com/item?id=43509524)
- [ ] [Welcome to Johnny's Software Lab! - Johnny's Software Lab](https://johnnysswlab.com/)，**高优，质量不错**



## 9. SIMD相关

* [Home | SIMD.info](https://simd.info/)，SIMD语义搜索，目前还在开发中
* [x86/x64 SIMD Instruction List (SSE to AVX512)](https://officedaytime.com/simd512e/)，SIMD指令的可视化
* [A64 SIMD Instruction List: SVE Instructions](https://dougallj.github.io/asil/)，上面的一个补充
* [x86 and amd64 instruction reference](https://www.felixcloutier.com/x86/)，x86指令的指南



## 10. Memory Order

如下是一篇我非常喜欢的blog的浓缩：

https://xorvoid.com/lockfree_programming_a_mental_model.html

现代计算机（server）端一般都会有多插槽，多插槽允许我们插多个CPU芯片：

- 对于dual-socket 每个socket 64core的机器来说，一共有128core
- 如果适用Symmetric Multithreading（或者超线程）的话，我们将有256的线程

![img](https://cdn.nlark.com/yuque/0/2025/png/23141164/1754032674022-f343562f-867b-44c0-bd14-6427ca18d844.png) ![img](https://cdn.nlark.com/yuque/0/2025/png/23141164/1754032685461-3cc62bcd-c1c2-4ade-9301-82e0442cc421.png)

实际上的内存架构如图右，NUMA，每个CPU有自己亲和的memory，跨NUMA访问延迟会更高。

因此类比来看，其实编程更像是在独立的计算机上编程。类比起来如下：

| Super-computer  超级计算机                         | Modern CPU  现代 CPU                                         |
| -------------------------------------------------- | ------------------------------------------------------------ |
| Cluster Node Processor  集群节点处理器             | CPU Core  CPU 核心                                           |
| Cluster Node Memory  集群节点内存                  | CPU Cache  CPU 缓存                                          |
| Cluster Interconnect Fabric 集群互连结构           | NOC (Network On Chip) Mesh, QPI, Infinity Fabric, etc NOC（网络芯片）Mesh、QPI、Infinity Fabric 等 |
| Packet Frame  数据包帧                             | Cache Line  缓存行                                           |
| Maximum Transmision Unit (MTU) 最大传输单元（MTU） | Cache Line Size (64 bytes, 128 bytes, etc) 缓存行大小（64 字节，128 字节等） |
| `msg_send(send_value)`                             | `*pointer_to_shared = send_value`                            |
| `recv_value = msg_recv()`                          | `recv_value = *pointer_to_shared`                            |

那么就会出现一些有意识但是直观的理解

Load are frequently stale(过时的)

```c++
int *ptr_to_shared;
void thread_1() {
    while (1) {
        int data = *ptr_to_shared;
        if (data != *ptr_to_shared)
            std::cout << "This can happend";
    }
}
```

可以理解，数据在发送-接收期间，原始的数据以及变化

Storage take time to propagate

```c++
int *ptr_to_shared1;
int *ptr_to_shared2;

void thread_1() {
    *ptr_to_shared1 = 1;
    std::cout << "value2: " << *ptr_to_shared2;
}

void thread_2() {
    *ptr_to_shared2 = 2;
    std::cout << "value1: " << *ptr_to_shared1;
}
```

发送和接收并非同步, 可以以任意的顺序到达

Reordering: 数据的发送和接收时存在延迟的

但是Fences bring order to Chaos

```c++
int    *ready_flag;  // init: *ready_flag == 0
data_t *data;        // init: ???

void writer_thread()
{
  *data = do_some_work_to_produce_data();
  *ready_flag = 1; // 可以重排之上
}

data_t reader_thread()
{
  while (1) {
    int ready = *ready_flag;
    if (ready) break;
  }
  return *data;
}
```

由于两个线程执行是乱序的, 所以结果很难保证;

我们可以在第一个线程当中添加`store_fence`来防止重排, 强制顺序. 在下面添加`load_fence`. 那么下面不得不提store_release和load_acquire.

现代CPU的目标:

* 避免因为数据等待而stall
* 因此会尽早开始load, 同时延迟store(异步提交)

还有更严格的mem_fence, 是一个完整的内存屏障, C++原子序列一致性fence, 明确阻止所有重排.

