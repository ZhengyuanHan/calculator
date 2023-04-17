import re
import math


def string_to_list(input_string):
    new_string = input_string.replace(' ', '')

    if '^' not in new_string:
        return re.findall(r'[+\-*/^%]+|\([^\(\)]+\)|[A-Za-z][A-Za-z0-9_]*|\d+\.?\d*|==|<=|>=|!=|<|>|&&|\|\||!', new_string)

    if '^' in new_string and not re.search(r'[+\-*/]+|==|<=|>=|!=|<|>|&&|\|\||!', new_string):
        return re.findall(r'[+\-*/^%]+|\([^\(\)]+\)|[A-Za-z][A-Za-z0-9_]*|\d+\.?\d*', new_string)

    list1 = re.findall(r'[+\-*/^%]+|\([^\(\)]+\)|[A-Za-z][A-Za-z0-9_]*|\d+\.?\d*|==|<=|>=|!=|<|>|&&|\|\||!', new_string)
    is_con_pow = False

    for i in range(0, len(list1)):
        if isinstance(list1[i], str) and re.match(r'\^+', list1[i]) and not is_con_pow:
            list1.insert(i - 1, '(')
            is_con_pow = True
        if isinstance(list1[i], str) and re.match(r'[+\-*/&%]+|==|<=|>=|!=|<|>|&&|\|\||!', list1[i]) and is_con_pow:
            list1.insert(i, ')')
            is_con_pow = False

    if is_con_pow:
        list1.append(')')
        is_con_pow = False

    fin_string = ''.join(list1)

    return re.findall(r'[+\-*/&^%]+|\([^\(\)]+\)|[A-Za-z][A-Za-z0-9_]*|\d+\.?\d*|==|<=|>=|!=|<|>|&&|\|\||!', fin_string)


def convert_selfchange_to_num(expression_str, dict_helper):
    self_change_list = expression_str.split(' ')

    for i in range(0, len(self_change_list)):
        if re.match(r'^-?([A-Za-z][A-Za-z0-9_]*)\+\+$', self_change_list[i]):
            expression_group = re.match(r'^(-?)([A-Za-z][A-Za-z0-9_]*)\+\+$', self_change_list[i])
            if expression_group.group(1) == '-':
                self_change_list[i] = '-' + str(float(dict_helper[expression_group.group(2)]))
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) + 1
            else:
                self_change_list[i] = str(float(dict_helper[expression_group.group(2)]))
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) + 1

        elif re.match(r'^-?([A-Za-z][A-Za-z0-9_]*)--$', self_change_list[i]):
            expression_group = re.match(r'^(-?)([A-Za-z][A-Za-z0-9_]*)--$', self_change_list[i])
            if expression_group.group(1) == '-':
                self_change_list[i] = '-' + str(float(dict_helper[expression_group.group(2)]))
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) - 1
            else:
                self_change_list[i] = str(float(dict_helper[expression_group.group(2)]))
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) - 1

        elif re.match(r'^-?\+\+([A-Za-z][A-Za-z0-9_]*)$', self_change_list[i]):
            expression_group = re.match(r'^(-?)\+\+([A-Za-z][A-Za-z0-9_]*)$', self_change_list[i])
            if expression_group.group(1) == '-':
                dict_helper.update({expression_group.group(2): float(dict_helper[expression_group.group(2)]) + 1})
                # dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) + 1
                self_change_list[i] = '-' + str(float(dict_helper[expression_group.group(2)]))
            else:
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) + 1
                self_change_list[i] = str(float(dict_helper[expression_group.group(2)]))

        elif re.match(r'^-?--([A-Za-z][A-Za-z0-9_]*)$', self_change_list[i]):
            expression_group = re.match(r'^(-?)--([A-Za-z][A-Za-z0-9_]*)$', self_change_list[i])
            if expression_group.group(1) == '-':
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) - 1
                self_change_list[i] = '-' + str(float(dict_helper[expression_group.group(2)]))
            else:
                dict_helper[expression_group.group(2)] = float(dict_helper[expression_group.group(2)]) - 1
                self_change_list[i] = str(float(dict_helper[expression_group.group(2)]))

    return ''.join(self_change_list)


