# Класс для узла B-дерева
class BTreeNode:
    # Инициализация узла B-дерева
    def __init__(self, t, leaf=False):
        self.t = t # минимальная степень B-дерева
        self.leaf = leaf # является ли узел листом
        self.keys = [] # ключи в узле
        self.children = [] # ссылки на потомков

    # Вставка ключа в незаполненный узел
    def insert_non_full(self, key):
        i = len(self.keys) - 1
        
        if self.leaf:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            self.keys.insert(i + 1, key)
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            if len(self.children[i + 1].keys) == 2 * self.t - 1:
                self.split_child(i + 1, self.children[i + 1])
                if key > self.keys[i + 1]:
                    i += 1
            self.children[i + 1].insert_non_full(key)

    # Разбиение заполненного узла
    def split_child(self, i, y):
        t = self.t
        z = BTreeNode(t, y.leaf)
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys[t - 1])

        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]

        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    # Обход дерева
    def traverse(self):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].traverse()
            print(self.keys[i], end=' ')
        if not self.leaf:
            self.children[len(self.keys)].traverse()

    # Поиск ключа в узле
    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and self.keys[i] == key:
            return self
        if self.leaf:
            return None
        return self.children[i].search(key)

    # Удаление ключа из узла
    def remove(self, key):
        idx = self.find_key(key)

        if idx < len(self.keys) and self.keys[idx] == key:
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            if self.leaf:
                return

            flag = (idx == len(self.keys))

            if len(self.children[idx].keys) < self.t:
                self.fill(idx)

            if flag and idx > len(self.keys):
                self.children[idx - 1].remove(key)
            else:
                self.children[idx].remove(key)

    # Нахождение индекса ключа
    def find_key(self, key):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        return idx

    # Удаление ключа из листового узла
    def remove_from_leaf(self, idx):
        self.keys.pop(idx)

    # удаление ключа из нелистового узла
    def remove_from_non_leaf(self, idx):
        key = self.keys[idx]

        if len(self.children[idx].keys) >= self.t:
            pred = self.get_predecessor(idx)
            self.keys[idx] = pred
            self.children[idx].remove(pred)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ = self.get_successor(idx)
            self.keys[idx] = succ
            self.children[idx + 1].remove(succ)
        else:
            self.merge(idx)
            self.children[idx].remove(key)

    # Получение предшественника ключа
    def get_predecessor(self, idx):
        current = self.children[idx]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    # Получение преемника ключа
    def get_successor(self, idx):
        current = self.children[idx + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    # Обеспечение минимального числа ключей в узле
    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    # Заимствование ключа у предшественника
    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]

        for i in range(len(child.keys) - 1, -1, -1):
            child.keys.insert(i + 1, child.keys.pop(i))
        if not child.leaf:
            for i in range(len(child.children) - 1, -1, -1):
                child.children.insert(i + 1, child.children.pop(i))
        
        child.keys.insert(0, self.keys[idx - 1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        
        self.keys[idx - 1] = sibling.keys.pop()

    # Заимствование ключа у преемника
    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])

        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        
        self.keys[idx] = sibling.keys.pop(0)

    # Слияние узлов
    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys.pop(idx))

        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        self.children.pop(idx + 1)

# Класс для B-дерева
class BTree:
    # Инициализация B-дерева
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    # Обход дерева
    def traverse(self):
        if self.root is not None:
            self.root.traverse()

    # Поиск ключа в дереве
    def search(self, key):
        return None if self.root is None else self.root.search(key)

    # Вставка ключа в дерево
    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            s = BTreeNode(self.t, False)
            s.children.insert(0, self.root)
            s.split_child(0, self.root)
            i = 0
            if s.keys[0] < key:
                i += 1
            s.children[i].insert_non_full(key)
            self.root = s
        else:
            root.insert_non_full(key)

    # Удаление ключа из дерева
    def delete(self, key):
        if not self.root:
            print("Дерево пустое")
            return

        self.root.remove(key)

        if len(self.root.keys) == 0:
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]

# Пример использования
if __name__ == "__main__":
    t = 3  # Минимальная степень B-дерева
    btree = BTree(t)

    # Вставка ключей
    keys = [10, 20, 5, 6, 12, 30]
    for key in keys:
        btree.insert(key)

    print("Обход дерева после вставки:")
    btree.traverse()
    print()

    # Поиск ключа
    key = 6
    result = btree.search(key)
    if result is not None:
        print(f"Ключ {key} найден в дереве.")
    else:
        print(f"Ключ {key} не найден в дереве.")

    # Удаление ключа
    btree.delete(20)
    print("Обход дерева после удаления ключа 20:")
    btree.traverse()
    print()