import numpy as np
import argparse
import sys

def parse_point(point_str):
    return tuple(map(float, point_str.split(':')))

def great_circle_path(start_point, angle, velocity, num_steps, radius=None):
    num_steps += 1
    start_point = parse_point(start_point)
    r0 = np.array(start_point, dtype=float)
    
    if radius is None:
        radius = np.sqrt(r0[0] * r0[0] + r0[1] * r0[1] + r0[2] * r0[2]) # calculates radius
    if radius == 0:
        exit("Radius cannot be 0")
    r0 = r0 / np.linalg.norm(r0) * radius  # Normalizes initial position vector to the radius
    
    temp_vec = np.array([1.0, 0.0, 0.0]) if abs(r0[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    tangent1 = np.cross(r0, temp_vec)
    tangent1 /= np.linalg.norm(tangent1)
    tangent2 = np.cross(r0, tangent1)
    tangent2 /= np.linalg.norm(tangent2)
    
    v0 = np.cos(angle) * tangent1 + np.sin(angle) * tangent2
    n = np.cross(r0, v0)
    n /= np.linalg.norm(n)
    omega = velocity / radius # omega is the angular velocity
    
    path = []
    for step in range(num_steps):
        t = step * omega
        r_t = np.cos(t) * r0 + np.sin(t) * np.cross(n, r0)
        path.append(tuple(r_t))
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute great circle path.")
    parser.add_argument("start", type=str, help="Starting point in 'x:y:z' format")
    parser.add_argument("angle", type=float, help="Travel direction in radians")
    parser.add_argument("velocity", type=float, help="A constant")
    parser.add_argument("num_steps", type=int, help="Number of steps to compute")
    parser.add_argument("radius", type=float, nargs="?", default=None, help="Optional to increase accuracy")
    
    args = parser.parse_args()
    
    path = great_circle_path(args.start, args.angle, args.velocity, args.num_steps, args.radius)
    output_string = "\n".join(f"{point[0]}:{point[1]}:{point[2]}" for point in path[1:])
    print(output_string)
    computed_output = output_string
