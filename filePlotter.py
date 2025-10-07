# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
import math
from typing import List, Tuple
from utilities import FileReader

def plot_errors(filename):
    headers, values=FileReader(filename).read_file() 
    time_list=[]
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    for i in range(0, len(headers) - 1):
        plt.plot(time_list, [lin[i] for lin in values], label= headers[i]+ " linear")
    
    #plt.plot([lin[0] for lin in values], [lin[1] for lin in values])
    plt.legend()
    plt.grid()
    plt.show()


def _read_simple_csv(filename: str) -> Tuple[List[str], List[List[float]]]:
    # Helper function to read CSV files using the utilities module
    headers, values = FileReader(filename).read_file()
    return headers, values


def plot_imu(filename: str):
    # Plot IMU accelerometer and gyroscope data vs time
    headers, rows = _read_simple_csv(filename)
    if len(headers) < 4:
        raise ValueError("IMU file must contain acc_x, acc_y, angular_z, stamp")

    # Convert timestamps from nanoseconds to seconds
    t0 = rows[0][-1]
    t = [(r[-1] - t0) / 1e9 for r in rows]  # seconds
    acc_x = [r[0] for r in rows]
    acc_y = [r[1] for r in rows]
    ang_z = [r[2] for r in rows]

    plt.figure()
    plt.plot(t, acc_x, label='acc_x (m/s^2)')
    plt.plot(t, acc_y, label='acc_y (m/s^2)')
    plt.plot(t, ang_z, label='angular_z (rad/s)')
    plt.xlabel('Time (s)')
    plt.ylabel('IMU values')
    plt.title('IMU Measurements vs Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_odometry(filename: str):
    # Plot odometry data: trajectory and time series
    headers, rows = _read_simple_csv(filename)
    if len(headers) < 4:
        raise ValueError("Odometry file must contain x, y, th, stamp")

    x_vals = [r[0] for r in rows]
    y_vals = [r[1] for r in rows]
    th_vals = [r[2] for r in rows]
    t0 = rows[0][-1]
    t_sec = [(r[-1] - t0) / 1e9 for r in rows]

    # First plot: x-y trajectory
    plt.figure()
    plt.plot(x_vals, y_vals, label='trajectory')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Odometry Trajectory (x-y)')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Second plot: x, y, theta vs time
    plt.figure()
    plt.plot(t_sec, x_vals, label='x (m)')
    plt.plot(t_sec, y_vals, label='y (m)')
    plt.plot(t_sec, th_vals, label='yaw th (rad)')
    plt.xlabel('Time (s)')
    plt.ylabel('Odometry values')
    plt.title('Odometry vs Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def _parse_laser_line(line: str):
    # Parse laser scan data from CSV format: array('f', [ranges]), angle_increment, stamp
    # Extract ranges list between '[' and the matching ']'
    start = line.find('[')
    end = line.rfind(']')
    if start == -1 or end == -1 or end < start:
        raise ValueError('Malformed laser line: cannot find ranges list')

    ranges_str = line[start+1:end]
    # Convert to list of floats without literal_eval; handle 'inf' and 'nan' strings
    ranges: List[float] = []
    for tok in ranges_str.split(','):
        t = tok.strip()
        if t == '' or t.lower() == 'nan':
            # Convert nan strings to actual NaN values
            ranges.append(float('nan'))
            continue
        if t.lower() in ('inf', '+inf', 'infinity', '+infinity'):
            ranges.append(float('inf'))
            continue
        if t.lower() in ('-inf', '-infinity'):
            ranges.append(float('-inf'))
            continue
        try:
            ranges.append(float(t))
        except Exception:
            # Skip any non-numeric artifacts
            continue

    # Parse remaining fields after the ranges list
    remainder = line[end+1:]
    # Strip leading ")" and spaces
    remainder = remainder.lstrip()  
    if remainder.startswith(')'):
        remainder = remainder[1:]
    remainder = remainder.lstrip()
    # Extract angle_increment and timestamp from remaining comma-separated values
    nums: List[float] = []
    for part in remainder.split(','):
        s = part.strip()
        if s == '':
            continue
        try:
            nums.append(float(s))
            if len(nums) >= 2:
                break
        except Exception:
            continue
    if len(nums) < 2:
        raise ValueError('Malformed laser line: expected angle_increment and stamp')
    angle_increment, stamp_ns = nums[0], nums[1]
    return ranges, angle_increment, stamp_ns


def plot_all_odometry(line_file: str, circle_file: str, spiral_file: str):
    # Plot all three motion trajectories (line, circle, spiral) on one graph for comparison
    plt.figure()
    
    # Plot line trajectory
    headers, rows = _read_simple_csv(line_file)
    x_vals = [r[0] for r in rows]
    y_vals = [r[1] for r in rows]
    plt.plot(x_vals, y_vals, label='line', linewidth=2)
    
    # Plot circle trajectory
    headers, rows = _read_simple_csv(circle_file)
    x_vals = [r[0] for r in rows]
    y_vals = [r[1] for r in rows]
    plt.plot(x_vals, y_vals, label='circle', linewidth=2)
    
    # Plot spiral trajectory
    headers, rows = _read_simple_csv(spiral_file)
    x_vals = [r[0] for r in rows]
    y_vals = [r[1] for r in rows]
    plt.plot(x_vals, y_vals, label='spiral', linewidth=2)
    
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('All Odometry Trajectories Comparison')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_laser_cartesian(filename: str, row_index: int = 2, angle_min: float = 0.0):
    # Plot a single laser scan row converted from polar to Cartesian coordinates
    # Read header then iterate to the desired row
    with open(filename, 'r') as f:
        header_line = f.readline()  # skip header
        for i, line in enumerate(f):
            if i == row_index:
                data_line = line.strip()
                break
        else:
            raise IndexError('Requested row_index out of range')

    ranges, angle_increment, _ = _parse_laser_line(data_line)

    # Convert polar coordinates to Cartesian, filtering out invalid ranges
    xs = []
    ys = []
    for i, r in enumerate(ranges):
        try:
            r_val = float(r)
        except Exception:
            continue
        # Skip NaN, Inf, and non-positive ranges
        if not math.isfinite(r_val) or r_val <= 0.0:
            continue
        theta = angle_min + i * angle_increment
        xs.append(r_val * math.cos(theta))
        ys.append(r_val * math.sin(theta))

    plt.figure()
    plt.scatter(xs, ys, s=5, label=f'scan row {row_index}')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Laser Scan Cartesian (single row)')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
import argparse

if __name__=="__main__":
    # Command line interface for sensor data plotting
    parser = argparse.ArgumentParser(description='Plot sensor logs')
    sub = parser.add_subparsers(dest='mode', required=True)

    # IMU plotting subcommand
    p_imu = sub.add_parser('imu', help='Plot IMU log (acc_x, acc_y, angular_z vs time)')
    p_imu.add_argument('--file', required=True, help='IMU CSV file')

    # Odometry plotting subcommand
    p_odom = sub.add_parser('odom', help='Plot Odometry trajectory (x-y)')
    p_odom.add_argument('--file', required=True, help='Odometry CSV file')

    # Laser scan plotting subcommand
    p_laser = sub.add_parser('laser', help='Plot Laser scan (one row) in Cartesian')
    p_laser.add_argument('--file', required=True, help='Laser CSV file')
    p_laser.add_argument('--row', type=int, default=2, help='Row index to plot (default: 2 = 3rd row)')
    p_laser.add_argument('--angle-min', type=float, default=0.0, help='Assumed angle_min in radians (default: 0.0)')

    # Combined odometry plotting subcommand
    p_all_odom = sub.add_parser('all-odom', help='Plot all three odometry trajectories (line, circle, spiral)')
    p_all_odom.add_argument('--line-file', required=True, help='Line odometry CSV file')
    p_all_odom.add_argument('--circle-file', required=True, help='Circle odometry CSV file')
    p_all_odom.add_argument('--spiral-file', required=True, help='Spiral odometry CSV file')
    
    args = parser.parse_args()

    # Execute the appropriate plotting function based on mode
    if args.mode == 'imu':
        plot_imu(args.file)
    elif args.mode == 'odom':
        plot_odometry(args.file)
    elif args.mode == 'laser':
        plot_laser_cartesian(args.file, row_index=args.row, angle_min=args.angle_min)
    elif args.mode == 'all-odom':
        plot_all_odometry(args.line_file, args.circle_file, args.spiral_file)
