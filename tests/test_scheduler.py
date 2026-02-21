import unittest
from datetime import datetime, timedelta
from scheduler import CarbonAwareScheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = CarbonAwareScheduler(region='us-east-1', carbon_threshold=400)
        self.job_ran = False

    def mock_job(self):
        self.job_ran = True

    def test_schedule_immediate(self):
        # Current mock intensity is 350, threshold is 400
        # Should run immediately
        deadline = datetime.now() + timedelta(hours=4)
        result = self.scheduler.schedule_batch_job("test-job", deadline, self.mock_job)
        self.assertTrue(result)
        self.assertTrue(self.job_ran)

    def test_defer_dirty_grid(self):
        # Set threshold below current mock intensity (350)
        self.scheduler.carbon_threshold = 300
        deadline = datetime.now() + timedelta(hours=4)
        result = self.scheduler.schedule_batch_job("test-job", deadline, self.mock_job)
        self.assertFalse(result)
        self.assertFalse(self.job_ran)

    def test_run_near_deadline(self):
        # Even if grid is dirty, if deadline is near, run it
        self.scheduler.carbon_threshold = 300
        # Deadline 1 hour from now (buffer is 2 hours)
        deadline = datetime.now() + timedelta(hours=1)
        result = self.scheduler.schedule_batch_job("test-job", deadline, self.mock_job)
        self.assertTrue(result)
        self.assertTrue(self.job_ran)

if __name__ == '__main__':
    unittest.main()
