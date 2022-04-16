import glob
import re

var_array = []
for file in glob.glob("./**/*.dm", recursive=True):
    # I want to record all variable instances into an array called var_array
    with open(file, "r", encoding="utf-8") as f:
        info = []
        for line in f.readlines():
            search = re.search(r"^/*var/(global/|)list/([a-zA-Z_/]+)/+([a-zA-Z_]+) = (.*)", line)
            if search is None:
                info.append(line)
                continue
            var_array.append(search.group(3))
            if(search.group(2) == "global"):
                info.append(line)
                continue
            info.append("GLOBAL_LIST_INIT_TYPED({}, /{}, {})".format(search.group(3), search.group(2), search.group(4)))

        with open(file, "w", encoding="utf-8") as f:
            f.write("".join(info))

for file in glob.glob("./**/*.dm", recursive=True):
    # I want to record all variable instances into an array called var_array
    with open(file, "r", encoding="utf-8") as f:
        info = f.read()
        for data in var_array:
            info = re.sub(r"([\. \[\]])("+re.escape(data)+r")([\.\[\] ])", "$1GLOB.$2$3", info)
        with open(file, "w", encoding="utf-8") as f:
            f.write(info)
