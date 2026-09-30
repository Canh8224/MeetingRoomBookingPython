from database import engine

try:
    with engine.connect() as connection:
        print("Ket noi MySQL thanh cong!")
except Exception as e:
    print("Ket noi that bai!")
    print(e)