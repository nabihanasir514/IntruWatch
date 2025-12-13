import streamlit as st
import json
import os


def signup_checkin():
    class CheckInNode:
        def __init__(self, username, reg_no, designation, gender):
            self.username = username
            self.reg_no = reg_no
            self.designation = designation
            self.gender = gender
            self.next = None


    class Student:
        def __init__(self, reg_no, room_no):
            self.reg_no = reg_no
            self.room_no = room_no


    class Faculty:
        def __init__(self, employee_no):
            self.employee_no = employee_no


    # ================== LINKED LIST ==================
    head = None


    def register(name, reg_no, designation, gender, room_no=None, employee_no=None):
        global head

        new_node = CheckInNode(name, reg_no, designation, gender)

        if designation == "Student":
            student = Student(reg_no, room_no)

        elif designation == "Faculty":
            faculty = Faculty(employee_no)

        new_node.next = head
        head = new_node


    def check_out(name, reg_no,designation, room_no):
        temp = head
        while temp:
            if (
                temp.username == name
                and temp.reg_no == reg_no
                and temp.designation == designation
                and temp.room_no == room_no
            ):
                return True
            temp = temp.next
        return False
    def sign_up(name, reg_no, designation, gender, room_no=None, employee_no=None):
        register(name, reg_no, designation, gender, room_no, employee_no)


    # ================== STREAMLIT UI ==================

    st.markdown(
        """
        <style>
        .stApp { background-color: #111111; }
        .stSidebar { background-color: #483490; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Register GIKI Residents")

    optionDesignation = st.selectbox("Designation", ["Student", "Faculty"])
    username = st.text_input("Username")

    reg_no = None
    room_no = None
    employee_no = None

    if optionDesignation == "Student":
        reg_no = st.text_input("Registration Number")
        room_no = st.text_input("Room Number (Hostel)")
    elif optionDesignation == "Faculty":
        reg_no = st.text_input("Employee ID")
        employee_no = st.text_input("Residential Number")

    gender_option = st.selectbox("Gender", ["Male", "Female"])
    gender = "M" if gender_option == "Male" else "F"

    if st.button("Sign Up"):
        if username and reg_no:
            sign_up(username, reg_no, optionDesignation, gender, room_no, employee_no)
            st.success("Account successfully created")
        else:
            st.warning("Please fill all required fields")
   


        