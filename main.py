# titik awal program
from controllers.user_controller import register_user, login_user
from views.user_view import register_menu, login_menu

while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Keluar")
    pilihan = input("Pilih menu: ")
    
    if pilihan == "1":
        username, password = register_menu()
        register_user(username, password)
    elif pilihan == "2":
        username, password = login_menu()
        login_user(username, password)
    elif pilihan == "3":
        break
    else:
        print("Pilihan tidak valid.")
        