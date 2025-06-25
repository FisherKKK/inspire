# Modern CPP

> 核心主要是记录看到CPP的一些简单内容

## 1. SmartPDF中的CallBack

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

