import heapq  # импортируем модуль heapq для работы с приоритетной очередью (минимальной кучей)
from collections import Counter  # импортируем Counter для подсчета частот символов

# Класс для узла в дереве Хаффмана
class Node:
    def __init__(self, char, freq):
        self.char = char  # символ
        self.freq = freq  # частота символа
        self.left = None  # левый потомок
        self.right = None # правый потомок

    # Метод для сравнения узлов по частоте (для приоритетной очереди)
    def __lt__(self, other):
        return self.freq < other.freq

# Функция для построения дерева Хаффмана
def build_huffman_tree(frequencies):
    # Создание приоритетной очереди из узлов
    priority_queue = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)  # преобразуем список в минимальную кучу
    
    # Пока в очереди больше одного узла
    while len(priority_queue) > 1:
        # Извлекаем два узла с наименьшей частотой
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        
        # Создаём новый объединённый узел
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        # Добавляем объединённый узел обратно в очередь
        heapq.heappush(priority_queue, merged)
    
    # Возвращаем корень дерева Хаффмана
    return priority_queue[0]

# Функция для генерации кодов Хаффмана
def generate_huffman_codes(root):
    def generate_codes_helper(node, current_code):
        if node is None:
            return
        
        # Если достигнут листовой узел (символ)
        if node.char is not None:
            codes[node.char] = current_code
            return
        
        # Рекурсивно идём влево и вправо, добавляя '0' или '1'
        generate_codes_helper(node.left, current_code + "0")
        generate_codes_helper(node.right, current_code + "1")
    
    codes = {}  # словарь для хранения кодов Хаффмана
    generate_codes_helper(root, "")  # начинаем с пустого кода
    return codes

# Функция для кодирования строки
def huffman_encoding(data):
    if not data:
        return "", {}
    
    # Подсчёт частот символов
    frequencies = Counter(data)
    
    # Построение дерева Хаффмана
    root = build_huffman_tree(frequencies)
    
    # Генерация кодов Хаффмана
    huffman_codes = generate_huffman_codes(root)
    
    # Кодирование данных
    encoded_data = ''.join(huffman_codes[char] for char in data)
    
    return encoded_data, huffman_codes

# Функция для декодирования строки
def huffman_decoding(encoded_data, huffman_codes):
    # Обратный словарь для поиска символа по коду
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decoded_data = []
    
    # Проходим по закодированным данным
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ""
    
    return ''.join(decoded_data)

# Пример использования
data = "Меня зовут Даша"
encoded_data, huffman_codes = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, huffman_codes)

print("Исходные данные:", data)
print("Закодированные данные:", encoded_data)
print("Коды Хаффмана:", huffman_codes)
print("Декодированные данные:", decoded_data)