def compute_prefix_function(pattern):
    """Вычисляем префикс-функцию для шаблона."""
    m = len(pattern)
    pi = [0] * m
    k = 0

    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = pi[k - 1]

        if pattern[k] == pattern[i]:
            k += 1

        pi[i] = k

    return pi

def kmp_search(text, pattern):
    """Функция для поиска подстроки в строке с использованием алгоритма Кнута-Морриса-Пратта."""
    n = len(text)
    m = len(pattern)
    
    # Вычисляем префикс-функцию для шаблона
    pi = compute_prefix_function(pattern)
    
    # Индекс для строки
    j = 0
    
    results = []

    for i in range(n):
        while j > 0 and pattern[j] != text[i]:
            j = pi[j - 1]

        if pattern[j] == text[i]:
            j += 1

        if j == m:
            results.append(i - m + 1)
            j = pi[j - 1]

    return results

# Пример использования
if __name__ == "__main__":
    text = "Я люблю читать книги"
    pattern = "читать"
    result = kmp_search(text, pattern)

    if result:
        print(f"Подстрока '{pattern}' найдена в следующих позициях: {result}")
    else:
        print(f"Подстрока '{pattern}' не найдена.")