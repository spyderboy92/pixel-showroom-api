import multiprocessing

# Use all available CPU cores
workers = multiprocessing.cpu_count() * 2 + 1
threads = 4  # Threads per worker
bind = "0.0.0.0:5000"
timeout = 120  # Timeout in seconds
worker_connections = 10  # Max simultaneous connections
loglevel = "info"  # Log level
preload_app = True  # Preload application for faster worker start
