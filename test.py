new_path = "C://Users//agyekume//Videos//INC2_21.mkv"

paths = new_path.split("//")
last_path = paths[-1].split(".")
filename = last_path[0]
if "_" in filename:
    filenum = filename[filename.index("_")+1:]
    new_filename = filename.replace(filenum, str(int(filenum)+1))
    new_path = new_path.replace(filename, new_filename)
else:
    new_filename = filename + "_1"
    new_path = new_path.replace(filename, new_filename)

print(new_path)
print("")