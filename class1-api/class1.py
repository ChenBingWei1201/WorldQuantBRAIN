import requests
from getpass import getpass
from time import sleep

MAX_SIM = 3;
LOGIN_URL = "https://api.worldquantbrain.com/authentication"
SIMULATION_URL = "https://api.worldquantbrain.com/simulations"
ALPHA_URL = "https://api.worldquantbrain.com/alphas"

EMAIL = "rain4030633@gmail.com"
PASSWORD = getpass("Enter your password: ")

# Login:

sess = requests.Session()

sess.auth = (EMAIL, PASSWORD)

login_request = sess.post(LOGIN_URL)

print(login_request.status_code, login_request.headers)

# Simulation:

simulation_data = {
    "type": "REGULAR",
    "settings": {
        "nanHandling": "OFF",
        "instrumentType": "EQUITY",
        "delay": 1,
        "universe": "TOP3000",
        "truncation": 0.08,
        "unitHandling": "VERIFY",
        "pasteurization": "ON",
        "region": "USA",
        "language": "FASTEXPR",
        "decay": 0,
        "neutralization": "SUBINDUSTRY",
        "visualization": False
    },
    "regular": "ts_rank(operating_income,252)"
}

simulation_response = sess.post(SIMULATION_URL, json=simulation_data)

print(simulation_response.headers["location"])

simulation_progress_url = simulation_response.headers["location"]
finished = False
while True:
    simulation_progress = sess.get(simulation_progress_url)
    if simulation_progress.headers.get("Retry-After", 0) == 0:
        break
    print("Sleeping for " + simulation_progress.headers["Retry-After"], "seconds")
    sleep(float(simulation_progress.headers["Retry-After"]))
print("Alpha done simulating, getting alpha details")
alpha_id = simulation_progress.json()["alpha"]
alpha = sess.get(f"{ALPHA_URL}/{alpha_id}")

# Alpha:
template = "<group_operater>(<ts_operator>(<compare_operator>(<flow_data>, <debt_data>), <days>), <group>)"

alpha_1_param = {
    "<group_operater>": "group_zscore",
    "<ts_operator>": "ts_sum",
}
