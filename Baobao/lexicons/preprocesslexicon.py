lexfile = open('lexicons/sentiment_lexicon.txt','r')

lexdata = lexfile.readlines()

lexfile.close()

lexdata = [x.strip() for x in lexdata]

lexdict = {}

for i in range(len(lexdata)):
    input = lexdata[i].split(' ')
    word = input[0][5:]
    intensity = input[1][10:]
    if intensity == 'strong':
        intensity = 1
    else:
        intensity = 0.5
    polarity = input[2][9:]
    if polarity == 'positive':
        polarity = 1
    else:
        polarity = -1
    lexdict[word] = [intensity, polarity]
