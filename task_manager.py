import json
import os
from datetime import datetime
from typing import List, Dict

class Task:
    def __init__(self, title: str, description: str = "", priority: str = "média"):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(data["title"], data["description"], data["priority"])
        task.id = data["id"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task


class TaskManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data]
            except:
                self.tasks = []
    
    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)
    
    def add_task(self, title: str, description: str = "", priority: str = "média"):
        task = Task(title, description, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Tarefa '{title}' adicionada com sucesso!")
    
    def list_tasks(self, show_completed: bool = False):
        if not self.tasks:
            print("Nenhuma tarefa encontrada.")
            return
        
        print("\n" + "="*60)
        print("LISTA DE TAREFAS")
        print("="*60)
        
        for i, task in enumerate(self.tasks, 1):
            if not show_completed and task.completed:
                continue
            
            status = "✓" if task.completed else "○"
            priority_icon = {"alta": "🔴", "média": "🟡", "baixa": "🟢"}.get(task.priority, "⚪")
            
            print(f"\n{i}. {status} {task.title}")
            print(f"   {priority_icon} Prioridade: {task.priority}")
            if task.description:
                print(f"   Descrição: {task.description}")
            print(f"   Criada em: {task.created_at}")
    
    def complete_task(self, task_number: int):
        if 1 <= task_number <= len(self.tasks):
            self.tasks[task_number - 1].completed = True
            self.save_tasks()
            print(f"✓ Tarefa '{self.tasks[task_number - 1].title}' concluída!")
        else:
            print("Número de tarefa inválido.")
    
    def delete_task(self, task_number: int):
        if 1 <= task_number <= len(self.tasks):
            task = self.tasks.pop(task_number - 1)
            self.save_tasks()
            print(f"✓ Tarefa '{task.title}' removida!")
        else:
            print("Número de tarefa inválido.")
    
    def get_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS")
        print("="*60)
        print(f"Total de tarefas: {total}")
        print(f"Concluídas: {completed}")
        print(f"Pendentes: {pending}")
        if total > 0:
            print(f"Progresso: {(completed/total)*100:.1f}%")


def main():
    manager = TaskManager()
    
    while True:
        print("\n" + "="*60)
        print("GERENCIADOR DE TAREFAS")
        print("="*60)
        print("1. Adicionar tarefa")
        print("2. Listar tarefas pendentes")
        print("3. Listar todas as tarefas")
        print("4. Concluir tarefa")
        print("5. Remover tarefa")
        print("6. Estatísticas")
        print("7. Sair")
        print("="*60)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            title = input("Título da tarefa: ").strip()
            if not title:
                print("O título não pode estar vazio.")
                continue
            description = input("Descrição (opcional): ").strip()
            priority = input("Prioridade (alta/média/baixa) [média]: ").strip().lower() or "média"
            if priority not in ["alta", "média", "baixa"]:
                priority = "média"
            manager.add_task(title, description, priority)
        
        elif choice == "2":
            manager.list_tasks(show_completed=False)
        
        elif choice == "3":
            manager.list_tasks(show_completed=True)
        
        elif choice == "4":
            manager.list_tasks(show_completed=False)
            try:
                num = int(input("\nNúmero da tarefa a concluir: "))
                manager.complete_task(num)
            except ValueError:
                print("Por favor, digite um número válido.")
        
        elif choice == "5":
            manager.list_tasks(show_completed=True)
            try:
                num = int(input("\nNúmero da tarefa a remover: "))
                manager.delete_task(num)
            except ValueError:
                print("Por favor, digite um número válido.")
        
        elif choice == "6":
            manager.get_statistics()
        
        elif choice == "7":
            print("\nAté logo! 👋")
            break
        
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
