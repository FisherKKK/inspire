# CPP中有意思的东西

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

 