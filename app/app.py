#LIBRARIES
import heapq
import os  
import pickle
import time
from datetime import datetime
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_navigation_bar import st_navbar
#Session Variables
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0A1F44, #203a43, #2c5364);
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background-color: #1c1f26;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#session states
if "checkin_head" not in st.session_state:
    st.session_state.checkin_head = None
if "guard_root" not in st.session_state:
    st.session_state.guard_root=None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "started" not in st.session_state:
    st.session_state["started"] = False
if "face_capture_count" not in st.session_state:
    st.session_state["face_capture_count"] = {}
if "face_recognizer" not in st.session_state:
    st.session_state["face_recognizer"] = None
if "face_labels" not in st.session_state:
    st.session_state["face_labels"] = {}
if "face_id_counter" not in st.session_state:
    st.session_state["face_id_counter"] = 0
#session states save the sessions dtaa for the local server
##### Camera View Logic
#session states save the sessions dtaa for the local server
##### CAmera View LOgic
def initialize_face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    return recognizer
def detect_face(img):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces, gray
def save_face_image(username, img_bgr, photo_num):
    photos_dir = Path("photos")
    photos_dir.mkdir(exist_ok=True)
    faces, gray = detect_face(img_bgr)
    if len(faces) == 0:
        return False, "No face detected. Please ensure your face is clearly visible."
    if len(faces) > 1:
        return False, "Multiple faces detected. Please ensure only one person is in frame."
    (x, y, w, h) = faces[0]
    face_roi = gray[y : y + h, x : x + w]
    face_roi = cv2.resize(face_roi, (200, 200))
    filename = photos_dir / f"{username}_{photo_num}.jpg"
    cv2.imwrite(str(filename), face_roi)
    return True, f"Face photo {photo_num} saved successfully!"
def train_face_recognizer():
    photos_dir = Path("photos")
    if not photos_dir.exists():
        return False
    faces = []
    labels = []
    label_map = {}
    current_label = 0
    photo_files = list(photos_dir.glob("*.jpg"))
    if len(photo_files) == 0:
        return False
    user_photos = {}
    for photo_file in photo_files:
        parts = photo_file.stem.split("_")
        if len(parts) >= 2:
            username = "_".join(parts[:-1])
            user_photos.setdefault(username, []).append(photo_file)
    for username, photo_list in user_photos.items():
        if username not in label_map:
            label_map[username] = current_label
            current_label += 1
        label_id = label_map[username]
        for photo_file in photo_list:
            img = cv2.imread(str(photo_file), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, (200, 200))
                faces.append(img)
                labels.append(label_id)
    if len(faces) == 0:
        return False
    recognizer = initialize_face_recognizer()
    recognizer.train(faces, np.array(labels))
    recognizer_dir = Path("recognizer_data")
    recognizer_dir.mkdir(exist_ok=True)
    recognizer.save(str(recognizer_dir / "face_recognizer.yml"))
    with open(recognizer_dir / "label_map.pkl", "wb") as f:
        pickle.dump(label_map, f)
    st.session_state["face_recognizer"] = recognizer
    st.session_state["face_labels"] = {v: k for k, v in label_map.items()}
    return True
def load_face_recognizer():
    recognizer_dir = Path("recognizer_data")
    recognizer_file = recognizer_dir / "face_recognizer.yml"
    label_file = recognizer_dir / "label_map.pkl"
    if not recognizer_file.exists() or not label_file.exists():
        return False
    try:
        recognizer = initialize_face_recognizer()
        recognizer.read(str(recognizer_file))
        with open(label_file, "rb") as f:
            label_map = pickle.load(f)
        st.session_state["face_recognizer"] = recognizer
        st.session_state["face_labels"] = {v: k for k, v in label_map.items()}
        return True
    except Exception as e:
        st.error(f"Error loading recognizer: {e}")
        return False
def recognize_face(img_bgr):
    if st.session_state["face_recognizer"] is None:
        if not load_face_recognizer():
            return None, "Face recognizer not trained yet."
    faces, gray = detect_face(img_bgr)
    if len(faces) == 0:
        return None, "No face detected."
    if len(faces) > 1:
        return None, "Multiple faces detected."
    recognizer = st.session_state["face_recognizer"]
    (x, y, w, h) = faces[0]
    face_roi = gray[y : y + h, x : x + w]
    face_roi = cv2.resize(face_roi, (200, 200))
    label, confidence = recognizer.predict(face_roi)
    if confidence < 100:
        username = st.session_state["face_labels"].get(label, "Unknown")
        return username, f"Recognized as {username} (confidence: {100 - confidence:.1f}%)"
    return None, f"Face not recognized (confidence too low: {100 - confidence:.1f}%)"

