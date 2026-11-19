import sys
import json
from PyQt.QtWidgets import *
from PyQt.QtCore import *
from PyQt.QtGui import *


class TaskWidget(QWidget):
    def __init__(self, text, parent, task_id):
        super().__init__()
        self.parent = parent
        self.task_id = task_id
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.toggle_task)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.update_style(False)
        
        self.delete_btn = QPushButton("x")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.clicked.connect(self.delete_task)
        
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.delete_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #404040; border-radius: 5px; margin: 2px;")
    
    def toggle_task(self):
        completed = self.checkbox.isChecked()
        self.update_style(completed)
        self.parent.save_and_update()
    
    def update_style(self, completed):
        color = "#888" if completed else "white"
        decoration = "line-through" if completed else "none"
        self.label.setStyleSheet(f"color: {color}; text-decoration: {decoration}; padding: 5px;")
    
    def delete_task(self):
        self.parent.delete_task(self.task_id)
        self.setParent(None)
        self.deleteLater()


class TaskTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.next_id = 1
        self.initUI()
        self.load_tasks()
    
    def initUI(self):
        self.setWindowTitle("Трекер задач")
        self.setGeometry(100, 100, 500, 400)
        
        widget = QWidget()
        widget.setStyleSheet("background-color: #606060;")
        self.setCentralWidget(widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Новая задача...")
        self.task_input.setStyleSheet("padding: 8px; background: #404040; color: white;")
        self.task_input.returnPressed.connect(self.add_task)
        
        self.tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout()
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.tasks_widget.setLayout(self.tasks_layout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.tasks_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: #505050; border: none;")
        
        self.stats_label = QLabel("Всего: 0 | Выполнено: 0")
        self.stats_label.setStyleSheet("color: white; padding: 5px;")
        
        layout.addWidget(self.task_input)
        layout.addWidget(scroll)
        layout.addWidget(self.stats_label)
        
        widget.setLayout(layout)
    
    def add_task(self):
        text = self.task_input.text().strip()
        if text:
            task = TaskWidget(text, self, self.next_id)
            self.tasks_layout.addWidget(task)
            self.tasks.append({'id': self.next_id, 'widget': task})
            self.next_id += 1
            self.task_input.clear()
            self.save_and_update()
    
    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_and_update()
    
    def save_and_update(self):
        data = []
        for task in self.tasks:
            widget = task['widget']
            data.append({
                'id': task['id'],
                'text': widget.label.text(),
                'completed': widget.checkbox.isChecked()
            })
        
        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump({'tasks': data, 'next_id': self.next_id}, f, ensure_ascii=False)
        
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['widget'].checkbox.isChecked())
        percent = (completed / total * 100) if total > 0 else 0
        self.stats_label.setText(f"Всего: {total} | Выполнено: {completed} ({int(percent)}%)")
    
    def load_tasks(self):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for task_data in data.get('tasks', []):
                    task = TaskWidget(task_data['text'], self, task_data['id'])
                    task.checkbox.setChecked(task_data['completed'])
                    task.update_style(task_data['completed'])
                    self.tasks_layout.addWidget(task)
                    self.tasks.append({'id': task_data['id'], 'widget': task})
                
                self.next_id = data.get('next_id', 1)
        except:
            pass
        
        self.save_and_update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(96, 96, 96))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(64, 64, 64))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(80, 80, 80))
    palette.setColor(QPalette.ButtonText, Qt.white)
    app.setPalette(palette)
    
    window = TaskTracker()
    window.show()
    sys.exit(app.exec_())
