import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists

# set input and output files

Fname = "speech.txt"
#OutputFname = sys.argv[2]

#make sure text files exist
if not os.path.exists(Fname):
    print ("text file input %s doesn't exist! Exiting" % textFname)
    exit()

file = open(Fname,"r")
outfile = open("output.txt", "w+")

if file.mode == 'r':
    contents = file.read()
file.close()

file_as_list = re.split('[ ?,.!:;"\n-]',contents)
words = [word.strip() for word in file_as_list]
words.sort(key = lambda x: x.lower())
output = {}

for w in words:
    num =  words.count(w)
    output[w] = num

for w,n in output.items():
    outfile.write(w + " ")
    outfile.write(str(n))
    outfile.write("\n")


#print(output)

outfile.close()