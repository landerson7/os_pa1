class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.pid = pid  # Process ID
        self.arrival_time = arrival_time  # Arrival time
        self.execution_time = execution_time  # Burst time (execution time)
        self.remaining_time = execution_time  # Remaining burst time
        self.status = 'new'  # Process status: new, ready, running, terminated
        self.response_time = -1  # Time from arrival to first execution
        self.waiting_time = 0  # Total time spent waiting
        self.turnaround_time = 0  # Total time from arrival to completion
        self.cpu_usage = 0  # Total CPU time used so far
    
    def update_status(self, new_status):
        self.status = new_status


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


def round_robin_scheduler(process_list, time_slice):
    """
    Round Robin scheduling algorithm with a time slice (Q-value).
    """
    print(f"{len(process_list)} processes")
    print(f"Using Round Robin with time slice = {time_slice}")
    
    process_list.sort(key=lambda p: p.arrival_time)
    ready_queue = []
    current_time = 0
    completed_processes = []

    while len(completed_processes) < len(process_list):
        # Add all processes that have arrived by current_time to the ready queue
        for process in process_list:
            if process.arrival_time <= current_time and process not in ready_queue and process not in completed_processes:
                ready_queue.append(process)
                print(f"Time {current_time:4}: {process.pid} arrived")

        if ready_queue:
            current_process = ready_queue.pop(0)

            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time

            run_time = min(current_process.remaining_time, time_slice)
            print(f"Time {current_time:4}: {current_process.pid} selected (burst {current_process.remaining_time:4})")
            
            current_time += run_time
            current_process.remaining_time -= run_time

            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                completed_processes.append(current_process)
                print(f"Time {current_time:4}: {current_process.pid} finished")
            else:
                ready_queue.append(current_process)
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


# Example main function to run the schedulers
if __name__ == "__main__":
    # FIFO Scheduler Example
    fifo_processes = [
        Process(pid='A', arrival_time=0, execution_time=5),
        Process(pid='B', arrival_time=1, execution_time=4),
        Process(pid='C', arrival_time=4, execution_time=2),
    ]
    print("FIFO Scheduler Output:")
    fifo_scheduler(fifo_processes)

    # SJF Scheduler Example
    print("\nSJF Scheduler Output:")
    sjf_processes = [
        Process(pid='A', arrival_time=0, execution_time=5),
        Process(pid='B', arrival_time=1, execution_time=4),
        Process(pid='C', arrival_time=4, execution_time=2),
    ]
    sjf_scheduler(sjf_processes)

    # Round Robin Scheduler Example with time slice = 2
    print("\nRound Robin Scheduler Output:")
    rr_processes = [
        Process(pid='A', arrival_time=0, execution_time=5),
        Process(pid='B', arrival_time=1, execution_time=4),
        Process(pid='C', arrival_time=4, execution_time=2),
    ]
    round_robin_scheduler(rr_processes, time_slice=2)
