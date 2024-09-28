import sys

class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.first_response_time = None
        self.waiting_time = 0
        self.turnaround_time = 0

def fifo_scheduler(process_list):
    """
    First In First Out (FIFO) scheduling algorithm.
    """
    print(f"{len(process_list)} processes")
    print("Using First In First Out")
    
    # Sort processes by arrival time
    process_list.sort(key=lambda p: p.arrival_time)
    
    current_time = 0
    for process in process_list:
        # If CPU is idle, advance current time to the arrival time of the process
        if current_time < process.arrival_time:
            for t in range(current_time, process.arrival_time):
                print(f"Time {t:4}: Idle")
            current_time = process.arrival_time
        
        print(f"Time {current_time:4}: {process.pid} arrived")
        print(f"Time {current_time:4}: {process.pid} selected (burst {process.execution_time:4})")
        
        # Calculate waiting time and response time
        process.waiting_time = current_time - process.arrival_time
        process.response_time = current_time - process.arrival_time  # In FIFO, response time equals waiting time
        
        # Simulate execution
        process_start_time = current_time
        current_time += process.execution_time
        process.cpu_usage = process.execution_time
        process.remaining_time = 0
        
        # Update turnaround time
        process.turnaround_time = current_time - process.arrival_time
        
        print(f"Time {current_time:4}: {process.pid} finished")
    
    while current_time < 20:
        print(f"Time {current_time:4}: Idle")
        current_time += 1

    print(f"Finished at time {current_time}")
    print()
    for process in process_list:
        print(f"{process.pid} wait {process.waiting_time:4} turnaround {process.turnaround_time:4} response {process.response_time:4}")


def sjf_scheduler(process_list):
    """
    Preemptive Shortest Job First (SJF) scheduling algorithm.
    """
    print(f"{len(process_list)} processes")
    print("Using preemptive Shortest Job First")
    
    # Sort processes by arrival time initially
    process_list.sort(key=lambda p: p.arrival_time)

    current_time = 0
    ready_queue = []
    completed_processes = []
    current_process = None

    while len(completed_processes) < len(process_list):
        # Add all processes that have arrived by current_time to the ready queue
        for process in process_list:
            if process.arrival_time <= current_time and process not in ready_queue and process not in completed_processes:
                ready_queue.append(process)
                print(f"Time {current_time:4}: {process.pid} arrived")
        
        # Sort ready queue by remaining time (SJF)
        ready_queue.sort(key=lambda p: p.remaining_time)

        if ready_queue:
            current_process = ready_queue.pop(0)

            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time

            print(f"Time {current_time:4}: {current_process.pid} selected (burst {current_process.remaining_time:4})")
            
            # Run the process for 1 unit of time
            process_start_time = current_time
            current_time += 1
            current_process.remaining_time -= 1

            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                completed_processes.append(current_process)
                print(f"Time {current_time:4}: {current_process.pid} finished")
        else:
            print(f"Time {current_time:4}: Idle")
            current_time += 1

    while current_time < 20:
        print(f"Time {current_time:4}: Idle")
        current_time += 1
    
    print(f"Finished at time {current_time}")
    print()
    for process in process_list:
        print(f"{process.pid} wait {process.waiting_time:4} turnaround {process.turnaround_time:4} response {process.response_time:4}")

def round_robin_scheduler(process_list, runfor, quantum, outfile):
    """
    Round Robin scheduling algorithm with a time slice (quantum).
    """
    outfile.write(f"{len(process_list)} processes\n")
    outfile.write(f"Using Round-Robin\n")
    outfile.write(f"Quantum   {quantum}\n\n")

    current_time = 0
    ready_queue = []
    completed_processes = []
    arrived_processes = []

    total_processes = len(process_list)

    # Process list sorted by arrival time
    process_list = sorted(process_list, key=lambda x: x.arrival_time)

    # Main loop
    while current_time < runfor and len(completed_processes) < total_processes:
        # Check for new arrivals
        for process in process_list:
            if process.arrival_time == current_time and process.pid not in arrived_processes:
                ready_queue.append(process)
                arrived_processes.append(process.pid)
                outfile.write(f"Time {current_time:4} : {process.pid} arrived\n")

        if ready_queue:
            current_process = ready_queue.pop(0)

            # If the process is running for the first time
            if current_process.first_response_time is None:
                current_process.first_response_time = current_time - current_process.arrival_time

            run_time = min(current_process.remaining_time, quantum)
            outfile.write(f"Time {current_time:4} : {current_process.pid} selected (burst {current_process.remaining_time:4})\n")

            # Advance current_time
            current_time += run_time

            # Decrease the remaining time
            current_process.remaining_time -= run_time

            # Check for new arrivals during the process's run time
            for t in range(current_time - run_time + 1, current_time):
                for process in process_list:
                    if process.arrival_time == t and process.pid not in arrived_processes:
                        ready_queue.append(process)
                        arrived_processes.append(process.pid)
                        outfile.write(f"Time {t:4} : {process.pid} arrived\n")

            # Check if the process has completed
            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                completed_processes.append(current_process.pid)
                outfile.write(f"Time {current_time:4} : {current_process.pid} finished\n")
            else:
                # Re-add the process to the ready queue
                ready_queue.append(current_process)
        else:
            outfile.write(f"Time {current_time:4} : Idle\n")
            current_time += 1

    # Fill in idle time if current_time is less than runfor
    while current_time < runfor:
        outfile.write(f"Time {current_time:4} : Idle\n")
        current_time += 1

    outfile.write(f"Finished at time {runfor}\n\n")

    # Print process stats
    for process in process_list:
        outfile.write(f"{process.pid} wait {process.waiting_time:4} turnaround {process.turnaround_time:4} response {process.first_response_time:4}\n")

def parse_input_file(input_file_name):
    parameters = {"processes": []}
    with open(input_file_name, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            tokens = line.split()
            if tokens[0] == "processcount":
                parameters["processcount"] = int(tokens[1])
            elif tokens[0] == "runfor":
                parameters["runfor"] = int(tokens[1])
            elif tokens[0] == "use":
                parameters["use"] = tokens[1]
            elif tokens[0] == "process":
                process_id = tokens[2]
                arrival_time = int(tokens[4])
                burst_time = int(tokens[6])
                process = Process(process_id, arrival_time, burst_time)
                parameters["processes"].append(process)
            elif tokens[0] == "quantum":
                parameters["quantum"] = int(tokens[1])

    # Error handling to check for required keys
    if "use" not in parameters:
        print("Error: Missing parameter 'use'")
        sys.exit(1)

    if parameters["use"] == "rr" and "quantum" not in parameters:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    if "runfor" not in parameters:
        print("Error: Missing 'runfor' parameter.")
        sys.exit(1)

    return parameters

def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    if not input_file_name.endswith(".in"):
        print(f"Error: Input file must have .in extension")
        sys.exit(1)

    output_file_name = input_file_name.replace(".in", ".out")

    parameters = parse_input_file(input_file_name)

    if "processes" in parameters and "runfor" in parameters:
        with open(output_file_name, 'w') as outfile:
            if parameters["use"] == 'rr':
                round_robin_scheduler(parameters["processes"], parameters["runfor"], parameters["quantum"], outfile)
            else:
                print(f"Error: Unknown scheduling algorithm '{parameters['use']}'")
                sys.exit(1)
    else:
        print("Error: Missing necessary parameters in input file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
