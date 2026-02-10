import json
import os

class Task:
    def __init__(self, id, title, description, status=False):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, id, title, description):
        new_task = Task(id, title, description)
        self.tasks.append(new_task)
        self.save_tasks()

    def list_tasks(self):
        for task in self.tasks:
            print(f"ID: {task.id}, Title: {task.title}, Description: {task.description}, Status: {'Completed' if task.status else 'Pending'}")

    def mark_task_completed(self, id):
        for task in self.tasks:
            if task.id == id:
                task.status = True
                self.save_tasks()
                return
        print("Task not found.")

    def save_tasks(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**data) for data in tasks_data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading tasks: {e}")

# Example usage
task_manager = TaskManager()
task_manager.add_task(1, "Buy groceries", "Milk, Eggs, Bread, Butter")
task_manager.add_task(2, "Clean house", "Living room, Kitchen, Bathroom")
task_manager.list_tasks()
task_manager.mark_task_completed(1)
task_manager.list_tasks()