def expression_parse(expression_str, dict_helper):
    new_expression_str = convert_selfchange_to_num(expression_str, dict_helper)
    # print(new_expression_str)
    expression_list = string_to_list(new_expression_str)
    # print(expression_list)
    relation_list = ['==', '<=', '>=', '!=', '<', '>']
    boolean_list = ['&&', '||', '!']
    s = 0
    num_list = []

    for i in range(0, len(expression_list)):
        if re.match(r'\(.+\)', expression_list[i]):
            sub_expression = expression_list[i].lstrip('(').rstrip(')')
            # print(sub_expression)
            expression_list[i] = expression_parse(sub_expression, dict_helper)

    for j in range(0, len(expression_list)):
        if isinstance(expression_list[j], str) and not expression_list[j].isdigit() and re.match(r'^[A-Za-z][A-Za-z0-9_]*$', expression_list[j]):
            if expression_list[j] not in dict_helper:
                dict_helper.update({expression_list[j]: 0.0})
                expression_list[j] = dict_helper[expression_list[j]]
            else:
                expression_list[j] = dict_helper[expression_list[j]]

    # print(expression_list)
    # print(dict_helper)
    if '^' in expression_list:
        for ex_i in range(len(expression_list) - 1, 1, -2):
            expression_list[ex_i - 2] = pow(float(expression_list[ex_i - 2]), float(expression_list[ex_i]))

        return expression_list[0]

    for k in range(0, len(expression_list)):
        if isinstance(expression_list[k], str) and expression_list[k] == '-':
            expression_list[k + 1] = -float(expression_list[k + 1])
        if isinstance(expression_list[k], str) and re.match(r'\*+', expression_list[k]):
            expression_list[k + 1] = float(expression_list[k - 1]) * float(expression_list[k + 1])
            expression_list[k - 1] = 0
        if isinstance(expression_list[k], str) and re.match(r'/+', expression_list[k]):
            if float(expression_list[k + 1]) == 0:
                return 'divide by zero'
            expression_list[k + 1] = float(expression_list[k - 1]) / float(expression_list[k + 1])
            expression_list[k - 1] = 0
        if isinstance(expression_list[k], str) and re.match(r'%+', expression_list[k]):
            expression_list[k + 1] = float(expression_list[k - 1]) % float(expression_list[k + 1])
            expression_list[k - 1] = 0

    for node in expression_list:
        if isinstance(node, float) or isinstance(node, int) or (isinstance(node, str) and re.match(r'^-?\d+\.?\d*$', node)):
            s += float(node)
        elif node in relation_list or node in boolean_list:
            num_list.append(s)
            num_list.append(node)
            s = 0

    if not num_list:
        # print(s)
        return s
    else:
        num_list.append(str(s))
        return relation_helper(num_list)


def relation_helper(num_list):
    remove_list = ['temp']
    for i in range(0, len(num_list)):
        if num_list[i] == '==':
            remove_list.append(num_list[i])
            if num_list[i - 1] == num_list[i + 1]:
                num_list[i + 1] = 1
            else:
                num_list[i + 1] = 0
            num_list[i - 1] = 'temp'
        if num_list[i] == '<=':
            remove_list.append(num_list[i])
            if float(num_list[i - 1]) <= float(num_list[i + 1]):
                num_list[i + 1] = 1
            else:
                num_list[i + 1] = 0
            num_list[i - 1] = 'temp'
        if num_list[i] == '>=':
            remove_list.append(num_list[i])
            if float(num_list[i - 1]) >= float(num_list[i + 1]):
                num_list[i + 1] = 1
            else:
                num_list[i + 1] = 0
            num_list[i - 1] = 'temp'
        if num_list[i] == '!=':
            remove_list.append(num_list[i])
            if num_list[i - 1] != num_list[i + 1]:
                num_list[i + 1] = 1
            else:
                num_list[i + 1] = 0
            num_list[i - 1] = 'temp'
        if num_list[i] == '>':
            remove_list.append(num_list[i])
            if float(num_list[i - 1]) > float(num_list[i + 1]):
                num_list[i + 1] = 1
            else:
                num_list[i + 1] = 0
            num_list[i - 1] = 'temp'
        if num_list[i] == '<':
            remove_list.append(num_list[i])
            if float(num_list[i - 1]) < float(num_list[i + 1]):
                num_list[i + 1] = 1
            else:
                num_list[i + 1] = 0
            num_list[i - 1] = 'temp'

    for op in remove_list:
        if op in num_list:
            num_list.remove(op)

    if '!' in num_list:
        for j in range(0, len(num_list)):
            if num_list[j] == '!':
                if int(num_list[j + 1]) == 0:
                    num_list[j + 1] = 1
                else:
                    num_list[j + 1] = 0
        num_list.remove('!')

    for k in range(0, len(num_list)):
        if num_list[k] == '&&':
            if float(num_list[k - 1]) == 0 and float(num_list[k + 1]) == 0:
                num_list[k + 1] = 0
            elif float(num_list[k - 1]) != 0 and float(num_list[k + 1]) != 0:
                num_list[k + 1] = 1
            else:
                num_list[k + 1] = 0

        if num_list[k] == '||':
            if float(num_list[k - 1]) == 0 and float(num_list[k + 1]) == 0:
                num_list[k + 1] = 0
            elif float(num_list[k - 1]) != 0 and float(num_list[k + 1]) != 0:
                num_list[k + 1] = 1
            else:
                num_list[k + 1] = 1

    return num_list[len(num_list) - 1]


