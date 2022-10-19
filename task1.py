# Дан массив связей пользователей. Вам необходимо реализовать функцию,
# которая принимает на вход три аргумента: информация о связях, как кортеж (tuple)
# кортежей, первое имя (str), второе имя (str). Функция должна возвращать True, если
# связь между любыми двумя заданными пользователями существует, например, если у
# двух пользователей есть общие друзья или у их друзей есть общие друзья и т.д., иначе
# False.

from collections import deque

def set_graph(net):
    unique_names = []
    graph = {}
    for i in net:
        name1, name2 = i
        if name1 not in unique_names:
            unique_names.append(name1)
        if name2 not in unique_names:
            unique_names.append(name2)
    for name in unique_names:
        graph[name] = []
        for j in net:
            name1, name2 = j
            if name1 == name:
                graph[name].append(name2)
            if name2 == name:
                graph[name].append(name1)
    return graph


def check_relation(net, first, second):
    graph = set_graph(net)
    search_queue = deque()
    search_queue += graph[first]
    searched = []
    while search_queue:
        person = search_queue.popleft()
        if person not in searched:
            if person == second:
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False

if __name__ == '__main__':
    net = (
        ("Ваня", "Лёша"), ("Лёша", "Катя"), ("Ваня", "Катя"), ("Вова", "Катя"), ("Лёша", "Лена"), ("Оля", "Петя"),
        ("Стёпа", "Оля"), ("Оля", "Настя"),
        ("Настя", "Дима"), ("Дима", "Маша")
    )

    assert check_relation(net, "Петя", "Стёпа") is True
    assert check_relation(net, "Маша", "Петя") is True
    assert check_relation(net, "Ваня", "Дима") is False
    assert check_relation(net, "Лёша", "Настя") is False
    assert check_relation(net, "Стёпа", "Маша") is True
    assert check_relation(net, "Лена", "Маша") is False
    assert check_relation(net, "Вова", "Лена") is True