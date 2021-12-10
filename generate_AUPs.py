import os, random, shutil

pdf_files = os.listdir("./AUPs/PDF")
html_files = os.listdir("./AUPs/HTML")
files = [os.path.join("./AUPs/PDF", f) for f in pdf_files]
files.extend([os.path.join("./AUPs/HTML", f) for f in html_files])

subset = random.sample(files, int(0.8 * len(files)))
print(subset)
random.shuffle(subset)
print(subset)
print(len(subset))
with open("AUPs.txt", "w") as outfile:
    for file in subset:
        print(file)
        with open(file, "r") as f:
            outfile.write(f.read())

test_files = [f for f in files if f not in subset]
try:
    os.mkdir("test_aups")
except FileExistsError:
    for f in os.listdir("./test_aups"):
        os.remove("./test_aups/" + f)
for f in test_files:
    shutil.copy(f, "./test_aups")
