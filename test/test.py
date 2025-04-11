# 定义一个二维列表
lst = [[4, 2], [1, 5], [3, 3], [2, 1]]

# 使用sorted()函数和lambda表达式按照二维列表的第一列进行排序
sorted_lst = sorted(lst, key=lambda x: x[0])
print(sorted_lst)
