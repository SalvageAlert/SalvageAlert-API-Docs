"""Free call: your plan, balance and rate limit. Python 3.9+, standard library only."""
from salvagealert import call

data, _ = call("GET", "/me")
print(data)
