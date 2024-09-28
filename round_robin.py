def round_robin_scheduler(process_list, quantum):
    """
    Round Robin (RR) scheduling algorithm.
    Each process is given a fixed time quantum for execution.
    """
    print(f"{len(process_list)} processes")
    print("Using Round Robin")
    print(f"Quantum {quantum}")

    # Sort processes by arrival time initially
    process_list.sort(key=lambda p: p.arrival_time)

    current_time = 0
    queue = []  # A queue to hold processes that are ready to execute
    completed_processes = []
    idle_time = 0

    # Keep track of when each process first starts executing
    first_execution = {p.pid: None for p in process_list}

    while process_list or queue:
        # Add new processes that have arrived by the current time to the queue
        while process_list and process_list[0].arrival_time <= current_time:
            new_process = process_list.pop(0)
            queue.append(new_process)
            print(f"Time {current_time:4}: {new_process.pid} arrived")

        # If no processes are ready, the CPU is idle
        if not queue:
            print(f"Time {current_time:4}: Idle")
            idle_time += 1
            current_time += 1
            continue

        # Select the first process in the queue
        current_process = queue.pop(0)

        # If the process hasn't been executed yet, log its start time (response time)
        if first_execution[current_process.pid] is None:
            first_execution[current_process.pid] = current_time
            current_process.response_time = current_time - current_process.arrival_time

        print(f"Time {current_time:4}: {current_process.pid} selected (remaining burst {current_process.remaining_time})")

        # Process execution: Execute the process for a time slice (quantum) or until completion, whichever comes first
        if current_process.remaining_time <= quantum:
            # Process completes within this time slice
            current_time += current_process.remaining_time
            current_process.cpu_usage += current_process.remaining_time
            current_process.remaining_time = 0
            current_process.turnaround_time = current_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
            print(f"Time {current_time:4}: {current_process.pid} finished")
            completed_processes.append(current_process)
        else:
            # Process is preempted after using the quantum
            current_time += quantum
            current_process.remaining_time -= quantum
            current_process.cpu_usage += quantum
            queue.append(current_process)  # Put the process back into the queue for the next round

    # Output the final metrics for each process
    for process in completed_processes:
        print(f"{process.pid} wait {process.waiting_time} turnaround {process.turnaround_time} response {process.response_time}")

    # If there was any idle time at the end
    if idle_time > 0:
        print(f"Idle for {idle_time} time units")

# Now this Round Robin scheduler function can be integrated into the larger scheduling system.
