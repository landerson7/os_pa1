
from data_struct import Process

def parse_input():
    process_list = []
    process_count = 0
    runfor = 0
    use = ''
    current_line = ''
    process_data = []
    while True:
        line = input()
        if line == 'end':
            break
        else:
            line = line.strip()
            if line.startswith('processcount'):
                process_count = int(line.split()[1])
            elif line.startswith('runfor'):
                runfor = int(line.split()[1])
            elif line.startswith('use'):
                use = line.split()[1]
            elif line.startswith('process'):
                tokens = line.split()
                name = tokens[tokens.index('name')+1]
                arrival = int(tokens[tokens.index('arrival')+1])
                burst = int(tokens[tokens.index('burst')+1])
                process_data.append({'pid': name, 'arrival_time': arrival, 'execution_time': burst})
    for data in process_data:
        process = Process(data['pid'], data['arrival_time'], data['execution_time'])
        process_list.append(process)
    return process_count, runfor, use, process_list

def sjf_scheduler(process_list, runfor):
    current_time = 0
    ready_queue = []
    running_process = None
    process_dict = {p.pid: p for p in process_list}

    # Sort the process list based on arrival time
    process_list.sort(key=lambda x: x.arrival_time)

    # For statistics
    total_processes = len(process_list)
    
    # For output
    print(f"{total_processes} processes")
    print("Using preemptive Shortest Job First")

    # We need to simulate time from 0 to runfor -1
    while current_time < runfor:
        # List to hold events at this time
        time_events = []
        # 1. Check for new arrivals at current_time
        arrivals = [p for p in process_list if p.arrival_time == current_time]
        for process in arrivals:
            time_events.append(f"Time {current_time:3d} : {process.pid} arrived")
            process.status = 'ready'
            ready_queue.append(process)
        # Remove arrived processes from process_list
        process_list = [p for p in process_list if p.arrival_time > current_time]

        # 2. Decide whether to preempt
        if running_process:
            # If any process in ready_queue has remaining_time < running_process.remaining_time
            if ready_queue:
                shortest_ready = min(ready_queue, key=lambda x: x.remaining_time)
                if shortest_ready.remaining_time < running_process.remaining_time:
                    # Preempt
                    running_process.status = 'ready'
                    ready_queue.append(running_process)
                    running_process = None

        # 3. If no process is running, select the next process
        if not running_process:
            if ready_queue:
                # Select process with shortest remaining_time
                ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
                running_process = ready_queue.pop(0)
                running_process.status = 'running'
                if running_process.response_time is None:
                    running_process.response_time = current_time - running_process.arrival_time
                time_events.append(f"Time {current_time:3d} : {running_process.pid} selected (burst {running_process.remaining_time:3d})")

        # 4. If no process is running and no ready processes, CPU is idle
        if not running_process and not time_events:
            time_events.append(f"Time {current_time:3d} : Idle")

        # 5. Execute running process for 1 time unit
        if running_process:
            running_process.remaining_time -=1
            running_process.cpu_usage +=1
            running_process.program_counter +=1  # Simplified
            # Check if process finishes at the end of this time unit
            if running_process.remaining_time == 0:
                running_process.status = 'terminated'
                running_process.turnaround_time = current_time +1 - running_process.arrival_time
                time_events.append(f"Time {current_time +1:3d} : {running_process.pid} finished")
                running_process = None

        # Output events for this time
        for event in time_events:
            print(event)

        current_time +=1

    # At the end
    print(f"Finished at time {current_time:3d}")

    # Now, output per-process statistics
    for process in sorted(process_dict.values(), key=lambda x: x.pid):
        process.waiting_time = process.turnaround_time - process.cpu_usage
        print(f"\n{process.pid} wait {process.waiting_time:3d} turnaround {process.turnaround_time:3d} response {process.response_time}")

def main():
    process_count, runfor, use, process_list = parse_input()
    if use.lower() == 'sjf':
        sjf_scheduler(process_list, runfor)
    else:
        print("Unsupported scheduling algorithm")

if __name__ == "__main__":
    main()