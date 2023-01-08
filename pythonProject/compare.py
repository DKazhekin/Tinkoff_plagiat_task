import argparse
import re

# Функция для удаления """Some text here""" комментариев
def del_triple(file):
    li = list(file)
    while file.find('"""') != -1:
        ind = file.find('"""')
        for i in range(3):
            del li[ind]
        file = "".join(li)
        ind2 = file.find('"""')
        for i in range(ind2 - ind):
            del li[ind]
        for i in range(3):
            del li[ind]
        file = "".join(li)
    return "".join(li)

# Функция для регулярного выражения
def replace_comment(match):
    value = match.group(1) or ''
    return value

# Функция расстония Левенштейна для двух строк
def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def main():
    # Массив результатов
    scores = []

    # Парсер командной строки
    parser = argparse.ArgumentParser(description='Plagiarism detector')
    parser.add_argument('input', type=str, help='Source file')
    parser.add_argument('output', type=str, help='Destionation file')
    args = parser.parse_args()

    # Чтение путей до двух source файлов из input.txt
    with open(args.input, 'r') as file:
        files = [line.rstrip() for line in file.readlines()]

        # Обработка каждой пары файлов из input.txt
        for f in files:
            path_to_data_1, path_to_data_2 = f.split()

            # Чтение текстов программм
            data_1 = open(path_to_data_1, 'r').read()
            data_2 = open(path_to_data_2, 'r').read()

            # Паттерн регулярного выражения для удаление однострочных комментариев вида: # Some text here
            comments_pattern1 = re.compile(r"(([\'\"]).*?\2)|(#.*)")
            data_1 = comments_pattern1.sub(replace_comment, data_1)
            data_2 = comments_pattern1.sub(replace_comment, data_2)

            # Уничтожение """Some text here""" комментариев c помощью функции del_triple(file)
            data_1 = del_triple(data_1)
            data_2 = del_triple(data_2)

            # Записываем результаты в массив scores
            scores.append(str(levenstein(" ".join(data_1.split()), " ".join(data_2.split()))/((len(" ".join(data_1.split())) + len(" ".join(data_2.split()))) / 2)))
    file.close()

    # Записываем результаты в массив scores.txt
    with open(args.output, "w") as file:
        for line in scores:
            file.write(line + '\n')
    file.close()

if __name__ == "__main__":
    main()