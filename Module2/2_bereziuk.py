arr = [2, 9, 12, 13, 15, 12, 2, 0, 6, 6, 3, 2]

print("Масив 12 елементів:")
print(" ".join(map(str, arr)))

try:
    n = int(input("Введіть номера елемента масиву: "))

    if n < 0 or n >= len(arr):
        print("Номер виходить за межі масиву.")
    else:
        sub_arr = arr[:n+1]
        
        print(f"Масив {n} елементів:")
        print(" ".join(map(str, sub_arr)))

        is_sorted = all(sub_arr[i] <= sub_arr[i+1] for i in range(len(sub_arr)-1))

        if is_sorted:
            print("впорядковано за зростанням")
        else:
            print("НЕ впорядковано за зростанням")
            
except ValueError:
    print("Будь ласка, введіть коректне ціле число.")