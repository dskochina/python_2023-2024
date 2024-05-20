# Функция для вычисления хеша строки
def hash_func(s, prime=101):
    h = 0
    for i in range(len(s)):
        h = (h * prime + ord(s[i])) % (2**32)
    return h

# Функция для поиска подстрок с использованием алгоритма Рабина-Карпа
def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    prime = 101
    pattern_hash = hash_func(pattern, prime)
    text_hash = hash_func(text[:m], prime)
    
    results = []

    for i in range(n - m + 1):
        # Проверяем хеши, и если они совпадают, проверяем сами строки
        if text_hash == pattern_hash and text[i:i + m] == pattern:
            results.append(i)

        # Вычисляем хеш следующего подстроки
        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * (prime ** (m - 1))) * prime + ord(text[i + m])
            text_hash %= 2**32  # Чтобы избежать переполнения

    return results

# Пример использования
if __name__ == "__main__":
    text = "Привет, меня зовут Даша"
    pattern = "Даша"
    result = rabin_karp(text, pattern)

    if result:
        print(f"Подстрока '{pattern}' найдена в следующих позициях: {result}")
    else:
        print(f"Подстрока '{pattern}' не найдена.")