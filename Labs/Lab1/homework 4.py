#homework 4

#reading the file
def decode(Message):
    with open(Message, 'r') as f:
        lines = f.readlines()

#divide the lines into a dictionary
    message_dict = {}
    for line in lines:
        number, word = line.split()
        message_dict[int(number)] = word

#determine th end of each pyramid layer
    pyramid = []  
    n = 1
    while n * (n + 1) // 2 <= max(message_dict.keys()):
        pyramid.append(n * (n + 1) // 2)
        n += 1

#extract the words from the last word of each layer
    decoded_message =  [message_dict[end] for end in pyramid]
    return ' '.join(decoded_message) 

decoded_message = decode('Message.txt')
print(decoded_message)


