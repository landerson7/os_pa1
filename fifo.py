from data_struct import Process
'''

link to conversation: https://chatgpt.com/share/66fb83f9-7df8-800b-95cf-ba69fdc4ac75
This link includes the basic data structure and the start of the FIFO algorithm since
I could not create the fifo scheduler without a basic data structure

'''
def fifo_scheduler(process_list):
    """
    First In First Out (FIFO) scheduling algorithm.
    """
    # Sort processes by arrival time
    process_list.sort(key=lambda p: p.arrival_time)
    
    current_time = 0
    for process in process_list:
        # If CPU is idle, advance current time to the arrival time of the process
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        # Calculate waiting time and response time
        process.waiting_time = current_time - process.arrival_time
        process.response_time = current_time - process.arrival_time  # In FIFO, response time equals waiting time
        
        # Update process status to 'running'
        process.update_status('running')
        
        # Simulate execution
        process_start_time = current_time
        current_time += process.execution_time
        process.cpu_usage = process.execution_time
        process.remaining_time = 0
        process.program_counter += process.execution_time  # Simplified increment
        
        # Update turnaround time
        process.turnaround_time = current_time - process.arrival_time
        
        # Update process status to 'terminated'
        process.update_status('terminated')
        
        # Output process execution details
        print(f"Process {process.pid} executed from time {process_start_time} to {current_time}")
    
    # Print summary of all processes
    print("\nProcess Execution Summary:")
    print("PID\tArrival\tExecution\tWaiting\tTurnaround\tResponse")
    for process in process_list:
        print(f"{process.pid}\t{process.arrival_time}\t{process.execution_time}\t\t{process.waiting_time}\t{process.turnaround_time}\t\t{process.response_time}")
    
if __name__ == "__main__":
    # Create a list of processes
    processes = [
        Process(pid=1, arrival_time=0, execution_time=5),
        Process(pid=2, arrival_time=2, execution_time=3),
        Process(pid=3, arrival_time=4, execution_time=1),
        Process(pid=4, arrival_time=6, execution_time=2),
    ]
    
    # Run FIFO scheduler
    fifo_scheduler(processes)
