from tkinter import *

root = Tk()

current_row = 0
first_name_label = Label(root, text="First Name")
last_name_label = Label(root, text="Last Name")
first_name_input = Entry(root)
last_name_input = Entry(root)
first_name_label.grid(row=current_row, sticky=W)
first_name_input.grid(row=current_row, column=1, sticky=E)
current_row += 1
last_name_label.grid(row=current_row, sticky=W)
last_name_input.grid(row=current_row, column=1, sticky=E)
current_row += 1

gender_label = Label(root, text="Gender")
gender_selection = StringVar()
male_option = Radiobutton(root, text="Male", variable=gender_selection, value="male")
female_option = Radiobutton(root, text="Female", variable=gender_selection, value="female")
gender_selection.set(0)
gender_label.grid(row=current_row, column=0, sticky=W, rowspan=2)
male_option.grid(row=current_row, column=1, sticky=E)
current_row += 1
female_option.grid(row=current_row, column=1, sticky=E)
current_row += 1

age_label = Label(root, text="Age")
age_label.grid(row=current_row, column=0, sticky=W)
age_spinbox = Spinbox(root, from_=10, to=99)
age_spinbox.config(font=("times", 16))
age_spinbox.grid(row=current_row, column=1, sticky=E)
current_row += 1

turtlez_label = Label(root, text="I like turtlez")
likert_label = Label(root, text="1=Strongly Disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly Agree")
turtlez_scale = Scale(root, from_=1, to=5, length=200, tickinterval=1, orient=HORIZONTAL)
turtlez_scale.set(3)
turtlez_label.grid(row=current_row, column=0, rowspan=2, sticky=W)
turtlez_scale.grid(row=current_row, column=1)
current_row += 1
likert_label.grid(row=current_row, column=1)
current_row += 1

fine_label = Label(root, text="Everything is fine")
likert_label_2 = Label(root, text="1=Strongly Disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly Agree")
fine_scale = Scale(root, from_=1, to=5, length=200, tickinterval=1, orient=HORIZONTAL)
fine_scale.set(3)
fine_label.grid(row=current_row, column=0, rowspan=2, sticky=W)
fine_scale.grid(row=current_row, column=1)
current_row += 1
likert_label_2.grid(row=current_row, column=1)
current_row += 1

meal_label = Label(root, text="Preferred meal")
meal_select_value = StringVar()
meal_select_value.set("chicken")
meal_option_menu = OptionMenu(root, meal_select_value, "chicken", "beef", "vegetarian")
meal_label.grid(row=current_row, column=0, sticky=W)
meal_option_menu.grid(row=current_row, column=1, sticky=E)
current_row += 1

def submit_info():
	result = "First Name: " + str(first_name_input.get()) + "\n"
	result += "Last Name: " + str(last_name_input.get()) + "\n"
	result += "Gender: " + str(gender_selection.get()) + "\n"
	result += "Age: " + str(age_spinbox.get()) + "\n"
	result += "I like turtlez: " + str(turtlez_scale.get()) + "\n"
	result += "Everything is fine: " + str(fine_scale.get()) + "\n"
	result += "Preferred meal: " + str(meal_select_value.get())
	print(result)
	return result

submit_button = Button(root, text="Submit", command=submit_info)
submit_button.grid(row=current_row, column=1, sticky=E)

col_count, row_count = root.grid_size()
for col in range(col_count):
    root.grid_columnconfigure(col, minsize=20)

for row in range(row_count):
    root.grid_rowconfigure(row, minsize=30)

root.mainloop()