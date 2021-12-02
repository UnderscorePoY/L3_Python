import imageio
import os

folder = r'C:\Users\thoma\Documents\MEGAsync\Cours\Maths\10_1_ALN\Projet'
gif_original = folder+"/"+'EulerImplicite_CFL502.gif'
gif_speed_up = folder+"/"+'EulerImplicite_CFL502_fast.gif'
dur = 0.02

print(gif_original)
print(os.path.isfile(gif_original))

gif = imageio.mimread(gif_original, memtest=False)

imageio.mimsave(gif_speed_up, gif, duration=0.02)
