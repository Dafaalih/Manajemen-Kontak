from tabulate import tabulate
import csv

class RedBlackTreeNode:
    def __init__(self, key, value, color, left=None, right=None, parent=None):
        self.key = key  # Nomor telepon sebagai kunci
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self, data_file="kontak.csv"):
        self.NIL = RedBlackTreeNode(None, None, "BLACK")
        self.root = self.NIL
        self.load_from_file(data_file)

    def insert(self, key, value):
        new_node = RedBlackTreeNode(key, value, "RED", self.NIL, self.NIL, self.NIL)
        self._insert_node(self.root, new_node)
        self._fix_insert(new_node)

    def _insert_node(self, root, new_node):
        if root == self.NIL:
            self.root = new_node
        elif new_node.key < root.key:
            if root.left == self.NIL:
                root.left = new_node
                new_node.parent = root
            else:
                self._insert_node(root.left, new_node)
        else:
            if root.right == self.NIL:
                root.right = new_node
                new_node.parent = root
            else:
                self._insert_node(root.right, new_node)

    def _fix_insert(self, node):
        while node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y.color == "RED":
                    node.parent.color = "BLACK"
                    y.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.color == "RED":
                    node.parent.color = "BLACK"
                    y.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)
        self.root.color = "BLACK"

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def search(self, key):
        return self._search(self.root, key, nomor)

    def _search(self, node, key, kontak):
        if kontak:
            if node == self.NIL or key == node.key:
                return node
            if key < node.key:
                return self._search(node.left, key, kontak)
            return self._search(node.right, key, kontak)
        else:
            if node == self.NIL or key.lower() == node.value.lower():
                return node
            left_result = self._search(node.left, key, kontak)
            right_result = self._search(node.right, key, kontak)
            return left_result if left_result != self.NIL else right_result

    def search_and_display(self, key, kontak):
        result = self._search(self.root, key, kontak)
        if result != self.NIL:
            data = self._inorder_traversal(result)
            print(tabulate(data, headers=["Nomor", "Nama"], tablefmt="fancy_grid"))
        else:
            print("Kontak tidak ditemukan.")

    def _inorder_traversal(self, node, descending=False):
        if node != self.NIL:
            left_data = self._inorder_traversal(node.left, descending)
            current_data = [[node.key, node.value]]
            right_data = self._inorder_traversal(node.right, descending)

            if descending:
                return right_data + current_data + left_data
            else:
                return left_data + current_data + right_data
        else:
            return []

    def display_contacts(self, descending=False):
        data = self._inorder_traversal(self.root, descending)
        if data:
            print(tabulate(data, headers=["Nomor", "Nama"], tablefmt="grid"))
        else:
            print("Tidak ada data kontak.")

    def delete(self, key):
        node = self.search(key)
        if node != self.NIL:
            self._delete_node(node)

    def _delete_node(self, node):
        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"

    def save_to_file(self, filename="kontak.csv"):
        data = self._inorder_traversal(self.root)
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Nomor", "Nama"])  # Menulis header
            csv_writer.writerows(data)

    def load_from_file(self, filename="kontak.csv"):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Mengabaikan baris header
                data = [row for row in csv_reader]

            self.root = self.NIL
            for entry in data:
                key, value = entry
                self.insert(key, value)
        except FileNotFoundError:
            print("File tidak ditemukan. Menggunakan data default.")