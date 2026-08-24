# =====================================================
# Dummy Data
# Inserts 100 sample student records for testing
# (Unchanged logic from the Tkinter version — only the
#  import path has moved to app.database.db_connection)
# =====================================================

from app.database.db_connection import (
    get_connection,
    close_connection
)


# =====================================================
# DUMMY STUDENT DATA
# Format: (roll_no, full_name, age, gender, course, email, phone, address)
# =====================================================

dummy_students = [

    (101, "Rahul Sharma",     20, "Male",   "BCA",    "rahul101@gmail.com",     "9876543201", "Mumbai"),
    (102, "Priya Verma",      21, "Female", "BSc IT", "priya102@yahoo.com",     "9876543202", "Delhi"),
    (103, "Aman Gupta",       19, "Male",   "BCom",   "aman103@outlook.com",      "9876543203", "Pune"),
    (104, "Sneha Patil",      22, "Female", "BCA",    "sneha104@hotmail.com",     "9876543204", "Nagpur"),
    (105, "Vikas Yadav",      20, "Male",   "BBA",    "vikas105@rediffmail.com",     "9876543205", "Lucknow"),
    (106, "Neha Singh",       21, "Female", "MBA",    "neha106@protonmail.com",      "9876543206", "Indore"),
    (107, "Arjun Mehta",      23, "Male",   "MCA",    "arjun107@icloud.com",     "9876543207", "Ahmedabad"),
    (108, "Kavya Nair",       20, "Female", "BSc CS", "kavya108@zoho.com",     "9876543208", "Chennai"),
    (109, "Rohit Das",        24, "Male",   "MCom",   "rohit109@live.com",     "9876543209", "Kolkata"),
    (110, "Pooja Kulkarni",   22, "Female", "BCA",    "pooja110@ymail.com",     "9876543210", "Hyderabad"),

    (111, "Aditya Joshi",     20, "Male",   "BCA",    "aditya111@gmail.com",    "9876543211", "Mumbai"),
    (112, "Simran Kaur",      21, "Female", "MBA",    "simran112@yahoo.com",    "9876543212", "Chandigarh"),
    (113, "Karan Malhotra",   22, "Male",   "BCom",   "karan113@outlook.com",     "9876543213", "Delhi"),
    (114, "Riya Sharma",      19, "Female", "BSc IT", "riya114@hotmail.com",      "9876543214", "Pune"),
    (115, "Manish Patel",     23, "Male",   "MCA",    "manish115@rediffmail.com",    "9876543215", "Ahmedabad"),
    (116, "Anjali Roy",       20, "Female", "BBA",    "anjali116@protonmail.com",    "9876543216", "Kolkata"),
    (117, "Deepak Yadav",     24, "Male",   "MBA",    "deepak117@icloud.com",    "9876543217", "Lucknow"),
    (118, "Nikita Jain",      22, "Female", "BCA",    "nikita118@zoho.com",    "9876543218", "Jaipur"),
    (119, "Suresh Kumar",     25, "Male",   "MCom",   "suresh119@live.com",    "9876543219", "Patna"),
    (120, "Ayesha Khan",      21, "Female", "BSc CS", "ayesha120@ymail.com",    "9876543220", "Bhopal"),

    (121, "Tarun Meena",      20, "Male",   "BCA",    "tarun121@gmail.com",     "9876543221", "Udaipur"),
    (122, "Megha Shah",       22, "Female", "MBA",    "megha122@yahoo.com",     "9876543222", "Surat"),
    (123, "Yash Thakur",      19, "Male",   "BBA",    "yash123@outlook.com",      "9876543223", "Shimla"),
    (124, "Pallavi Rao",      23, "Female", "MCA",    "pallavi124@hotmail.com",   "9876543224", "Bengaluru"),
    (125, "Rakesh Soni",      24, "Male",   "BCom",   "rakesh125@rediffmail.com",    "9876543225", "Kanpur"),
    (126, "Divya Iyer",       20, "Female", "BSc IT", "divya126@protonmail.com",     "9876543226", "Chennai"),
    (127, "Harsh Vardhan",    21, "Male",   "BCA",    "harsh127@icloud.com",     "9876543227", "Noida"),
    (128, "Komal Arora",      22, "Female", "MBA",    "komal128@zoho.com",     "9876543228", "Delhi"),
    (129, "Nitin Bansal",     23, "Male",   "MCA",    "nitin129@live.com",     "9876543229", "Faridabad"),
    (130, "Shruti Desai",     20, "Female", "BBA",    "shruti130@ymail.com",    "9876543230", "Vadodara"),

    (131, "Akash Mishra",     21, "Male",   "BCA",    "akash131@gmail.com",     "9876543231", "Prayagraj"),
    (132, "Bhavna Kapoor",    22, "Female", "BSc CS", "bhavna132@yahoo.com",    "9876543232", "Amritsar"),
    (133, "Chirag Modi",      23, "Male",   "MBA",    "chirag133@outlook.com",    "9876543233", "Rajkot"),
    (134, "Disha Verma",      20, "Female", "BCom",   "disha134@hotmail.com",     "9876543234", "Gwalior"),
    (135, "Eshan Ali",        24, "Male",   "MCom",   "eshan135@rediffmail.com",     "9876543235", "Aligarh"),
    (136, "Falak Sheikh",     21, "Female", "BCA",    "falak136@protonmail.com",     "9876543236", "Aurangabad"),
    (137, "Gaurav Tiwari",    22, "Male",   "BSc IT", "gaurav137@icloud.com",    "9876543237", "Varanasi"),
    (138, "Heena Parmar",     20, "Female", "MBA",    "heena138@zoho.com",     "9876543238", "Nashik"),
    (139, "Imran Siddiqui",   23, "Male",   "BBA",    "imran139@live.com",     "9876543239", "Meerut"),
    (140, "Juhi Sinha",       19, "Female", "BCA",    "juhi140@ymail.com",      "9876543240", "Ranchi"),

    (141, "Kishore Reddy",    24, "Male",   "MCA",    "kishore141@gmail.com",   "9876543241", "Hyderabad"),
    (142, "Lavanya Pillai",   21, "Female", "BSc CS", "lavanya142@yahoo.com",   "9876543242", "Kochi"),
    (143, "Mohit Chauhan",    22, "Male",   "BCom",   "mohit143@outlook.com",     "9876543243", "Dehradun"),
    (144, "Nandini Bose",     20, "Female", "MBA",    "nandini144@hotmail.com",   "9876543244", "Kolkata"),
    (145, "Omkar Jadhav",     23, "Male",   "BCA",    "omkar145@rediffmail.com",     "9876543245", "Satara"),
    (146, "Preeti Nanda",     21, "Female", "BBA",    "preeti146@protonmail.com",    "9876543246", "Bhubaneswar"),
    (147, "Qasim Khan",       24, "Male",   "MCom",   "qasim147@icloud.com",     "9876543247", "Moradabad"),
    (148, "Rupali Sen",       22, "Female", "BSc IT", "rupali148@zoho.com",    "9876543248", "Siliguri"),
    (149, "Sahil Arjun",      20, "Male",   "MBA",    "sahil149@live.com",     "9876543249", "Goa"),
    (150, "Tanvi Chawla",     19, "Female", "BCA",    "tanvi150@ymail.com",     "9876543250", "Panipat"),

    (151, "Uday Raj",         22, "Male",   "BCom",   "uday151@gmail.com",      "9876543251", "Jaipur"),
    (152, "Vaishali Patnaik", 21, "Female", "MBA",    "vaishali152@yahoo.com",  "9876543252", "Cuttack"),
    (153, "Wasim Akhtar",     24, "Male",   "MCA",    "wasim153@outlook.com",     "9876543253", "Patna"),
    (154, "Xena Dsouza",      20, "Female", "BBA",    "xena154@hotmail.com",      "9876543254", "Goa"),
    (155, "Yogesh Pawar",     23, "Male",   "BCA",    "yogesh155@rediffmail.com",    "9876543255", "Kolhapur"),
    (156, "Zoya Mirza",       22, "Female", "BSc CS", "zoya156@protonmail.com",      "9876543256", "Lucknow"),

    (157, "Abhishek Rana",    21, "Male",   "MBA",    "abhishek157@icloud.com",  "9876543257", "Shimla"),
    (158, "Bharti Kumari",    20, "Female", "BCom",   "bharti158@zoho.com",    "9876543258", "Patna"),
    (159, "Chetan Solanki",   22, "Male",   "BCA",    "chetan159@live.com",    "9876543259", "Indore"),
    (160, "Devika Menon",     21, "Female", "MCA",    "devika160@ymail.com",    "9876543260", "Kochi"),

    (161, "Eklavya Singh",    24, "Male",   "BBA",    "eklavya161@gmail.com",   "9876543261", "Agra"),
    (162, "Farah Ali",        20, "Female", "MBA",    "farah162@yahoo.com",     "9876543262", "Bhopal"),
    (163, "Girish Naik",      23, "Male",   "BSc IT", "girish163@outlook.com",    "9876543263", "Hubli"),
    (164, "Himani Arora",     22, "Female", "BCA",    "himani164@hotmail.com",    "9876543264", "Delhi"),
    (165, "Irfan Qureshi",    21, "Male",   "MCom",   "irfan165@rediffmail.com",     "9876543265", "Nagpur"),
    (166, "Jinal Shah",       20, "Female", "BBA",    "jinal166@protonmail.com",     "9876543266", "Surat"),

    (167, "Kunal Saxena",     22, "Male",   "MBA",    "kunal167@icloud.com",     "9876543267", "Noida"),
    (168, "Lata Verghese",    21, "Female", "BSc CS", "lata168@zoho.com",      "9876543268", "Thrissur"),
    (169, "Madan Lal",        24, "Male",   "BCA",    "madan169@live.com",     "9876543269", "Jodhpur"),
    (170, "Nisha Paul",       23, "Female", "MCA",    "nisha170@ymail.com",     "9876543270", "Shillong"),

    (171, "Ojas Kulkarni",    20, "Male",   "BBA",    "ojas171@gmail.com",      "9876543271", "Pune"),
    (172, "Pinky Rani",       22, "Female", "MBA",    "pinky172@yahoo.com",     "9876543272", "Ranchi"),
    (173, "Qadir Hussain",    21, "Male",   "BCom",   "qadir173@outlook.com",     "9876543273", "Srinagar"),
    (174, "Ritu Sharma",      20, "Female", "BCA",    "ritu174@hotmail.com",      "9876543274", "Delhi"),
    (175, "Sanjay Kumar",     24, "Male",   "MCom",   "sanjay175@rediffmail.com",    "9876543275", "Kanpur"),

    (176, "Trisha Bose",      22, "Female", "BSc IT", "trisha176@protonmail.com",    "9876543276", "Kolkata"),
    (177, "Utkarsh Jain",     21, "Male",   "MBA",    "utkarsh177@icloud.com",   "9876543277", "Jaipur"),
    (178, "Vidhi Shah",       20, "Female", "BBA",    "vidhi178@zoho.com",     "9876543278", "Ahmedabad"),
    (179, "Waseem Khan",      23, "Male",   "MCA",    "waseem179@live.com",    "9876543279", "Lucknow"),
    (180, "Xavier Dmello",    22, "Male",   "BCA",    "xavier180@ymail.com",    "9876543280", "Goa"),

    (181, "Yamini Joshi",     21, "Female", "MBA",    "yamini181@gmail.com",    "9876543281", "Mumbai"),
    (182, "Zaheer Abbas",     24, "Male",   "BCom",   "zaheer182@yahoo.com",    "9876543282", "Hyderabad"),
    (183, "Ankit Verma",      20, "Male",   "BCA",    "ankit183@outlook.com",     "9876543283", "Delhi"),
    (184, "Bhavna Singh",     23, "Female", "MCA",    "bhavna184@hotmail.com",    "9876543284", "Patna"),
    (185, "Cyrus Engineer",   22, "Male",   "BSc CS", "cyrus185@rediffmail.com",     "9876543285", "Mumbai"),

    (186, "Diya Kapoor",      21, "Female", "MBA",    "diya186@protonmail.com",      "9876543286", "Chandigarh"),
    (187, "Eshwar Rao",       24, "Male",   "MCom",   "eshwar187@icloud.com",    "9876543287", "Hyderabad"),
    (188, "Fiona Thomas",     20, "Female", "BBA",    "fiona188@zoho.com",     "9876543288", "Kochi"),
    (189, "Gopal Das",        22, "Male",   "BCA",    "gopal189@live.com",     "9876543289", "Kolkata"),
    (190, "Harini Iyer",      21, "Female", "BSc IT", "harini190@ymail.com",    "9876543290", "Chennai"),

    (191, "Ishan Kapoor",     23, "Male",   "MBA",    "ishan191@gmail.com",     "9876543291", "Delhi"),
    (192, "Jyoti Mishra",     20, "Female", "BCom",   "jyoti192@yahoo.com",     "9876543292", "Prayagraj"),
    (193, "Kartik Arya",      22, "Male",   "MCA",    "kartik193@outlook.com",    "9876543293", "Bhopal"),
    (194, "Leena Fernandes",  21, "Female", "BBA",    "leena194@hotmail.com",     "9876543294", "Goa"),
    (195, "Manav Gupta",      24, "Male",   "BCA",    "manav195@rediffmail.com",     "9876543295", "Noida"),

    (196, "Nikita Roy",       20, "Female", "MBA",    "nikita196@protonmail.com",    "9876543296", "Kolkata"),
    (197, "Onkar Singh",      23, "Male",   "BSc CS", "onkar197@icloud.com",     "9876543297", "Amritsar"),
    (198, "Priti Yadav",      22, "Female", "MCom",   "priti198@zoho.com",     "9876543298", "Lucknow"),
    (199, "Rohan Patil",      21, "Male",   "BCA",    "rohan199@live.com",     "9876543299", "Pune"),
    (200, "Sakshi Jain",      20, "Female", "MBA",    "sakshi200@ymail.com",    "9876543300", "Indore"),

]


