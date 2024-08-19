# seenu-agent

seenu-agent is a Python package that provides a framework for creating and managing agents to perform tasks like translation, summarization, and more. The package includes three main classes: Agent, Task, and TaskManager, allowing you to create complex workflows by chaining tasks together.
Installation

# Install the package using pip:


pip install seenu-agent

Below is a sample usage of the seenu-agent package:
# Importing the Classes

from seenu_agent import Agent, Task, TaskManager

# Creating Agents 
** Translation Agent **

translation_llm = {'repo_name': 'Helsinki-NLP/opus-tatoeba-fi-en', 'operation': 'translation'}
translation_agent = Agent(name='Translator', llm=translation_llm)

** Custom Function Agent **

def custom_function(text):
    return text.lower()

custom_agent = Agent(name='Custom Function Agent', function=custom_function)

# Creating Tasks


translation_task = Task(name='Translation Task', task_id=1, agent=translation_agent)
custom_task = Task(name='Custom Function Task', task_id=3, agent=custom_agent)

# Managing Tasks

task_manager = TaskManager()
task_manager.add_task(translation_task)
task_manager.add_task(custom_task)

# Running Tasks
Sequential Mode

input_texts = ["Your text here..."]
sequential_results = task_manager.run(input_texts, mode='sequential')

for i, task_results in enumerate(sequential_results):
    print(f"Task {i+1} Results:")
    for result in task_results:
        print(f"  Result : {result}")

Example Output

plaintext

Sequential Task Output:
Task 1 Results:
  Result : Translated text here...
Task 2 Results:
  Result : Summarized text here...
Task 3 Results:
  Result : Transformed text here...


License

This project is licensed under the MIT License - see the LICENSE file for details.
