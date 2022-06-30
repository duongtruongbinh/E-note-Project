from operator import imod
import PySimpleGUI as sg
import SignIn
import SignUp


sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

PASSWORD_FORM = "Have at least six digits, at least one upper-case letter"


def LoginMenu():

    layout = [
        [sg.Text('Username: ')],
        [sg.InputText(key='-Username-')],
        [sg.Text('Password: ')],
        [sg.Text("Wrong Password", visible=False, key='-WrongPassword-')],
        [sg.InputText(key='-Password-', password_char='*', tooltip=PASSWORD_FORM),
         sg.Button("Show", key="-Show-", size=(5))],
        [sg.Button('Login'), sg.Button("Sign Up"), sg.Button('Cancel')]
    ]

    return sg.Window('Login', layout, resizable=True)


def SignUpMenu():
    layout = [
        [sg.Text('Username: ')],
        [sg.InputText(key='-Username-')],
        [sg.Text('Password: ')],
        [sg.Text(f'{PASSWORD_FORM}', visible=False, key='-WrongPassword-')],
        [sg.InputText(key='-Password1-', password_char='*',
                      tooltip=PASSWORD_FORM)],
        [sg.Text('Retype password: ')],
        [sg.Text("Unmatch Password", visible=False, key='-Unmatch-')],
        [sg.InputText(key='-Password2-', password_char='*',
                      tooltip=PASSWORD_FORM)],
        [sg.Button('Confirm'), sg.Button('Cancel')]
    ]

    return sg.Window('Sign Up', layout, resizable=True)


def Login():
    window = LoginMenu()

    while True:
        event, value = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            return False

        if event == 'Login':
            username = window['-Username-'].get()
            password = window['-Password-'].get()

            # Check password is in the correct format
            if len(password) < 6 or not any(c.isupper() for c in password):
                window['-WrongPassword-'].update(visible=True)
                window['-WrongPassword-'].update(
                    value="Password is not in the correct format")
                continue

            if SignIn.sign_in(username, password):
                sg.popup('Login Success')
                break
            else:
                sg.popup('Login Failed')
                break

        if event == '-Show-':
            if window['-Show-'].get_text() == 'Show':
                window['-Password-'].update(password_char='')
                window['-Show-'].update('Hide')
            else:
                window['-Password-'].update(password_char='*')
                window['-Show-'].update('Show')

        if event == 'Sign Up':
            window.close()
            window = SignUpMenu()

        if event == 'Confirm':
            username = window['-Username-'].get()
            password_one = window['-Password1-'].get()

            if len(password_one) < 6 or not any(c.isupper() for c in password_one):
                window['-WrongPassword-'].update(visible=True)
                continue

            password_two = window['-Password2-'].get()

            if password_one != password_two:
                window['-Unmatch-'].update(visible=True)
                continue

            if SignUp.sign_up(username, str(password_one)):
                sg.popup('Sign Up Success')
                break

    window.close()
    return True
