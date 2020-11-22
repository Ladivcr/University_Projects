#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from actualizar import list

sg.theme('DarkTeal12')

layout = [[sg.Text('Hola, bienvenido')],
          [sg.Button('Ver clientes')],
          [sg.Listbox(
            values = ['ID |  Nombre  | RFC'],
            enable_events = True,
            key = "File List",
            size = (70, 40),
            )],

          [sg.Button('Salir')]]

# Create the Window
window = sg.Window('Window Title', layout, margins=(100, 50))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Salir':  # if user closes window or clicks cancel
        break
    elif event == 'Ver clientes':
        clientes = list()

        window["File List"].update(values = clientes)


window.close()
