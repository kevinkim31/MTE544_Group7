import matplotlib.pyplot as plt
from utilities import FileReader


def plot_linear_errors(filename):
    """
    Generate plots for linear errors:
    - e vs t and e_dot vs t (combined)
    - e vs e_dot
    """
    headers, values = FileReader(filename).read_file()
    
    # Extract data columns
    e_list = [row[0] for row in values]
    e_dot_list = [row[1] for row in values]
    e_int_list = [row[2] for row in values]
    
    # Calculate time from timestamps (convert nanoseconds to seconds)
    time_list = []
    first_stamp = values[0][-1]
    for val in values:
        time_list.append((val[-1] - first_stamp) / 1e9)
    
    # Figure 1: e and e_dot vs t
    fig1 = plt.figure(figsize=(10, 6))
    plt.plot(time_list, e_list, 'b-', linewidth=2, marker='o', markersize=3, 
             markevery=max(1, len(time_list)//20), label='e (error)', alpha=0.8)
    plt.plot(time_list, e_dot_list, 'r--', linewidth=2, marker='s', markersize=3, 
             markevery=max(1, len(time_list)//20), label='e_dot (error derivative)', alpha=0.8)
    plt.xlabel('Time (s)', fontsize=12, fontweight='bold')
    plt.ylabel('Error Value', fontsize=12, fontweight='bold')
    plt.title('Linear Error and Derivative vs Time', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Figure 2: e vs e_dot (phase plot)
    fig2 = plt.figure(figsize=(10, 6))
    plt.plot(e_list, e_dot_list, 'g-', linewidth=2, marker='^', markersize=3, 
             markevery=max(1, len(e_list)//20), label='Phase trajectory', alpha=0.8)
    plt.scatter(e_list[0], e_dot_list[0], c='lime', s=100, marker='o', 
               edgecolors='black', linewidths=2, label='Start', zorder=5)
    plt.scatter(e_list[-1], e_dot_list[-1], c='red', s=100, marker='X', 
               edgecolors='black', linewidths=2, label='End', zorder=5)
    plt.xlabel('e (linear error)', fontsize=12, fontweight='bold')
    plt.ylabel('e_dot (linear error derivative)', fontsize=12, fontweight='bold')
    plt.title('Linear Error Phase Plot (e vs e_dot)', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.show()


def plot_angular_errors(filename):
    """
    Generate plots for angular errors:
    - e vs t and e_dot vs t (combined)
    - e vs e_dot
    """
    headers, values = FileReader(filename).read_file()
    
    # Extract data columns
    e_list = [row[0] for row in values]
    e_dot_list = [row[1] for row in values]
    e_int_list = [row[2] for row in values]
    
    # Calculate time from timestamps (convert nanoseconds to seconds)
    time_list = []
    first_stamp = values[0][-1]
    for val in values:
        time_list.append((val[-1] - first_stamp) / 1e9)
    
    # Figure 1: e and e_dot vs t
    fig1 = plt.figure(figsize=(10, 6))
    plt.plot(time_list, e_list, 'b-', linewidth=2, marker='o', markersize=3, 
             markevery=max(1, len(time_list)//20), label='e (error)', alpha=0.8)
    plt.plot(time_list, e_dot_list, 'r--', linewidth=2, marker='s', markersize=3, 
             markevery=max(1, len(time_list)//20), label='e_dot (error derivative)', alpha=0.8)
    plt.xlabel('Time (s)', fontsize=12, fontweight='bold')
    plt.ylabel('Error Value', fontsize=12, fontweight='bold')
    plt.title('Angular Error and Derivative vs Time', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Figure 2: e vs e_dot (phase plot)
    fig2 = plt.figure(figsize=(10, 6))
    plt.plot(e_list, e_dot_list, 'g-', linewidth=2, marker='^', markersize=3, 
             markevery=max(1, len(e_list)//20), label='Phase trajectory', alpha=0.8)
    plt.scatter(e_list[0], e_dot_list[0], c='lime', s=100, marker='o', 
               edgecolors='black', linewidths=2, label='Start', zorder=5)
    plt.scatter(e_list[-1], e_dot_list[-1], c='red', s=100, marker='X', 
               edgecolors='black', linewidths=2, label='End', zorder=5)
    plt.xlabel('e (angular error)', fontsize=12, fontweight='bold')
    plt.ylabel('e_dot (angular error derivative)', fontsize=12, fontweight='bold')
    plt.title('Angular Error Phase Plot (e vs e_dot)', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.show()


def plot_pose_vs_time(filename):
    """
    Generate plot for robot pose vs time:
    - x, y, theta vs t (all in one plot)
    """
    headers, values = FileReader(filename).read_file()
    
    # Extract data columns
    x_list = [row[0] for row in values]
    y_list = [row[1] for row in values]
    theta_list = [row[2] for row in values]
    
    # Calculate time from timestamps (convert nanoseconds to seconds)
    time_list = []
    first_stamp = values[0][-1]
    for val in values:
        time_list.append((val[-1] - first_stamp) / 1e9)
    
    # Figure: x, y, theta vs t
    fig = plt.figure(figsize=(10, 6))
    plt.plot(time_list, x_list, 'b-', linewidth=2, marker='o', markersize=3, 
             markevery=max(1, len(time_list)//20), label='x', alpha=0.8)
    plt.plot(time_list, y_list, 'r--', linewidth=2, marker='s', markersize=3, 
             markevery=max(1, len(time_list)//20), label='y', alpha=0.8)
    plt.plot(time_list, theta_list, 'g-.', linewidth=2, marker='^', markersize=3, 
             markevery=max(1, len(time_list)//20), label='theta', alpha=0.8)
    plt.xlabel('Time (s)', fontsize=12, fontweight='bold')
    plt.ylabel('Pose Value', fontsize=12, fontweight='bold')
    plt.title('Robot Pose vs Time', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.show()


def plot_trajectory(filename):
    """
    Generate plot for robot trajectory:
    - x vs y (2D trajectory)
    """
    headers, values = FileReader(filename).read_file()
    
    # Extract data columns
    x_list = [row[0] for row in values]
    y_list = [row[1] for row in values]
    
    # Figure: x vs y trajectory
    fig = plt.figure(figsize=(10, 6))
    plt.plot(x_list, y_list, 'b-', linewidth=2, marker='o', markersize=3, 
             markevery=max(1, len(x_list)//20), label='Robot trajectory', alpha=0.8)
    plt.scatter(x_list[0], y_list[0], c='lime', s=150, marker='o', 
               edgecolors='black', linewidths=2, label='Start', zorder=5)
    plt.scatter(x_list[-1], y_list[-1], c='red', s=150, marker='X', 
               edgecolors='black', linewidths=2, label='End', zorder=5)
    plt.xlabel('x', fontsize=12, fontweight='bold')
    plt.ylabel('y', fontsize=12, fontweight='bold')
    plt.title('Robot Trajectory (x vs y)', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10, framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axis('equal')  # Equal aspect ratio for proper trajectory visualization
    plt.tight_layout()
    
    plt.show()
    
    





import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot error data from CSV files.')
    parser.add_argument('--linear', type=str, help='CSV file with linear error data')
    parser.add_argument('--angular', type=str, help='CSV file with angular error data')
    parser.add_argument('--pose', type=str, help='CSV file with robot pose data')
    parser.add_argument('--trajectory', type=str, help='CSV file with robot trajectory data')
    
    args = parser.parse_args()
    
    if args.linear:
        print(f"Plotting linear errors from: {args.linear}")
        plot_linear_errors(args.linear)
    
    if args.angular:
        print(f"Plotting angular errors from: {args.angular}")
        plot_angular_errors(args.angular)
    
    if args.pose:
        print(f"Plotting robot pose vs time from: {args.pose}")
        plot_pose_vs_time(args.pose)
    
    if args.trajectory:
        print(f"Plotting robot trajectory from: {args.trajectory}")
        plot_trajectory(args.trajectory)
    
    if not any([args.linear, args.angular, args.pose, args.trajectory]):
        print("Please specify at least one file using --linear, --angular, --pose, or --trajectory")
        parser.print_help()



