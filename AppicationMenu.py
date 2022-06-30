import PySimpleGUI as sg
import Transfer as tf
import os


def MainMenu():
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.

    list_of_file = ['File1', 'File2', 'File3']

    note_layout = [
        [sg.Input(default_text='Untitled', key='-Notename-',
                  enable_events=True, expand_x=True)],
        [sg.Multiline(default_text='Write your note here', size=(
            30, 10), key='-Text-', autoscroll=True, no_scrollbar=True, expand_y=True, expand_x=True)],
        [sg.Button('Save', key='-Save-', expand_x=True), sg.Button("Open", key='-Open-', expand_x=True),
         sg.Button("Delete", key='-Delete-', expand_x=True)],
    ]

    dowload_layout = [
        [sg.Text('Select a file to download:')],
        [sg.Listbox(values=list_of_file, size=(30, 10), key='-FileList-',
                    no_scrollbar=True, expand_y=True, expand_x=True)],
        [sg.Button('Download', key='-Download-',
                   expand_x=True)],
    ]

    upload_layout = layout = [
        [sg.Text('Select a file to upload:')],
        [sg.Input(expand_x=True, expand_y=True),
         sg.FileBrowse(key='-FileBrowse-')],
        [sg.Button('Upload', expand_x=True)]
    ]

    layout = [
        [sg.TabGroup([
            [sg.Tab('Note', note_layout)],
            [sg.Tab('Download', dowload_layout)],
            [sg.Tab('Upload', upload_layout)]],
            key='-TabGroup-', expand_x=True, expand_y=True)]
    ]

    return sg.Window('E-Note', layout, resizable=True)


window = MainMenu()

# Initialize the value list for later use
value = []
while True:
    event, value = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == '-Save-':
        # Get the note name
        note_name = window['-Notename-'].get()
        # Get the note text
        note_text = window['-Text-'].get()
        # Save the note to resource folder
        with open(f'resource/{note_name}.txt', 'w') as f:
            f.write(note_text)
        f.close()
        # Update the list of notes
        # list_of_file = .GetListOfNotes()
        # window['-FileList-'].update(list_of_file)

    if event == '-Open-':
        # Show all the txt file in local and server
        # list_of_file = .GetListOfNotes()
        sg.popup('Open')

    if event == '-Download-':
        # Tell server to send file to this client
        file_name = window['-FileList-'].get()
        tf.SendFile(file_name)
        # Get the file from server
        tf.ReceiveFile(file_name)
        # Open the file

    if event == '-Upload-':
        # Get the file name
        file_name = window['-FileBrowse-'].get()
        # Send the file to server
        tf.SendFile(file_name)
        # Get the file from server


window.close()
