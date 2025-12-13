import streamlit as st
import numpy as np
# import cv2
import pandas as pd
from streamlit_navigation_bar import st_navbar
from streamlit_lottie import st_lottie

# from app.pages.Signup_CheckIn import signup_check_in
import time
from pathlib import Path
from datetime import datetime
#from pages.Login import login_function, signup_function
import heapq
from datetime import datetime
import time
# from pages.Login import signup_function
global choice1 ,choice,flaglogin
menu = ["Login Admin", "Check In","Check Out","About Us"] 
#-----------------PAGE CONFIGURATION AND STYLES-----------------
st.set_page_config(
    page_title="InTru Watch",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #07040f; 
    }
    .stSidebar {
        background-color:#0d0321; 
    }
    .stNavbar {
        background-color: #FFFFF;
    }
    .stText{
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'started' not in st.session_state:
    st.session_state.started = False

# Show welcome message only if not started
if not st.session_state.started:
    st.markdown("---")
    st.markdown('<p style= "text-align: center ; font-family:sans-serif; font-size: 90px; color: #3293a8;"><b> InTru Watch<b></p>', unsafe_allow_html=True)
    st.markdown("### Secure Campus with Real-Time Surveillance and Alerts")
    st.markdown("##### Welcome to InTru Watch, your trusted partner in campus security." \
                " Our advanced surveillance system leverages cutting-edge technology to ensure the safety and well-being of students, faculty, and staff." \
                " With real-time monitoring and instant alerts, InTru Watch provides a proactive approach to campus security, allowing for swift responses to potential threats." \
                " Experience peace of mind knowing that InTru Watch is dedicated to creating a secure environment for learning and growth.")
    
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .stButton>button{
            background-color: #00D4FF;
            justify-content: center;
            color: #000000;  
            font-size:40px;
            font-weight: bold;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-align: center;
        }
        </style>  
    """, unsafe_allow_html=True)
    
    button1 = st.button("       Lets Get Started!        ")
    
    if button1:
        st.session_state.started = True
        st.rerun()

#---------------------------------------------
# flaglogin = False
#---------------------------------------------
#-------chcek in logic---

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



def main():
    if st.session_state.started:
        #if st.session_state.get('logged_in', False):
            choice1 = st.sidebar.radio("Navigation", menu)
            if choice1 == "Login Admin":
                st.write("Admin Login Page")
                tab1, tab2 = st.tabs(["Login", "Sign Up"])
                #sign_up("admin", "admin123")  # Pre-populate with a default admin account for testing   
                with tab1:
                    st.write("Login Page")
                    
                    # login_function()
                   
                    flaglogin=st.button("Login Functionality Here")
                with tab2:
                     st.write("Sign Up Page")
                    # signup_function()
            elif choice1 == "Check In":
                st.write("Check In Page")
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
    
            elif choice1 == "Check Out":
                    st.write("Check Out Page")
                                        
                    st.markdown(
                        """
                        <style>
                        .stApp { background-color: #111111; }
                        .stSidebar { background-color: #483490; }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    st.subheader("Check Out - Residents GIKI")

                    optionDesignation = st.selectbox("Designation", ["Student", "Faculty"])
                    username = st.text_input("Username")

                    reg_no = None
                    room_no = None
                    employee_no = None


                    reg_no = st.text_input("Registration Number/Employee ID")
                    room_no = st.text_input("Room Number (Hostel)/Residential Number")

                    if st.button("Check Out"):
                            sign_in(username, reg_no,optionDesignation,room_no)
                            if sign_in(username, reg_no,optionDesignation,room_no):
                                st.success("Check Out  successfully ")
                            else:
                                st.warning("No such Resident found")



      
            elif choice1=="About Us":
                    st.write("About Us Page")
                                           
                    st.markdown(
                        """
                        <style>
                        .stApp { background-color: #111111; }
                        .stSidebar { background-color: #483490; }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    #about us page details
                    st.markdown("""
                    
                    """)
                    st.markdown("### Our Team")
                    st.markdown("- Areej Arif 2024113")
                    st.markdown("- Tuba Hussain 2024XXX")
                    st.markdown("- Muhammad Hasan Asif 2024XXX")
                    st.markdown("- Muhammad Anas 2024XXX")
                    st.markdown("### Contact Us")
                    st.markdown("Email: gikigiki@gmail.com")
                    st.markdown("Phone: +1-234-567-8901")
                    st.markdown("Address: Giki")    
                    st.markdown("### Follow Us")
                    st.markdown("- [Twitter](#)")   
                    # print("\t\t\t\t\t\tAbout Us")
                    # print("After the tragic loss of seven year old Jibrael, there was a dire need for enhanced security around campus.")
                    # print("An innocent life may have been saved if security personnel location was known.We felt strongly for the berieved;")
                    # print("something had to be done to keep this from happening in the future.IntruWatch was designed with the safety of GIKIans in mind.")
                    # print("It keeps track of CCTV cameras, security guard locations and details of those entering and leaving campus to make GIKI safer for all it's inhabitants.")
flaglogin=True
class AlertSystem:
    def __init__(self):
        # Heap to store alerts as tuples: (priority, timestamp, message)
        # Python heapq is a min-heap → smallest priority (1 = High) comes first
        self.heap = []
        # Priority map:
        # 1 = High (Immediate threat, e.g., Fire, Intrusion)
        # 2 = Medium (Suspicious activity, e.g., motion near camera)
        # 3 = Low (Minor alerts, e.g., low battery, system warning)
    
    def add_alert(self, priority, message):
        """
        Adds a new alert to the system with current timestamp.
        Arguments:
            priority: int → 1 (High), 2 (Medium), 3 (Low)
            message: str → description of the alert
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        heapq.heappush(self.heap, (priority, timestamp, message))
    
    def get_active_alerts(self):
        """
        Returns a sorted list of all active alerts.
        Sorting order: priority → timestamp
        (Does NOT remove alerts from the heap)
        """
        return sorted(self.heap)
# class AuthorizedDatabase:
#     def __init__(self):
#         # Simulating Hash Map {ID: Name}
#         self.db = {
#             "USER_001": "Admin Alice",
#             "USER_002": "Security Bob",
#             "USER_003": "Staff Charlie"
#         }

#     def check_access(self, user_id):
#         return self.db.get(user_id, None)
# if __name__ == "__main__":
#     auth_db = AuthorizedDatabase()

#     # List of user IDs to check
#     user_ids = ["USER_001", "USER_002", "USER_004", "USER_003", "USER_005"]

#     for uid in user_ids:
#         user_name = auth_db.check_access(uid)
#         if user_name:
#             print(f"Access granted for {uid}: {user_name}")
#         else:
#             print(f"Access denied for {uid}")
# Event linked list for Campus Guardian system
class EventNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class EventLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.max_size = 5  # Keep last 5 events

    def add_event(self, event_data):
        new_node = EventNode(event_data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

        # Trim old events if size exceeds max_size
        if self.size > self.max_size:
            current = self.head
            for _ in range(self.max_size - 1):
                current = current.next
            current.next = None
            self.size = self.max_size

    def get_all_events(self):
        events = []
        current = self.head
        while current:
            events.append(current.data)
            current = current.next
        return events
def logic_further():
      if flaglogin:
          st.write("Logged In Successfully")
          menu = ["Dashboard"," Camera View","Event Log","Alerts","Analytics","About Us"]
          choice = st.sidebar.radio("Navigation", menu)
    #   if st.session_state.get('logged_in', True):
          if choice == "Dashboard":
                st.write("Dashboard Page")
          elif choice=="Camera View":
                st.write("Camera View Page")
            #     cap = cv2.VideoCapture(0)
            #     if not cap.isOpened():
            #         st.write("Error: Could not open video source.")
            #         exit()

            #     st.write("Camera opened successfully. Press 'q' to exit.")

            #     while True:
            #     # Read a frame from the video source
            #     # 'ret' is a boolean (True/False) and 'frame' is the image data (NumPy array)
            #         ret, frame = cap.read()

            #         if not ret:
            #             print("Can't receive frame (stream end?). Exiting ...")
            #             break

            #     # Display the captured frame in a window named 'Camera Feed'
            #         cv2.imshow('Camera Feed', frame)

            #     # Wait for 1 millisecond for a key press
            #     # Break the loop if the 'q' key is pressed
            #         if cv2.waitKey(1) & 0xFF == ord('q'):
            #             break

            # # Release the camera and destroy all OpenCV windows
            #     cap.release()
            #     cv2.destroyAllWindows()
          elif choice=="Alerts":
                st.write("Alerts Page")
                alerts= st.text_input("Add Alert Here")
                priority= st.selectbox("Select Priority", [1,2,3])
                add=st.button("Add Alert")
                if add:
                    st.success("Alert Added Successfully")
                alert_system = AlertSystem()
                #Adding alerts related to camera/security and general safety
                alert_system.add_alert(priority, alerts)
                time.sleep(1)
                alert_system.add_alert(2, "Motion Detected near Gate 1 Camera")       # Medium priority
                time.sleep(1)
                alert_system.add_alert(1, "Intrusion Detected in Lab 3")             # High priority
                time.sleep(1)
                alert_system.add_alert(1, "Fire Alarm Triggered in Cafeteria")       # High priority
                time.sleep(1)
                alert_system.add_alert(3, "Camera 2 Battery Low")                    # Low priority
                time.sleep(1)
                alert_system.add_alert(2, "Unauthorized Access Attempt at Library")  # Medium priority
                time.sleep(1)
                alert_system.add_alert(3, "System Maintenance Reminder")             # Low priority
                
                # Get all active alerts sorted by priority (High → Medium → Low)
                active_alerts = alert_system.get_active_alerts()
                
                print("Active Campus Guardian Alerts (sorted by priority):")
                for alert in active_alerts:
                    st.write(f"Priority: {alert[0]}, Time: {alert[1]}, Message: {alert[2]}")
          elif choice=="Event Log":
            event_log = EventLinkedList()
            addevent=st.text_input("Add Sample Events")
            adde=st.button("Add Event")
            if adde:
                event_log.add_event(addevent)
                st.success("Event Added Successfully")
            # Add realistic campus intrusion/security events
            event_log.add_event("Gate 1 Breach Detected")
            event_log.add_event("Unauthorized Access in Lab 3")
            event_log.add_event("Motion Detected Near Library")
            event_log.add_event("Fire Alarm Triggered in Cafeteria")
            event_log.add_event("Suspicious Person in Parking Lot")
            event_log.add_event("Emergency Exit Door Forced Open")  # Oldest event will be trimmed

            # Display recent security events (newest to oldest)
            print("Recent Campus Security Events:")
            for event in event_log.get_all_events():
                st.write(event)   
          elif choice=="Analytics":
                st.write("Analytics Page")  
          elif choice=="About Us":
                st.write("About Us Page")
          else:
                st.write("Welcome to InTru Watch")



#------main defined
main()
logic_further()




     
