# n ~ ln(Fn*sqrt(5)-1) / ln((1 + sqrt(5)) / 2)
# но предыдущие так или иначе придётся считать, так что разницы нет

def main():
    left, right = map(int, input().strip().split())
    assert left < right, "Начало должно быть меньше конца"
    fn1, fn2 = 0, 1
    fibonacci = []
    while fn2 < left:
        fn1, fn2 = fn2, fn1 + fn2
    while fn2 <= right:  # 2 цикла во избежание двойных сравнений
        fibonacci.append(fn2)
        fn1, fn2 = fn2, fn1 + fn2
    if fibonacci:
        print(*fibonacci, sep=" ")
    else:
        print("В заданном диапазоне нет чисел Фибоначчи")


if __name__ == "__main__":
    main()
