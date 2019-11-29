# ReMoC

#### 介绍
人大迁移率计算软件包(ReMoC)是基于第一性原理计算软件包``Vienna ab-initio Simulation Package (VASP)的输出结果，计算半导体载流子迁移率的软件包。在此软件包中，载流子迁移率计算所使用到的能带输运固体的形变势理论，近似认为电子主要被长波声子散射。同时，为了更精确的描述有限厚度的层状材料，我们还引入了转变函数来桥接二维材料和准三维层状材料。


#### 环境要求

1. VASP **5.4.4**
2. Python **3.x**
3. numpy **>=1.12.1**

#### 使用说明

 **fitmobility-guide文件中包含详细的介绍。** 

您可以从以下文献中获得更加详细的信息。 **如果您使用了本软件包来计算载流子迁移率，请引用如下文献。** 

1、High-mobility transport anisotropy and linear dichroism in few-layer black phosphorus  
Jingsi Qiao, Xianghua Kong, Zhi-Xin Hu, Feng Yang, Wei Ji
Nature Communications  **5** , 4475 (2014)

**如果您使用了转变函数的迁移率形式，请您再引用如下两篇文献:**

2、Calculated carrier mobility of h-BN/γ-InSe/h-BN van der Waals heterostructures
P Kang, V Michaud-Rioux, X-H Kong, G-H Yu and H Guo 
2D Mater. 4, 045014  (2017) 

3、Few-layer Tellurium: one-dimensional like layered elementary semiconductor with striking physical properties
Jingsi Qiao, Yuhao Pan, Feng Yang, Cong Wang, Yang Chai and Wei Ji, *
Sci. Bull.   **63(3)**  , 159-168 (2018)

目前版本为 **v0.1**。如果您在安装、使用时需要帮助，或者发现bug，可以扫以下二维码加入微信群聊联系我们：

![](http://sim.phys.ruc.edu.cn/upload/images/2019/2/2516421481.png "")