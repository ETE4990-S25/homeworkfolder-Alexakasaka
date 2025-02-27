def decode(message_file):
    # Read the content of the file
    with open(message_file, 'r') as file:
        lines = file.readlines()
    
    # Parse the lines into a dictionary
    message_dict = {}
    for line in lines:
        number, word = line.split()
        message_dict[int(number)] = word
    
    # Determine the end of each pyramid line
    pyramid_ends = []
    n = 1
    while n * (n + 1) // 2 <= max(message_dict.keys()):
        pyramid_ends.append(n * (n + 1) // 2)
        n += 1
    
    # Extract the words corresponding to the end of each pyramid line
    decoded_message = [message_dict[end] for end in pyramid_ends]
    
    # Join the words to form the final message
    return ' '.join(decoded_message)

# Test the function with the provided file
decoded_message = decode('Message.txt')
print(decoded_message)