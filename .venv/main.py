import FreeSimpleGUI as sg
import json

# Retrieve initial todos
with open("todos.json", "r") as f:
    data = json.load(f)
    todos = data["todos"]

# Define constants
BTN_SIZE = (7, 1)
ACTIVE_TODOS = [todo["task"] for todo in todos if todo["completed"] is False]
COMPLETED_TODOS = [todo["task"] for todo in todos if todo["completed"] is True]

sg.theme("DarkBlue13")

# Define layouts
active_todos_tab = sg.Tab(title="Active", layout=[
    [sg.Listbox(values=ACTIVE_TODOS, key="-ACTIVE_TODOS_LIST-", size=(50, 10), horizontal_scroll=True)]],
                          key="-ACTIVE_TAB-")

completed_todos_tab = sg.Tab(title="Completed", layout=[
    [sg.Listbox(values=COMPLETED_TODOS, key="-COMPLETED_TODOS_LIST-", size=(50, 10), horizontal_scroll=True)]],
                             key="-COMPLETED_TAB-")

todos_tab_group = sg.TabGroup([[active_todos_tab, completed_todos_tab]], key="-SELECTED_TAB-")

buttons_column_layout = [
    [sg.Button("Complete", key="-COMPLETE_TODO_BTN-", size=BTN_SIZE)],
    [sg.Button("Edit", key="-EDIT_TODO_BTN-", size=BTN_SIZE)],
    [sg.Button("Delete", key="-DELETE_TODO_BTN-", size=BTN_SIZE)]
]

frame_layout = [
    [sg.Column([[todos_tab_group]]), sg.Column(buttons_column_layout)]
]

layout = [
    [sg.InputText(key="-ADD_TODO-", tooltip="Add a task"), sg.Button("Add", key="-ADD_TODO_BTN-", size=BTN_SIZE)],
    [sg.Frame("To-Dos", frame_layout, key="-TODO_FRAME-")],
    [sg.Button("Cancel", size=BTN_SIZE)]
]

window = sg.Window("Todo App", layout)

# Event loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    print(event, values)
    match event:
        case "-ADD_TODO_BTN-":
            if not values["-ADD_TODO-"]:
                sg.popup("There's no task to add.")
            window["-ACTIVE_TODOS_LIST-"].update(
                window["-ACTIVE_TODOS_LIST-"].get_list_values() + [values["-ADD_TODO-"]])
            window["-ADD_TODO-"].update("")
            todos.append({"task": values["-ADD_TODO-"], "completed": False})
        case "-DELETE_TODO_BTN-":
            try:
                list_key = "-ACTIVE_TODOS_LIST-" if len(values["-ACTIVE_TODOS_LIST-"]) else "-COMPLETED_TODOS_LIST-"
                todos = [todo for todo in todos if todo["task"] != values[list_key][0]]
                window[list_key].update(
                    [todo for todo in window[list_key].get_list_values() if todo != values[list_key][0]])
            except IndexError:
                sg.popup_error("No task selected to delete.", title="Error")
        case "-COMPLETE_TODO_BTN-":
            try:
                for todo in todos:
                    if todo["task"] == values["-ACTIVE_TODOS_LIST-"][0]:
                        todo["completed"] = True
                window["-ACTIVE_TODOS_LIST-"].update([todo["task"] for todo in todos if
                                                      todo["task"] != values["-ACTIVE_TODOS_LIST-"][0] and todo[
                                                          "completed"] is False])
                window["-COMPLETED_TODOS_LIST-"].update(
                    window["-COMPLETED_TODOS_LIST-"].get_list_values() + values["-ACTIVE_TODOS_LIST-"])
            except IndexError:
                sg.popup_error("No task selected to complete.", title="Error")
        case "-EDIT_TODO_BTN-":
            try:
                selected_task = values["-ACTIVE_TODOS_LIST-"][0]
                edited_task = sg.popup_get_text(message="Edit task:", default_text=selected_task)
                for todo in todos:
                    if todo["task"] == selected_task:
                        todo["task"] = edited_task
                window["-ACTIVE_TODOS_LIST-"].update([todo["task"] for todo in todos if todo["completed"] is False])
            except IndexError:
                sg.popup_error("No task selected to edit.", title="Error")

# Write changes to json file
new_todos = {"todos": todos}
with open("todos.json", "w") as f:
    json.dump(new_todos, f, indent=4)

window.close()
