input = raw_input('Please enter some text: ')

dic = {}
dic.clear()

for i in range(len(input)):
    char = input[i:i+1]
    dic[char] = 1 + dic.get(char, 0)

print ' Text has been analyzed'
print 'Please enter the letter for its occurance or click escape to end the program'



