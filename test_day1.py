# 1. 创建字典
operators_dict = {'<': 'less than', '==': 'equal'}

# 2. 第一轮打印
print('Here is the original dict:')

# sorted(operators_dict) 会返回一个排好序的键列表：['<', '==']
# 我们遍历这个列表，每次拿到一个符号 (operator)
for operator in sorted(operators_dict):
    # 通过键 (operator) 去字典里查对应的值 (meaning)
    meaning = operators_dict[operator]
    print(f'Operator {operator} means {meaning}.')

# 3. 添加新键值对
operators_dict['>'] = 'greater than'

# 4. 打印题目要求的“换行” (就是打印一个空的东西)
print()

# 5. 第二轮打印 (此时字典里有3个东西了)
print('The dict was changed to:')

for operator in sorted(operators_dict):
    meaning = operators_dict[operator]
    print(f'Operator {operator} means {meaning}.')