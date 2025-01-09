# anchorscad_lib.utils.process_manager

The `process_manager` module provides a system for managing and executing multiple subprocesses concurrently, with a limit on the number of processes that can run simultaneously. This is useful for efficiently utilizing system resources when performing batch processing tasks.

anchorscad_runner uses this when recursively loading every module in a folder and rendering 
all the located shapes. It will use a process for each available CPU core (minus one).

## Main Features

- Manage concurrent execution of subprocesses
- Limit the number of simultaneous processes
- Automatically wait for processes to complete when the limit is reached
- Track the status of each process

## Basic Usage

```python
from anchorscad_lib.utils.process_manager import ProcessManager, ProcessManagerEntry

# Define a custom entry class
class MyProcessEntry(ProcessManagerEntry):
    def started(self):
        print("Process started")

    def ended(self, status):
        print(f"Process ended with status {status}")

# Create a process manager
manager = ProcessManager(max_jobs=4)

# Run a process
entry = MyProcessEntry()
manager.run_proc(entry, ['ls', '-l'])
```

## ProcessManager Class

The `ProcessManager` class is responsible for managing the execution of subprocesses.

### Key Methods

- `run_proc(proc_entry, *args, **kwargs)`: Starts a new subprocess. If the maximum number of concurrent processes is reached, it waits for some to complete.
- `count_procs()`: Returns the number of currently running processes.
- `wait_for_completions(max_count=None)`: Waits for the number of active processes to drop below `max_count`.
- `finished_status()`: Waits for all processes to finish and returns the number of successful and failed jobs.

### Initialization Parameters

- `max_jobs`: Maximum number of concurrent processes (default is the number of CPU cores minus one).
- `poll_time`: Time interval (in seconds) to wait between checks for process completion.

## ProcessManagerEntry Class

The `ProcessManagerEntry` class represents an entry in the process manager. It should be extended by clients to define custom behavior for process start and end events.

### Key Methods

- `started()`: Called just before the process is created.
- `set_popen_obj(popen_obj)`: Called with the `Popen` object after the process is started.
- `ended(status)`: Called when the process ends, with the termination status.

## Example Usage

### Running Multiple Processes

```python
from anchorscad_lib.utils.process_manager import ProcessManager, ProcessManagerEntry

class MyProcessEntry(ProcessManagerEntry):
    def started(self):
        print("Process started")

    def ended(self, status):
        print(f"Process ended with status {status}")

manager = ProcessManager(max_jobs=2)

# Run multiple processes
for i in range(5):
    entry = MyProcessEntry()
    manager.run_proc(entry, ['echo', f'Process {i}'])

# Wait for all processes to finish
success, failure = manager.finished_status()
print(f"Success: {success}, Failure: {failure}")
```

## Technical Details

- Uses Python's `subprocess.Popen` for process creation and management.
- Automatically adjusts the number of concurrent processes based on system capabilities.
- Provides hooks for custom behavior on process start and end.

## Error Handling

The module does not explicitly handle exceptions from subprocesses. It is recommended to implement error handling in the `ended` method of `ProcessManagerEntry` subclasses.

## Installation

```bash
pip install anchorscad-utils
```
 