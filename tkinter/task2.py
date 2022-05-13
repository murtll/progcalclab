from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Action:
    def __init__(self, action, name, default_enabled=False):
        self.apply = action
        self.name = name
        self.default_enabled = default_enabled

        self.checkbox = None
        self.enabled_var = None


actions = {
    'rect': [
        Action(lambda x, y: 2 * (x + y), 'Per'),
        Action(lambda x, y: x * y, 'Sqr')
    ],
    'calc': [
        Action(lambda x, y: x + y, 'Sum'),
        Action(lambda x, y: x - y, 'Sub'),
        Action(lambda x, y: x * y, 'Mul'),
        Action(lambda x, y: x / y, 'Div')
    ]
}


def clear():
    global a
    global b
    global answer
    global rect_canvas

    answer_label.configure(foreground='#be9a52')
    answer.set('Enter some values\nthen click "Calculate"')

    a.set('')
    b.set('')

    rect_canvas.delete('all')

def swap():
    global a
    global b

    tmp = a.get()
    a.set(b.get())
    b.set(tmp)

    calculate()

def calculate():
    global a
    global b
    global answer
    global answer_label
    global chosen_kind_var

    chosen_kind = chosen_kind_var.get()
    answer_label.configure(foreground='#be9a52')

    try:
        a_float = float(a.get())
        b_float = float(b.get())

        if chosen_kind == 'rect' and (a_float < 0 or b_float < 0):
            raise ValueError('Both numbers must be greater than 0 when chosen kind is rectangle!')

        result = 'Answers: \n'

        for action in actions[chosen_kind]:
            if action.enabled_var.get():
                current_ans = action.apply(a_float, b_float)
                str_ans = ''

                if current_ans == int(current_ans):
                    str_ans = str(int(current_ans))
                else:
                    str_ans = '%.2f' % current_ans

                result += f'\n{action.name}: {str_ans}'
        
        answer.set(result)
    except:
        answer.set('Invalid input')
        answer_label.configure(foreground='#ff0000')

def validate_callback(_input):
    try:
        float(_input)
        return True
    except:
        pass

    if _input == '' or _input == '-':
        return True

    return False

def display_actions():
    global ops_menu
    global content
    global chosen_kind_var

    chosen_kind = chosen_kind_var.get()

    for e in actions['calc' if chosen_kind == 'rect' else 'rect']:
        if e.checkbox != None:
            e.checkbox.grid_remove()

    ops_menu.delete(2, 5)

    for i, action in enumerate(actions[chosen_kind]):
        if action.enabled_var == None:
            action.enabled_var = BooleanVar()
            action.enabled_var.set(action.default_enabled)

        action.checkbox = ttk.Checkbutton(content, text=action.name, variable=action.enabled_var, onvalue=True)

        action.checkbox.grid(row=4, column=i)

        ops_menu.add_checkbutton(variable=action.enabled_var, label=action.name)

def display_help():
    global root

    help_window = messagebox.Message(root, title='Help', message='ты пидорас')
    help_window.show()

if __name__ == '__main__':
    root = Tk()
    root.geometry('800x400')

    menu_bar = Menu(root)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    ops_menu = Menu(menu_bar, tearoff=0)
    ops_menu.add_command(label="Clear", command=clear)
    ops_menu.add_separator()

    menu_bar.add_cascade(label="Ops", menu=ops_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About...", command=display_help)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)


    mainstyle = ttk.Style()
    mainstyle.configure('.', background='#1e1e1e', font=('Droid Sans Mono', 10), foreground='#3885bf')
    mainstyle.configure('TButton', foreground='#42c39d')
    mainstyle.configure('TCheckbutton', foreground='#c87f4d')
    mainstyle.configure('TEntry', foreground='#1e1e1e')    
    mainstyle.map('.', background=[('active', '#2e2e2e'), ('pressed', '#2e2e2e')])

    content = ttk.Frame(root, padding=(3,3,12,12))
    frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=100, height=100)

    a = StringVar()
    b = StringVar()

    answer = StringVar()
    answer.set('Enter some values\nthen click "Calculate"')

    validate = root.register(validate_callback)

    a_label = ttk.Label(content, text="First number:")
    a_entry = ttk.Entry(content, textvariable=a, validate='key', validatecommand=(validate, '%P'), justify = CENTER, font=('Droid Sans Mono', 12))
    a_entry.focus_force()

    b_label = ttk.Label(content, text="Second number:")
    b_entry = ttk.Entry(content, textvariable=b, validate='key', validatecommand=(validate, '%P'), justify = CENTER, font=('Droid Sans Mono', 12))

    answer_label = ttk.Label(frame, textvariable=answer, foreground='#be9a52', font=('Droid Sans Mono', 12))
    
    chosen_kind_var = StringVar()
    chosen_kind_var.set('calc')

    calc_radio = ttk.Radiobutton(content, text='Calculator', variable=chosen_kind_var, value='calc', command=display_actions)
    rect_radio = ttk.Radiobutton(content, text='Rectangle', variable=chosen_kind_var, value='rect', command=display_actions)

    display_actions()


    calculate_button = ttk.Button(content, text="Calculate", command=calculate)
    clear_button = ttk.Button(content, text="Clear", command=clear)
    swap_button = ttk.Button(content, text="Swap", command=swap)


    content.grid(column=0, row=0, sticky=(N, S, E, W))
    frame.grid(column=0, row=0, columnspan=4, rowspan=3, sticky=(N, S, E, W))
    answer_label.grid(column=0, row=0, pady=5, padx=5)

    calc_radio.grid(row=3, column=0, pady=5, padx=5, columnspan=2)
    rect_radio.grid(row=3, column=2, pady=5, padx=5, columnspan=2)

    a_label.grid(column=4, row=1, columnspan=2, sticky=(N, W), padx=5)
    a_entry.grid(column=4, row=2, columnspan=2, sticky=(N, W), pady=5, padx=5)
    b_label.grid(column=4, row=3, columnspan=2, sticky=(N, W), padx=5)
    b_entry.grid(column=4, row=4, columnspan=2, sticky=(N, W), pady=5, padx=5)

    calculate_button.grid(column=6, row=2)
    clear_button.grid(column=6, row=3)
    swap_button.grid(column=6, row=4)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.columnconfigure(0, weight=4)
    content.columnconfigure(1, weight=4)
    content.columnconfigure(2, weight=4)
    content.columnconfigure(3, weight=4)
    content.columnconfigure(4, weight=1)
    content.columnconfigure(5, weight=1)
    content.columnconfigure(6, weight=1)
    content.rowconfigure(0, weight=1)

    frame.rowconfigure(1, weight=4)

    root.mainloop()