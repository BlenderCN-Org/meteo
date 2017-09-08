#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import types

#create image with format (time,x,y)
image = np.random.rand(10,10,10)
image2 = np.random.rand(10,10,10)

#setup figure
fig = plt.figure()
ax1=fig.add_subplot(1,2,1)
ax2=fig.add_subplot(1,2,2)

#set up list of images for animation
ims=[]
for time in range(np.shape(image)[1]):
    im = ax1.imshow(image[time,:,:])
    im2, = ax2.plot(image[0:time,5,5])

    ims.append([im, im2])

#run animation
ani = anim.ArtistAnimation(fig,ims, interval=50,blit=False)
plt.show()
