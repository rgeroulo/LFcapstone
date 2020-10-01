#The Projects class contains all the attributes that a project would have.
class Projects:
    def __init__(self, ProjectID = '', CompanyName = '', ProjectTitle = '',BME = '', CMPEN = '', CMPSC = '', DS = '', 
                ED = '', EE = '', EGEE = '', ESC = '', IE = '',MATSE = '', ME = '', Confidentiality = '', IP = '', CourseTime = '', CourseName = '', PhysicalPrototype = ''):
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