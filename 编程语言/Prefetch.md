# Prefetch

## 1. 预取操作

1. 缓存不命中会导致产生200-300时钟周期的stall
2. hardware prefetch并非总是可能的
3. 可以通过hint compiler的方式, 告诉程序预取RAM中的内容到Cache中: `__builtin_prefetch` (编译器扩展) 或者`_mm_prefetch` (针对Intel平台)

## 2. 预取的问题

1. 预取只是对编译器的hint, 不一定有效



## 3. Appendix

1. [Is software prefetching (__builtin_prefetch) useful for performance?](https://news.ycombinator.com/item?id=16960919)

2. [Performance optimization] (https://www.one-tab.com/page/th0sLbEkS6e17UuP8sMilA)