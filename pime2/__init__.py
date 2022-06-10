"""
pime 2 module

"""

# Regex constants
NAME_REGEX = r"^[a-zA-Z0-9_.-]{3,128}$"
# used in "where" e.g.
CHAINED_NAME_REGEX = r"^[a-zA-Z0-9_.-]{3,128}(\s*,\s*[a-zA-Z0-9_.-]{3,128})*,?$"
BASE64_REGEX = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"

# Request/Response/Task timeouts
# in seconds
NEIGHBOR_DISCOVER_PING_TIMEOUT = 0.5
ROUTER_LOOP_TASK_TIMEOUT = 600
MESSAGE_SENDING_REMOTE_TIMEOUT = 30
