# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from fastapi import FastAPI
from datetime import datetime, timedelta

class Doctor:
    def __init__(self, id, name, speciality, max_patients_per_day, bookings_left):
        self.id = id
        self.name = name
        self.speciality = speciality
        self.max_patients_per_day = max_patients_per_day
        self.bookings_left = bookings_left

class Appointment:
    def __init__(self, id, doctor_id, patient_name, appointment_date):
        self.id = id
        self.doctor_id = doctor_id
        self.patient_name = patient_name
        self.appointment_date = appointment_date



doctors_db = [
    Doctor(id = 1, name = "Dr. Pankaj", speciality = "Cardiology", max_patients_per_day = 5, bookings_left = {"Monday": 5, "Tuesday": 4, "Wednesday": 5, "Thursday": 5, "Friday": 5, "Saturday": 5}),
    Doctor(id = 2, name = "Dr. Snehal", speciality = "Dermatology", max_patients_per_day = 10, bookings_left = {"Monday": 9, "Tuesday": 10, "Wednesday": 10, "Thursday": 10, "Friday": 10, "Saturday": 10}),
    Doctor(id = 3, name = "Dr. Geeta", speciality = "Gynecology", max_patients_per_day = 4, bookings_left = {"Monday": 4, "Tuesday": 4, "Wednesday": 4, "Thursday": 4, "Friday": 4, "Saturday": 4}),
    Doctor(id = 4, name = "Dr. Atharva", speciality = "Neurology", max_patients_per_day = 8, bookings_left = {"Monday": 8, "Tuesday": 8, "Wednesday": 8, "Thursday": 8, "Friday": 8, "Saturday": 8}),
    Doctor(id = 5, name = "Dr. Yashwant", speciality = "Pediatrics", max_patients_per_day = 15, bookings_left = {"Monday": 15, "Tuesday": 15, "Wednesday": 15, "Thursday": 15, "Friday": 15, "Saturday": 15})]

appointment_db = [
    Appointment(id = 1, doctor_id = 1, patient_name="Dheeraj", appointment_date="2024-04-23"),
    Appointment(id = 2, doctor_id=2, patient_name="Bob", appointment_date="2024-04-22")]
 


app = FastAPI()

@app.get("/doctors")
async def get_doctors():
    return doctors_db

@app.get("/doctors/{doctor_id}")
async def get_details(doctor_id: int):
    for doctor in doctors_db:
        if doctor.id == doctor_id:
            return doctor
    return {"error": "Doctor not found"}

@app.get("/{doctor_id}/availability")
async def get_availability(doctor_id: int):
    for doctor in doctors_db:
        if doctor.id == doctor_id:
            return doctor.bookings_left
    return {"error": "Doctor not found"}

@app.post("/book-appointment")
async def book_appointment(doctor_id: int, patient_name: str, appointment_date: str):
    for doctor in doctors_db:
        if doctor.id == doctor_id:
            doctor_needed = doctor
    if not doctor_needed:
        return {"error": "Doctor not found"}
    else:
        input_date = datetime.strptime(appointment_date, "%Y-%m-%d")

        today = datetime.now()
        next_week = today + timedelta(days=7)

        if today < input_date <= next_week:
            input_day = input_date.strftime("%A")
            if input_day in doctor_needed.bookings_left:
                if doctor_needed.bookings_left[input_day] != 0:
                    appointment_id = len(appointment_db) + 1
                    new_appointment = Appointment(id = appointment_id, doctor_id = doctor_id, patient_name = patient_name, appointment_date = appointment_date)
                    appointment_db.append(new_appointment)
                    doctor_needed.bookings_left[input_day] = doctor_needed.bookings_left[input_day] - 1
                    return {"message": f"Appointment booked successfully! Appointment ID: {appointment_id}"}
                else:
                    return {"error": "Doctor booked for the day. Please check availability for a different day."}
            else:
                return {"error": "Doctor not available on Sundays."}
        else:
            return {"error": "Invalid appointment date. Please choose a date within the next 7 days."}
        
@app.get("/all-appointments")
async def get_appointments():
    return appointment_db
    
    
     




































