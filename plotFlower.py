from skimage import io
import os
import shutil
import matplotlib.pyplot as plt

randFlowerFile = "flower1_1111_1.png"
dirPath = os.getcwd()
randomFlower = io.imread(dirPath+"/images/"+randFlowerFile)

plt.figure(figsize=(4, 4))
plt.imshow(randomFlower, cmap='gray')
plt.axis('off')
plt.show()