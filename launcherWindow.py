import flet as ft
import minecraft_launcher_lib as mc
import win32con
import win32gui
from launcherDef import *

title = ft.Text(value="bitzzz Launcher", size=35)

optionVersionAvailable = [ft.dropdown.Option(version) for version in versionAvailableList]
versionDownload = ft.Dropdown(label="Versión", options=optionVersionAvailable)
nicknameField = ft.TextField(label="Ingrese su nickname")
forgeCheck = ft.Checkbox(label="Forge", value=False)
downloadBar = ft.ProgressBar(width=600)
statusDownload = ft.Text(value="...")
downloadPercent = ft.Text(value="...")

def onRunMinecraft(e):
    username = nicknameField.value
    version = versionDownload.value
    ram = 4
    runMinecraft(username, version)

gif_image = ft.Image(src=f"resources/tizigif.gif", width=200)
image = ft.Image(src=f"resources/patrick.jpeg", width=200)
imageCamayo = ft.Image(src=f"resources/camayo.jpeg", width=200)

runMinecraftButton = buttonLauncher(text="Jugar", on_click=onRunMinecraft)
configButton = ft.IconButton(icon=ft.icons.SETTINGS)

def main(page: ft.Page):
    page.title = "bitzzz Launcher"
    page.window.width = 1200
    page.window.height = 720

    hwnd = win32gui.GetForegroundWindow()
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style &= ~win32con.WS_MAXIMIZEBOX
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & ~win32con.WS_THICKFRAME)
    win32gui.SetWindowPos(hwnd, 0, 0, 0, 1200, 720, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER | win32con.SWP_NOOWNERZORDER | win32con.SWP_FRAMECHANGED)

    configButton.on_click = lambda e: configWindow(page)

    optionVersionInstalled = [ft.dropdown.Option(version) for version in versionInstalledList]
    def versionsUpdate(e):
        optionVersionInstalledNew = [ft.dropdown.Option(version) for version in versionInstalledList]
        versionInstalledDrop.options = optionVersionInstalledNew
        page.update()
    versionInstalledDrop = ft.Dropdown(label="Versión", options=optionVersionInstalled, on_click=versionsUpdate)

    def downloadMinecraft(e):
        version = versionDownload.value
        mc.install.install_minecraft_version(version, mainDirectory, callback=callback)
        versionInstalledDrop.options.append(ft.dropdown.Option(versionDownload.value))
        versionInstalledDrop.value = versionDownload.value
        page.update()
        print("SE DESCARGO CORRECTAMENTE")
    downloadButton = buttonLauncher(text="Descargar Versión", on_click=downloadMinecraft)

    def mostrarProgreso(iteration, total):
        percent = ("{0:." + str(1) + "f}").format((iteration / float(total)))
        percentE = ("{0:." + str(2) + "f}").format(100 * (iteration / float(total)))
        porcentaje = float(percent)
        downloadBar.value = porcentaje
        downloadPercent.value = f"{percentE}%"
        page.update()

    def mostrarStatus(status):
        statusDownload.value = status
        page.update()

    valorMax = [0]

    callback = {
        "setStatus": lambda status: mostrarStatus(status),
        "setProgress": lambda valor: mostrarProgreso(valor, valorMax[0]),
        "setMax": lambda valor: valorMaximo(valorMax, valor),
    }

    page.add(
        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            title,
            configButton,
        ]),
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            gif_image,
            image,
            imageCamayo,
        ]),
        ft.Text(value="Descargar Version"),
        ft.Row(controls=[
            versionDownload,
            downloadButton,
        ]),
        ft.Column(width=620, controls = [
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Descargando..."), statusDownload]),
            ft.Row(controls=[downloadBar, downloadPercent]),
        ]),
        ft.Text(value="Jugar Minecraft"),
        ft.Row(alignment=ft.CrossAxisAlignment.END, controls=[
            nicknameField,
            versionInstalledDrop,
            forgeCheck,
            runMinecraftButton,
        ]),
    )

if __name__ == "__main__":
    ft.app(main)
