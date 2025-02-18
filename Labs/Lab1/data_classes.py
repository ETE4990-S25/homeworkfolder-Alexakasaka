#defining the person class
class person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def to_dict(student):
        #put the parameters into a dictionary
        return {"name": self.name, "age": self.age, "email": self.email}\

#definsing student class that inherits from person
class student(person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
    
    def to_dict(self):
        person_dict = super().to_dict()
        person_dict["student_id"] = self.student_id
        return person_dict
#stolen from the lecture notes and copilot
##class to save and display data
class DataHandler:
    @staticmethod
    def save_to_json(filename, people):
        #saving the list of person and student objects to a json file
        with open(filename, 'w') as file:
            json.dump([person.to_dict() for person in people], file, indent=4) #convert object to json file

    @staticmethod
    def display_json(filename):
        try:
            #open and read the json file
            with open(filename, 'r') as file:
                data = json.load(file) 
                print(json.dumps(data, indent=4))
        except FileNotFoundError:
            print("File not found.") #if file not found, print this message


        
    