def error_code(program_str):
    if program_str.split(' ')[0] != 'print':
        if re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*[+\-*/^%]+\s*([A-Za-z][A-Za-z0-9_]*)$', program_str):
            return 0
        elif re.match(r'^(-?\d+\.?\d*)\s*[+\-*/^%]+\s*([A-Za-z][A-Za-z0-9_]*)$', program_str):
            return 0
        elif re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*[+\-*/^%]+\s*(-?\d+\.?\d*)$', program_str):
            return 0
        elif re.match(r'^(-?\d+\.?\d*)\s*=\s*([A-Za-z][A-Za-z0-9_]*)$', program_str):
            return 0

    program_item_list = re.findall(r'\+|-|\*|/|%|^|\([^\(\)]+\)|[A-Za-z][A-Za-z0-9_]*|\d+\.?\d*|==|<=|>=|!=|<|>|&&|\|\||!', program_str)
    # print(program_item_list)

    for i in range(0, len(program_item_list)):
        if program_item_list[i] == '0' and program_item_list[i - 1] == '/':
            return 1

        if not re.search(r'^\s*\*/\s*$', program_str):
            if i < len(program_item_list) - 1 and program_item_list[i] == '+' and program_item_list[i + 1] == '+':
                return 3
            if i < len(program_item_list) - 1 and program_item_list[i] == '-' and program_item_list[i + 1] == '-':
                return 3
            elif i == len(program_item_list) - 1 and re.match(r'[+\-*/^%]', program_item_list[i]):
                return 2
            elif i == 0 and re.match(r'[+*/^%]', program_item_list[i]):
                return 2
            elif (i == len(program_item_list) - 1 or i == 0) and re.match(r'^(\+=|-=|/=|%=|\^=|\*=)$', program_item_list[i]):
                return 2
            elif i == len(program_item_list) - 1 and re.match(r'^==|<=|>=|!=|<|>|&&|\|\||!$', program_item_list[i]):
                return 2
            elif i == 0 and re.match(r'^==|<=|>=|!=|<|>|&&|\|\|$', program_item_list[i]):
                return 2


def op_equals_helper(program_str):
    op_str = re.search(r'(\+=|-=|/=|%=|\^=|\*=|&&=|\|\|=)', program_str).group(1)
    program_item_list = program_str.split(op_str)
    new_program_str = program_item_list[0] + re.match(r'(\+|-|/|%|\^|\*|&&|\|\|)', op_str).group(1) + program_item_list[1]
    return new_program_str


