import re
import csv

def parse_odom_txt(input_file, output_csv):
    # Read the entire file
    with open(input_file, 'r') as f:
        content = f.read()

    # Split into message blocks based on blank lines
    blocks = [block.strip() for block in content.split('\n\n') if block.strip()]

    times = []
    x_positions = []
    y_positions = []
    angular_zs = []

    for block in blocks:
        # Normalize whitespace in the block
        block_text = " ".join(block.split())

        # Define regex patterns for each field
        sec_match = re.search(r"sec:\s*(-?\d+)", block_text)
        nsec_match = re.search(r"nsec:\s*(-?\d+)", block_text)
        x_match = re.search(r"position\s*{\s*[^}]*x:\s*(-?\d+\.\d+)", block_text)
        y_match = re.search(r"position\s*{\s*[^}]*y:\s*(-?\d+\.\d+)", block_text)
        angular_z_match = re.search(r"angular\s*{\s*[^}]*z:\s*(-?\d+\.\d+)", block_text)

        # Check if all required fields are present
        if all([sec_match, nsec_match, x_match, y_match, angular_z_match]):
            # Extract values
            sec = int(sec_match.group(1))
            nsec = int(nsec_match.group(1))
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            angular_z = float(angular_z_match.group(1))

            # Compute time in seconds
            time = sec + nsec / 1_000_000_000.0

            # Store the data
            times.append(time)
            x_positions.append(x)
            y_positions.append(y)
            angular_zs.append(angular_z)

        else:
            print(f"Skipping incomplete message: {block_text[:50]}...")

    # Write to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'x', 'y', 'angular_z'])
        for t, x, y, az in zip(times, x_positions, y_positions, angular_zs):
            writer.writerow([t, x, y, az])

    print(f"Converted {len(times)} messages to {output_csv}")

if __name__ == "__main__":
    input_file = "odom_data.txt"
    output_file = "odom_data.csv"
    parse_odom_txt(input_file, output_file)