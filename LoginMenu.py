import PySimpleGUI as sg

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

def LoginMenu():
    layout = [
        [sg.Text('Username: ')],
        [sg.InputText(key='-Username-')],
        [sg.Text('Password: ')],
        [sg.InputText(key='-Password-', password_char='*')],
        [sg.Button('Login'),sg.Button("Sign Up"), sg.Button('Cancel')]
    ]

    return sg.Window('Login', layout, resizable=True)

def SignUpMenu():
    layout = [
        [sg.Text('Username: ')],
        [sg.InputText(key='-Username-')],
        [sg.Text('Password: ')],
        [sg.InputText(key='-Password1-', password_char='*')],
        [sg.Text('Retype password: ')],
        [sg.InputText(key='-Password2-', password_char='*')],
        [sg.Button('Confirm'), sg.Button('Cancel')]
    ]

    return sg.Window('Sign Up', layout, resizable=True)

window = LoginMenu()

while True:
    event, value = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Login':
        username = window['-Username-'].get()
        password = window['-Password-'].get()
        if username == 'admin' and password == 'admin':
            sg.popup('Login Success')
            break
        else:
            sg.popup('Login Failed')
            break
    if event == 'Signed Up':
        window.close()
        window = SignUpMenu()
    
window.close()