import json
from pathlib import Path

# -------------------------
# Base Class
# -------------------------
class Person:
    """Base class for Patient and Doctor"""
    def __init__(self, name, unique_id):
        self.name = name
        self.unique_id = unique_id

    def __str__(self):
        return f"{self.unique_id} - {self.name}"

    def __repr__(self):
        return self.__str__()


# -------------------------
# Patient Class
# -------------------------
class Patient(Person):
    def __init__(self, name, patient_id, age, disease, status="Admitted", doctor_id=None):
        super().__init__(name, patient_id)
        self.age = age
        self.disease = disease
        self.status = status
        self.doctor_id = doctor_id

    def admit(self):
        self.status = "Admitted"

    def discharge(self):
        self.status = "Discharged"

    def assign_doctor(self, doctor_id):
        self.doctor_id = doctor_id

    def to_dict(self):
        return {
            "name": self.name,
            "patient_id": self.unique_id,
            "age": self.age,
            "disease": self.disease,
            "status": self.status,
            "doctor_id": self.doctor_id
        }


# -------------------------
# Doctor Class
# -------------------------
class Doctor(Person):
    def __init__(self, name, doctor_id, specialization):
        super().__init__(name, doctor_id)
        self.specialization = specialization

    def to_dict(self):
        return {
            "name": self.name,
            "doctor_id": self.unique_id,
            "specialization": self.specialization
        }


# -------------------------
# Hospital Management System
# -------------------------
class HospitalManagement:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.data_file = Path("hospital_records.json")

    # Add patient
    def add_patient(self):
        print("\n--- Add Patient ---")
        pid = input("Enter Patient ID: ")
        name = input("Enter name: ")
        age = input("Enter age: ")
        disease = input("Enter disease: ")
        self.patients[pid] = Patient(name, pid, age, disease)
        print("Patient added successfully.")

    # View patient list
    def view_patients(self):
        print("\n--- Patient List ---")
        if not self.patients:
            print("No patient data available.")
            return

        print(f"{'ID':<8} {'Name':<20} {'Age':<5} {'Disease':<15} {'Status':<12} {'Doctor':<10}")
        print("-" * 70)
        for p in self.patients.values():
            print(f"{p.unique_id:<8} {p.name:<20} {p.age:<5} {p.disease:<15} {p.status:<12} {p.doctor_id}")
        print("-" * 70)

    # Search patient
    def search_patient(self):
        keyword = input("Enter Patient ID or Name keyword: ").lower()
        results = [p for p in self.patients.values() if keyword in p.unique_id.lower() or keyword in p.name.lower()]

        if results:
            for p in results:
                print(p)
        else:
            print("Patient not found.")

    # Discharge
    def discharge_patient(self):
        pid = input("Enter Patient ID to discharge: ")
        if pid in self.patients:
            self.patients[pid].discharge()
            print("Patient discharged successfully.")
        else:
            print("Patient ID not found.")

    # Add doctor
    def add_doctor(self):
        print("\n--- Add Doctor ---")
        did = input("Enter Doctor ID: ")
        name = input("Enter Doctor Name: ")
        spec = input("Enter Specialization: ")
        self.doctors[did] = Doctor(name, did, spec)
        print("Doctor added successfully.")

    # View doctors
    def view_doctors(self):
        print("\n--- Doctor List ---")
        if not self.doctors:
            print("No doctor data available.")
            return

        print(f"{'ID':<8} {'Name':<20} {'Specialization':<15}")
        print("-" * 50)
        for d in self.doctors.values():
            print(f"{d.unique_id:<8} {d.name:<20} {d.specialization:<15}")
        print("-" * 50)

    # Assign doctor
    def assign_doctor(self):
        pid = input("Enter Patient ID: ")
        did = input("Enter Doctor ID: ")

        if pid not in self.patients:
            print("Patient not found.")
            return
        if did not in self.doctors:
            print("Doctor not found.")
            return

        self.patients[pid].assign_doctor(did)
        print("Doctor assigned successfully.")

    # Save data
    def save_data(self):
        data = {
            "patients": {pid: p.to_dict() for pid, p in self.patients.items()},
            "doctors": {did: d.to_dict() for did, d in self.doctors.items()}
        }

        try:
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print("Error saving file:", e)

    # Load data
    def load_data(self):
        if not self.data_file.exists():
            print("No saved data found.")
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)

            self.patients = {pid: Patient(**info) for pid, info in data["patients"].items()}
            self.doctors = {did: Doctor(**info) for did, info in data["doctors"].items()}

            print("Data loaded successfully.")
        except Exception as e:
            print("Error loading file:", e)


# -------------------------
# CLI Menu
# -------------------------
def menu():
    HMS = HospitalManagement()

    while True:
        print("\n======= Hospital Management System =======")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Discharge Patient")
        print("5. Add Doctor")
        print("6. View Doctors")
        print("7. Assign Doctor to Patient")
        print("8. Save Records")
        print("9. Load Records")
        print("0. Exit")

        ch = input("Enter choice: ")

        if ch == "1": HMS.add_patient()
        elif ch == "2": HMS.view_patients()
        elif ch == "3": HMS.search_patient()
        elif ch == "4": HMS.discharge_patient()
        elif ch == "5": HMS.add_doctor()
        elif ch == "6": HMS.view_doctors()
        elif ch == "7": HMS.assign_doctor()
        elif ch == "8": HMS.save_data()
        elif ch == "9": HMS.load_data()
        elif ch == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
