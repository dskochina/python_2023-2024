def bad_character_heuristic(pattern):
    """Функция для создания таблицы 'плохих символов'."""
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char

def good_suffix_heuristic(pattern):
    """Функция для создания таблицы 'хороших суффиксов'."""
    m = len(pattern)
    good_suffix = [0] * (m + 1)
    border_pos = [0] * (m + 1)
    i = m
    j = m + 1
    border_pos[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    j = border_pos[0]
    for i in range(m + 1):
        if good_suffix[i] == 0:
            good_suffix[i] = j
        if i == j:
            j = border_pos[j]

    return good_suffix

def boyer_moore_search(text, pattern):
    """Функция для поиска подстроки в строке с использованием алгоритма Бойера-Мура."""
    m = len(pattern)
    n = len(text)
    
    bad_char = bad_character_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)
    
    s = 0
    results = []

    while s <= n - m:
        j = m - 1

        # Пока символы совпадают, продолжаем двигаться влево
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # Если j < 0, это означает, что паттерн полностью совпал с текущим сдвигом в тексте
        if j < 0:
            results.append(s)
            s += good_suffix[0]  # Сдвигаем паттерн вправо по правилу хорошего суффикса
        else:
            # Сдвигаем паттерн по максимуму из правил плохого символа и хорошего суффикса
            bad_char_shift = j - bad_char.get(text[s + j], -1)
            good_suffix_shift = good_suffix[j + 1]
            s += max(good_suffix_shift, bad_char_shift)

    return results

# Пример использования
if __name__ == "__main__":
    text = "Здравствуйте, давайте поищем подстроку в этом тексте"
    pattern = "подстроку"
    result = boyer_moore_search(text, pattern)

    if result:
        print(f"Подстрока '{pattern}' найдена в следующих позициях: {result}")
    else:
        print(f"Подстрока '{pattern}' не найдена.")