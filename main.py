from manajemen_kontak import RedBlackTree

if __name__ == "__main__":
    rb_tree = RedBlackTree()

    while True:
        print("\nMenu:")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Tampilkan Semua Kontak")
        print("4. Hapus Kontak")
        print("5. Edit Kontak")
        print("6. Simpan Data ke File")
        print("0. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            rb_tree.display_contacts(descending=False)
            nomor = input("Nomor Kontak: ")
            nama = input("Nama Kontak: ")
            rb_tree.insert(nomor, nama)
        elif choice == "2":
            print("Mencari kontak berdasarkan")
            print("[1] Nomor")
            print("[2] Nama")
            pili = input("--> ")
            if pili == "1":
                nomor = input("Masukkan nomor untuk mencari kontak: ")
                rb_tree.search_and_display(nomor, kontak = True)
            elif pili == "2":
                nama = input("Masukkan nama untuk mencari kontak: ")
                rb_tree.search_and_display(nama, kontak = False)
                
        elif choice == "3":
            print("Tampilkan Berdasarkan")
            print("1. Ascending")
            print("1. Descending")
            pilih = input(">> ")
            if pilih == "1":
                rb_tree.display_contacts(descending=False)
            elif pilih == "2":
                rb_tree.display_contacts(descending=True)
        elif choice == "4":
            rb_tree.display_contacts(descending=False)
            nomor = input("Masukkan nomor untuk menghapus kontak: ")
            rb_tree.delete(nomor)
        elif choice == "5":
            rb_tree.display_contacts(descending=False)
            nomor = input("Masukkan nomor untuk mengedit kontak: ")
            result = rb_tree.search(nomor)
            if result != rb_tree.NIL:
                new_nama = input("Masukkan nama baru: ")
                result.value = new_nama
                print("Kontak diedit.")
            else:
                print("Kontak tidak ditemukan.")
        elif choice == "6":
            konfirmasi = input("Apakah anda yakin ingin menyimpan perubahan ? (y/n)")
            if konfirmasi == "y":
                filename = "kontak.csv"
                rb_tree.save_to_file(filename)
                print("Data disimpan ke file.")
            elif konfirmasi == "n":
                print("Kembali ke menu")
                continue
            else:
                print("Invalid Input!")
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")