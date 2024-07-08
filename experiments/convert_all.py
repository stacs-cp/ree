import glob
import re
import time
import subprocess
import os
import signal

# Step 1: List all the files matching the pattern
files = glob.glob('./tests/gcmulti-func-gcmulti_rand-*.solution')
solveTimes = []

# Step 2: Loop through each file
for file in files:
    # Extract numbers from the filename
    numbers = re.findall(r'gcmulti-func-gcmulti_rand-(\d+)-(\d+)-(\d+)-(\d+)\.solution', file)
    if numbers:
        # numbers[0] contains a tuple of the four numbers as strings
        n, e, c, cpn = numbers[0]
        
        # Step 3: Open and read the file
        with open(file, 'r') as f:
            content_lines = f.readlines()

        # Filter out lines that start with "language" or "$"
        filtered_content = [line for line in content_lines if not line.startswith('language') and not line.startswith('$')]
        
        # Join the remaining lines back into a single string
        filtered_content = ''.join(filtered_content)

        filtered_content = filtered_content.replace('letting c', 'letting solution')

        # Create the formatted string
        formatted_string = f'''letting n be {n}
letting numberColours be {c} 
letting coloursPerNode be {cpn}
{filtered_content}'''
        
        # You can now print or process the formatted string as needed
        #print(formatted_string)
        name = file[:-9].split("/")[-1]
        verification_file = f"experiments/verify-converted/{name}SOL.param"

        verification_spec = "./experiments/verify-converted/func_TO_rel.essence"
        
        with open(verification_file, 'w') as file:
            file.write(formatted_string)

        conjureCall = ['conjure','solve', verification_spec,verification_file ]
        start = time.time_ns() 
        # Start the subprocess in a new process group
        proc = subprocess.Popen(conjureCall, preexec_fn=os.setsid)

        try:
            # Wait for the process to complete, or kill it after a timeout
            proc.wait(timeout=100)
        except subprocess.TimeoutExpired:
            # Send the signal to all the processes in the process group
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

        solveTime =time.time_ns() - start
        solveTime = round(solveTime/1000000000,2)
        #print(solveTime)
        solveTimes.append(solveTime)

print(max(solveTimes))
print(sum(solveTimes)/len(solveTimes))
