class TrieNode:
    def __init__(self):
        # Словарь для хранения дочерних узлов (символов)
        self.children = {}
        # Флаг, указывающий, является ли этот узел концом слова
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        # Создание корневого узла дерева
        self.root = TrieNode()
    
    def insert(self, word):
        # Начинаем с корневого узла
        node = self.root
        # Для каждого символа в слове
        for char in word:
            # Если символ еще не является дочерним узлом, добавляем его
            if char not in node.children:
                node.children[char] = TrieNode()
            # Переходим к следующему узлу
            node = node.children[char]
        # После вставки всех символов помечаем конечный узел слова
        node.is_end_of_word = True
    
    def search(self, word):
        # Начинаем с корневого узла
        node = self.root
        # Для каждого символа в слове
        for char in word:
            # Если символ отсутствует среди дочерних узлов, слово не существует
            if char not in node.children:
                return False
            # Переходим к следующему узлу
            node = node.children[char]
        # Проверяем, является ли текущий узел конечным узлом слова
        return node.is_end_of_word
    
    def delete(self, word):
        # Внутренняя функция для удаления слова из дерева
        def _delete(node, word, depth):
            # Если мы дошли до конца слова
            if depth == len(word):
                # Если текущий узел не является конечным узлом, слово не существует
                if not node.is_end_of_word:
                    return False
                # Убираем флаг конечного узла
                node.is_end_of_word = False
                # Возвращаем True, если у текущего узла больше нет дочерних узлов
                return len(node.children) == 0
            
            char = word[depth]
            # Если символ не является дочерним узлом, слово не существует
            if char not in node.children:
                return False
            
            # Рекурсивно вызываем удаление для следующего узла
            should_delete_current_node = _delete(node.children[char], word, depth + 1)
            
            # Если необходимо удалить текущий узел
            if should_delete_current_node:
                # Удаляем текущий символ из дочерних узлов
                del node.children[char]
                # Возвращаем True, если у текущего узла больше нет дочерних узлов
                return len(node.children) == 0
            return False
        
        # Вызываем внутреннюю функцию для удаления слова из корневого узла
        _delete(self.root, word, 0)

# Пример использования
trie = Trie()
words = ["привет", "мир", "меня", "зовут", "Даша"]
for word in words:
    trie.insert(word)

print(trie.search("привет"))     # True
print(trie.search("мир"))        # True
print(trie.search("меня"))       # True
print(trie.search("зовут"))      # True
print(trie.search("Даша"))       # True
print(trie.search("пока"))       # False

trie.delete("привет")
print(trie.search("привет"))     # False