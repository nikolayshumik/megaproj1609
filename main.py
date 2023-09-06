n = int(input("Введите число карт: "))

cowboy = list(map(int, input("Введите комбинацию ковбоя: ").split()))
winning_combination = list(map(int, input("Введите комбинацию выигрышных карт: ").split()))

start, end = map(int, input("Введите начало и конец отрезка для сортировки: ").split())

if start <= 0 or end > len(cowboy):
    print("Выбранный отрезок некорректный")
    exit()

sorted_cowboy = cowboy.copy()

sorted_cowboy[start-1:end] = sorted(sorted_cowboy[start-1:end])

is_winning = sorted_cowboy == winning_combination

if is_winning:
    print("YES")
else:
    print("NO")