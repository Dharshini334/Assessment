#open file in read mode
file1 = open("/Users/dharshini/Documents/pythonProjects/Assessment Task1/sentences.txt","r")
output_file = open("/Users/dharshini/Documents/pythonProjects/Assessment Task1/sentence_analysis.txt","w")

#read line by line of the file
# lines = file1.readlines()

#iterate line by line
count=0
for line in file1:
    words = line.split()

    #Skip if there are no words
    if not words:
        continue

    #print sentence
    sentence1 = f"Sentence: {line.strip()}"
    print(sentence1)

    #print word count
    sentence2 = f"Word Count: {len(words)}"
    print(sentence2)
    
    #find longest words and palindromes in each sentence
    max_length = max(len(word) for word in words)
    longest_words=[]
    palindromes=[]
    for word in words:
        if len(word) == max_length:
            longest_words.append(word)
        lower_case = word.lower()
        if lower_case == lower_case[::-1] and len(word)>1:
            palindromes.append(word)

    sentence3 = f"Longest Words: {', '.join(longest_words)}"
    print(sentence3)
    sentence4 = f"Palindromes: {", ".join(palindromes) if palindromes else None}"
    print(sentence4)

    print()

    #Write to the file
    output_text = f"{sentence1}\n{sentence2}\n{sentence3}\n{sentence4}\n\n"
    output_file.write(output_text)

    count+=1

#Closing both files
file1.close()
output_file.close()
