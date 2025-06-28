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
