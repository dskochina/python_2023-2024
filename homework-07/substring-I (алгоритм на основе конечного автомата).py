class FiniteAutomaton:
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.alphabet = set(pattern)
        self.transition_table = self.build_transition_table()

    def build_transition_table(self):
        """Строим таблицу переходов для конечного автомата"""
        transition_table = [{} for _ in range(self.m + 1)]

        for state in range(self.m + 1):
            for char in self.alphabet:
                next_state = self.get_next_state(state, char)
                transition_table[state][char] = next_state

        return transition_table

    def get_next_state(self, state, char):
        """Определяем следующее состояние для заданного состояния и символа"""
        if state < self.m and char == self.pattern[state]:
            return state + 1

        for next_state in range(state, 0, -1):
            if self.pattern[next_state - 1] == char:
                k = 0
                while k < next_state - 1 and self.pattern[k] == self.pattern[state - next_state + 1 + k]:
                    k += 1
                if k == next_state - 1:
                    return next_state

        return 0

    def search(self, text):
        """Ищем вхождения паттерна в текст с использованием построенного автомата"""
        n = len(text)
        state = 0
        results = []

        for i in range(n):
            char = text[i]
            state = self.transition_table[state].get(char, 0)
            if state == self.m:
                results.append(i - self.m + 1)

        return results

# Пример использования
if __name__ == "__main__":
    text = "Пишем текст, в котором будем искать подстроку"
    pattern = "подстроку"
    fa = FiniteAutomaton(pattern)
    result = fa.search(text)

    if result:
        print(f"Подстрока '{pattern}' найдена в следующих позициях: {result}")
    else:
        print(f"Подстрока '{pattern}' не найдена.")