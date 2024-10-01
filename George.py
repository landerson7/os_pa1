import sys
from colorama import Fore, Style

class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.first_response_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.cpu_usage = 0
        self.program_counter = 0

def fifo_scheduler(process_list, runfor, outfile, htmlfile):
    html_output = '<pre style="color:black;">\n'
    html_output += '<span style="color:blue;">  {}</span>\n'.format(f"{len(process_list)} processes")
    html_output += '<span style="color:cyan;">Using First In First Out</span>\n'

    outfile.write(f"  {len(process_list)} processes\n")
    outfile.write("Using First In First Out\n")

    current_time = 0
    
    for process in process_list:
        if current_time < process.arrival_time:
            for t in range(current_time, process.arrival_time):
                outfile.write(f"Time  {t:2} : Idle\n")
                html_output += f"Time  {t:2} : <span style='color:blue;'>Idle</span>\n"
            current_time = process.arrival_time

        outfile.write(f"Time  {current_time:2} : P{process.pid} arrived\n")
        outfile.write(f"Time  {current_time:2} : P{process.pid} selected (burst  {process.execution_time:3})\n")

        html_output += f"Time  {current_time:2} : <span style='color:green;'>P{process.pid} arrived</span>\n"
        html_output += f"Time  {current_time:2} : <span style='color:green;'>P{process.pid} selected (burst {process.execution_time:3})</span>\n"
        
        process.waiting_time = current_time - process.arrival_time
        process.response_time = current_time - process.arrival_time
        
        current_time += process.execution_time
        process.turnaround_time = current_time - process.arrival_time
        
        outfile.write(f"Time  {current_time:2} : P{process.pid} finished\n")
        html_output += f"Time  {current_time:2} : <span style='color:red;'>P{process.pid} finished</span>\n"
    
    while current_time < runfor:
        outfile.write(f"Time  {current_time:2} : Idle\n")
        html_output += f"Time  {current_time:2} : <span style='color:blue;'>Idle</span>\n"
        current_time += 1

    outfile.write(f"Finished at time  {current_time}\n\n")
    html_output += f"<span style='color:purple;'>Finished at time  {current_time}</span>\n"

    for process in process_list:
        outfile.write(f"P{process.pid} wait  {process.waiting_time:2} turnaround  {process.turnaround_time:2} response  {process.response_time:2}\n")
        html_output += f"<span style='color:black;'>P{process.pid} wait  {process.waiting_time:2} turnaround  {process.turnaround_time:2} response  {process.response_time:2}</span>\n"

    html_output += "</pre>"
    htmlfile.write(html_output)

def sjf_scheduler(process_list, runfor, outfile, htmlfile):
    """
    Shortest Job First (Preemptive) scheduling algorithm.
    """
    current_time = 0
    ready_queue = []
    running_process = None
    process_dict = {p.pid: p for p in process_list}

    process_list.sort(key=lambda x: x.arrival_time)
    total_processes = len(process_list)

    # Write the process count and header
    outfile.write(f"  {total_processes} processes\n")
    outfile.write("Using preemptive Shortest Job First\n")  # Removed extra newline here
    html_output = '<pre style="color:black;">\n'

    while current_time < runfor:
        time_events = []
        arrivals = [p for p in process_list if p.arrival_time == current_time]
        for process in arrivals:
            time_events.append(f"  Time {current_time:3d} : P{process.pid} arrived\n")
            html_output += f"  Time {current_time:3d} : <span style='color:green;'>P{process.pid} arrived</span>\n"
            process.status = 'ready'
            ready_queue.append(process)
        process_list = [p for p in process_list if p.arrival_time > current_time]

        if running_process:
            if ready_queue:
                shortest_ready = min(ready_queue, key=lambda x: x.remaining_time)
                if shortest_ready.remaining_time < running_process.remaining_time:
                    running_process.status = 'ready'
                    ready_queue.append(running_process)
                    running_process = None

        if not running_process and ready_queue:
            ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
            running_process = ready_queue.pop(0)
            running_process.status = 'running'
            if running_process.response_time is None:
                running_process.response_time = current_time - running_process.arrival_time
            time_events.append(f"  Time {current_time:3d} : P{running_process.pid} selected (burst {running_process.remaining_time:3d})\n")
            html_output += f"  Time {current_time:3d} : <span style='color:green;'>P{running_process.pid} selected (burst {running_process.remaining_time:3d})</span>\n"

        if not running_process and not time_events:
            time_events.append(f"  Time {current_time:3d} : Idle\n")
            html_output += f"  Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"

        if running_process:
            running_process.remaining_time -= 1
            running_process.cpu_usage += 1
            running_process.program_counter += 1
            if running_process.remaining_time == 0:
                running_process.status = 'terminated'
                running_process.turnaround_time = current_time + 1 - running_process.arrival_time
                time_events.append(f"  Time {current_time +1:3d} : P{running_process.pid} finished\n")
                html_output += f"  Time {current_time +1:3d} : <span style='color:red;'>P{running_process.pid} finished</span>\n"
                running_process = None

        for event in time_events:
            outfile.write(event)

        current_time += 1

    outfile.write(f"Finished at time {current_time:3d}\n\n")
    html_output += f"<span style='color:purple;'>Finished at time {current_time}</span>\n</pre>"
    htmlfile.write(html_output)

