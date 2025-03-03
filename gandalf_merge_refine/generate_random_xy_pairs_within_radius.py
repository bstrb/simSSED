import random
import math

def generate_xy_pairs(x, y, radius, num_points, decimals=None):
    """
    Generate a specified number of (x, y) pairs uniformly distributed
    within a circle of a given radius around a center (x, y).
    
    Parameters:
        x (float): The x-coordinate of the center.
        y (float): The y-coordinate of the center.
        radius (float): The radius of the circle.
        num_points (int): The number of random points to generate.
        decimals (int, optional): Maximum number of decimals for x and y.
    
    Yields:
        tuple: A tuple (x, y) representing a random point within the circle.
    """
    for _ in range(num_points):
        theta = random.uniform(0, 2 * math.pi)
        r = radius * math.sqrt(random.uniform(0, 1))
        new_x = x + r * math.cos(theta)
        new_y = y + r * math.sin(theta)
        if decimals is not None:
            new_x = round(new_x, decimals)
            new_y = round(new_y, decimals)
        yield (new_x, new_y)

# Example usage:
if __name__ == "__main__":
    center_x, center_y = 512, 512
    radius = 10
    num_points = 100
    decimals = 2  # set maximum decimals to 3
    for point in generate_xy_pairs(center_x, center_y, radius, num_points, decimals):
        print(point)
