import imageio
from os import listdir
from os.path import isfile, join

folder = r'C:\Users\thoma\Documents\MEGAsync\Cours\Maths\10_1_ALN\Projet'
img_folder = folder+r"\gif"

files = [f for f in listdir(img_folder) if isfile(join(img_folder, f))]
print(files)

with imageio.get_writer(folder+r"\anim2.gif", mode="I") as writer:
    for file in files:
        image = imageio.imread(img_folder+"/"+file)
        writer.append_data(image)
