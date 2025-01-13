'''
Created on 28 Jan 2022

@author: gianni
'''

from dataclasses import dataclass, field
import os
from subprocess import Popen, TimeoutExpired
import time
import select

def _get_max_jobs():
    '''Determines the default number of outstanding processes to run.'''
    cores = os.cpu_count()
    if cores <= 2:
        return cores
    return cores - 1

DEFAULT_MAX_JOBS=_get_max_jobs()


@dataclass
class ProcessManagerEntry:
    '''Base class for a ProcessManager entry. This is extended by clients
    and notification of a terminated process is provided with the termination
    status.'''
    
    popen_obj: Popen=None
    stdout_chunks: list[bytes]=field(default_factory=list, init=False)
    stderr_chunks: list[bytes]=field(default_factory=list, init=False)

    def started(self):
        '''Called just before process is created.'''
        pass
    
    def set_popen_obj(self, popen_obj):
        '''Called with the Popen object, should set self.open_obj'''
        self.popen_obj = popen_obj
    
    def ended(self, status):
        pass
    
    def _ended(self, status):
        self.collect_io()
        self.ended(status)

    def collect_io(self):
        '''Collects the stdout and stderr from the process.'''
        if self.popen_obj is None:
            return

        try:
            self.popen_obj.communicate(timeout=0.01)
        except TimeoutExpired:
            return
    
    def raise_unknow_fd(self, fd):
        """Handles an unknown fd from select.poll()."""
        raise ValueError(f"Unknown fd: {fd}")
    
    def raise_unknow_event(self, event):
        """Handles an unknown event from select.poll()."""
        raise ValueError(f"Unknown event: {event}")
    
    def communicate(self):
        '''Communicates with the process.'''
        if self.popen_obj is None:
            return (None, None)
        self.collect_io()
        return self.popen_obj.communicate()

@dataclass
class ProcessManager:
    '''Allows for background execution of a limited number of processes.
    If run_proc() is called when max_jobs or more entries are running,
    it will wait until those processes finish.'''
    current_entries: list=field(default_factory=list)
    finished_entries: list=field(default_factory=list)
    max_jobs: int=DEFAULT_MAX_JOBS
    poll_time: float=0.2
    
    def run_proc(self, proc_entry: ProcessManagerEntry, *args, **kwargs) -> None:
        self.wait_for_completions()
        proc_entry.started()
        proc_entry.set_popen_obj(Popen(*args, **kwargs))
        self.current_entries.append(proc_entry)

    def count_procs(self) -> int:
        next_current_entries = []
        for p in self.current_entries:
            p.collect_io()
            status = p.popen_obj.poll()
            if status is None:
                next_current_entries.append(p)
            else:
                self.finished_entries.append(p)
                p._ended(p.popen_obj.wait())
                
        self.current_entries = next_current_entries
        return len(self.current_entries)
        
    def wait_for_completions(self, max_count: int=None) -> int:
        """Waits for the number of active jobs to drop below max_count.
        If max_count is None, it will wait for the the configured max_count
        which is defaulted to DEFAULT_MAX_JOBS which is the number of cores
        minus one.
        
        Returns the number of active jobs at the time of return.
        """
        if max_count is None:
            max_count = self.max_jobs - 1
        while True:
            count = self.count_procs()
            if count <= max_count:
                return count
            time.sleep(self.poll_time)

    def finished_status(self) -> tuple[int, int]:
        """Wait for all processes to finish and return the number of successful and
        failed jobs."""
        self.wait_for_completions(0)
        succeed_count = 0
        failed_count = 0
        for p in self.finished_entries:
            if p.popen_obj.wait():
                failed_count += 1
            else:
                succeed_count += 1
                
        return succeed_count, failed_count
