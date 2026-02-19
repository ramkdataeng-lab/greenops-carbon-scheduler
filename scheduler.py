import requests
import time
from datetime import datetime, timedelta

class CarbonAwareScheduler:
    """
    A scheduler that defers batch workloads based on real-time grid carbon intensity.
    Implements the 'Green Window' logic from the GreenOps Framework.
    """
    
    def __init__(self, region='us-east-1', carbon_threshold=400):
        self.region = region
        self.carbon_threshold = carbon_threshold
        self.api_url = "https://api.carbon-aware-sdk.com/emissions" # Placeholder API
    
    def get_grid_carbon_intensity(self):
        """
        Fetches the current carbon intensity (gCO2eq/kWh) for the region.
        In a real implementation, you would use an API key for ElectricityMaps or WattTime.
        """
        try:
            # Simulated response for demonstration purposes
            # response = requests.get(f"{self.api_url}/{self.region}")
            # return response.json()['carbon_intensity']
            print(f"Checking grid intensity for {self.region}...") 
            return 350 # Mock value: assume moderate grid intensity
        except Exception as e:
            print(f"Error fetching grid data: {e}")
            return 0 # Fail open (allow job to run) if API is down

    def schedule_batch_job(self, job_id, sla_deadline, job_func):
        """
        Determines whether to run a job now or defer it based on carbon intensity.
        
        :param job_id: Unique identifier for the job
        :param sla_deadline: datetime object representing the latest time the job can finish
        :param job_func: The function to execute if the window is green
        """
        current_intensity = self.get_grid_carbon_intensity()
        print(f"Current Grid Intensity: {current_intensity} gCO2/kWh")
        
        # Check if the grid is "dirty"
        if current_intensity > self.carbon_threshold:
            time_remaining = sla_deadline - datetime.now()
            
            # If we have a safe buffer (e.g., > 2 hours), defer the job
            if time_remaining > timedelta(hours=2):
                print(f"⚠️  Grid is dirty (> {self.carbon_threshold} gCO2/kWh). Deferring job {job_id}.")
                print(f"   Time remaining before SLA breach: {time_remaining}")
                print(f"   Action: Suggest rescheduling for +1 hour.")
                return False # Job was deferred

        # If grid is green OR deadline is approaching, run it now
        print(f"✅ Executing job {job_id}. Intensity is acceptable or deadline is near.")
        job_func()
        return True

# Example Usage
if __name__ == "__main__":
    def my_etl_job():
        print("   [System] Running ETL Pipeline...")
    
    scheduler = CarbonAwareScheduler(region='us-east-1', carbon_threshold=300)
    
    # Define an SLA deadline 4 hours from now
    deadline = datetime.now() + timedelta(hours=4)
    
    scheduler.schedule_batch_job("ETL-Daily-001", deadline, my_etl_job)
