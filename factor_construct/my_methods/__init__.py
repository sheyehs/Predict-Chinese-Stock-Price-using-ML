"""
如何import自定义python库：
1，首先建立一个文件夹，命名为库名A
2，具体文件必须以.py为格式，命名为文件名B
3，在B.py中如通常那样写好要在其他地方引用的方法或类c
4，最后在该文件夹内创建一个__init__.py，如本文件
5，在该文件中写下如此格式：from .B import c
6，将该文件夹（库）复制到想要import之的文件的同级路径，或者干脆放到环境内的site-packages文件夹内
7，在目标文件中写下如此格式：import A( as a)

import流程：工作文件——>文件夹A中的__init__.py——>文件夹A中的其他文件B.py下的c
"""

"""
author: Siltka (Shi Yaoen)
update: 2022/2/20
"""

from .factor_construct import extract_variable, extract_variable_oneFile, industry_adjust_ewa, industry_proportion
