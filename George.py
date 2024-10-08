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
        self.response_time = None
        self.cpu_usage = 0
        self.program_counter = 0
        self.status = 'new'

def fifo_scheduler(process_list, runfor, outfile, htmlfile):
    # Sort the process list by arrival time
    process_list = sorted(process_list, key=lambda p: p.arrival_time)

    html_output = '<pre style="color:black;">\n'
    html_output += '<span style="color:blue;">  {}</span>\n'.format(f"{len(process_list)} processes")
    html_output += '<span style="color:cyan;">Using First-Come First-Served</span>\n'

    outfile.write(f"  {len(process_list)} processes\n")
    outfile.write("Using First-Come First-Served\n")

    current_time = 0
    total_processes = len(process_list)
    ready_queue = []
    processes_to_arrive = process_list.copy()
    processes_completed = 0

    # Keep track of all processes by PID
    processes = {p.pid: p for p in process_list}

    while current_time < runfor and processes_completed < total_processes:
        # Check for new arrivals at the current time
        while processes_to_arrive and processes_to_arrive[0].arrival_time == current_time:
            process = processes_to_arrive.pop(0)
            ready_queue.append(process)
            outfile.write(f"Time {current_time:3d} : {process.pid} arrived\n")
            html_output += f"Time {current_time:3d} : <span style='color:green;'>{process.pid} arrived</span>\n"

        if ready_queue:
            current_process = ready_queue[0]
            if current_process.status == 'new':
                outfile.write(f"Time {current_time:3d} : {current_process.pid} selected (burst {current_process.execution_time:3d})\n")
                html_output += f"Time {current_time:3d} : <span style='color:green;'>{current_process.pid} selected (burst {current_process.execution_time:3d})</span>\n"
                current_process.response_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_time - current_process.arrival_time
                current_process.status = 'running'

            # Run the process until completion
            run_time = current_process.execution_time
            prev_time = current_time
            current_time += run_time
            current_process.turnaround_time = current_time - current_process.arrival_time
            current_process.status = 'terminated'
            outfile.write(f"Time {current_time:3d} : {current_process.pid} finished\n")
            html_output += f"Time {current_time:3d} : <span style='color:red;'>{current_process.pid} finished</span>\n"
            ready_queue.pop(0)
            processes_completed += 1

            # Check for arrivals during the process's execution
            for t in range(prev_time + 1, current_time):
                while processes_to_arrive and processes_to_arrive[0].arrival_time == t:
                    process = processes_to_arrive.pop(0)
                    ready_queue.append(process)
                    outfile.write(f"Time {t:3d} : {process.pid} arrived\n")
                    html_output += f"Time {t:3d} : <span style='color:green;'>{process.pid} arrived</span>\n"
        else:
            outfile.write(f"Time {current_time:3d} : Idle\n")
            html_output += f"Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"
            current_time += 1

    # Fill remaining time with idle if necessary
    while current_time < runfor:
        outfile.write(f"Time {current_time:3d} : Idle\n")
        html_output += f"Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"
        current_time += 1

    outfile.write(f"Finished at time  {runfor}\n\n")
    html_output += f"<span style='color:purple;'>Finished at time  {runfor}</span>\n\n"

    # Output process statistics
    def get_pid_number(pid):
        if pid.startswith('P'):
            return int(pid[1:])
        else:
            return int(pid)

    process_list_sorted = sorted(process_list, key=lambda p: get_pid_number(p.pid))
    for process in process_list_sorted:
        outfile.write(f"{process.pid} wait {process.waiting_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time:3d}\n")
        html_output += f"<span style='color:black;'>{process.pid} wait {process.waiting_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time:3d}</span>\n"

    html_output += "</pre>"
    htmlfile.write(html_output)

def sjf_scheduler(process_list, runfor, outfile, htmlfile):
    current_time = 0
    ready_queue = []
    running_process = None

    total_processes = len(process_list)

    outfile.write(f"  {total_processes} processes\n")
    outfile.write("Using preemptive Shortest Job First\n")
    html_output = '<pre style="color:black;">\n'
    html_output += f"<span style='color:blue;'>  {total_processes} processes</span>\n"
    html_output += "<span style='color:cyan;'>Using preemptive Shortest Job First</span>\n"

    processes = {p.pid: p for p in process_list}
    processes_to_arrive = sorted(process_list, key=lambda x: x.arrival_time)

    while current_time < runfor:
        time_events = []

        arrivals = []
        while processes_to_arrive and processes_to_arrive[0].arrival_time == current_time:
            process = processes_to_arrive.pop(0)
            arrivals.append(process)
            event = f"Time {current_time:3d} : {process.pid} arrived\n"
            time_events.append(event)
            html_event = f"Time {current_time:3d} : <span style='color:green;'>{process.pid} arrived</span>\n"
            html_output += html_event
            process.status = 'ready'
            ready_queue.append(process)

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
            if running_process.first_response_time is None:
                running_process.first_response_time = current_time - running_process.arrival_time
                running_process.response_time = current_time - running_process.arrival_time
            event = f"Time {current_time:3d} : {running_process.pid} selected (burst {running_process.remaining_time:3d})\n"
            time_events.append(event)
            html_event = f"Time {current_time:3d} : <span style='color:green;'>{running_process.pid} selected (burst {running_process.remaining_time:3d})</span>\n"
            html_output += html_event

        if not running_process and not time_events:
            event = f"Time {current_time:3d} : Idle\n"
            time_events.append(event)
            html_event = f"Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"
            html_output += html_event

        if running_process:
            running_process.remaining_time -= 1
            running_process.cpu_usage += 1
            running_process.program_counter += 1
            if running_process.remaining_time == 0:
                running_process.status = 'terminated'
                running_process.turnaround_time = current_time + 1 - running_process.arrival_time
                running_process.waiting_time = running_process.turnaround_time - running_process.execution_time
                event = f"Time {current_time +1:3d} : {running_process.pid} finished\n"
                time_events.append(event)
                html_event = f"Time {current_time +1:3d} : <span style='color:red;'>{running_process.pid} finished</span>\n"
                html_output += html_event
                running_process = None

        for event in time_events:
            outfile.write(event)

        current_time += 1

    while current_time < runfor:
        outfile.write(f"Time {current_time:3d} : Idle\n")
        html_output += f"Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"
        current_time += 1

    outfile.write(f"Finished at time {current_time:3d}\n\n")
    html_output += f"<span style='color:purple;'>Finished at time {current_time}</span>\n\n"

    def get_pid_number(pid):
        if pid.startswith('P'):
            return int(pid[1:])
        else:
            return int(pid)

    process_list_sorted = sorted(processes.values(), key=lambda p: get_pid_number(p.pid))
    for process in process_list_sorted:
        process.response_time = process.first_response_time if process.first_response_time is not None else 0
        stats = f"{process.pid} wait {process.waiting_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time:3d}\n"
        outfile.write(stats)
        html_output += f"<span style='color:black;'>{stats.strip()}</span>\n"

    html_output += "</pre>"
    htmlfile.write(html_output)

