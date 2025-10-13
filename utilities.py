from math import atan2, asin, sqrt

M_PI=3.1415926535

class Logger:
    # A simple CSV logger class that writes data to a file.
    # Creates a file with headers and provides methods to append data rows.

    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        self.filename = filename

        # Create/overwrite the file and write the header row
        with open(self.filename, 'w') as file:
            header_str=""

            for header in headers:
                header_str+=header
                header_str+=", "
            
            header_str+="\n"
            
            file.write(header_str)

    def log_values(self, values_list):
        # Append a row of values to the CSV file.
        # Values are converted to strings and separated by commas.

        # Open in append mode ('a') to add data without overwriting
        with open(self.filename, 'a') as file:
            vals_str=""

            # Convert each value to string and add comma separator
            for value in values_list:
                vals_str += str(value)
                vals_str += ", "
            
            vals_str+="\n"
            
            file.write(vals_str)
            
    def save_log(self):
        # Placeholder method for potential future functionality
        pass

class FileReader:
    # A CSV file reader that extracts headers and numeric data from a file.
    # Assumes comma-separated values with a header row.

    def __init__(self, filename):
        self.filename = filename
        
    def read_file(self):
        # Read CSV file and return headers and data rows.
        # Returns: (headers_list, data_rows_list)

        read_headers=False

        table=[]
        headers=[]
        with open(self.filename, 'r') as file:
            # Read the first line to extract headers
            if not read_headers:
                for line in file:
                    values=line.strip().split(',')

                    # Build headers list, stopping at empty values
                    for val in values:
                        if val=='':
                            break
                        headers.append(val.strip())

                    read_headers=True
                    break
            
            # Skip the header line again (since we already read it)
            next(file)
            
            # Read each subsequent line as data
            for line in file:
                values = line.strip().split(',')
                
                row=[]                
                
                # Convert each value to float, stopping at empty values
                for val in values:
                    if val=='':
                        break
                    row.append(float(val.strip()))

                table.append(row)
        
        return headers, table

def euler_from_quaternion(quat):
    # Convert quaternion (w in last place) to euler yaw angle.
    # Quaternions are a 4D representation of 3D rotations that avoid gimbal lock.
    
    # Args: quat: [x, y, z, w] - quaternion components
    # Returns: yaw: rotation angle around the z-axis in radians
    
    # Note: This only extracts yaw (z-axis rotation), not roll and pitch.
    # For a mobile robot on flat ground, yaw is typically the only angle needed.

    x = quat[0]
    y = quat[1]
    z = quat[2]
    w = quat[3]
    
    # Calculate yaw (z-axis rotation) using the quaternion-to-euler conversion formula
    # This formula comes from the standard rotation matrix to Euler angle conversion
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = atan2(siny_cosp, cosy_cosp)  # atan2 handles quadrant correctly
    
    return yaw