def textsplit(result):
    pages = []

    #splits texts into segments by punctuation
    result = result.replace('.', '.@*')
    result = result.replace(',', ',@*')
    result = result.replace(';', ';@*')
    result = result.replace('!', '!@*')
    result = result.replace('?', '?@*')
    result = result.replace('\n', '\n@*')
    result = result.split('@*')

    index = 0
    start = 0
    character_count = 0

    #divides text in to pages when over 300 charaters
    while index < len(result):
        character_count += len(result[index])
        if character_count > 300:
            pages.append(result[start:index+1])
            start = index+1
            character_count = 0
        index += 1
    
    if (character_count != 0):
        pages.append(result[start:index])


    #loads swear word list
    text_file = open("./Resources/swearWords.txt", "r")
    swearWords = text_file.read().split('\n')

    polly_pages=[]
    video_pages=[]

    #replaces swear words in text
    for page in pages:
        polly_output=[]
        video_output=[]
        for phrase in page:
            pollytext = phrase
            for word in swearWords:
                phrase = phrase.replace(" "+ word+" ", " "+word[0]+(len(word)-1)*"*"+" ")
                pollytext = pollytext.replace(" "+word+" ", " </beep> ")
            video_output.append(phrase)
            polly_output.append(pollytext)
        video_pages.append(video_output)
        polly_pages.append(polly_output)


    return (video_pages,polly_pages)

