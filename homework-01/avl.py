# Класс для создания узла дерева
class Node:
    def __init__(self, key, height=1, left=None, right=None):
        self.key = key # ключ узла
        self.height = height # высота узла
        self.left = left # левый потомок
        self.right = right # правый потомок


class AVLTree:
    # Класс для AVL-дерева
    def __init__(self):
        self.root = None # инициализация корня дерева

    def get_height(self, node):
        # Получение высоты узла
        if not node:
            return 0
        return node.height

    def update_height(self, node):
        # Обновление высоты узла
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        # Получение баланса узла (разница высот левого и правого поддеревьев)
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        # Левый поворот узла
        y = z.right
        T2 = y.left

        # Выполнение поворота
        y.left = z
        z.right = T2

        # Обновление высот узлов
        self.update_height(z)
        self.update_height(y)

        return y

    def right_rotate(self, z):
        # Правый поворот узла
        y = z.left
        T3 = y.right

        # Выполнение поворота
        y.right = z
        z.left = T3

        # Обновление высот узлов
        self.update_height(z)
        self.update_height(y)

        return y

    def rebalance(self, node):
        # Балансировка узла
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

    def insert(self, node, key):
        # Вставка ключа в дерево
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        return self.rebalance(node)

    def delete(self, node, key):
        # Удаление ключа из дерева
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

    def get_min_value_node(self, node):
        # Получение узла с минимальным значением ключа
        current = node
        while current.left:
            current = current.left
        return current

    def pre_order(self, node):
        # Префиксный обход дерева (вывод ключей в порядке: корень-левый-правый)
        if not node:
            return
        print(f"{node.key} ", end="")
        self.pre_order(node.left)
        self.pre_order(node.right)

    def insert_key(self, key):
        # Вставка ключа в дерево
        self.root = self.insert(self.root, key)

    def delete_key(self, key):
        # Удаление ключа из дерева
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