import FreeSimpleGUI as sg
import json

#Retrieve initial todos
with open("todos.json", "r") as f:
    data = json.load(f)
    todos = data["todos"]

#Define constants
BTN_SIZE = (7, 1)
ACTIVE_TODOS = [todo["task"] for todo in todos if todo["completed"] == False]
COMPLETED_TODOS = [todo["task"] for todo in todos if todo["completed"] == True]

sg.theme("DarkBlue13")

#Define layouts
active_todos_tab = sg.Tab(title="Active", layout=[[sg.Listbox(values=ACTIVE_TODOS, key="-ACTIVE_TODOS_LIST-", size=(50, 10), horizontal_scroll=True)]], key="-ACTIVE_TAB")

completed_todos_tab = sg.Tab(title="Completed", layout=[[sg.Listbox(values=COMPLETED_TODOS, key="-COMPLETED_TODOS_LIST-", size=(50, 10), horizontal_scroll=True)]], key="-COMPLETED_TAB")

todos_tab_group = sg.TabGroup([[active_todos_tab, completed_todos_tab]])

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
    [sg.Frame("To-Dos",frame_layout, key="-TODO_FRAME-")],
    [sg.Button("Cancel", size=BTN_SIZE)]
]

window = sg.Window("Todo App", layout)

#Event loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"): break
    print(event, values)
    match event:
        case "-ADD_TODO_BTN-":
            window["-ACTIVE_TODOS_LIST-"].update(window["-ACTIVE_TODOS_LIST-"].get_list_values() + [values["-ADD_TODO-"]])
            window["-ADD_TODO-"].update("")
            todos.append({"task": values["-ADD_TODO-"], "completed": False})
        case "-DELETE_TODO_BTN-":
            todos = [todo for todo in todos if todo["task"] != values["-ACTIVE_TODOS_LIST-"][0]]
            window["-ACTIVE_TODOS_LIST-"].update([todo["task"] for todo in todos])
        case "-COMPLETE_TODO_BTN-":
            for todo in todos:
                if todo["task"] == values["-ACTIVE_TODOS_LIST-"][0]:
                    todo["completed"] = True
            window["-ACTIVE_TODOS_LIST-"].update([todo["task"] for todo in todos if todo["task"] != values["-ACTIVE_TODOS_LIST-"][0] and todo["completed"] == False])
            window["-COMPLETED_TODOS_LIST-"].update(window["-COMPLETED_TODOS_LIST-"].get_list_values() + values["-ACTIVE_TODOS_LIST-"])


#Write changes to json file
new_todos = { "todos": todos}
with open("todos.json", "w") as f:
    json.dump(new_todos, f, indent=4)

window.close()

