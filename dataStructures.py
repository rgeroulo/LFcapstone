# The student class contains all the attributes that a student would have.
class Students(object):
    def __init__(self, Major='', ProjectID='', TimeA='', TimeB='', TimeC='', Comments='', Student_NDA='', Student_IP='',
                 campus_id='', last_name='', first_name='', OnCampus='', Var14=''):
        self.major = Major
        self.projectID = ProjectID
        self.timeA = TimeA
        self.timeB = TimeB
        self.timeC = TimeC
        self.comments = Comments
        self.studentNDA = Student_NDA
        self.studentIP = Student_IP
        self.campusID = campus_id
        self.lastName = last_name
        self.firstName = first_name
        self.onCampus = OnCampus
        self.var14 = Var14


# The Projects class contains all the attributes that a project would have.
class Projects(object):
    def __init__(self, ProjectID='', CompanyName='', ProjectTitle='', BME='', CMPEN='', CMPSC='', DS='',
                 ED='', EE='', EGEE='', ESC='', IE='', MATSE='', ME='', Confidentiality='', IP='', CourseTime='',
                 CourseName='', PhysicalPrototype=''):
        self.projectID = ProjectID
        self.companyName = CompanyName
        self.projectTitle = ProjectTitle
        self.bme = BME
        self.cmpen = CMPEN
        self.cmpsc = CMPSC
        self.ds = DS
        self.ed = ED
        self.ee = EE
        self.egee = EGEE
        self.esc = ESC
        self.ie = IE
        self.matse = MATSE
        self.me = ME
        self.confidentiality = Confidentiality
        self.ip = IP
        self.courseTime = CourseTime
        self.courseName = CourseName
        self.physicalPrototype = PhysicalPrototype
