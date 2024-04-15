import os

# Get the number of CPU cores
cpu_cores = os.cpu_count()

# Determine the number of workers based on CPU cores
workers = cpu_cores * 2 + 1

# Set the number of threads per worker
threads = min(4, cpu_cores)  # Limit threads to a reasonable number, e.g., 4 or the number of CPU cores

# Bind to 0.0.0.0:8080 for external access
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')

# Allow all IPs in X-Forwarded-For header
forwarded_allow_ips = '*'

# Specify headers for secure scheme
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}
