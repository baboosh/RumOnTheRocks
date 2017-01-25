import os
import json

with open("./saves/notes.txt", "w+") as fp:
    longestLine = 0
    fp.write("All saves files in saves" + "\n")
    fp.write("\n")
    for i in os.listdir("./saves/"):
        path = './saves/' + i
        if path.endswith(".json"):
            with open(path) as f:
                config = json.load(f)
                ctime = config["LMT"]

            message = str(i) + " " + str(ctime) + "\n"
            if len(message) > longestLine:
                longestLine = len(message)
            fp.write(message)
    lines = "-" * longestLine
    print(str(longestLine))
    fp.write(lines)

# with open("./saves/notes.txt", "w+") as fp:
#     longestLine = 0
#     for line in fp:
#         print(len(line), line, longestLine)
#         if len(line) > longestLine:
#             longestLine = len(line)