##### Login Logic for Admin
##Linked List 
class LoginNode:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.next = None
login_head = None # global head
def insert(name, password):
    global login_head
    new_node = LoginNode(name, password)
    new_node.next = login_head
    login_head = new_node
#sign in for Admin
def sign_in(name, password):
    global login_head
    temp = login_head
    while temp is not None:
        if temp.username == name and temp.password == password:
            return True
        temp = temp.next
    return False
#sign up for Admin(Register)
def sign_up(name, password):
    insert(name, password)
###UI-StrreamLit
def signup_function():
    st.subheader("Create New Admin Account")
    username = st.text_input("Choose Username", key="signup_username")
    password = st.text_input("Choose Password", type="password", key="signup_password")
    button = st.button("Sign Up", key="signup_button")
    if button:
        if username and password:
            sign_up(username, password)
            st.success(f"Account created for {username}!")
        else:
            st.warning("Please fill in all fields")
###UI-STreamlit
def login_function():
    st.subheader("Admin Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    button = st.button("Login", key="login_button")
    global login_head
    if login_head is None:
        sign_up("admin", "admin123")
    if button:
        if sign_in(username, password):
            st.success(f"Logged In as {username}")
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.rerun()
        else:
            st.warning("Incorrect Username/Password")
#global 
count_studentlogin = 0

###  Check in Node
class CheckInNode:
    def __init__(self, username, reg_no, designation, gender, room_no=None, employee_no=None):
        self.username = username
        self.reg_no = reg_no
        self.designation = designation
        self.gender = gender
        self.room_no = room_no
        self.employee_no = employee_no
        self.next = None

### global variables
checkin_head = None
count_studentlogin = 0
count_faculty = 0
count_other = 0
count_girls_hostel=0
count_boys=0
count_res=0
#register
def register(name, reg_no, designation, gender, room_no=None, employee_no=None):
    global checkin_head, count_faculty, count_studentlogin, count_other,count_girls_hostel,count_boys,count_other
    if designation == "Student":
        count_studentlogin += 1
    elif designation == "Faculty":
        count_faculty += 1
    else:
        count_other += 1
    # if room_no=="NGH"or"GH":
    #     count_girls_hotsel+=1
    # elif room_no=="H1"or"H2"or"H3"or"H4"or"H5"or"H6"or"H7":
    #     count_boys+=1
    # else:
    #     count_res+=1
    new_node = CheckInNode(name, reg_no, designation, gender, room_no, employee_no)
    new_node.next = checkin_head
    checkin_head = new_node

#resident_sign_up
def resident_sign_up(name, reg_no, designation, gender, room_no=None, employee_no=None):
    register(name, reg_no, designation, gender, room_no, employee_no)

#global variable
checkoutst = 0
chcekoutFt = 0

# resident checkout 
def resident_check_out(name, identifier, designation, location):
    global checkin_head, checkoutst, chcekoutFt
    current = checkin_head
    previous = None
    while current:
        identifier_match = (current.reg_no == identifier) or (current.employee_no == identifier)
        location_match = (current.room_no == location) or (current.employee_no == location)
        if (
            current.username == name
            and current.designation == designation
            and identifier_match
            and location_match
        ):
            if designation == "Student":
                checkoutst += 1
            elif designation == "Faculty":
                chcekoutFt += 1
            if previous is None:
                checkin_head = current.next
            else:
                previous.next = current.next
            return True
        previous = current
        current = current.next
    return False
#checkin counter
def compute_checkin_counters():
    students=0
    faculty=0
    current=st.session_state.checkin_head
    while current:
        if current.designation=="Student":
            students+=1
        elif current.designation=="Faculty":
            faculty+=1
        current=current.next
    return students,faculty
### list convertion
def list_converter():
    global checkin_head
    data_list = []
    current = checkin_head
    while current:
        data_list.append(
            {
                "Username": current.username,
                "Designation": current.designation,
                "Gender": current.gender,
                "Reg/Emp No": current.reg_no if current.designation == "Student" else current.employee_no,
                "Hostel No": current.room_no
            }
        )
        current = current.next
    return data_list

### dumy data
def dummy_data():
    # --- OTHERS ---
    resident_sign_up("Bilal", "111001", "Others", "M")
    resident_sign_up("Ayesha", "111002", "Others", "F")
    resident_sign_up("Hamza", "111003", "Others", "M")
    
    # --- FACULTY (D, E, F Types) ---
    resident_sign_up("Kamran", "EMP456", "Faculty", "M", room_no="D")
    resident_sign_up("Dania", "EMP789", "Faculty", "F", room_no="E")
    resident_sign_up("Asad", "EMP101", "Faculty", "M", room_no="F")
    resident_sign_up("Sadia", "EMP102", "Faculty", "F", room_no="D")
    resident_sign_up("Faisal", "EMP103", "Faculty", "M", room_no="E")
    resident_sign_up("Rabia", "EMP104", "Faculty", "F", room_no="F")
    resident_sign_up("Imran", "EMP105", "Faculty", "M", room_no="D")
    resident_sign_up("Nadia", "EMP106", "Faculty", "F", room_no="E")
    resident_sign_up("Tariq", "EMP107", "Faculty", "M", room_no="F")
    resident_sign_up("Bushra", "EMP108", "Faculty", "F", room_no="D")
    resident_sign_up("Salman", "EMP109", "Faculty", "M", room_no="E")
    resident_sign_up("Khadija", "EMP110", "Faculty", "F", room_no="F")
    # --- STUDENTS: GIRLS (GH, NGH) options---
    resident_sign_up("Samina", "2023114", "Student", "F", room_no="GH")
    resident_sign_up("Ayesha", "2024331", "Student", "F", room_no="NGH")
    resident_sign_up("Zara", "2024567", "Student", "F", room_no="GH")
    resident_sign_up("Nimra", "2024789", "Student", "F", room_no="NGH")
    resident_sign_up("Fatima", "2024901", "Student", "F", room_no="GH")
    resident_sign_up("Iqra", "2024123", "Student", "F", room_no="NGH")
    resident_sign_up("Hira", "2024345", "Student", "F", room_no="GH")
    resident_sign_up("Laiba", "2024568", "Student", "F", room_no="NGH")
    resident_sign_up("Samina", "2022114", "Student", "F", room_no="GH")
    resident_sign_up("Ayesha", "2023221", "Student", "F", room_no="NGH")
    resident_sign_up("Zara", "2025445", "Student", "F", room_no="GH")
    resident_sign_up("Nimra", "2023678", "Student", "F", room_no="NGH")
    resident_sign_up("Fatima", "2022890", "Student", "F", room_no="GH")
    resident_sign_up("Iqra", "2022233", "Student", "F", room_no="NGH")
    resident_sign_up("Hira", "2023456", "Student", "F", room_no="GH")
    resident_sign_up("Laiba", "2025899", "Student", "F", room_no="NGH")

    # --- STUDENTS: BOYS (H1 - H7) ---
    resident_sign_up("Ali", "2024113", "Student", "M", room_no="H1")
    resident_sign_up("Omar", "2024222", "Student", "M", room_no="H2")
    resident_sign_up("Hassan", "2024455", "Student", "M", room_no="H3")
    resident_sign_up("Bilal", "2024678", "Student", "M", room_no="H4")
    resident_sign_up("Usman", "2024890", "Student", "M", room_no="H5")
    resident_sign_up("Hamza", "2024012", "Student", "M", room_no="H6")
    resident_sign_up("Saad", "2024234", "Student", "M", room_no="H7")
    resident_sign_up("Ahmed", "2024456", "Student", "M", room_no="H1")
    resident_sign_up("Ali", "2023112", "Student", "M", room_no="H2")
    resident_sign_up("Omar", "2025115", "Student", "M", room_no="H3")
    resident_sign_up("Hassan", "2022334", "Student", "M", room_no="H4")
    resident_sign_up("Bilal", "2022567", "Student", "M", room_no="H5")
    resident_sign_up("Usman", "2025789", "Student", "M", room_no="H6")
    resident_sign_up("Hamza", "2023119", "Student", "M", room_no="H7")
    resident_sign_up("Saad", "2025344", "Student", "M", room_no="H1")
    resident_sign_up("Ahmed", "2022578", "Student", "M", room_no="H2")

  
dummy_data()

### Tree implementation for guards
class Guard:
    def __init__(self, name=None, guardid=None, duty=None):
        self.name = name
        self.guardid = guardid
        self.duty = duty
        self.left = None
        self.right = None
    def insert(self, name, guardid, duty):
        if self.guardid is None:
            self.name = name
            self.guardid = guardid
            self.duty = duty
            return
        if guardid < self.guardid:
            if self.left is None:
                self.left = Guard(name, guardid, duty)
            else:
                self.left.insert(name, guardid, duty)
        elif guardid > self.guardid:
            if self.right is None:
                self.right = Guard(name, guardid, duty)
            else:
                self.right.insert(name, guardid, duty)
    def inorder(self):
        result = []
        if self.left:
            result.extend(self.left.inorder())
        if self.name is not None:
            result.append((self.name, self.guardid, self.duty))
        if self.right:
            result.extend(self.right.inorder())
        return result
    def findguard(self, target_id):
        if self.guardid is None:
            return None
        if target_id == self.guardid:
            return self
        if target_id < self.guardid and self.left:
            return self.left.findguard(target_id)
        if target_id > self.guardid and self.right:
            return self.right.findguard(target_id)
        return None
# Helper Functions (Outside the Class)
def flatten_bst(root):
    if not root or root.guardid is None:
        return []
    queue = [root]
    result = []
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
    return result
# Assigning Guards location
def assign_guards_to_locations(root, locations):
    assigned = {}
    all_guards = flatten_bst(root)
    index = 0
    for location, count in locations.items():
        assigned[location] = []
        for _ in range(count):
            if index < len(all_guards):
                assigned[location].append(all_guards[index].name)
                index += 1
    return assigned
# --- Streamlit Display Logic ---

def display_guard_analytics(root):
    st.markdown("---")
    st.title("University Guard Assignments & Analytics")
    # st.balloons()
    locations = {
        "FCSE": 1,
        "FBS": 1,
        "FME": 1,
        "Brabers Building": 2,
        "Library": 1,
        "TUC": 2,
        "Entrance Main": 1,
        "Entrance Ayann": 1,
        "Residential Area": 3
    }
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("All Guards (BST Inorder)")
        inorder_data = root.inorder()
        if inorder_data:
            for name, gid, duty in inorder_data:
                st.write(f"ID: **{gid}** | Name: {name} | Duty: {duty}")
        else:
            st.info("No guards registered.")

    # Process Assignments
    assignments = assign_guards_to_locations(root, locations)

    with col2:
        st.subheader("Location Assignments")
        for loc, guards in assignments.items():
            guard_names = ", ".join(guards) if guards else "None Assigned"
            st.write(f"**{loc}**: {guard_names}")

    st.markdown("---")
    
    # Charting Section
    st.subheader("Guard Distribution Visualization")
    locations_list = list(assignments.keys())
    num_guards = [len(guards) for guards in assignments.values()]

    if sum(num_guards) > 0:
        fig, ax = plt.subplots(figsize=(2, 2))
        # Filter out locations with 0 guards for a cleaner pie chart
        plot_labels = [loc for loc, num in zip(locations_list, num_guards) if num > 0]
        plot_sizes = [num for num in num_guards if num > 0]
        
        ax.pie(plot_sizes, labels=plot_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.set_title('Active Guard Distribution')
        st.pyplot(fig)
        # Bar Chart for Capacity
        st.subheader("Guards per Location (Bar Chart)")
        st.bar_chart(dict(zip(locations_list, num_guards))) #zip() for tuple
    else:
        st.warning("Add guards to view distribution charts.")
    st.markdown("---")
    st.subheader("Guard Coverage Status")

    unguarded_locations = [
        location for location, guards in assignments.items() if len(guards) == 0
    ]
# location 
    if unguarded_locations:
        st.error("🚨 SECURITY ALERT: Unguarded Locations Detected")

        for loc in unguarded_locations:
            st.warning(f"⚠️ No guard assigned at **{loc}**")
        st.info("**Notify the on-duty guards**")

# Usage Example (Initialize root if not exists)
if "guard_root" not in st.session_state:
    st.session_state.guard_root = Guard()
    # Adding Dummy Data
    st.session_state.guard_root.insert("John", 101, "Main Gate")
    st.session_state.guard_root.insert("Alice", 102, "Library")
    st.session_state.guard_root.insert("Bob", 103, "Residential")
####Charting Function for Analytics
def charting():
    if not checkin_head:
        st.info("No resident data registered yet for analytics.")
        return
    data = list_converter()
    df = pd.DataFrame(data)
    st.subheader("Gender Distribution")
    gender_counts = df["Gender"].value_counts()
    designation_counts = df["Designation"].value_counts()
    
    hostel_counts = df["Hostel No"].value_counts()
    st.bar_chart(gender_counts)
    st.subheader("Designation Distribution")
    st.bar_chart(designation_counts, color="#7D2D2D")
    st.area_chart(hostel_counts,color="#A16868")
    display_guard_analytics(st.session_state.guard_root)    

##### Alert System
### Heap Data Structure
class AlertSystem:
    def __init__(self):
        self.heap = []

    def add_alert(self, priority, message,location):
        timestamp = datetime.now().strftime("%H:%M:%S")
        heapq.heappush(self.heap, (priority, timestamp, message,location))
    def get_active_alerts(self):
        return sorted(self.heap)
####  Events 
## linked list implmenttaion
class EventNode:
    def __init__(self, data):
        self.data = data
        self.next = None
class EventLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.max_size = 5
    def add_event(self, event_data):
        new_node = EventNode(event_data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
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
#insertion sort for reg number sorting 
def insertion_sort_reg_numbers(reg_numbers):
    for i in range(1, len(reg_numbers)):
        key = reg_numbers[i]
        j = i - 1
        while j >= 0 and reg_numbers[j] > key:
            reg_numbers[j + 1] = reg_numbers[j]
            j -= 1
        reg_numbers[j + 1] = key
    return reg_numbers
#get reg numbers from the linked list 
def get_reg_numbers_from_checkins():
    regs = []#list for travering the regs
    current = st.session_state.checkin_head #checkin_head ->head ptr for linked list
    while current:
        if current.designation == "Student":
            regs.append(current.reg_no)
        current = current.next
    return regs
reg_numbers = get_reg_numbers_from_checkins()
reg=["2024113","2023114", "2023221", "2022114","2023111","2023112","202577"]
sorted_regs = insertion_sort_reg_numbers(reg)
#### Navigation Before Login Admin
menu_pre_login = ["Login Admin", "Check In", "Check Out", "About Us"]
#### Navigation After Login Admin
menu_post_login = ["Dashboard", "Camera View", "Event Log", "Alerts", "Guards Manager", "Analytics"]

#### After Login LOgic for Admin
def logic_further():
    st.sidebar.title(f"Welcome, {st.session_state.current_user}")
    st.sidebar.markdown("---")  #session
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    #session state preservation
    choice = st.sidebar.radio("Navigation", menu_post_login)
    #naviagtion bar
    if choice == "Dashboard":# page 1
        st.set_page_config(layout="wide", initial_sidebar_state="expanded")
        st.header("Admin Dashboard")
        st.info("Welcome to the Admin Control Panel.")
        UNI_LAT = 34.0691
        UNI_LON = 72.6441
        n = 9
        map_data = pd.DataFrame(np.random.randn(n, 2) / [50, 50] + [UNI_LAT, UNI_LON], columns=["lat", "lon"])
        st.map(map_data)
        st.subheader("---")
       # display counter logic
        students_in,faculty_in=compute_checkin_counters()
        Totalstuents =300
        intrusionVal = 13
        countgaurds = 28
        hostels_total=14
        camera_total=37
        TotalFaculty=100
        checkoutst=Totalstuents-students_in
        chcekoutFt=TotalFaculty-faculty_in
        col0,col1, col2,col33, col3, col4, col5, col6, col7,col8 = st.columns([1,1, 1, 1,1, 1, 1, 1, 1,1])
        with col0:
            st.metric("Total Students:",Totalstuents)
        with col1:
            st.metric("Check In (on Campus)", students_in, "Students")
        with col2:
            st.metric("Check Out (out Campus)", checkoutst, "Students")
        with col33:
             st.metric("Total Faculty:",TotalFaculty)
        with col3:
            st.metric("Faculty(CheckIn)",faculty_in, "Faculty")
        with col4:
             st.metric("Faculty(Checkout)", chcekoutFt, "Faculty")
        with col5:
            st.metric(label="Total Intrusions", value=intrusionVal)
        with col6:
            st.metric(label="Total Guards", value=countgaurds)
        with col7 :
             st.metric(label="Total Intrusions", value=hostels_total)
        with col8 :
              st.metric(label="Total Cameras",value=camera_total)
        st.markdown("---")
        data = list_converter()
        df = pd.DataFrame(data)
        df = df[["Username", "Designation", "Gender", "Reg/Emp No"]]
        st.subheader("Registered Residents")
        if df.empty:
            st.info("No check-ins yet.")
        else:
            st.dataframe(df)
            df2=pd.DataFrame(sorted_regs)
            st.write("Sorted Registration Numbers:")
            st.dataframe(df2)
            st.subheader("Intrusion")
            col1_a, col1_b = st.columns(2)
            with col1_a:
                st.markdown("**Occurance**")
                st.success("23%", icon="⬆️")
            with col1_b:
                st.markdown("**No Occrance**")
                st.error("3%", icon="⬇️")
        st.info("**Intru Watch Dashboard**")
    elif choice == "Camera View":
        st.header("Face Recognition & Entry Check")
        if st.session_state.current_user is None:
            st.warning("Please login as admin to use camera features.")
            return
        st.markdown("### Instructions:")
        st.markdown(
            """
        1. **First Time Setup**: Capture 3 photos of a person's face to register them in the system.
        2. **Entry Check**: On the 4th capture, the system will recognize the face and verify entry.
        3. **No Intrusion**: If face is recognized, a "No Intrusion" message will be displayed.
        """
        )
        person_name = st.text_input(
            "Enter Person Name for Face Registration/Recognition",
            key="person_name_input",
            placeholder="e.g., John Doe",
        )
        if not person_name:
            st.warning("Please enter a person's name to proceed.")
            return
        if person_name not in st.session_state.face_capture_count:
            st.session_state.face_capture_count[person_name] = 0
        current_count = st.session_state.face_capture_count[person_name]
        if current_count < 3:
            st.info(f"📸 **Registration Mode**: Capture photo {current_count + 1} of 3 for {person_name}")
        else:
            st.success(f"✅ **Recognition Mode**: {person_name} is registered. Next capture will verify entry.")
        img_file = st.camera_input("Capture Face", key="face_camera")
        if img_file is not None:
            file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
            img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if current_count < 3:
                success, message = save_face_image(person_name, img_bgr, current_count + 1)
                if success:
                    st.session_state.face_capture_count[person_name] = current_count + 1
                    st.success(f"✅ {message}")
                    if st.session_state.face_capture_count[person_name] == 3:
                        st.balloons()
                        st.success(f"🎉 Registration Complete! {person_name} is now registered in the system.")
                        st.info("Next capture will be used for entry verification.")
                        if train_face_recognizer():
                            st.success("Face recognizer trained successfully!")
                else:
                    st.error(f"❌ {message}")
                    st.info("Please try again with a clear face view.")
            else:
                recognized_name, recognition_message = recognize_face(img_bgr)
                if recognized_name and recognized_name == person_name:
                    st.success("✅ **NO INTRUSION DETECTED**")
                    st.balloons()
                    st.info(f"👤 Face recognized: {person_name}")
                    st.info(f"📊 {recognition_message}")
                    st.markdown("---")
                    st.markdown("### ✅ Entry Authorized")
                    st.markdown(f"**Person**: {person_name}")
                    st.markdown(f"**Status**: Verified - No Intrusion")
                    st.markdown(f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                elif recognized_name:
                    st.warning(f"⚠️ Face recognized as {recognized_name}, but name entered was {person_name}.")
                    st.info("Please verify the person's identity.")
                else:
                    st.error("❌ **INTRUSION DETECTED**")
                    st.warning(f"⚠️ {recognition_message}")
                    st.info("Face not recognized. This person is not registered in the system.")
                    st.markdown("---")
                    st.markdown("### 🚨 Security Alert")
                    st.markdown("**Person**: Unknown")
                    st.markdown("**Status**: Unauthorized Entry Detected")
                    st.markdown(f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("---")
        st.subheader("Registration Status")
        photos_dir = Path("photos")
        if photos_dir.exists():
            all_photos = list(photos_dir.glob("*.jpg"))
            st.info(f"Total face photos saved: {len(all_photos)}")
            person_photos = list(photos_dir.glob(f"{person_name}_*.jpg"))
            if person_photos:
                st.write(f"Photos for {person_name}: {len(person_photos)}")
                cols = st.columns(min(3, len(person_photos)))
                for idx, photo_path in enumerate(person_photos[:3]):
                    with cols[idx]:
                        st.image(str(photo_path), caption=f"Photo {idx + 1}", use_container_width=True)
    elif choice == "Alerts":
        st.header("Security Alerts (Priority Queue)")
        st.warning("Alerts would be notified to the nearest security personal.")
        alert_system = AlertSystem()
        with st.form("alert_form"):
            alerts = st.text_input("Add Custom Alert")
            priority = st.selectbox(
                "Select Priority",
                [1, 2, 3],
                format_func=lambda x: f"{x} ({'High' if x == 1 else 'Medium' if x == 2 else 'Low'})",
            )
            location=st.selectbox(
                "Select Area:",
                ["BB","Tuc","Residence","FMCE","FEE","FCSE","FBS","ACB","Admin Block","Sports Complex","Area(uc)"]
            )
            add = st.form_submit_button("Add Alert")
        alert_sound=st.button("Alert with sound")
        if alert_sound:
            st.audio('alert-33762 (1).mp3',width="stretch",start_time=40,end_time=42)
            st.error("Ringing the Alarms for notification.")
          
        if add and alerts:
            alert_system.add_alert(priority, alerts,location)
            st.success("Alert Added Successfully")
        alert_system.add_alert(2, "Motion Detected near Gate 1 Camera","BB")
        alert_system.add_alert(1, "Intrusion Detected in Lab 3","FMCE")
        alert_system.add_alert(3, "Camera 2 Battery Low","TUC")
        active_alerts = alert_system.get_active_alerts()
        st.subheader("Active Alerts (Sorted by Priority)")
        alert_data = []
        for p, t, m,l in active_alerts:
            alert_data.append({"Priority": p, "Time": t, "Message": m,"Location":l})
        df_alerts = pd.DataFrame(alert_data)
        st.dataframe(df_alerts)
      
    elif choice == "Event Log":
        st.header("Recent Event Log (Fixed-Size List)")
        event_log = EventLinkedList()
        with st.form("event_form"):
            addevent = st.text_input("Add Sample Event")
            adde = st.form_submit_button("Add Event")
        if adde and addevent:
            event_log.add_event(addevent)
            st.success("Event Added Successfully!!")
        event_log.add_event("Unauthorized Access in Lab 3")
        event_log.add_event("Motion Detected Near Library")
        event_log.add_event("Fire Alarm Triggered in Cafeteria")
        st.subheader("Events (Most Recent First)")
        eventsalerts=event_log.get_all_events()
        # for event in event_log.get_all_events():
        #     st.markdown(f"- {event}")
        eventalert_data = []
        for p in eventsalerts :
            eventalert_data.append({"Event":p})
        df_ealerts = pd.DataFrame(eventalert_data)
        st.dataframe(df_ealerts)
    elif choice == "Analytics":
        st.header("Resident Analytics")
        charting()
    elif choice == "Guards Manager":
        st.header("Guards Manager")
        name = st.text_input("Enter the guard name to assign duty:")
        guard_id = st.number_input("Enter the guard id to assign duty:", min_value=0, step=1)
        duty = st.text_input("Enter the guard duty:")
        root = Guard()
        if name and guard_id and duty:
            root.insert(name, int(guard_id), duty)
        root.insert("Alice", 5, "Gate B")
        root.insert("Bob", 15, "Gate C")
        root.insert("Eve", 3, "Library")
        root.insert("Charlie", 7, "TUC")
        root.insert("Dave", 12, "Brabers")
        root.insert("Fay", 18, "Entrance")
        guard_rows = root.inorder()
        alert_data = [{"Name": p, "Guard Id": t, "Duty Assigned": m} for p, t, m in guard_rows]
        df_alerts = pd.DataFrame(alert_data)
        st.dataframe(df_alerts)
     

#location connnect for displaying where the gaurds would be 
#### Graphs 
def location_conect_giki():
    locations = {
        "FCSE": 1,
        "FBS": 1,
        "FME": 1,
        "Brabers Building": 2,
        "Library": 1,
        "TUC": 2,
        "Entrance Main": 1,
        "Entrance Ayann": 1,
        "Residential Area": 3,
    }
### using BST( breath search first )
    def flatten_bst(root):
        if not root:
            return []
        queue = [root]
        result = []
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node)
                queue.append(node.left)
                queue.append(node.right)
        return result
### Assigning locations to guards
    def assign_guards_to_locations(root, locations):
        assigned = {}
        all_guards = flatten_bst(root)
        index = 0
        for location, count in locations.items():
            assigned[location] = []
            for _ in range(count):
                if index < len(all_guards):
                    assigned[location].append(all_guards[index].name)
                    index += 1
        return assigned
###
    root = Guard("John", 10, "Gate A")
    root.insert("Alice", 5, "Gate B")
    root.insert("Bob", 15, "Gate C")
    root.insert("Eve", 3, "Library")
    root.insert("Charlie", 7, "TUC")
    root.insert("Dave", 12, "Brabers")
    root.insert("Fay", 18, "Entrance")
    st.title("University Guard Assignments")
    st.markdown(""------"")
    st.subheader("All guards in BST order:")
    inorder_list = root.inorder()
    for line in inorder_list:
        st.write(line)
    assignments = assign_guards_to_locations(root, locations)
    st.subheader("Guard Assignments per Location:")
    for loc, guards in assignments.items():
        st.write(f"{loc}: {guards}")
    locations_list = list(assignments.keys())
    num_guards = [len(guards) for guards in assignments.values()]
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(num_guards, labels=locations_list, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
    ax.set_title("Guard Distribution Across University Locations")
    st.pyplot(fig)
    plt.figure(figsize=(10, 6))
    plt.bar(locations_list, num_guards, color="skyblue")
    plt.xlabel("University Locations")
    plt.ylabel("Number of Guards Assigned")
    plt.title("Guards Assigned per University Location")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(plt)


def main():
    if not st.session_state.started:
        st.markdown("---")
        st.set_page_config(
            page_title="Intru Watch",
            page_icon=":",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(
            '<p style="text-align: center; font-family:sans-serif; font-size: 90px; color: #3293a8;"><b>InTru Watch</b></p>',
            unsafe_allow_html=True,
        )
        st.markdown("### Secure Campus with Real-Time Surveillance and Alerts")
        st.markdown("##### Welcome to InTru Watch")
        st.markdown(
            """
            <style>
            .stButton>button1{
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
        """,
            unsafe_allow_html=True,
        )
        button1 = st.button(" Lets Get Started!")
        if button1:
            st.session_state.started = True
            st.rerun()
        return
    if st.session_state.logged_in:
        logic_further()
        return
    choice1 = st.sidebar.radio("Navigation", menu_pre_login)
    if choice1 == "Login Admin":
        st.header("Admin Login & Sign Up")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            sign_up("Admin", "admin123")
            login_function()
        with tab2:
            signup_function()
    elif choice1 == "Check In":
        st.header("Resident Check In/Registration")
        optionDesignation = st.selectbox("Designation", ["Student", "Faculty"])
        username = st.text_input("Username")
        reg_no = None
        room_no = None
        employee_no = None
        if optionDesignation == "Student":
            reg_no = st.text_input("Registration Number")
            room_no = st.text_input("Hostel")
        elif optionDesignation == "Faculty":
            employee_no = st.text_input("Employee ID")
            reg_no = employee_no
            room_no = st.text_input("Residential Number")
        gender_option = st.selectbox("Gender", ["Male", "Female"])
        gender = "M" if gender_option == "Male" else "F"
        if st.button("Sign Up (Check In)"):
            if username and reg_no:
                resident_sign_up(username, reg_no, optionDesignation, gender, room_no, employee_no)
                st.success(f"{optionDesignation} {username} successfully checked in!")
            else:
                st.warning("Please fill all required fields")
    elif choice1 == "Check Out":
        st.header("Resident Check Out")
        optionDesignation = st.selectbox("Designation", ["Student", "Faculty"])
        username = st.text_input("Username")
        identifier = st.text_input("Registration Number/Employee ID")
        location = st.text_input("Hostel /Residential Number")
        if st.button("Check Out"):
            if resident_check_out(username, identifier, optionDesignation, location):
                st.success(f"{optionDesignation} {username} successfully checked out!")
            else:
                st.warning("No matching resident found for check-out.")
    elif choice1 == "About Us":
        st.write("About Us Page")
        st.markdown(
            """
            <style>
            .stApp { background-color: #111111; }
            .stSidebar { background-color: #483490; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        Team = ["Areej Arif 2024127", "Ayesha Khalid 2024127", "Nabiha Nair 2024514"]
        Contact_Details = ["Email: IntruWatch@gmail.com", "Phone: +92-234-567-8901"]
        st.markdown("About Us")
        st.markdown("Our goal is to make GIKI safer for all its inhabitants. Due to lack of information about GIKI's security landscape, it's impossible")
        st.markdown("to take action on time in case of an emergency. Our team at Intruwatch is dedicated to reduce chances of avoidable incidents by")
        st.markdown("tracking security personnel location and delivering timely alerts to those close to a possible threat.")
        st.markdown("It also keeps track of CCTV cameras, and details of those entering and leaving campus.")
        st.markdown("### Our Team")
        st.markdown(Team[0])
        st.markdown(Team[1])
        st.markdown(Team[2])
        st.markdown("### Contact Us")
        st.markdown(Contact_Details[0])
        st.markdown(Contact_Details[1])
        st.markdown("Address: Giki")
        st.markdown("### Follow Us")
        st.markdown("- [Twitter](#)")


if __name__ == "__main__":
    main()
