
from data_struct import Process

def sjf_scheduler(process_list):
    """
    Preemptive Shortest Job First (SJF) scheduling algorithm.
    """
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
        
        # Sort ready queue by remaining time (SJF)
        ready_queue.sort(key=lambda p: p.remaining_time)

        if ready_queue:
            # Select the process with the shortest remaining burst time
            current_process = ready_queue.pop(0)

            # If CPU is idle, set current time to the process arrival time
            if current_time < current_process.arrival_time:
                current_time = current_process.arrival_time

            # If it's the first time this process is selected, set response time
            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time

            # Run the process for 1 unit of time (since it's preemptive)
            process_start_time = current_time
            current_time += 1
            current_process.remaining_time -= 1
            current_process.cpu_usage += 1

            # If the process is finished
            if current_process.remaining_time == 0:
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                current_process.update_status('terminated')
                completed_processes.append(current_process)

                print(f"Process {current_process.pid} finished at time {current_time}")
            else:
                # Put back in the ready queue if not finished
                ready_queue.append(current_process)
        else:
            # If no process is ready, advance time and print "Idle"
            print(f"Time {current_time}: Idle")
            current_time += 1

    # Print summary of all processes
    print("\nProcess Execution Summary:")
    print("PID\tArrival\tExecution\tWaiting\tTurnaround\tResponse")
    for process in process_list:
        print(f"{process.pid}\t{process.arrival_time}\t{process.execution_time}\t\t{process.waiting_time}\t{process.turnaround_time}\t\t{process.response_time}")

if __name__ == "__main__":
    # Create a list of processes
    processes = [
        Process(pid=1, arrival_time=0, execution_time=5),
        Process(pid=2, arrival_time=1, execution_time=4),
        Process(pid=3, arrival_time=4, execution_time=2),
    ]
    
    # Run SJF scheduler
    sjf_scheduler(processes)
