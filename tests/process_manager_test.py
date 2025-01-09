import unittest
from anchorscad_lib.utils.process_manager import ProcessManager, ProcessManagerEntry
from dataclasses import dataclass
import sys

@dataclass
class TstProcessEntry(ProcessManagerEntry):
    """Test process entry that records start/end events"""
    started_called: bool = False
    ended_called: bool = False
    end_status: int = None
    
    def started(self):
        self.started_called = True
    
    def ended(self, status):
        self.ended_called = True
        self.end_status = status


class ProcessManagerTest(unittest.TestCase):
    
    def test_basic_process_flow(self):
        # Create process manager with small max jobs for testing
        pm = ProcessManager(max_jobs=2)
        
        # Create test process that just sleeps briefly
        entry = TstProcessEntry()
        pm.run_proc(entry, [sys.executable, '-c', 'import time; time.sleep(0.1)'])
        
        # Verify process started
        self.assertTrue(entry.started_called)
        self.assertFalse(entry.ended_called)
        
        # Wait for completion
        succeed_count, failed_count = pm.finished_status()
        
        # Verify process completed successfully
        self.assertEqual(succeed_count, 1)
        self.assertEqual(failed_count, 0)
        self.assertTrue(entry.ended_called)
        self.assertEqual(entry.end_status, 0)

    def test_multiple_processes(self):
        pm = ProcessManager(max_jobs=2)
        entries = []
        
        # Start 3 processes (more than max_jobs)
        for _ in range(3):
            entry = TstProcessEntry()
            entries.append(entry)
            pm.run_proc(entry, [sys.executable, '-c', 'import time; time.sleep(0.1)'])
            
        # Verify only max_jobs processes started initially
        running_count = len([e for e in entries if e.started_called and not e.ended_called])
        self.assertLessEqual(running_count, 2)
        
        # Wait for all to complete
        succeed_count, failed_count = pm.finished_status()
        
        self.assertEqual(succeed_count, 3)
        self.assertEqual(failed_count, 0)
        
        # Verify all processes completed
        for entry in entries:
            self.assertTrue(entry.started_called)
            self.assertTrue(entry.ended_called)
            self.assertEqual(entry.end_status, 0)

    def test_failed_process(self):
        pm = ProcessManager()
        entry = TstProcessEntry()
        
        # Run process that exits with error
        pm.run_proc(entry, [sys.executable, '-c', 'exit(1)'])
        
        succeed_count, failed_count = pm.finished_status()
        
        self.assertEqual(succeed_count, 0)
        self.assertEqual(failed_count, 1)
        self.assertTrue(entry.ended_called)
        self.assertEqual(entry.end_status, 1)

    def test_wait_for_completions(self):
        pm = ProcessManager(max_jobs=2)
        entries = []
        
        # Start processes
        for _ in range(3):
            entry = TstProcessEntry()
            entries.append(entry)
            pm.run_proc(entry, [sys.executable, '-c', 'import time; time.sleep(0.1)'])
        
        # Wait for count to drop below 2
        count = pm.wait_for_completions(1)
        self.assertLessEqual(count, 1)
        
        # Wait for all to complete
        count = pm.wait_for_completions(0)
        self.assertEqual(count, 0)

if __name__ == '__main__':
    unittest.main() 