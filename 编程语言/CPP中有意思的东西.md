# 编程相关

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