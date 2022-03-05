import datetime
# declare empty list
lst = []
# another empty list for sorted stuff
sorted_lst = []
# declare index
index = 0
# input
string = input("Enter the string of numbers: ")

# start clock
begin = datetime.datetime.now()

# calculate 1000 times
for n in range(0,1000):
    # convert elements in string to int and into list
    for ele in string:
        lst.append(int(ele))

    # arbitrary number in list
    min = lst[0] 

    # sort list
    for i in range(0,len(lst)): 
        if min > lst[i]:
            min = lst[i]
            index = i

# end clock
end = datetime.datetime.now()

# calculate runtime
runtime = (end - begin)/1000

# print output
print("No. of times string has been rotated = ", index)
print("Runtime: ", runtime)



