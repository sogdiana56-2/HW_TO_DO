import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        checkbox = ft.Checkbox(value=bool(completed))

        # Обновление состояния в базе при смене чекбокса
        def toggle_completed(e):
            main_db.update_task_completed(task_id, checkbox.value)
        checkbox.on_change = toggle_completed

        # Редактирование задачи
        def enable_edit(_):
            task_field.read_only = False
            task_field.update()
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать", on_click=enable_edit, icon_color=ft.Colors.ORANGE_700)

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()
        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED_700)

        return ft.Row([checkbox, task_field, edit_button, save_button, delete_button])

    def add_task(_):
        if task_input.value:
            task_id = main_db.add_task(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value, False))
            task_input.value = ''
            page.update()

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все"),
        ft.ElevatedButton("В работе"),
        ft.ElevatedButton("Готово")
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    def clear_completed_tasks(_):
        main_db.delete_completed_tasks()
        load_task()
    clear_button = ft.ElevatedButton("Очистить выполненные", on_click=clear_completed_tasks)

    task_input = ft.TextField(label='Введите новую задачу', expand=True)
    add_button = ft.IconButton(icon=ft.Icons.ADD, tooltip='Добавить задачу', on_click=add_task)

    page.add(
        ft.Row([task_input, add_button]),
        filter_buttons,
        clear_button,
        task_list
    )

    load_task()

if __name__ == '__main__':
    main_db.init_db() 
    ft.app(target=main)
