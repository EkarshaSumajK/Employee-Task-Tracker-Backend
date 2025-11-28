import requests
import json
import random

BASE_URL = "http://localhost:8000/api/v1"

def print_result(endpoint, method, status, response_json):
    print(f"--- {method} {endpoint} ---")
    print(json.dumps(response_json, indent=2))
    print("\n")

def run_tests():
    # 1. Login
    login_data = {"username": "admin", "password": "admin123"}
    try:
        response = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
        if response.status_code == 200:
            resp_json = response.json()
            print_result("/login/access-token", "POST", response.status_code, resp_json)
            
            # Extract token from new format
            if "data" in resp_json and "access_token" in resp_json["data"]:
                token = resp_json["data"]["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
            else:
                print("Failed to extract token from response")
                return
        else:
            print_result("/login/access-token", "POST", response.status_code, response.text)
            return
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return

    # 2. Users
    # GET /users/
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print_result("/users/", "GET", response.status_code, response.json())

    # POST /users/
    new_user = {
        "username": f"user_{random.randint(10000,99999)}",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=new_user, headers=headers)
    print_result("/users/", "POST", response.status_code, response.json())
    
    user_id = None
    if response.status_code == 200:
        resp_json = response.json()
        if "data" in resp_json and "id" in resp_json["data"]:
            user_id = resp_json["data"]["id"]

    if user_id:
        # GET /users/{id}
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        print_result(f"/users/{user_id}", "GET", response.status_code, response.json())

        # PUT /users/{id}
        update_data = {"password": "newpassword456"}
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data, headers=headers)
        print_result(f"/users/{user_id}", "PUT", response.status_code, response.json())

        # DELETE /users/{id}
        response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
        print_result(f"/users/{user_id}", "DELETE", response.status_code, response.json())

    # 3. Employees
    # GET /employees/
    response = requests.get(f"{BASE_URL}/employees/", headers=headers)
    print_result("/employees/", "GET", response.status_code, response.json())

    # POST /employees/
    new_emp = {
        "name": "Test Employee",
        "role": "Tester",
        "email": f"test_{random.randint(10000,99999)}@example.com"
    }
    response = requests.post(f"{BASE_URL}/employees/", json=new_emp, headers=headers)
    print_result("/employees/", "POST", response.status_code, response.json())

    emp_id = None
    if response.status_code == 200:
        resp_json = response.json()
        if "data" in resp_json and "id" in resp_json["data"]:
            emp_id = resp_json["data"]["id"]

    if emp_id:
        # GET /employees/{id}
        response = requests.get(f"{BASE_URL}/employees/{emp_id}", headers=headers)
        print_result(f"/employees/{emp_id}", "GET", response.status_code, response.json())

        # PUT /employees/{id}
        update_data = {"role": "Senior Tester"}
        response = requests.put(f"{BASE_URL}/employees/{emp_id}", json=update_data, headers=headers)
        print_result(f"/employees/{emp_id}", "PUT", response.status_code, response.json())

        # DELETE /employees/{id}
        response = requests.delete(f"{BASE_URL}/employees/{emp_id}", headers=headers)
        print_result(f"/employees/{emp_id}", "DELETE", response.status_code, response.json())

    # 4. Tasks
    # GET /tasks/
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print_result("/tasks/", "GET", response.status_code, response.json())

    # POST /tasks/
    # Need an employee ID. Fetch one.
    emp_resp = requests.get(f"{BASE_URL}/employees/", headers=headers).json()
    if emp_resp.get("data"):
        employee_id = emp_resp["data"][0]['id']
        new_task = {
            "title": "Test Task",
            "description": "Testing API",
            "status": "Pending",
            "employee_id": employee_id
        }
        response = requests.post(f"{BASE_URL}/tasks/", json=new_task, headers=headers)
        print_result("/tasks/", "POST", response.status_code, response.json())

        task_id = None
        if response.status_code == 200:
            resp_json = response.json()
            if "data" in resp_json and "id" in resp_json["data"]:
                task_id = resp_json["data"]["id"]
        
        if task_id:
            # GET /tasks/{id}
            response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
            print_result(f"/tasks/{task_id}", "GET", response.status_code, response.json())

            # PUT /tasks/{id}
            update_data = {"status": "In Progress"}
            response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
            print_result(f"/tasks/{task_id}", "PUT", response.status_code, response.json())

            # DELETE /tasks/{id}
            response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
            print_result(f"/tasks/{task_id}", "DELETE", response.status_code, response.json())

    # 5. Stats
    response = requests.get(f"{BASE_URL}/stats/dashboard", headers=headers)
    print_result("/stats/dashboard", "GET", response.status_code, response.json())

    # 6. Company
    response = requests.get(f"{BASE_URL}/company/overview", headers=headers)
    print_result("/company/overview", "GET", response.status_code, response.json())

if __name__ == "__main__":
    run_tests()
