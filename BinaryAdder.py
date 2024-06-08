'''
Written by Bonney Seth

This code is for adding together two binary values using boolean operations
'''
#####MODIFY THE CODE BELOW SO IT ADDS THE TWO BINARY VALUES TOGETHER

#Binary values given as strings (to allow for leading 0)
bin1 = '10001011'
bin2 = '01000111'

remainder = 0
tot_out_val = ''

#Loop backwards through the binary string values (I.e., move right to left)
for i in range(len(list(bin1))-1,-1,-1):
    bin_val1 = int(bin1[i])
    bin_val2 = int(bin2[i])
    out_val = 0
    if (bin_val1 and bin_val2) and remainder:
        out_val = 1
        remainder = 1
    elif (bin_val1 and bin_val2) or (bin_val1 and remainder) or (bin_val2 and remainder):
        out_val = 0
        remainder = 1
    elif (bin_val1 or bin_val2) or remainder:
        out_val = 1
        remainder = 0
    elif not((bin_val1 and bin_val2) and remainder):
        out_val = 0
        remainder = 0
    else: 
        print("I don't know what is happening")
    tot_out_val = str(out_val) + tot_out_val 

print(tot_out_val)