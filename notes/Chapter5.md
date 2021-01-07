# Chapter5: Thread-Level Parallelism

王志英 1350848-683 zywang@nudt.edu.cn

要求：需要记住的概念、原理等

主要讲多处理情况下，体系结构给予的支持。体系结果要做的哪些必要的调整

## Introduction

单处理机在芯片工艺进步的情况下

-   受到光速的影响，CPU主频到3GHz，一个节拍就能发射10cm，再快就超过集成电路大小了。
-   原子间距的影响，集成度的提高受到物理约束，在更小的原子间距的情况下，无法保持集成电路物理性质
-   做立体的集成电路受到功耗和散热的影响，一层大概是200W的功率

（个人认为量子计算机只能作为协处理器）

使用多处理机

-   多处理器的连接

-   体系结构进展能够支撑多处理机
-   并行软件的进展很好

-   对高端服务器的需求



### A Taxonomy of Parallel Architectures

-   SISD
-   SIMD
-   MISD
-   MIMD

当前MIMD面临的应用从通用角度来讲带来了更好的性价比

-   具有灵活性
    -   对单用户大任务提高了效率
    -   还可以完成多任务
-   可以充分利用商业化微处理器再性价比上的优势
    -   多处理机紧耦合协同工作
    -   单系统
    -   共享存储器（基本要求：共享存储空间）





线程级并行：讲授如何在多个线程上协同工作

-   一组线程协同完成一个任务（并行处理）
-   多个相对独立的进程进行部分协同工作（请求级并行）



片上多处理（多核CPU处理器），或称为单片多处理。其与多处理机系统从体系结构上看是相通的



在多处理机上共享了代码、数据等的进程叫做==线程==



线程数量可以比处理器数量大



根据存储器互联处理器的数量分为

1.  集中式共享存储器体系结构（Centralized Shared-Memory Architecture）

    物理上靠近、直接连到共享存储器中

    处理机数量较少，共享的是一个集中的存储器

    通过大容量的Cache和总线连接，则每个处理器访问存储器时间是相同的

    多处理器、紧耦合、协同工作

    只有一个单独的主存，该主存对各处理器的关系是对称的，有时可称为对称式共享存储器多处理机（SMP: Symmetric shared-memory Multiprocessor）（体系结构称为：UMA：uiform memory architrcture）

2.  分布式存储器结构多处理器

    处理器和存储器都是分布式的

    处理器和访存的数量都很大，需要高带宽的互联

    远程访问延迟

    优势

    1.  存储带宽可以根据连接节点形成带宽扩展
    2.  降低了对局部存储器访问延迟

    缺点

    1.  在远程访问中，访存时间、通讯时间有较高延迟
    2.  超节点SMP，每个节点有2-8个处理器



### Models for Communication and Memory Archutrcture

通讯：数据的共享和交换，意味着对贡献数据的访问

两种数据共享方式

1.  对于集中式共享，共享地址空间的数据共享

    只要地址统一编址，逻辑上就是共享的地址空间，通过对共享数据读写即可

    对于分布式共享，DSM（distributed shared-memory）体系结构，使用NUMAs（non-uniform memory access）

2.  独立的地址空间，没有统一编址

    逻辑空间不一样的情况下，称为多计算机

    群集系统（多个计算机使用高速互连网络连接成一个集群）

    消息传递是同步的，需要花费时间等待产生数据节点发送数据，接收后再发出响应，效率较低。



### Performance Metrics for Communication

1.  通讯带宽

2.  通讯延迟

    Sender overhead+Time of flight+Transmission time+Reciver overhead

3.  通讯延迟隐藏



### Advantages of Different Communication Mechanisms

共享存储通讯

1.  透明的，兼容性好
2.  编程容易，在简化编译器设计方面也有优势
4.  通信开销低，带宽利用好
5.  硬件控制cache的能力，减少了通信延迟即对共享数据的访问冲突



消息船体通信

1.  通讯明了清晰
2.  硬件简单
3.  有同步操作



### 并行处理面临的挑战

1.  程序中有限的并行性
2.  相对较高的通信开销

Amdahl定律
$$
系统加速比=\frac{1}{\frac{并行比例}{100}+(1-可加速部分比率)}
$$


### Characteristics of Application Domains

体系结构的目的：减少串行的比例



### Scientific/Technical Applications

 快速FFT变换，LU分解



### Computation/Communication for the Parallel Programs





## Centralized Shared-Memory Architecturs

针对小规模系统，每个节点有自己的Cache，假设每个节点一个处理器

支持对共享数据和私有数据的Cache缓存。私有数据供一个单独的处理器使用，而贡献数据供多个处理器使用。



What is Multiprocessor Cache Coherence?

Cache相关性：多个cache共享数据拷贝以及这些数据拷贝的等同一致的问题。读出来的数据是不是一样的

Cache一致性：什么时候可以读出来那个写进去的正确的数值



A memory system is coherent if

1.  一个处理机自己写自己读，中间没有别的处理机进行写
2.  两个处理机，一个写了另一个读，写和读之间没有别的写
3.  两个处理机的写操作顺序在各个处理器看来都一致



相关性和一致性是互补的