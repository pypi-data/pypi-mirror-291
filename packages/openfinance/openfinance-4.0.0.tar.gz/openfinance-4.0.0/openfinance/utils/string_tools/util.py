from __future__ import print_function
import math

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if '\u4e00' <= uchar <= '\u9fff':
        return True
    else:
        return False

def num_to_string(number):
    """
    参数:
    number (int, float): 需要转换的数字。

    返回:
    str: 转换后的字符串表示。
    """
    if abs(number) < 10000:
        fractional_part, integer_part = math.modf(number)
        if fractional_part == 0:
            return f"{int(number)}"
        else:
            return f"{number:.2f}"
    elif abs(number) < 100000000:
        number = number/10000
        return f"{number:.2f}万"
    elif abs(number) < 1000000000000:
        number = number/100000000
        return f"{number:.2f}亿"    
    else:
        return f"{number:.2g}" 

if __name__ == "__main__":
    print(is_chinese("中文"))
    print(is_chinese("eg"))
