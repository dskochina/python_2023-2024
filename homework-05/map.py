# Реализация map с методом цепочек
class ChainHashMap:
    def __init__(self, capacity=10):
        # Инициализация хэш-таблицы с заданной вместимостью
        self.capacity = capacity
        # Создание списка списков для хранения элементов
        self.table = [[] for _ in range(capacity)]
        # Начальный размер таблицы
        self.size = 0

    def _hash(self, key):
        # Внутренний метод для вычисления хэш-значения ключа
        return hash(key) % self.capacity

    def put(self, key, value):
        # Метод для добавления или обновления элемента по ключу
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        # Проверка наличия ключа в текущем списке (бакете)
        for index, (k, v) in enumerate(bucket):
            if k == key:
                # Обновление значения, если ключ уже существует
                bucket[index] = (key, value)
                return
        # Добавление нового элемента, если ключ не найден
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        # Метод для получения значения по ключу
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        # Метод для удаления элемента по ключу
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        for index, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[index]
                self.size -= 1
                return True
        return False

    def contains(self, key):
        # Метод для проверки наличия ключа
        return self.get(key) is not None

# Реализация map с методом открытой адресации
class OpenAddressingHashMap:
    def __init__(self, capacity=10):
        # Инициализация хэш-таблицы с заданной вместимостью
        self.capacity = capacity
        # Создание списка для хранения элементов
        self.table = [None] * capacity
        # Начальный размер таблицы
        self.size = 0

    def _hash(self, key, probe):
        # Внутренний метод для вычисления хэш-значения ключа с учетом проб
        return (hash(key) + probe) % self.capacity

    def put(self, key, value):
        # Метод для добавления или обновления элемента по ключу
        probe = 0
        hash_index = self._hash(key, probe)
        while self.table[hash_index] is not None and self.table[hash_index][0] != key:
            probe += 1
            hash_index = self._hash(key, probe)
        if self.table[hash_index] is None:
            self.size += 1
        self.table[hash_index] = (key, value)

    def get(self, key):
        # Метод для получения значения по ключу
        probe = 0
        hash_index = self._hash(key, probe)
        while self.table[hash_index] is not None:
            k, v = self.table[hash_index]
            if k == key:
                return v
            probe += 1
            hash_index = self._hash(key, probe)
        return None

    def remove(self, key):
        # Метод для удаления элемента по ключу
        probe = 0
        hash_index = self._hash(key, probe)
        while self.table[hash_index] is not None:
            k, v = self.table[hash_index]
            if k == key:
                self.table[hash_index] = None
                self.size -= 1
                return True
            probe += 1
            hash_index = self._hash(key, probe)
        return False

    def contains(self, key):
        # Метод для проверки наличия ключа
        return self.get(key) is not None
    
# Класс-обёртка для выбора метода разрешения коллизий
class CustomHashMap:
    def __init__(self, method='chain', capacity=10):
        # Инициализация хэш-таблицы с выбором метода разрешения коллизий
        if method == 'chain':
            self.map = ChainHashMap(capacity)
        elif method == 'open':
            self.map = OpenAddressingHashMap(capacity)
        else:
            raise ValueError("Неизвестный метод разрешения коллизий")

    def put(self, key, value):
        # Метод для добавления или обновления элемента по ключу
        self.map.put(key, value)

    def get(self, key):
        # Метод для получения значения по ключу
        return self.map.get(key)

    def remove(self, key):
        # Метод для удаления элемента по ключу
        return self.map.remove(key)

    def contains(self, key):
        # Метод для проверки наличия ключа
        return self.map.contains(key)

# Пример использования:
custom_map_chain = CustomHashMap(method='chain')
custom_map_chain.put("a", 1)
print("Значение по ключу 'a' (метод цепочек):", custom_map_chain.get("a"))  # Вывод: 1

custom_map_open = CustomHashMap(method='open')
custom_map_open.put("a", 1)
print("Значение по ключу 'a' (метод открытой адресации):", custom_map_open.get("a"))  # Вывод: 1