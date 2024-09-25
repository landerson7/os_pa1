class Process:
    def __init__(self, pid, arrival_time, execution_time, priority=0):
        self.pid = pid  # Unique Process ID
        self.arrival_time = arrival_time  # Time when process arrives in the system
        self.execution_time = execution_time  # Total CPU time required
        self.remaining_time = execution_time  # Remaining CPU time
        self.priority = priority  # Priority of the process (lower number means higher priority)
        self.status = 'new'  # Current status: new, ready, running, waiting, terminated
        self.program_counter = 0  # Address of the next instruction to execute
        self.registers = {}  # Simulated CPU registers
        self.memory_requirements = 0  # Amount of memory required
        self.open_files = []  # List of open files
        self.io_devices = []  # List of I/O devices allocated
        self.cpu_usage = 0  # Total CPU time used so far
        self.waiting_time = 0  # Total time spent waiting
        self.turnaround_time = 0  # Total time from arrival to completion
        self.response_time = None  # Time from arrival to first execution

    def update_status(self, new_status):
        """Update the process status."""
        self.status = new_status

    def execute(self, time_slice):
        """
        Simulate process execution for a given time slice.
        """
        if self.status in ['new', 'ready', 'waiting']:
            self.status = 'running'
            if self.response_time is None:
                self.response_time = current_time - self.arrival_time  # current_time needs to be defined

        actual_execution = min(self.remaining_time, time_slice)
        self.remaining_time -= actual_execution
        self.cpu_usage += actual_execution
        self.program_counter += actual_execution  # Simplified increment

        if self.remaining_time == 0:
            self.status = 'terminated'
            self.turnaround_time = current_time - self.arrival_time  # current_time needs to be defined

    # Additional methods and attributes can be added as needed.

