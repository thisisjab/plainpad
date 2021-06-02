from tkinter import messagebox as msg
from tkinter.constants import CURRENT
from pandas.core.frame import DataFrame
from termcolor import colored
import plainpad_repo as repo
import tkinter as tk

APP_TITLE = "PlainPad"
APP_WIDTH = 640
APP_HEIGHT = 480
APP_PADDING = 5
APP_PRIMARY_COLOR = '#B2DFDB'
APP_PRIMARY_DARK_COLOR = '#26A69A'
APP_PRIMARY_LIGHT_COLOR = '#FAFAFA'
# This is used to save index of notes listbox row + row's note_id
# Its format is like ('notes_listbox_row_index, note_id)
LIST_OF_IDS = []

# Used for initializing data.csv
repo.create_data()


def load_lbox_notes_data():
    del LIST_OF_IDS[:]
    lbox_notes.delete(0, tk.END)
    for index, row in repo.get_notes().iterrows():
        # Inserting the name without first and last character
        # First and last character in note name repersent double quote
        lbox_notes.insert(index, row['Name'][1:-1])
        LIST_OF_IDS.append((index, row['Id']))


def open_note():
    if lbox_notes.curselection():
        # First it gets index of selected row
        # Second finds the tuple in `LIST_OF_IDS` that holds this index
        # Then gets note id from that tuple's second index
        note = repo.get_note(LIST_OF_IDS[lbox_notes.curselection()[0]][1])
        rb_value.set(2)
        entry_note_name.delete(0, tk.END)
        entry_note_name.insert(0, note.iloc[0]['Name'])
        entry_note_content.delete(1.0, tk.END)
        entry_note_content.insert(1.0, note.iloc[0]['Content'])
    else:
        msg.showerror("Error", "Select a note to open!")


def save_note():
    note_name = entry_note_name.get()
    note_content = entry_note_content.get(1.0, tk.END)
    if note_name == '' or note_name.isspace():
        msg.showerror('Error', 'Please specify a name for your note.')
    else:
        rb = rb_value.get()
        if rb == 1:  # Add
            repo.add_note(note_name, note_content)
            load_lbox_notes_data()
        elif rb == 2:  # Update
            if lbox_notes.curselection():
                # First it gets index of selected row
                # Second finds the tuple in `LIST_OF_IDS` that holds this index
                # Then gets note id from that tuple's second index
                index = lbox_notes.curselection()[0]
                note_id = LIST_OF_IDS[index][1]
                repo.update_note(note_id, note_name, note_content)
                load_lbox_notes_data()
            else:
                msg.showerror('Error', 'Select a note to edit')


def delete_note():
    if lbox_notes.curselection():
        # First it gets index of selected row
        # Second finds the tuple in `LIST_OF_IDS` that holds this index
        # Then gets note id from that tuple's second index
        index = lbox_notes.curselection()[0]
        note_id = LIST_OF_IDS[index][1]
        repo.remove_note(note_id)
        load_lbox_notes_data()
    else:
        msg.showerror('Error', 'Select a note to delete')


def find_note():
    filter = entry_search.get()
    notes = repo.find_notes(filter)
    del LIST_OF_IDS[:]
    lbox_notes.delete(0, tk.END)
    for index, row in notes.iterrows():
        lbox_notes.insert(index, row['Name'][1:-1])
        tp = (index, row['Id'])
        print(tp, type(tp))
        LIST_OF_IDS.append(tp)


main_window = tk.Tk()
main_window.title(APP_TITLE)
main_window.geometry(str(APP_WIDTH) + 'x' + str(APP_HEIGHT))
main_window.minsize(APP_WIDTH - 100, APP_HEIGHT - 100)
main_window.config(padx=APP_PADDING, pady=APP_PADDING, bg=APP_PRIMARY_COLOR)

