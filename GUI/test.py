dir = "/Users/felipebautista/Workspaces/sdmay23-16/sdmay23-16/GUI/log.txt"

words = ["connection", "Labels"]



def search_word(dir,word,file):
    with open(dir, 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        for line in lines:
            # check if string present on a current line
            if line.find(word) != -1:
                
                file += line + '\n'
        print(file)

output = ""

for word in words:
    search_word(dir,word,output)
    print(output)

