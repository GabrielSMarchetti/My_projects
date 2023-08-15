import pyautogui as pg
import os
import time
import PySimpleGUI as sg

IMAGE_PATH = os.path.join(os.getcwd(), 'imagens')
completed_screen = os.path.join(IMAGE_PATH, 'completed.png')
confirm_button = os.path.join(IMAGE_PATH, 'confirm.png')
browse_inactive = os.path.join(IMAGE_PATH, 'browse_inactive.png')
browse_active = os.path.join(IMAGE_PATH, 'browse_active.png')
start = os.path.join(IMAGE_PATH, 'start.png')


def locate_completed():
    dim = pg.locateOnScreen(completed_screen, confidence=0.6)
    if dim:
        confirm_button_obj = pg.locateOnScreen(
            confirm_button, confidence=0.6, region=dim)
        pg.click(confirm_button_obj)
        time.sleep(0.5)
        return True
    return False


def open_browser():
    browse_inactive_obj = pg.locateOnScreen(browse_inactive, confidence=0.8)
    browse_active_obj = pg.locateOnScreen(browse_active, confidence=0.8)
    if browse_inactive_obj:
        pg.click(browse_inactive_obj)
    elif browse_active_obj:
        pg.click(browse_active_obj)
    time.sleep(0.5)


def select_dungeon(dungeon: str):
    dungeon = os.path.join(IMAGE_PATH, f'{dungeon}.png')
    dungeon_obj = pg.locateOnScreen(dungeon, confidence=0.8)
    if (dungeon_obj):
        print('Dungeon selecionada')
        start_dungeon(dungeon_obj)
    else:
        print('Abrindo Browser')
        open_browser()
        dungeon_obj = pg.locateOnScreen(dungeon, confidence=0.8)
        start_dungeon(dungeon_obj)
    time.sleep(0.5)


def new_box(box):
    return [box[0], box[1], box[2] + 50, box[3] + 50]


def start_dungeon(box: tuple):
    start_obj = pg.locateOnScreen(start, confidence=0.6)
    new_box_region = new_box(box)
    if (start_obj):
        print('Start Encontrado')
        pg.click(start_obj)
    else:
        print('Start nao encontrado')
        pg.click(box)
        time.sleep(0.5)
        start_obj = pg.locateOnScreen(
            start, region=new_box_region, confidence=0.6)
        pg.click(start_obj)
    time.sleep(0.5)


def main():
    dungeons = ['agua', 'ar', 'fogo', 'terra', 'volcanic']
    layout = [
        [sg.Text('Qual Dungeon?'), sg.Combo(dungeons, key='dungeon')],
        [sg.Text('Quantas runs?'), sg.InputText(key='runs', size=(5, 1))],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Dungeon Bot', layout)
    event, values = window.read()
    window.close()
    times = int(values['runs'])

    while times > 0:
        open_browser()
        select_dungeon(values['dungeon'])
        while not locate_completed():
            time.sleep(2)
        times -= 1

    sg.popup_ok('Fim das runs')


if __name__ == '__main__':
    main()
