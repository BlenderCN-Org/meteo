#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig2 = plt.figure()

x = np.arange(-39, 40)
y = np.arange(-39, 40).reshape(-1, 1)
base = np.hypot(x, y)

ims = []
for add in np.arange(60):
    ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 120)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=30, repeat_delay=60, blit=True)

plt.show()
