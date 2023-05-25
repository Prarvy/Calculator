# Designed by Prakash Srinivasan ( prarvy@gmail.com )
# Project Name: Calculator
# Version: 1.0: Base version by author
import tkinter as tk


# Convert Float numbers (with zero after decimal point) to Integers
def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num


# Calculate the length excluding the '-' and '.' symbol
def check_length(num):
    count = 0
    for _ in num:
        if _ == '.' or _ == '-':
            pass
        else:
            count += 1
    return count


class Calculator:
    # Initialize the Calculator parameters
    def __init__(self, _window):

        self.window = _window
        self.c_no = None  # Current Number
        self.p_no = None  # Previous Number
        self.c_op = None  # Current Operator
        self.p_op = None  # Previous Operator
        self.c_cl = None  # Current Click
        self.p_cl = None  # Previous Click
        self.l_cl = None  # Last Click
        self.t_er = None  # Temporary Error
        self.t_no = None  # Temporary Number
        self.display = None

        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.operators = ['+', '-', '/', '*']
        self.font_style = ('Arial Bold', 25)
        self.display_font_style = ('Arial Bold', 45)
        self.board = ['7', '8', '9', ' ', '+',
                      '4', '5', '6', ' ', '-',
                      '1', '2', '3', '=', '*',
                      '0', 'C', '.', '+/-', '/']
        self.display_keys()

    # Display Calculator layout
    def display_keys(self):

        self.c_no = '0'
        self.p_no = ''
        self.c_op = ''
        self.p_op = ''
        self.c_cl = ''
        self.p_cl = ''
        self.l_cl = ''
        self.t_er = False

        self.display = tk.Label(self.window, text=self.c_no, font=self.display_font_style,
                                width=10, height=1, justify='right', anchor=tk.NE, bg='white',
                                fg='dark green', borderwidth=3, padx=10, pady=10)
        self.display.grid(row=0, column=0, columnspan=5)

        for i in range(20):
            if i == 3 or i == 8:  # No Buttons
                pass
            else:
                if i in (4, 9, 14, 19):
                    bg_color = 'orange'
                elif i == 13:
                    bg_color = 'green'
                elif i in (16, 17, 18):
                    bg_color = 'grey'
                else:
                    bg_color = 'white'
                button = tk.Button(self.window, text=self.board[i], font=self.font_style, padx=4, pady=2,
                                   borderwidth=3, width=3, height=1, bg=bg_color)
                button.grid(row=1 + (i // 5), column=i % 5)
                button.bind('<Button-1>', self.process)

    # Perform Calculator operations
    def process(self, event):
        click_event = event.widget
        current_click = click_event.cget("text")

        # Perform operations for 'C' button
        if current_click == 'C':
            self.c_no = '0'
            self.p_no = ''
            self.c_op = ''
            self.p_op = ''
            self.c_cl = ''
            self.p_cl = ''
            self.l_cl = current_click
            self.display.configure(text=self.c_no)

        # Perform operations for '.' button
        elif current_click == '.':
            if self.l_cl == '=':
                self.c_no = '0.'
                self.p_no = ''
                self.c_op = ''
                self.p_op = ''
                self.c_cl = ''
                self.p_cl = ''
                self.l_cl = current_click
            elif self.l_cl in self.operators:
                self.c_no = '0.'
                self.l_cl = current_click
            elif self.c_no == '0':
                self.c_no = '0.'
                self.l_cl = current_click
            elif current_click in [x for x in self.c_no]:
                self.l_cl = current_click
            else:
                self.c_no += current_click
                self.l_cl = current_click
            self.display.configure(text=self.c_no)

        # Perform operations for '+/-' button
        elif current_click == '+/-':
            if self.c_no == '0':
                self.c_no = '0'
            else:
                self.c_no = str(format_number(-float(self.c_no)))
            self.display.configure(text=self.c_no)

        # Perform operations for Operators button
        elif current_click in self.operators:
            if self.l_cl in self.operators:
                self.c_op = current_click
            elif self.l_cl == '=':
                self.c_no = self.c_no
                self.c_op = current_click
            else:
                self.equal_operator()
                self.p_no = self.c_no
                self.c_op = current_click
            self.l_cl = current_click
            self.display.configure(text=self.c_no)

        # Perform operations for Numbers button
        elif current_click in self.numbers:
            if self.l_cl in self.operators:
                self.p_no = self.c_no
                self.c_no = current_click

            elif self.l_cl == '=':
                self.c_no = current_click
                self.p_no = ''
                self.c_op = ''
                self.p_op = ''
                self.c_cl = ''
                self.p_cl = ''
            elif self.l_cl == '.':
                self.c_no += current_click
            elif self.l_cl == '0':
                if self.c_no == '0':
                    if check_length(self.c_no) >= 10:
                        pass
                    else:
                        self.c_no = current_click
                else:
                    if check_length(self.c_no) >= 10:
                        pass
                    else:
                        self.c_no += current_click
            elif self.l_cl in self.numbers:
                if check_length(self.c_no) >= 10:
                    pass
                elif self.c_no != '0':
                    self.c_no += current_click
            else:
                if self.c_no == '0':
                    self.c_no = current_click
                else:
                    if check_length(self.c_no) >= 10:
                        pass
                    else:
                        self.c_no += current_click
            self.l_cl = current_click
            self.display.configure(text=self.c_no)

        # Perform operations for '=' Button
        else:
            if self.l_cl == current_click:
                self.p_no, self.c_no = self.c_no, self.p_no
                self.equal_operator()
            else:
                self.equal_operator()

            if self.t_er:
                self.display.configure(text='Error.')
                self.t_er = False
            else:
                self.display.configure(text=self.c_no)
            self.l_cl = current_click

    # Perform calculations
    def equal_operator(self):
        if self.c_op == '+':
            self.t_no = format_number(float(self.p_no) + float(self.c_no))
            if check_length(str(self.t_no)) > 10:
                self.t_er = True
            else:
                self.p_no = self.c_no
                self.c_no = str(self.t_no)
        elif self.c_op == '-':
            self.t_no = format_number(float(self.p_no) - float(self.c_no))
            if check_length(str(self.t_no)) > 10:
                self.t_er = True
            else:
                self.p_no = self.c_no
                self.c_no = str(self.t_no)
        elif self.c_op == '*':
            self.t_no = format_number(float(self.p_no) * float(self.c_no))
            if check_length(str(self.t_no)) > 10:
                if check_length(str(round(self.t_no // 1))) > 10:
                    self.t_er = True
                elif check_length(str(round(self.t_no // 1))) == 10:
                    self.p_no = self.c_no
                    self.c_no = str(round(self.t_no))
                    if check_length(self.c_no) > 10:
                        self.t_er = True
                else:
                    num_len = check_length(str(round(self.t_no // 1)))
                    self.p_no = self.c_no
                    self.c_no = str(round(self.t_no, 10 - num_len))
            else:
                self.p_no = self.c_no
                self.c_no = str(self.t_no)
        elif self.c_op == '/':
            if self.c_no == '0':
                self.t_er = True
            else:
                self.t_no = format_number(float(self.p_no) / float(self.c_no))
                if check_length(str(self.t_no)) > 10:
                    if check_length(str(round(self.t_no // 1))) > 10:
                        self.t_er = True
                    elif check_length(str(round(self.t_no // 1))) == 10:
                        self.p_no = self.c_no
                        self.c_no = str(round(self.t_no))
                        if check_length(self.c_no) > 10:
                            self.t_er = True
                    else:
                        num_len = check_length(str(round(self.t_no // 1)))
                        self.p_no = self.c_no
                        self.c_no = str(round(self.t_no, 10 - num_len))
                else:
                    self.p_no = self.c_no
                    self.c_no = str(self.t_no)
        else:
            if self.l_cl in self.numbers:
                self.p_no = self.c_no
                self.c_no = self.c_no
            elif self.l_cl == '=':
                self.c_no = self.p_no
            else:
                self.c_no = '0'


if __name__ == '__main__':
    window = tk.Tk()
    window.title('C A L C U L A T O R')
    window.config(borderwidth=8)
    window.config(background='#f2f2f2')
    window.iconbitmap(window, default="calc.ico")
    calculator = Calculator(window)
    window.mainloop()
