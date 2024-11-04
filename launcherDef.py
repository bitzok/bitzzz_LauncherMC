import flet as ft
import minecraft_launcher_lib as mc
import psutil as ps
import os
import subprocess

user = os.environ["USERNAME"]
mainDirectory = f"C:/Users/{user}/AppData/Roaming/.bitzzzlauncher"

versionInstalled = mc.utils.get_installed_versions(mainDirectory)
versionAvailable = mc.utils.get_version_list()
versionInstalledList = []
versionAvailableList = []

ramVirtual = ps.virtual_memory()
ramGb = int(ramVirtual.total / (1024 ** 3))
ramAsign = 4

mc.utils.get_version_list()

for versionInstalled in versionInstalled:
    versionInstalledList.append(versionInstalled['id'])

for versionAvailable in versionAvailable:
    if "type" in versionAvailable and versionAvailable["type"] == "release":
        versionAvailableList.append(versionAvailable['id'])
    

class buttonLauncher(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = "#FF89C0"
        self.color = "#5B2F44"
        self.text = text
        self.on_click = on_click

def runMinecraft(username: str, version: str) -> None:
    options = {
        'username': username,
        'uuid': '',
        'token': '',
        'jvmArguments': [f'-Xmx{ramAsign}G', f'-Xms{ramAsign}G'],
        'launcherVersion': '0.0.1'
    }
    runOptions = mc.command.get_minecraft_command(version, mainDirectory, options)
    subprocess.run(runOptions)

def configWindow(page: ft.Page):
    dialog = ft.AlertDialog(
        title=ft.Text("Configuración"),
        content=ft.Text("Asignación de memoria RAM"),
        actions=[
            ft.Slider(min=2, max=ramGb, divisions=ramGb-2, value=2, label="{value}"),
            ft.TextButton(
                text="Cerrar",
                on_click=lambda e: closeModal(page)
            )
        ]
    )
    page.dialog = dialog
    dialog.open = True
    page.update()

def closeModal(page: ft.Page):
    page.dialog.open = False
    page.update()

def valorMaximo(valorMax, valor):
    valorMax[0] = valor
