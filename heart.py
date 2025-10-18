import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Name to display
name = "Areeb"

# Create figure
fig, ax = plt.subplots(figsize=(6, 6))
fig.set_facecolor("black")
ax.set_facecolor("black")
ax.axis("off")

# Heart parametric equation
t = np.linspace(0, 2 * np.pi, 500)
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

# Initialize line and fill
line, = ax.plot([], [], color="red", linewidth=2)
fill = ax.fill([], [], color="red", alpha=0.3)[0]

# Name text (start invisible)
text = ax.text(0, -1.5, name, fontsize=24, ha='center', va='center',
               color='white', fontweight='bold', fontfamily='serif', alpha=0)

# Set plot limits
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)

# Animation update function
def update(frame):
    if frame < len(x):
        # Draw partial heart line
        line.set_data(x[:frame], y[:frame])
    else:
        # Fill heart fully and fade in name
        fill.set_xy(np.column_stack([x, y]))
        text.set_alpha((frame - len(x)) / 50)  # Fade-in effect

    return line, fill, text

# Frames: heart drawing + name fade
total_frames = len(x) + 50
ani = FuncAnimation(fig, update, frames=total_frames, interval=15, blit=True)

plt.show()
