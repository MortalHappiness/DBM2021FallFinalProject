import glob

n = int(input("n = "))
memory = [0] * n

for file in glob.glob("*.txt"):
    print(file)
