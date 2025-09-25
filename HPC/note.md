# Chap1 Intro

单处理器时代: 基于CPU的处理器通过增加时钟频率提高算力性能, 目前桌面和数据中心分别能达到GFLOPS和TFLOPS (极限情况下)

多线程时代: 主要关注任务的吞吐, 目前GPU能达到百TFLOPS的浮点算力

CPU和GPU的主要区别:

* CPU的设计目的主要是减少延迟, 例如层级Cache, 分支预测
* GPU由现代电子游戏驱动, 设计目的是更高的浮点数运算以及更大的内存带宽

![image-20250924204403065](.\assets\1.png)



CUDA是什么: Compute Unified Device Architecture

在2006年之前, 图形芯片非常难用, 必须要通过等同的graphic api才能进行同等的编程, 例如OpenGL, Direct3D. 也就是说以前如果要在GPU上实现通用计算, 就必须要通过类似图形API进行绘图实现. 也被称之为General Purpose Programming using GPU (GPGPU).

2007年Nvidia发布CUDA之后, GPU上的编程就变得简单多

对于应用加速来说, 即使理论算力有很多, 但是往往受到内存带宽的影响, 因此对于GPU来说会尽最大程度上利用**片上缓存**.

## Chap2 Heterogeneous Data Parallel Computing