def round_robin_scheduler(process_list, runfor, quantum, outfile, htmlfile):
    outfile.write(f"  {len(process_list)} processes\n")
    outfile.write(f"Using Round-Robin\nQuantum   {quantum}\n\n")
    html_output = '<pre style="color:black;">\n'
    html_output += '<span style="color:blue;">  {}</span>\n'.format(f"{len(process_list)} processes")
    html_output += f"<span style='color:cyan;'>Using Round-Robin</span>\n"
    html_output += f"<span style='color:cyan;'>Quantum {quantum}</span>\n"

    current_time = 0
    ready_queue = []
    completed_processes = []
    arrived_processes = []
    total_processes = len(process_list)

    process_list = sorted(process_list, key=lambda x: x.arrival_time)

    # Initial arrival of processes at time 0
    for process in process_list:
        if process.arrival_time == 0:
            ready_queue.append(process)
            arrived_processes.append(process.pid)
            outfile.write(f"Time {current_time:3d} : {process.pid} arrived\n")
            html_output += f"Time {current_time:3d} : <span style='color:green;'>{process.pid} arrived</span>\n"

    while current_time < runfor and len(completed_processes) < total_processes:
        if ready_queue:
            current_process = ready_queue.pop(0)

            if current_process.first_response_time is None:
                current_process.first_response_time = current_time - current_process.arrival_time
                current_process.response_time = current_time - current_process.arrival_time

            run_time = min(current_process.remaining_time, quantum)
            outfile.write(f"Time {current_time:3d} : {current_process.pid} selected (burst {current_process.remaining_time:3d})\n")
            html_output += f"Time {current_time:3d} : <span style='color:green;'>{current_process.pid} selected (burst {current_process.remaining_time:3d})</span>\n"

            prev_time = current_time
            current_time += run_time
            current_process.remaining_time -= run_time

            # Check for new arrivals during the process's run time
            arrivals_during_run = []
            for t in range(prev_time + 1, current_time + 1):
                for process in process_list:
                    if process.arrival_time == t and process.pid not in arrived_processes:
                        arrivals_during_run.append(process)
                        arrived_processes.append(process.pid)
                        outfile.write(f"Time {t:3d} : {process.pid} arrived\n")
                        html_output += f"Time {t:3d} : <span style='color:green;'>{process.pid} arrived</span>\n"

            # Add arrivals to ready queue before adding the preempted process
            ready_queue.extend(arrivals_during_run)

            # If the process has completed
            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                completed_processes.append(current_process.pid)
                outfile.write(f"Time {current_time:3d} : {current_process.pid} finished\n")
                html_output += f"Time {current_time:3d} : <span style='color:red;'>{current_process.pid} finished</span>\n"
            else:
                # Add the preempted process back to the ready queue
                ready_queue.append(current_process)
        else:
            outfile.write(f"Time {current_time:3d} : Idle\n")
            html_output += f"Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"
            current_time += 1

            # Check for new arrivals at the current time
            for process in process_list:
                if process.arrival_time == current_time and process.pid not in arrived_processes:
                    ready_queue.append(process)
                    arrived_processes.append(process.pid)
                    outfile.write(f"Time {current_time:3d} : {process.pid} arrived\n")
                    html_output += f"Time {current_time:3d} : <span style='color:green;'>{process.pid} arrived</span>\n"

    while current_time < runfor:
        outfile.write(f"Time {current_time:3d} : Idle\n")
        html_output += f"Time {current_time:3d} : <span style='color:blue;'>Idle</span>\n"
        current_time += 1

    outfile.write(f"Finished at time  {runfor}\n\n")
    html_output += f"<span style='color:purple;'>Finished at time  {runfor}</span>\n\n"

    def get_pid_number(pid):
        if pid.startswith('P'):
            return int(pid[1:])
        else:
            return int(pid)

    process_list_sorted = sorted(process_list, key=lambda p: get_pid_number(p.pid))
    for process in process_list_sorted:
        process.response_time = process.first_response_time if process.first_response_time is not None else 0
        outfile.write(f"{process.pid} wait {process.waiting_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time:3d}\n")
        html_output += f"<span style='color:black;'>{process.pid} wait {process.waiting_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time:3d}</span>\n"

    html_output += "</pre>"
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
            elif tokens[0] == "end":
                break

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