# Notes Listbox
notes_frame = tk.Frame(main_window)
notes_frame.config(bg=APP_PRIMARY_LIGHT_COLOR)
notes_frame.grid(row=0, column=0, sticky='news')
notes_frame.rowconfigure(0, weight=1)
notes_frame.columnconfigure(0, weight=1)
lbox_notes = tk.Listbox(notes_frame)
lbox_notes.grid(row=0, column=0, pady=5, padx=5, sticky='news')
lbox_notes.config(borderwidth=0, highlightthickness=0,)
scroll_notes = tk.Scrollbar(notes_frame, orient=tk.VERTICAL,
                            command=lbox_notes.yview)
scroll_notes.grid(row=0, column=1, sticky='nes')
lbox_notes['yscrollcommand'] = scroll_notes.set

# Toolbar frame
toolbar_frame = tk.Frame(main_window, bg=APP_PRIMARY_COLOR)
toolbar_frame.grid(row=0, column=1, sticky='news')
toolbar_frame.columnconfigure(0, weight=1)
toolbar_frame.columnconfigure(1, weight=1)
toolbar_frame.columnconfigure(2, weight=1)
toolbar_frame.columnconfigure(3, weight=1)
toolbar_frame.rowconfigure(2, weight=1)

# Toolbar main buttons
btn_open = tk.Button(toolbar_frame, text='Open',
                     bg=APP_PRIMARY_DARK_COLOR, border=0, command=open_note)
btn_delete = tk.Button(toolbar_frame, text='Delete',
                       bg=APP_PRIMARY_DARK_COLOR, border=0,
                       command=delete_note)
btn_save = tk.Button(toolbar_frame, text='Save',
                     bg=APP_PRIMARY_DARK_COLOR, border=0, command=save_note)
btn_open.grid(row=0, column=0, sticky='new', padx=2)
btn_delete.grid(row=0, column=1, sticky='new', padx=2)
btn_save.grid(row=0, column=2, sticky='new', columnspan=2, padx=2)

# Tollbar note name
lbl_note_name = tk.Label(toolbar_frame, text='Note Name', bg=APP_PRIMARY_COLOR)
lbl_note_name.grid(row=1, column=0, pady=5, padx=5, sticky='nes')
entry_note_name = tk.Entry(toolbar_frame)
entry_note_name.grid(row=1, column=1, pady=5, sticky='news')

# Add note or Edit note radiobuttons
rb_value = tk.IntVar()
rb_value.set(1)
radio1 = tk.Radiobutton(
    toolbar_frame, text='Add Note', value=1, variable=rb_value,
    bg=APP_PRIMARY_COLOR)
radio2 = tk.Radiobutton(
    toolbar_frame, text='Edit Note', value=2, variable=rb_value,
    bg=APP_PRIMARY_COLOR)
radio1.grid(row=1, column=2, sticky='w')
radio2.grid(row=1, column=3, sticky='w')

# Toolbar content frame that holds a text and a scrollbar
content_frame = tk.Frame(toolbar_frame, bg=APP_PRIMARY_COLOR)
content_frame.grid(row=2, column=0, columnspan=4,
                   sticky='news', padx=1, pady=5)
content_frame.columnconfigure(0, weight=1)
content_frame.rowconfigure(0, weight=1)
entry_note_content = tk.Text(content_frame, width=1)
entry_note_content.grid(row=0, column=0, sticky='news')
scroll_content = tk.Scrollbar(content_frame, orient=tk.VERTICAL,
                              command=entry_note_content.yview)

scroll_content.grid(row=0, column=1, padx=2, sticky='ns')
entry_note_content['yscrollcommand'] = scroll_content.set

# Search bar for searching notes - placed in buttom
entry_search = tk.Entry(main_window)
entry_search.grid(row=2, column=1, sticky='new', pady=5, padx=2)
btn_search = tk.Button(main_window, text='Find',
                       bg=APP_PRIMARY_DARK_COLOR, border=0, command=find_note)
btn_search.grid(row=2, column=0, sticky='new', padx=2, pady=2)

load_lbox_notes_data()
main_window.rowconfigure(0, weight=1)
main_window.columnconfigure(0, weight=1)
main_window.columnconfigure(1, weight=10)
main_window.mainloop()