def round_robin_scheduler(process_list, runfor, quantum, outfile, htmlfile):
    outfile.write(f"  {len(process_list)} processes\n")
    outfile.write(f"Using Round-Robin\nQuantum {quantum}\n")

    current_time = 0
    ready_queue = []
    completed_processes = []
    arrived_processes = []
    total_processes = len(process_list)

    process_list = sorted(process_list, key=lambda x: x.arrival_time)
    html_output = '<pre style="color:black;">\n'

    while current_time < runfor and len(completed_processes) < total_processes:
        for process in process_list:
            if process.arrival_time == current_time and process.pid not in arrived_processes:
                ready_queue.append(process)
                arrived_processes.append(process.pid)
                outfile.write(f"  Time {current_time:4} : P{process.pid} arrived\n")
                html_output += f"  Time {current_time:4} : <span style='color:green;'>P{process.pid} arrived</span>\n"

        if ready_queue:
            current_process = ready_queue.pop(0)

            if current_process.first_response_time is None:
                current_process.first_response_time = current_time - current_process.arrival_time

            run_time = min(current_process.remaining_time, quantum)
            outfile.write(f"  Time {current_time:4} : P{current_process.pid} selected (burst {current_process.remaining_time:4})\n")
            html_output += f"  Time {current_time:4} : <span style='color:green;'>P{current_process.pid} selected (burst {current_process.remaining_time:4})</span>\n"

            current_time += run_time
            current_process.remaining_time -= run_time

            for t in range(current_time - run_time + 1, current_time):
                for process in process_list:
                    if process.arrival_time == t and process.pid not in arrived_processes:
                        ready_queue.append(process)
                        arrived_processes.append(process.pid)
                        outfile.write(f"  Time {t:4} : P{process.pid} arrived\n")
                        html_output += f"  Time {t:4} : <span style='color:green;'>P{process.pid} arrived</span>\n"

            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                completed_processes.append(current_process.pid)
                outfile.write(f"  Time {current_time:4} : P{current_process.pid} finished\n")
                html_output += f"  Time {current_time:4} : <span style='color:red;'>P{current_process.pid} finished</span>\n"
            else:
                ready_queue.append(current_process)
        else:
            outfile.write(f"  Time {current_time:4} : Idle\n")
            html_output += f"  Time {current_time:4} : <span style='color:blue;'>Idle</span>\n"
            current_time += 1

    while current_time < runfor:
        outfile.write(f"  Time {current_time:4} : Idle\n")
        html_output += f"  Time {current_time:4} : <span style='color:blue;'>Idle</span>\n"
        current_time += 1

    outfile.write(f"Finished at time {runfor}\n\n")
    html_output += f"<span style='color:purple;'>Finished at time {runfor}</span>\n</pre>"
    htmlfile.write(html_output)

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
    html_file_name = input_file_name.replace(".in", ".html")

    parameters = parse_input_file(input_file_name)

    if "processes" in parameters and "runfor" in parameters:
        with open(output_file_name, 'w') as outfile, open(html_file_name, 'w') as htmlfile:
            if parameters["use"] == 'fcfs':
                fifo_scheduler(parameters["processes"], parameters["runfor"], outfile, htmlfile)
            elif parameters["use"] == 'sjf':
                sjf_scheduler(parameters["processes"], parameters["runfor"], outfile, htmlfile)
            elif parameters["use"] == 'rr':
                round_robin_scheduler(parameters["processes"], parameters["runfor"], parameters["quantum"], outfile, htmlfile)
            else:
                print(f"Error: Unknown scheduling algorithm '{parameters['use']}'")
                sys.exit(1)
    else:
        print("Error: Missing necessary parameters in input file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
