def strict(func):
    """
    Декоратор для проверки типов аргументов функции
    на соответствие аннотациям типов.
    Если тип аргумента не соответствует аннотации,
    выбрасывается исключение TypeError.
    """

    def wrapper(*args, **kwargs):
        """
        Обёртка для декорируемой функции.
        """

        annotations = func.__annotations__

        for i, (arg, expected_type) in enumerate(
            zip(args, annotations.values())
        ):

            if i == len(args):
                break

            param_name = list(annotations.keys())[i]

            if not isinstance(arg, expected_type):
                raise TypeError(
                    f'Аргумент "{param_name}" должен быть типа {expected_type}'
                )

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    """
    Функция складывания двух чисел.
    """
    return a + b


if __name__ == '__main__':
    print(sum_two(1, 2))
    # print(sum_two(1, 2.4))
