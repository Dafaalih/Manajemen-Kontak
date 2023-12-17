from tabulate import tabulate
import csv

class RedBlackTreeNode:
    def __init__(self, nama, nomor, color, left=None, right=None, parent=None):
        self.nama = nama
        self.nomor = nomor
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self, data_file="kontak.csv"):
        self.NIL = RedBlackTreeNode(None, None, "BLACK")
        self.root = self.NIL
        self.load_from_file(data_file)

    def insert(self, nama, nomor):
        new_node = RedBlackTreeNode(nama, nomor, "RED", self.NIL, self.NIL, self.NIL)
        existing_node = self.search(nama)

        if existing_node != self.NIL:
            print(f"Kontak dengan nama '{nama}' sudah ada.")
            print("1. Tambah kontak dengan nama yang berbeda")
            print("2. Ganti nomor kontak yang sudah ada")
            choice = input("Pilih opsi (1/2): ")

            if choice == "1":
                print("Ganti nama yang berbeda")
                nama = input("==> ")
                self.insert(nama, nomor)
            elif choice == "2":
                existing_node.nomor = nomor
                print(f"Nomor kontak dengan nama '{nama}' berhasil diubah.")
            else:
                print("Pilihan tidak valid. Kontak tidak ditambahkan.")

        else:
            self._insert_node(self.root, new_node)
            self._fix_insert(new_node)
            print(f"Kontak dengan nama '{nama}' berhasil ditambahkan.")

    def _insert_node(self, root, new_node):
        if root == self.NIL:
            self.root = new_node
        elif new_node.nama < root.nama:
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
            # Kasus 1: Orang tua adalah kiri dari kakek
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                # Kasus 1a: Paman (y) adalah merah
                if y.color == "RED":
                    node.parent.color = "BLACK"
                    y.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    # Kasus 1b: Node adalah anak kanan
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    # Kasus 1c: Node adalah anak kiri
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
            else:
                # Kasus 2: Orang tua adalah kanan dari kakek
                y = node.parent.parent.left
                # Kasus 2a: Paman (y) adalah merah
                if y.color == "RED":
                    node.parent.color = "BLACK"
                    y.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    # Kasus 2b: Node adalah anak kiri
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    # Kasus 2c: Node adalah anak kanan
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)
        # Kasus 3: Akar selalu hitam
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

    def search_nama(self, nama):
        result_list = []
        self._search_helper(self.root, nama, result_list)
        return result_list

    def _search_helper(self, node, nama, result_list):
        if node != self.NIL:
            self._search_helper(node.left, nama, result_list)
            if nama.lower() in node.nama.lower():
                result_list.append(node)
            self._search_helper(node.right, nama, result_list)

    def search(self, nama):
        return self._search(self.root, nama)

    def _search(self, node, nama):
        if node == self.NIL or nama == node.nama:
            return node
        if nama < node.nama:
            return self._search(node.left, nama)
        return self._search(node.right, nama)

    def _inorder_traversal(self, node, descending=False):
        if node != self.NIL:
            left_data = self._inorder_traversal(node.left, descending)
            current_data = [[node.nama, node.nomor]]
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
            print(tabulate(data, headers=["Nama", "Nomor"], tablefmt="fancy_grid"))
        else:
            print("Tidak ada data kontak.")

    def delete(self, nama):
        node = self.search(nama)
        if node != self.NIL:
            self._delete_node(node)
        else:
            print(f"Kontak dengan nama {nama} tidak ditemukan.")

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
                # Kasus 1: Sibling (w) adalah MERAH
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                # Kasus 2: Kedua anak dari sibling adalah HITAM
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    # Kasus 3: Anak kanan dari sibling adalah HITAM
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right
                    # Kasus 4: Sibling dan anak-anaknya adalah HITAM
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

    def edit_contact(self, nama, new_nomor, new_nama):
        node_to_edit = self.search(nama)

        if node_to_edit != self.NIL:
            node_to_edit.nomor = new_nomor
            node_to_edit.nama = new_nama
            print(f"Kontak dengan nama {nama} telah diedit.")
        else:
            print(f"Kontak dengan nama {nama} tidak ditemukan.")

    def save_to_file(self, filename="kontak.csv"):
        data = self._inorder_traversal(self.root)
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Nama", "Nomor"])
            csv_writer.writerows(data)

    def load_from_file(self, filename="kontak.csv"):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  
                data = [row for row in csv_reader]

            self.root = self.NIL
            for entry in data:
                nama, value = entry
                self.insert(nama, value)
        except FileNotFoundError:
            print("File tidak ditemukan. Menggunakan data default.")