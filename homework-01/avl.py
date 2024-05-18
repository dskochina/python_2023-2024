# Класс для создания узла дерева
class Node:
    def __init__(self, key, height=1, left=None, right=None):
        self.key = key # ключ узла
        self.height = height # высота узла
        self.left = left # левый потомок
        self.right = right # правый потомок

# Класс для AVL-дерева
class AVLTree:

    # Инициализация корня дерева
    def __init__(self):
        self.root = None

    # Получение высоты узла
    def get_height(self, node):
        # 
        if not node:
            return 0
        return node.height

    # Обновление высоты узла
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # Получение баланса узла (разница высот левого и правого поддеревьев)
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Левый поворот узла
    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Выполнение поворота
        y.left = z
        z.right = T2

        # Обновление высот узлов
        self.update_height(z)
        self.update_height(y)

        return y

    # Правый поворот узла
    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Выполнение поворота
        y.right = z
        z.left = T3

        # Обновление высот узлов
        self.update_height(z)
        self.update_height(y)

        return y

    # Балансировка узла
    def rebalance(self, node):
        self.update_height(node)
        balance = self.get_balance(node)

        # Левое поддерево перевесило
        if balance > 1:
            # Лево-правый случай
            if self.get_balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
            # Лево-левый случай.
            return self.right_rotate(node)

        # Правое поддерево перевесило
        if balance < -1:
            # Право-левый случай
            if self.get_balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
            # Право-правый случай
            return self.left_rotate(node)

        return node

    # Вставка ключа в дерево
    def insert(self, node, key):
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        return self.rebalance(node)

    # Удаление ключа из дерева
    def delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        return self.rebalance(node)

    # Получение узла с минимальным значением ключа
    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # Обход дерева в прямом порядке (вывод ключей в порядке: корень-левый-правый)
    def pre_order(self, node):
        if not node:
            return
        print(f"{node.key} ", end="")
        self.pre_order(node.left)
        self.pre_order(node.right)

    # Вставка ключа в дерево
    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    # Удаление ключа из дерева
    def delete_key(self, key):
        self.root = self.delete(self.root, key)


# Пример использования AVL-дерева
avl_tree = AVLTree()

# Добавление элементов
elements_to_insert = [30, 20, 40, 15, 50, 25]
for elem in elements_to_insert:
    avl_tree.insert_key(elem)

print("Обход дерева в прямом порядке после вставки новых узлов:")
avl_tree.pre_order(avl_tree.root)
print()

# Удаление элемента
avl_tree.delete_key(15)
print("Обход дерева в прямом порядке после удаления узла:")
avl_tree.pre_order(avl_tree.root)
print()