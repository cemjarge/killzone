import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DraggablePoints:
    def __init__(self, scatter, line, rect1, rect2, rect3):
        self.scatter = scatter
        self.line = line
        self.rect1 = rect1
        self.rect2 = rect2
        self.rect3 = rect3
        self.dragging_point = None
        self.fig = scatter.figure
        self.ax = scatter.axes

        # Connect the events to their respective methods
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.scatter.axes: return

        # Find the closest point to the mouse click
        contains, attr = self.scatter.contains(event)
        if not contains: return

        ind = attr['ind'][0]
        self.dragging_point = ind

    def on_motion(self, event):
        if self.dragging_point is None: return
        if event.inaxes != self.scatter.axes: return

        # Keep the x-coordinate fixed and only update the y-coordinate
        x, _ = self.scatter._offsets[self.dragging_point]
        y = event.ydata
        self.scatter._offsets[self.dragging_point] = [x, y]

        # Update the line connecting the points
        self.line.set_data(self.scatter.get_offsets().T)

        # Update the bounding boxes around the points
        self.update_rectangle(self.rect1, 0, 4)  # Update first rectangle (around points 1-4)
        self.update_rectangle(self.rect2, 4, 8)  # Update second rectangle (around points 2-5)
        self.update_rectangle(self.rect3, 8, 12)  # Update second rectangle (around points 2-5)

        self.fig.canvas.draw_idle()

    def on_release(self, event):
        self.dragging_point = None

    def update_rectangle(self, rect, start_idx, end_idx):
        # Get the points within the specified index range
        points = self.scatter._offsets[start_idx:end_idx]
        x_min = points[:, 0].min()
        x_max = points[:, 0].max()
        y_min = points[:, 1].min()
        y_max = points[:, 1].max()

        # Update the rectangle's position and size
        rect.set_bounds(x_min, y_min, x_max - x_min, y_max - y_min)


# Example usage
x = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14]
y = [-1, 2, -2, 1, -3, -7, -1, -2, 1, -3, 7, 3]

fig, ax = plt.subplots()
scatter = ax.scatter(x, y)
line, = ax.plot(x, y, 'b-')  # Create the line connecting the points

# Create the first rectangle around the first 4 points (points 1-4)
rect1 = patches.Rectangle((min(x[:4]), min(y[:4])), 
                          max(x[:4]) - min(x[:4]), 
                          max(y[:4]) - min(y[:4]), 
                          linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect1)

# Create the second rectangle around the next 4 points (points 5-8)
rect2 = patches.Rectangle((min(x[4:8]), min(y[4:8])), 
                          max(x[4:8]) - min(x[4:8]), 
                          max(y[4:8]) - min(y[4:8]), 
                          linewidth=1, edgecolor='g', facecolor='none')
ax.add_patch(rect2)

# Create the third rectangle around the next 4 points (points 9-12)
rect3 = patches.Rectangle((min(x[8:12]), min(y[8:12])), 
                          max(x[8:12]) - min(x[8:12]), 
                          max(y[8:12]) - min(y[8:12]), 
                          linewidth=1, edgecolor='b', facecolor='none')
ax.add_patch(rect3)

draggable = DraggablePoints(scatter, line, rect1, rect2, rect3)

plt.show()