# =====================================================
# INSERT DUMMY STUDENTS
# =====================================================

def insert_dummy_students():
    """
    Inserts any dummy student records that don't already exist —
    a record is skipped only if its roll_no OR email already
    exists in the students table (INSERT OR IGNORE respects the
    roll_no PRIMARY KEY and email UNIQUE constraints for this).
    Existing students are left completely untouched.

    Returns (success: bool, inserted_count: int, skipped_count: int)
    """

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        # COUNT BEFORE INSERTING
        cursor.execute("SELECT COUNT(*) FROM students")
        before_count = cursor.fetchone()[0]

        # INSERT ALL RECORDS, SKIPPING ANY THAT CONFLICT
        # ON roll_no (PRIMARY KEY) OR email (UNIQUE)
        cursor.executemany("""
            INSERT OR IGNORE INTO students (
                roll_no,
                full_name,
                age,
                gender,
                course,
                email,
                phone,
                address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, dummy_students)

        conn.commit()

        # COUNT AFTER INSERTING
        cursor.execute("SELECT COUNT(*) FROM students")
        after_count = cursor.fetchone()[0]

        inserted_count = after_count - before_count
        skipped_count  = len(dummy_students) - inserted_count

        return True, inserted_count, skipped_count

    except Exception as error:

        print("\n[ERROR] Failed to insert dummy data:", error)
        return False, 0, 0

    finally:

        close_connection(conn, cursor)