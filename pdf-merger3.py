import sys
import os
import PyPDF2

merger = PyPDF2.PdfFileMerger()

def ind_merge():
    list = []
    print('Please drag and drop the files. When finished, press Enter: ')
    while True:
        inputs = input()
        if inputs == '':
            break
        else:
            list.append(inputs)

    #iterate among the documents
    s = 0
    for pdf in list:

      #para evitar la mierda del "DS_Store" que tira errores y no corre
        if pdf.endswith('.pdf'):
            s = s + 1 
            merger.append(pdf)
            print(f'{s} merged...')

    name = input('With what name should we save the file? ')
    where = input('And now, where do you want to save it? For the default directory, just press Enter. Else, drag and drop the destination folder: ')
    if where == '':
        os.chdir(os.getcwd())
        merger.write(f'{name}.pdf')
    else:
        os.chdir(where)
        merger.write(f'{name}.pdf')
    print('All done!')

def folder_merge():
    print('Please drag and drop the folder containing files. Press enter when finished:')
    while True:
        folder = input()
        if folder == '':
            break
        else:
            pdf_list = [os.path.join(folder,file) for file in os.listdir(folder)]

    #iterate among the documents
    s = 0
    print(pdf_list)
    for pdf in pdf_list:

      #para evitar la mierda del "DS_Store" que tira errores y no corre
        if pdf.endswith('.pdf'):
            s = s + 1
            merger.append(pdf)
            print(f'{s} merged...')

    name = input('With what name should we save the file? ')
    print('And now, where do you want to save it?')
    where = input('For the current directory, just press Enter. Else, drag and drop the destination folder: ')
    if where == '':
        os.chdir(os.getcwd())
        merger.write(f'{name}.pdf')
    else:
        os.chdir(where)
        merger.write(f'{name}.pdf')
    print('All done!')

what_prog = int(input('Enter 1 for folder merge or 2 for individual merge: '))

if what_prog == 1:
    folder_merge()
elif what_prog == 2:
    ind_merge()


