#MyFloat

## 项目说明

该项目基于Python 3.5编写，核心部分为MyFloat类，该类是16位二进制浮点数类，具有格式化输出，加法，减法，乘法，除法几项功能。

该类具有以下特点：

- 不包含0，无法对0进行计算和显示
- 计算结果的舍入采用Trounding策略
- 尾数最高位规格化为1，报错按照邮件说明处理
- 重载了 + - * / 四个运算符，可以直接使用，对MyFloat类进行四则运算
- 由于Python 3.0版本之后的新变化，除法运算采用truedivide，重载的运算为`__truediv__`而不是`__div__`

## 快速测试

    C:\Windows\system32>MyFloat -0.8 2
    
    add:
    System result: 1.2
    Float result: 1.1875
    MyFloat result: 0_0000001_0_1001100
    
    sub:
    System result: -2.8
    Float result: -2.8125
    MyFloat result: 0_0000010_1_1011010
    
    mul:
    System result: -1.6
    Float result: -1.59375
    MyFloat result: 0_0000001_1_1100110
    
    div:
    System result: -0.4
    Float result: -0.3984375
    MyFloat result: 1_0000001_1_1100110

## 代码说明

### 1. MyFloat类

#### \__init__(self, origin_float)

该函数初始化了MyFloat类，输入变量`origin_float`是一个标准的float类型，通过函数`Trans_to_16_bit()`构建出16位二进制浮点数。如果输入变量为缺省，那么将初始化为1.0。

在MyFloat类中，16位二进制浮点数以阶符`sign_exp`、阶码`exponent`、数符`sign_man`、尾数`mantissa`四部分储存。其中阶符和数符为int类型，阶码和尾数为str类型。

#### \__str__(self)

该函数用于输出MyFloat的值。输出格式如下。

    Float result: -0.0595703125
    MyFloat result: 1_0000100_1_1111010

#### \__add__(self, hand)

该函数用于重载“+”运算符，输入变量`self` `hand`为MyFloat类型，返回值为输入变量相加的到的和，是MyFloat类型变量。函数`__sub__()`和`__mul__()`与该函数类似，分别用于重载“-”和“*”。

#### \__truediv__(self, hand)

该函数用于重载“/”运算符，输入变量`self` `hand`为MyFloat类型，返回值为输入变量相除的到的商，是MyFloat类型变量。这里需要特别注意，由于Python 3.0版本之后的新变化，除法运算采用truedivide，重载的运算为`__truediv__`而不是`__div__`。

### 2. Standardize(un_stand_float)

该函数用于规格化计算结果，具有防止尾数溢出，将尾数最高位置为1，将阶码和尾数补齐为7位的功能。输入变量`un_stand_float`为没有规格化的MyFloat类型，返回值为规格化后的MyFloat类型。

### 3. Trans_to_origin(binary_float)

该函数用于将16位二进制数转化为标准的float类型。输入变量`binary_float`为MyFloat类型，返回值为float类型。

### 4. Trans_to_16_bit(origin_float)

该函数用于将float类型数转化为16位二进制数。输入变量`origin_float`为float类型，返回值为由阶符、阶码、数符、尾数组成的列表。

### 5. Trans_to_exponent(man_of_float)

该函数用于将float型尾数转化为7位二进制尾数。输入变量`man_of_float`为已经被规格到`[0.5, 1)`之间的float类型，输出变量为str类型，存储7位二进制尾数。

### 6. Trans_to_mantissa(n)

该函数用于将阶数转化为7位二进制阶码。输入变量`n`为int类型，存储float数的阶数，输出变量为str类型，存储7位二进制阶码。

## 测试报告

### 1. 错误测试

#### 输入为零

	C:\Windows\system32>MyFloat -0.0 0.75
	
	...
	
	Exception: ERROR. Zero is not allowed.

#### 计算结果为零

	C:\Windows\system32>MyFloat -0.75 0.75
	
	...
	
	Exception: ERROR. Result is Zero.

### 2. 误差测试

在Linux下使用脚本test.py进行了测试。该脚本从`[500, 500)`中随机浮点数，分别对加减乘除四种运算进行了1000组测试，输出错误，同时计算与系统计算结果的误差，输出到相应csv文件。

    → ~ python test.py 
    cur error 0
    cur error 1
    cur error 2
    cur error 3

总共出现了4次错误，是输入或计算结果为0导致，可忽略。四种运算的误差平均值如下。

| 运算 | 平均误差 |
| :---: | :---: |
| +  | 0.014385962 |
| -  | 0.014194835 |
| *  | 0.014521381 |
| /  | 0.008693603 |

可以看到，误差平均值均在0.01左右，可以接受，其中除法误差最低，在0.008左右。考虑出现误差的主要原因为以下几点。

- 加减法运算时，如果计算结果溢出，需要右移并对尾数进行规格化，所以可能会舍弃1位数据，导致精度下降。对阶时，阶码较小的数的尾数需要右移来和阶码较大的数保持阶码一致，所以可能会舍弃若干位数据，导致精度下降。
- 乘法运算时，计算结果的尾数需要舍弃后7位数据，导致精度下降。
- 除法运算时，算法中只计算了8位结果，仍未被除尽的部分被舍弃，导致精度下降。
- 由浮点数转化为16位二进制数时，由于尾数只有7位，而且需要进行规格化，所以可能会舍弃若干位数据，导致精度下降。
