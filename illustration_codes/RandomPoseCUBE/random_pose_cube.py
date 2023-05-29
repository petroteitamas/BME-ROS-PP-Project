import numpy as np
import random as rnd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import random
import math
import numpy as np


def cube_spawning_coordinates(how_many_cubes, workspace_size_x, workspace_size_y, cube_size, gripper_finger_needed_space):
  needed_radius_for_one_cube=math.sqrt(2)*cube_size/2+gripper_finger_needed_space

  list_of_coordinate_pairs=list()
  x,y = np.zeros(how_many_cubes),np.zeros(how_many_cubes)
  x[0],y[0]=np.round(rnd.uniform(0,workspace_size_x)),np.round(rnd.uniform(0, workspace_size_y))
  list_of_coordinate_pairs.append((int(x[0]),int(y[0])))

  min_distances=[]
  i=1

  while i<how_many_cubes :
      x_temp,y_temp=np.round(rnd.uniform(0,workspace_size_x)),np.round(rnd.uniform(0,workspace_size_y))
      distances = []

      for j in range(0,i):
          distances.append(np.sqrt((x_temp-x[j])**2+(y_temp-y[j])**2))
      min_distance = np.min(distances)

      if min_distance>2*needed_radius_for_one_cube:
          min_distances.append(min_distance)
          x[i]=x_temp
          y[i]=y_temp
          list_of_coordinate_pairs.append((int(x[i]),int(y[i])))
          i = i+1

  #print(list_of_coordinate_pairs)


  colors=['r', 'g', 'b']
  list_with_features=list()

  for element in list_of_coordinate_pairs:
    random.shuffle(colors)
    picked_color=colors[0]

    orientation=rnd.uniform(0,360)

    actual_item=list()
    actual_item.append(element)
    actual_item.append(round(np.deg2rad(orientation),2))
    actual_item.append(picked_color)

    list_with_features.append(actual_item)

    circle = plt.Circle(element, radius=needed_radius_for_one_cube, color=picked_color)
    fig = plt.gcf()
    ax = fig.gca()
    ax.add_patch(circle)


    def plot_rotated_square(center, cube_size, rotated_angle):
        # Calculate the coordinates of the rectangle corners
        corners = np.array([
            [-cube_size/2, -cube_size/2],  # Bottom-left
            [cube_size/2, -cube_size/2],   # Bottom-right
            [cube_size/2, cube_size/2],    # Top-right
            [-cube_size/2, cube_size/2]    # Top-left
        ])

        # Convert the angle to radians
        theta = np.radians(rotated_angle)

        # Create a rotation matrix
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])

        # Rotate the corners around the center
        rotated_corners = np.dot(corners, rotation_matrix.T) + center

        # Plot the rotated square
        plt.fill(rotated_corners[:, 0], rotated_corners[:, 1], color='white')


    plot_rotated_square(element, cube_size, orientation)


    plt.scatter(element[0], element[1], color='black', s=cube_size/4)


  ax.set_aspect('equal', adjustable='box')
  plt.xlim(-workspace_size_x/10, workspace_size_x*1.2)
  plt.ylim(-workspace_size_y/10, workspace_size_x*1.2)
  print("The location of cubes:")
  plt.show()

  print("The list of the features of cubes:")

  return list_with_features


#TODO: eltolás + rescaling a munkatér-koordináta rendszerbe
def transform_to_real_coordinates():
  return


cube_spawning_coordinates(6, 400, 400, 30, 15)