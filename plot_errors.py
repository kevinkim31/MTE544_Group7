import matplotlib.pyplot as plt


class FileReader:
    def __init__(self, filename):
        self.filename = filename
        
    def read_file(self):
        read_headers = False
        table = []
        headers = []
        with open(self.filename, 'r') as file:
            if not read_headers:
                for line in file:
                    values = line.strip().split(',')
                    for val in values:
                        if val == '':
                            break
                        headers.append(val.strip())
                    read_headers = True
                    break
            next(file)
            for line in file:
                values = line.strip().split(',')
                row = []
                for val in values:
                    if val == '':
                        break
                    row.append(float(val.strip()))
                table.append(row)
        return headers, table


def plot_position_single(part_name, filename):
    """
    Plot logged positions (x, y) from particle filter vs odometry
    for a single part (x on x-axis, y on y-axis)
    """
    headers, values = FileReader(filename).read_file()
    
    # Extract indices from headers
    odom_x_idx = headers.index('odom_x')
    odom_y_idx = headers.index('odom_y')
    pf_x_idx = headers.index('pf_x')
    pf_y_idx = headers.index('pf_y')
    
    # Extract odometry x, y
    odom_x = [row[odom_x_idx] for row in values]
    odom_y = [row[odom_y_idx] for row in values]
    
    # Extract particle filter x, y
    pf_x = [row[pf_x_idx] for row in values]
    pf_y = [row[pf_y_idx] for row in values]
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Plot odometry
    ax.plot(odom_x, odom_y, 
            color='blue', marker='o', linestyle='-',
            markersize=4, linewidth=1.5, alpha=0.7,
            label='Odometry')
    
    # Plot particle filter
    ax.plot(pf_x, pf_y, 
            color='red', marker='s', linestyle='--',
            markersize=4, linewidth=1.5, alpha=0.7,
            label='Particle Filter')
    
    ax.set_xlabel('X Position (m)', fontsize=12)
    ax.set_ylabel('Y Position (m)', fontsize=12)
    ax.set_title(f'Position Comparison: {part_name} - Odometry vs Particle Filter', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    plt.show()


def plot_theta_single(part_name, filename):
    """
    Plot logged positions (theta) from particle filter vs odometry
    for a single part (time on x-axis, theta on y-axis)
    """
    headers, values = FileReader(filename).read_file()
    
    # Extract indices from headers
    odom_th_idx = headers.index('odom_th')
    pf_th_idx = headers.index('pf_th')
    stamp_idx = headers.index('stamp')
    
    # Calculate time list (relative to first timestamp)
    first_stamp = values[0][stamp_idx]
    time_list = [(row[stamp_idx] - first_stamp) / 1e9 for row in values]  # Convert nanoseconds to seconds
    
    # Extract odometry theta
    odom_th = [row[odom_th_idx] for row in values]
    
    # Extract particle filter theta
    pf_th = [row[pf_th_idx] for row in values]
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Plot odometry theta
    ax.plot(time_list, odom_th, 
            color='blue', marker='o', linestyle='-',
            markersize=3, linewidth=1.5, alpha=0.7,
            label='Odometry')
    
    # Plot particle filter theta
    ax.plot(time_list, pf_th, 
            color='red', marker='s', linestyle='--',
            markersize=3, linewidth=1.5, alpha=0.7,
            label='Particle Filter')
    
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.set_ylabel('Theta (rad)', fontsize=12)
    ax.set_title(f'Theta Comparison: {part_name} - Odometry vs Particle Filter', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Plot particle filter vs odometry comparisons.')
    parser.add_argument('--part5', type=str, required=True, help='robotPose.csv file for Part5')
    parser.add_argument('--part6_1', type=str, required=True, help='robotPose.csv file for Part6.1')
    parser.add_argument('--part6_2', type=str, required=True, help='robotPose.csv file for Part6.2')
    
    args = parser.parse_args()
    
    # Section 1: Position plots (x vs y) - 3 separate graphs
    print("Plotting Section 1: Position comparison (x vs y)")
    print("  - Part5")
    plot_position_single('Part5', args.part5)
    print("  - Part6.1")
    plot_position_single('Part6.1', args.part6_1)
    print("  - Part6.2")
    plot_position_single('Part6.2', args.part6_2)
    
    # Section 2: Theta plots (time vs theta) - 3 separate graphs
    print("Plotting Section 2: Theta comparison (time vs theta)")
    print("  - Part5")
    plot_theta_single('Part5', args.part5)
    print("  - Part6.1")
    plot_theta_single('Part6.1', args.part6_1)
    print("  - Part6.2")
    plot_theta_single('Part6.2', args.part6_2)
