import os
from manajemen_kontak import RedBlackTree
from tabulate import tabulate

if __name__ == "__main__":
    rb_tree = RedBlackTree()
    while True:
        os.system("cls")
        rb_tree.display_contacts(descending=False)
        print("\nMenu:")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Tampilkan Semua Kontak")
        print("4. Hapus Kontak")
        print("5. Edit Kontak")
        print("6. Simpan dan Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            os.system("cls")
            rb_tree.display_contacts(descending=False)
            nama = input("Nama Kontak: ")
            nomor = input("Nomor Kontak: ")
            rb_tree.insert(nama, nomor)

        elif choice == "2":
            os.system("cls")
            print("Mencari kontak... ")
            nama = input("--> ")
            result_node = rb_tree.search_nama(nama)
            if result_node != rb_tree.NIL:
                data = [[node.nama, node.nomor] for node in result_node]
                print(tabulate(data, headers=["Nama", "Nomor"], tablefmt='fancy_grid'))
            else:
                print(f"\nNilai '{nama}' tidak ditemukan dalam data.")

            input("\nTekan enter untuk kembali ke menu")
                
        elif choice == "3":
            os.system("cls")
            print("Tampilkan Berdasarkan")
            print("1. Ascending")
            print("2. Descending")
            pilih = input(">> ")
            if pilih == "1":
                rb_tree.display_contacts(descending=False)
                input("\nTekan enter untuk kembali ke menu")
            elif pilih == "2":
                rb_tree.display_contacts(descending=True)
                input("\nTekan enter untuk kembali ke menu")

        elif choice == "4":
            os.system("cls")
            rb_tree.display_contacts(descending=False)
            nama = input("Masukkan nama untuk menghapus kontak: ")
            rb_tree.delete(nama)

        elif choice == "5":
            rb_tree.display_contacts(descending=False)
            nomor = input("Masukkan nomor untuk mengedit kontak: ")
            new_nomor = input("Masukkan nomor baru: ")
            new_nama = input("Masukkan nama baru: ")
            rb_tree.edit_contact(nomor, new_nomor, new_nama)

        elif choice == "6":
            konfirmasi = input("Apakah anda yakin ingin menyimpan perubahan ? (y/n)")
            if konfirmasi == "y":
                filename = "kontak.csv"
                rb_tree.save_to_file(filename)
                print("Data berhasil disimpan ke file.")
                break
            elif konfirmasi == "n":
                print("Kembali ke menu")
                continue
            else:
                print("Invalid Input!")

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")