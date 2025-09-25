my_num = 15
count = 2
my_list = []
try:
    my_var = "hello"
    my_list.append(my_num)
    my_list.pop(count)
    if my_num > 10:
        print("my_num is greater than 10")
    
    elif my_num <=10:
        print("my_num is less than or equal to 10")
except TypeError as e:
    print(f" {e}: my_num is not a number. Please provide a number")
except IndexError as e:
    print(e, f"my_list only has {len(my_list)} element(s). count, {count}, is out of range.")
except Exception as e:
    print(e)
else:
    exponent = my_num**my_num
    print(exponent)
finally:
    print("my_num", my_num, "count", count, "my_list", my_list)