if __name__ == '__main__':
    variables_dict = {}
    result_list = []
    is_comments = False

    while True:
        try:
            user_input = input()

            if re.search(r'^\s*/\*\s*$', user_input) and not is_comments:
                is_comments = True
            elif re.search(r'^\s*\*/\s*$', user_input) and is_comments:
                is_comments = False

            if re.match(r'check', user_input):
                print(variables_dict)
                print(result_list)
                print(is_comments)

            if not is_comments:
                if re.match(r'^\s*#\s*$', user_input):
                    continue
                if error_code(user_input) == 1:
                    result_list.append('divide by zero')

                elif error_code(user_input) == 0 or error_code(user_input) == 2:
                    result_list.append('parse error')

                if re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*$', user_input):
                    input_parse = re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*$', user_input)
                    variables_dict.update({input_parse.group(1): 0.0})

                elif re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*(=)\s*(.+)$', user_input):
                    input_parse = re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*(=)\s*(.+)', user_input)
                    if re.match(r'^-?\d+\.?\d*$', input_parse.group(3)):
                        variables_dict.update({input_parse.group(1): float(input_parse.group(3))})
                        # print(variables_dict)
                    elif re.match(r'^[A-Za-z][A-Za-z0-9_]*', input_parse.group(3)) and not re.search(r'[+\-*/&^]+',
                                                                                                     input_parse.group(
                                                                                                         3)):
                        if input_parse.group(3) not in variables_dict:
                            variables_dict.update({input_parse.group(3): 0.0})
                            variables_dict.update({input_parse.group(1): variables_dict[input_parse.group(3)]})
                        else:
                            variables_dict.update({input_parse.group(1): variables_dict[input_parse.group(3)]})
                    else:
                        variables_dict.update(
                            {input_parse.group(1): expression_parse(input_parse.group(3), variables_dict)})

                elif re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*(\+=|-=|/=|%=|\^=|\*=|&&=|\|\|=)\s*(.+)$', user_input):
                    input_parse = re.match(r'^([A-Za-z][A-Za-z0-9_]*)\s*(\+=|-=|/=|%=|\^=|\*=|&&=|\|\|=)\s*(.+)$', user_input)
                    if input_parse.group(1) not in variables_dict:
                        variables_dict.update({input_parse.group(1): 0.0})
                        variables_dict.update(
                            {input_parse.group(1): expression_parse(op_equals_helper(user_input), variables_dict)})
                    else:
                        variables_dict.update(
                            {input_parse.group(1): expression_parse(op_equals_helper(user_input), variables_dict)})

                elif re.match(r'^([A-Za-z][A-Za-z0-9_]*)\+\+$', user_input):
                    input_parse = re.match(r'^([A-Za-z][A-Za-z0-9_]*)\+\+$', user_input)
                    if input_parse.group(1) not in variables_dict:
                        variables_dict.update({input_parse.group(1): 1.0})
                    else:
                        variables_dict.update(
                            {input_parse.group(1): variables_dict[input_parse.group(1)] + 1.0})
                elif re.match(r'^\+\+([A-Za-z][A-Za-z0-9_]*)$', user_input):
                    input_parse = re.match(r'^\+\+([A-Za-z][A-Za-z0-9_]*)$', user_input)
                    if input_parse.group(1) not in variables_dict:
                        variables_dict.update({input_parse.group(1): 1.0})
                    else:
                        variables_dict.update(
                            {input_parse.group(1): variables_dict[input_parse.group(1)] + 1.0})
                elif re.match(r'^([A-Za-z][A-Za-z0-9_]*)--$', user_input):
                    input_parse = re.match(r'^([A-Za-z][A-Za-z0-9_]*)--$', user_input)
                    if input_parse.group(1) not in variables_dict:
                        variables_dict.update({input_parse.group(1): -1.0})
                    else:
                        variables_dict.update(
                            {input_parse.group(1): variables_dict[input_parse.group(1)] - 1.0})
                elif re.match(r'^--([A-Za-z][A-Za-z0-9_]*)$', user_input):
                    input_parse = re.match(r'^([A-Za-z][A-Za-z0-9_]*)--$', user_input)
                    if input_parse.group(1) not in variables_dict:
                        variables_dict.update({input_parse.group(1): -1.0})
                    else:
                        variables_dict.update(
                            {input_parse.group(1): variables_dict[input_parse.group(1)] - 1.0})

                if re.match(r'^(print)\s+(-?\d+\.?\d*)$', user_input):
                    input_parse = re.match(r'^(print)\s+(-?\d+\.?\d*)$', user_input)
                    result_list.append(float(input_parse.group(2)))
                    # print(float(input_parse.group(2)))

                elif re.match(r'^(print)\s+(.+)$', user_input):
                    input_parse = re.match(r'^(print)\s+(.+)$', user_input)
                    if error_code(input_parse.group(2)) == 2:
                        result_list.append('parse error')
                    elif ',' in input_parse.group(2):
                        output_list = []
                        print_list = input_parse.group(2).replace(' ', '').split(',')

                        for variable in print_list:
                            if error_code(variable) == 2:
                                result_list.append('parse error')
                            elif not re.search(r'[+\-*/%^]+|==|<=|>=|!=|<|>|&&|\|\||!', variable):
                                output_list.append(variables_dict[variable])
                            else:
                                output_list.append(expression_parse(variable, variables_dict))

                        result_list.append(output_list)

                    elif re.search(r'[+\-*/%^]+|==|<=|>=|!=|<|>', input_parse.group(2)):
                        result_list.append(expression_parse(input_parse.group(2), variables_dict))

                        # print(expression_parse(input_parse.group(2), variables_dict))

                    else:
                        if input_parse.group(2) not in variables_dict:
                            variables_dict.update({input_parse.group(2): 0.0})
                            result_list.append(variables_dict[input_parse.group(2)])
                        else:
                            result_list.append(variables_dict[input_parse.group(2)])
                        # print(float(variables_dict[input_parse.group(2)]))
                elif re.match(r'^(print)\s*$', user_input):
                    result_list.append('parse error')
            else:
                continue

        except EOFError:
            if 'parse error' in result_list:
                print('parse error')
                break

            for result_i in range(0, len(result_list)):
                if isinstance(result_list[result_i], list):
                    for output_i in range(0, len(result_list[result_i])):
                        if result_list[result_i][output_i] == 'divide by zero':
                            print(result_list[result_i][output_i])
                            break
                        elif output_i == len(result_list[result_i]) - 1:
                            print(result_list[result_i][output_i])
                        else:
                            print(result_list[result_i][output_i], end=' ')
                else:
                    if result_list[result_i] == 'divide by zero':
                        print(result_list[result_i])
                        break
                    else:
                        print(result_list[result_i])

            break
