import PySimpleGUI as sg

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

menu_layout = [
    ["File", ["Save", "Save in Server"]],
    ["Open", ["Open", "Open in Server"]],
    ["Download"],
]

layout = [
    [sg.Menu(menu_layout, tearoff=True)],
    [sg.Text('Untitle', key='-Notename-', enable_events=True)],
    [sg.Multiline(default_text='Write your note here', size=(
        30, 10), key='-Text-', autoscroll=True, no_scrollbar=True, expand_y=True, expand_x=True)],
]

window = sg.Window('E-Note', layout, resizable=True)

# Initialize the value list for later use
value = []
while True:
    event, value = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == '-Notename-':
        notename = sg.popup_get_text('Enter the name of the note')
        window['-Notename-'].update(notename)

window.close()
