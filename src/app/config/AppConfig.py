"""
Global configuration values utilised by the appliction
"""

# DB config
mongo_db_username = "****"
mongo_db_password = "****"

# the interval in seconds between reading items from the queue
sensor_read_interval_seconds = 0
# the interval in seconds between writing items to the queue
sensor_write_interval_seconds = 0

# The max number items written to the queue
max_queue_size = 5

# The number of read and write processes that operate on the shared queue
number_read_processes = 3
number_write_processes = 2



