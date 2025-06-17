def sum_even(list):
    sum = 0
    for i in list:
        if i % 2 == 0:
            sum += i
    return sum

input_list = input("Nhập danh sách các số, các số cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))

sum = sum_even(numbers)
print("Tổng các số chẵn trong List là: ", sum)