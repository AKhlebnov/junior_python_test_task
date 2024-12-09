"""
Модуль для вычисления времени общего присутствия ученика и преподавателя
в рамках заданного интервала урока.
"""


def get_common_intervals(
    pupil: list[tuple[int, int]],
    tutor: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """
    Функция для нахождения пересечения временных
    интервалов между учеником и преподавателем.
    """

    intersection_p = []

    for p_start, p_end in pupil:

        for t_start, t_end in tutor:

            start = max(p_start, t_start)
            end = min(p_end, t_end)

            if start < end:
                intersection_p.append((start, end))

    return intersection_p


def filter_intervals_by_lesson(
    people: list[tuple[int, int]],
    lesson: list[int]
) -> list[tuple[int, int]]:
    """
    Функция для фильтрования интервалов.
    Оставляет только те, которые пересекаются с интервалом урока.
    """

    intersection_l = []

    for p_start, p_end in people:

        start = max(p_start, lesson[0])
        end = min(p_end, lesson[1])

        if start < end:
            intersection_l.append((start, end))

    return intersection_l


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Функция для объединения пересекающихся интервалов в один.
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current_start, current_end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]

        if current_start <= last_end:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged


def calculate_total_time(intervals: list[tuple[int, int]]) -> int:
    """
    Функция вычисления общего времени.
    """

    total = 0

    for start, end in intervals:

        total += end - start

    return total


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Функция вычисляет общее время пересечения интервалов ученика,
    преподавателя и урока.
    """

    lesson_interval = intervals['lesson']
    # Преобразуем интервалы учеников и преподавателей в списки пар
    pupil_intervals = [
        (intervals['pupil'][i], intervals['pupil'][i + 1])
        for i in range(0, len(intervals['pupil']), 2)
    ]
    tutor_intervals = [
        (intervals['tutor'][i], intervals['tutor'][i + 1])
        for i in range(0, len(intervals['tutor']), 2)
    ]
    # Находим пересечения между учеником и преподавателем
    common_intervals = get_common_intervals(pupil_intervals, tutor_intervals)
    # Фильтруем пересечения с интервалом урока
    lesson_intervals = filter_intervals_by_lesson(
        common_intervals, lesson_interval
    )
    # Объединяем пересекающиеся интервалы
    merged_intervals = merge_intervals(lesson_intervals)
    # Вычисляем общее время
    total_time = calculate_total_time(merged_intervals)

    return total_time
