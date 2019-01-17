class Job:
    def __init__(self, job):
        self.id = job.get_attribute("id")
        self.name = job.find_element_by_class_name("name").text
        self.title = job.find_element_by_class_name("title").text
        self.date = job.find_element_by_class_name("itemDate").text
        self.start = job.find_element_by_class_name("startTime").text
        self.end = job.find_element_by_class_name("endTime").text
        self.location = job.find_element_by_class_name("locationName").text

    def job_message(self):
        return (self.name + "\n" + self.title + "\nFrom " + self.start + " to "
            + self.end + "\nOn " + self.date + "\nAt " + self.location+ "\n\n")

    def get_id(self):
        return self.id