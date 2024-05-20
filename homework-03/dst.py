class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    # Если дерево пустое, создаём новый узел и делаем его корнем
    if root is None:
        return Node(key)
    
    # Рекурсивно вставляем новый ключ в соответствующее поддерево
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
    
    return root

def search(root, key):
    # Если корень - None или ключ корня совпадает с искомым ключом, возвращаем корень
    if root is None or root.val == key:
        return root
    
    # Если ключ меньше корня, идём налево
    if root.val < key:
        return search(root.right, key)
    
    # Если ключ больше корня, идём направо
    return search(root.left, key)

def inorder(root):
    # Рекурсивно обходим дерево в порядке "возрастания" значений узлов
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

def delete(root, key):
    # Если дерево пустое, возвращаем None
    if root is None:
        return root
    
    # Рекурсивно обходим дерево, пока не найдём узел с искомым ключом
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    
    # Когда узел с искомым ключом найден:
    else:
        # У узла нет детей или только один ребенок
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp
        
        # У узла два ребенка: находим наименьший узел в правом поддереве (преемника)
        temp = minValueNode(root.right)
        
        # Копируем значение преемника в текущий узел
        root.val = temp.val
        
        # Удаляем преемника из правого поддерева
        root.right = delete(root.right, temp.val)
    
    return root

def minValueNode(node):
    current = node
    
    # Ищем наименьший узел, проходя влево до упора
    while(current.left is not None):
        current = current.left
    
    return current

# Пример использования
root = None
root = insert(root, 70)
root = insert(root, 50)
root = insert(root, 90)
root = insert(root, 30)
root = insert(root, 60)

print("Обход дерева:")
inorder(root)

# Удаление узла со значением 50
root = delete(root, 50)
print("\nОбход дерева после удаления узла:")
inorder(root)