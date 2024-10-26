import re
import os
def parse_and_create_srv_files(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    output_dir = 'new_srvs'
    os.makedirs(output_dir, exist_ok=True)
    current_class = None
    is_sent_params = False
    is_recv_params = False
    class_pattern = r'class (\w+)\(_BaseMsg\):'
    sent_params_pattern = r'_sent_parameters\s*=\s*\[(.*?)\]'
    recv_params_pattern = r'_received_parameters\s*=\s*\[(.*?)\]'

    for line in lines:
        
        class_match = re.match(class_pattern, line)
        if class_match:
            current_class = class_match.group(1)
            print(f"Processing class: {current_class}")

            output_file_path = os.path.join(output_dir, f"{current_class}.srv")
            with open(output_file_path, 'w') as srv_file:
                continue  

        if '_sent_parameters' in line:
            is_sent_params = True
            is_recv_params = False
            continue

        if '_received_parameters' in line:
            is_recv_params = True
            is_sent_params = False
            
            with open(output_file_path, 'a') as srv_file:
                srv_file.write("---\n")  
            continue

        if is_sent_params:
            param_match = re.search(r'_CanMsgParam\(\s*\'([^\']+)\'', line)
            if param_match:
                param_name = param_match.group(1)
                with open(output_file_path, 'a') as srv_file:
                    srv_file.write(f"float32 {param_name}\n")

        if is_recv_params:
            param_match = re.search(r'_CanMsgParam\(\s*\'([^\']+)\'', line)
            if param_match:
                param_name = param_match.group(1)
                with open(output_file_path, 'a') as srv_file:
                    srv_file.write(f"float32 {param_name}\n")

    print("Service files created successfully.")

parse_and_create_srv_files(r'myactuator\msgs.py')
