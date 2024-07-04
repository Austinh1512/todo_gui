import FreeSimpleGUI as sg
import json

with open("todos.json", "r") as f:
    data = json.load(f)
    todos = data["todos"]

BTN_SIZE = (7, 1)
LISTBOX_VALUES = [todo["text"] for todo in todos]

sg.theme("DarkBlue13")

listbox_column_layout = [
    [sg.Listbox(values=LISTBOX_VALUES, key="-TODOS_LIST-", size=50, expand_y=True, horizontal_scroll=True)]
]

buttons_column_layout = [
    [sg.Button("Complete", key="-COMPLETE_TODO_BTN-", size=BTN_SIZE)],
    [sg.Button("Edit", key="-EDIT_TODO_BTN-", size=BTN_SIZE)],
    [sg.Button("Delete", key="-DELETE_TODO_BTN-", size=BTN_SIZE)]
]

frame_layout = [
    [sg.Column(listbox_column_layout, expand_x=True, expand_y=True), sg.Column(buttons_column_layout)]
]


layout = [
    [sg.InputText(key="-ADD_TODO-", tooltip="Add a task"), sg.Button("Add", key="-ADD_TODO_BTN-", size=BTN_SIZE)],
    [sg.Frame("To-Dos",frame_layout, key="-TODO_FRAME-", expand_x=True)],
    [sg.Button("Cancel", size=BTN_SIZE)]
]

window = sg.Window("Todo App", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"): break
    print(event, values)
    match event:
        case "-ADD_TODO_BTN-":
            window["-TODOS_LIST-"].update([values["-ADD_TODO-"]] + window["-TODOS_LIST-"].get_list_values())
            window["-ADD_TODO-"].update("")
            

window.close()

