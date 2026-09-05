# ============================================================
# ToolKit 2.0
# CORE ENGINE
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

import os
import sys
import time
import json
import hashlib
import shutil
import subprocess
import platform
import datetime
import random
import tempfile
import ctypes


# ============================================================
# KONFIGURACJA
# ============================================================

APP_NAME = "ToolKit 2.0"


# ============================================================
# GŁÓWNE OKNO
# ============================================================

root = tk.Tk()

root.title(APP_NAME)

root.geometry(
    "1200x750"
)

root.minsize(
    1000,
    650
)


# ============================================================
# KOLORY
# ============================================================

BG = "#111827"
CARD = "#1f2937"
BUTTON = "#374151"
TEXT = "#f9fafb"
ACCENT = "#38bdf8"

root.configure(
    bg=BG
)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TNotebook",
    background=BG,
    borderwidth=0
)
style.configure(
    "TNotebook.Tab",
    background=CARD,
    foreground=TEXT,
    padding=[15, 8],
    font=("Segoe UI", 11, "bold")
)
style.configure(
    "Tool.TButton",
    background=BUTTON,
    foreground=TEXT,
    padding=12,
    font=("Segoe UI", 10, "bold")
)



style.map(
    "Tool.TButton",
    background=[
        (
            "active",
            ACCENT
        )
    ]
)



# ============================================================
# FUNKCJE SYSTEMOWE
# ============================================================


def popup(title,text):
    try:
        title = translate_ui_text(title)
        text = translate_ui_text(text)
    except Exception:
        pass

    messagebox.showinfo(
        title,
        text
    )



def error(text):
    try:
        title = t("Błąd")
        text = translate_ui_text(text)
    except Exception:
        title = "Błąd"

    messagebox.showerror(
        title,
        text
    )



def choose_file():

    return filedialog.askopenfilename()



def choose_folder():

    return filedialog.askdirectory()


def run_elevated_windows_command(executable, parameters=""):
    """Launch a Windows executable using the standard UAC elevation prompt."""
    if os.name != "nt":
        return False

    try:
        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            parameters,
            None,
            1
        )
        return result > 32
    except Exception:
        return False


def translate_ui_text(text):
    """Translate exact phrases and known phrases embedded in UI messages."""
    if not isinstance(text, str):
        return text

    translated = t(text)
    if translated != text:
        return translated

    for phrase in sorted(PHRASES, key=len, reverse=True):
        if phrase in translated:
            translated = translated.replace(phrase, t(phrase))
    return translated


def run_command(command):
    try:
        result = subprocess.check_output(
            command,
            shell=True,
            stderr=subprocess.STDOUT
        )
        return result.decode(errors="ignore")
    except Exception as e:
        return str(e)


# ============================================================
# HEADER
# ============================================================


header=tk.Frame(
    root,
    bg=BG
)

header.pack(
    fill="x"
)

title=tk.Label(

    header,

    text="⚡ ToolKit 2.0",

    bg=BG,

    fg=ACCENT,

    font=(

        "Segoe UI",

        28,

        "bold"

    )

)

title.pack(

    pady=20

)



subtitle=tk.Label(

    header,

    text="Professional Windows Utility Suite",

    bg=BG,

    fg=TEXT,

    font=(

        "Segoe UI",

        12

    )

)


subtitle.pack()



# ============================================================
# SYSTEM ZAKŁADEK
# ============================================================


tabs=ttk.Notebook(

    root

)


tabs.pack(

    expand=True,

    fill="both",

    padx=15,

    pady=15

)



# ============================================================
# KATEGORIE
# ============================================================


categories={}

# lists/dicts for translation support
translatable_buttons = []
tools_button_registry = []
tab_texts = {}




def create_tab(name):


    frame=tk.Frame(

        tabs,

        bg=BG

    )


    tabs.add(

        frame,

        text=name

    )


    categories[name]=frame
    # register original tab text for translation
    try:
        frame._orig_tab_text = name
    except Exception:
        pass

    tab_texts[frame] = name


    return frame



tab_dashboard=create_tab(
    "🏠 Start"
)


tab_files=create_tab(
    "📁 Pliki"
)


tab_system=create_tab(
    "💻 System"
)


tab_hardware=create_tab(
    "🔧 Hardware"
)


tab_network=create_tab(
    "🌐 Sieć"
)


tab_security=create_tab(
    "🛡 Bezpieczeństwo"
)


tab_backup=create_tab(
    "💾 Backup"
)


tab_tools=create_tab(
    "🛠 Narzędzia"
)


tab_dev=create_tab(
    "👨‍💻 Developer"
)


tab_admin=create_tab(
    "⚙ Admin"
)


tab_godmode=create_tab(
    "👑 GodMode"
)

# Language tab for changing UI language
tab_language = create_tab(
    "🌐 Język"
)


# Aliasy dla sekcji, które odwołują się do nazw z wcześniejszych wersji
# skryptu; dzięki temu przyciski trafiają do właściwych kart bez błędów.
tab_developer=tab_dev
tab_cleaner=tab_tools
tab_windows=tab_admin
tab_remote=tab_network
tab_automation=tab_tools
tab_monitor=tab_hardware
tab_advanced=tab_admin
tab_core=tab_admin



# ============================================================
# SYSTEM KAFELKÓW
# ============================================================


def add_button(
        parent,
        text,
        command,
        row,
        col
):


    host=getattr(parent, "_button_host", None)


    if host is None:

        host=tk.Frame(
            parent,
            bg=BG
        )

        host.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        parent._button_host=host


    tile_color = CARD if (row + col) % 2 == 0 else "#263549"


    tile=tk.Frame(
        host,
        bg=tile_color,
        highlightthickness=1,
        highlightbackground="#475569"
    )

    tile.grid(
        row=row,
        column=col,
        padx=8,
        pady=8,
        sticky="nsew"
    )


    display_text = text
    translator = globals().get("t")
    if translator is not None:
        display_text = translator(text)

    button=ttk.Button(

        tile,

        text=display_text,

        command=command,

        style="Tool.TButton"

    )


    button.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # register button for translation
    try:
        button._orig_text = text
        translatable_buttons.append(button)
    except Exception:
        pass

    return button



def setup_grid(frame):


    host=getattr(frame, "_button_host", None)


    if host is None:

        host=tk.Frame(
            frame,
            bg=BG
        )

        host.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        frame._button_host=host


    for i in range(4):

        host.columnconfigure(
            i,
            weight=1
        )


    for i in range(10):

        host.rowconfigure(
            i,
            weight=1
        )



for frame in categories.values():

    setup_grid(frame)


# ============================================================
# GODMODE
# ============================================================


def godmode_create_folder():

    folder_name = "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        folder_name
    )

    try:

        os.makedirs(desktop, exist_ok=True)

        popup(
            t("GodMode"),
            t("Utworzono folder:") + f"\n{desktop}"
        )

    except Exception as e:

        error(str(e))



def godmode_open_tool(target):

    try:

        if target == "admin_tools":

            run_elevated_windows_command("control.exe", "admintools")

        elif target in {"cmd", "cmd.exe"}:

            run_elevated_windows_command("cmd.exe", "/k")

        elif target in {"powershell", "powershell.exe"}:

            run_elevated_windows_command("powershell.exe", "-NoLogo")

        else:

            os.startfile(target)

        popup(t("GodMode"), t("Uruchomiono narzędzie"))

    except Exception as e:

        error(str(e))



def godmode_open_admin_tools():

    godmode_open_tool("admin_tools")



def godmode_open_cmd():

    godmode_open_tool("cmd")



def godmode_open_powershell():

    godmode_open_tool("powershell")



def godmode_open_taskmgr():

    godmode_open_tool("taskmgr")



def godmode_open_devmgmt():

    godmode_open_tool("devmgmt.msc")



def godmode_open_regedit():

    godmode_open_tool("regedit")



def godmode_open_control():

    godmode_open_tool("control")



def godmode_open_defender():

    godmode_open_tool("windowsdefender:")



def godmode_open_dxdiag():

    godmode_open_tool("dxdiag")



def godmode_open_compmgmt():

    godmode_open_tool("compmgmt.msc")



def godmode_run_sfc():

    try:

        if not run_elevated_windows_command("cmd.exe", "/k sfc /scannow"):
            raise OSError("Nie udało się uruchomić SFC z podniesieniem uprawnień")

        popup(t("GodMode"), t("Uruchomiono SFC /scannow"))

    except Exception as e:

        error(str(e))



def godmode_run_dism():

    try:

        if not run_elevated_windows_command("cmd.exe", "/k DISM /Online /Cleanup-Image /RestoreHealth"):
            raise OSError("Nie udało się uruchomić DISM z podniesieniem uprawnień")

        popup(t("GodMode"), t("Uruchomiono DISM /Online /Cleanup-Image /RestoreHealth"))

    except Exception as e:

        error(str(e))



godmode_buttons=[

    ("📁 Utwórz folder GodMode", godmode_create_folder),

    ("🛠 Panele administracyjne", godmode_open_admin_tools),

    ("💻 CMD", godmode_open_cmd),

    ("🧠 PowerShell", godmode_open_powershell),

    ("📊 Menedżer zadań", godmode_open_taskmgr),

    ("🖥 Menedżer urządzeń", godmode_open_devmgmt),

    ("🗂 Rejestr", godmode_open_regedit),

    ("🎛 Panel sterowania", godmode_open_control),

    ("🛡 Defender", godmode_open_defender),

    ("🎮 Informacje DirectX", godmode_open_dxdiag),

    ("🧰 Zarządzanie komputerem", godmode_open_compmgmt),

    ("🛠 SFC /Scannow", godmode_run_sfc),

    ("🧱 DISM Repair", godmode_run_dism)

]


row=0
col=0


for text, cmd in godmode_buttons:

    add_button(

        tab_godmode,

        text,

        cmd,
        row,
        col

    )


    col+=1


    if col==4:

        col=0

        row+=1


# ============================================================
# START SCREEN
# ============================================================



welcome=tk.Label(

    tab_dashboard,

    text="""

⚡ ToolKit 2.0


Profesjonalny zestaw narzędzi:


✓ System

✓ Pliki

✓ Sieć

✓ Hardware

✓ Backup

✓ Bezpieczeństwo

✓ Administracja

✓ Developer


Wybierz kategorię.

""",

    bg=BG,

    fg=TEXT,

    font=(

        "Segoe UI",

        15

    )

)


welcome.pack(

    pady=50

)


# --- Language switch (Polski / English / Русский) ---
translations = {
    "English": {
        "subtitle": "Professional Windows Utility Suite",
        "welcome": """

⚡ ToolKit 2.0


Professional toolset:


✓ System

✓ Files

✓ Network

✓ Hardware

✓ Backup

✓ Security

✓ Administration

✓ Developer


Choose a category.

"""
    },
    "Polski": {
        "subtitle": "Profesjonalny zestaw narzędzi",
        "welcome": welcome.cget("text")
    },
    "Русский": {
        "subtitle": "Профессиональный набор утилит",
        "welcome": """

⚡ ToolKit 2.0


Профессиональный набор утилит:


✓ Система

✓ Файлы

✓ Сеть

✓ Аппаратное обеспечение

✓ Резервное копирование

✓ Безопасность

✓ Администрирование

✓ Разработка


Выберите категорию.

"""
    }
}


# current language
current_lang = "English"


# phrase translations: original -> {lang: translation}
PHRASES = {
    # === OGÓLNE / DIALOGI ===
    "Błąd": {"English": "Error", "Polski": "Błąd", "Русский": "Ошибка"},
    "OK": {"English": "OK", "Polski": "OK", "Русский": "OK"},
    "Informacje": {"English": "Info", "Polski": "Informacje", "Русский": "Инфо"},
    "Szukaj": {"English": "Search", "Polski": "Szukaj", "Русский": "Поиск"},
    "Nazwa pliku": {"English": "File name", "Polski": "Nazwa pliku", "Русский": "Имя файла"},
    "Prefix": {"English": "Prefix", "Polski": "Prefix", "Русский": "Префикс"},
    "Hasło główne": {"English": "Master password", "Polski": "Hasło główne", "Русский": "Главный пароль"},
    "Hasło": {"English": "Password", "Polski": "Hasło", "Русский": "Пароль"},
    "Nazwa": {"English": "Name", "Polski": "Nazwa", "Русский": "Имя"},
    "Wartość": {"English": "Value", "Polski": "Wartość", "Русский": "Значение"},
    "Długość": {"English": "Length", "Polski": "Długość", "Русский": "Длина"},
    "Tekst": {"English": "Text", "Polski": "Tekst", "Русский": "Текст"},
    "Kod": {"English": "Code", "Polski": "Kod", "Русский": "Код"},
    "Domena": {"English": "Domain", "Polski": "Domena", "Русский": "Домен"},
    "Adres": {"English": "Address", "Polski": "Adres", "Русский": "Адрес"},
    "Port": {"English": "Port", "Polski": "Port", "Русский": "Порт"},
    "Prefix np. 192.168.1": {"English": "Prefix e.g. 192.168.1", "Polski": "Prefix np. 192.168.1", "Русский": "Префикс напр. 192.168.1"},
    "Nazwa pakietu": {"English": "Package name", "Polski": "Nazwa pakietu", "Русский": "Имя пакета"},
    "Projekt": {"English": "Project", "Polski": "Projekt", "Русский": "Проект"},
    "Wyrażenie": {"English": "Expression", "Polski": "Wyrażenie", "Русский": "Выражение"},
    "Schowek": {"English": "Clipboard", "Polski": "Schowek", "Русский": "Буфер обмена"},
    "Język:": {"English": "Language:", "Polski": "Język:", "Русский": "Язык:"},
    "ToolKit 2.0": {"English": "ToolKit 2.0", "Polski": "ToolKit 2.0", "Русский": "ToolKit 2.0"},
    "ToolKit 2.0.0": {"English": "ToolKit 2.0.0", "Polski": "ToolKit 2.0.0", "Русский": "ToolKit 2.0.0"},
    "GodMode": {"English": "GodMode", "Polski": "GodMode", "Русский": "GodMode"},
    "Utworzono folder:": {"English": "Folder created:", "Polski": "Utworzono folder:", "Русский": "Создана папка:"},
    "Uruchomiono narzędzie": {"English": "Tool launched", "Polski": "Uruchomiono narzędzie", "Русский": "Инструмент запущен"},
    "Pliki": {"English": "Files", "Polski": "Pliki", "Русский": "Файлы"},
    "Eksplorator": {"English": "Explorer", "Polski": "Eksplorator", "Русский": "Проводник"},
    "Skopiowano": {"English": "Copied", "Polski": "Skopiowano", "Русский": "Скопировано"},
    "Przeniesiono": {"English": "Moved", "Polski": "Przeniesiono", "Русский": "Перемещено"},
    "Usuń": {"English": "Delete", "Polski": "Usuń", "Русский": "Удалить"},
    "Usunąć plik?": {"English": "Delete file?", "Polski": "Usunąć plik?", "Русский": "Удалить файл?"},
    "Usunięto": {"English": "Deleted", "Polski": "Usunięto", "Русский": "Удалено"},
    "Zapisano raport": {"English": "Report saved", "Polski": "Zapisano raport", "Русский": "Отчет сохранен"},
    "Zapisano": {"English": "Saved", "Polski": "Zapisano", "Русский": "Сохранено"},
    "Utworzono kopię": {"English": "Backup created", "Polski": "Utworzono kopię", "Русский": "Резервная копия создана"},
    "Przywrócono": {"English": "Restored", "Polski": "Przywrócono", "Русский": "Восстановлено"},
    "Archiwum OK": {"English": "Archive OK", "Polski": "Archiwum OK", "Русский": "Архив OK"},
    "Nowa generacja Toolkit GUI": {"English": "New generation of Toolkit GUI", "Polski": "Nowa generacja Toolkit GUI", "Русский": "Новое поколение Toolkit GUI"},
    "Host": {"English": "Host", "Polski": "Host", "Русский": "Хост"},
    "Numer": {"English": "Number", "Polski": "Numer", "Русский": "Номер"},
    "Zakres np. 192.168.1.0/24": {"English": "Range e.g. 192.168.1.0/24", "Polski": "Zakres np. 192.168.1.0/24", "Русский": "Диапазон напр. 192.168.1.0/24"},
    "MAC": {"English": "MAC", "Polski": "MAC", "Русский": "MAC"},
    "Pierwszy hash": {"English": "First hash", "Polski": "Pierwszy hash", "Русский": "Первый хэш"},
    "Drugi hash": {"English": "Second hash", "Polski": "Drugi hash", "Русский": "Второй хэш"},
    "Komenda:": {"English": "Command:", "Polski": "Komenda:", "Русский": "Команда:"},
    "Sekundy:": {"English": "Seconds:", "Polski": "Sekundy:", "Русский": "Секунды:"},
    "Wpisz polecenie CMD:": {"English": "Enter CMD command:", "Polski": "Wpisz polecenie CMD:", "Русский": "Введите команду CMD:"},

    # === ZAKŁADKI (TABY) ===
    "🏠 Start": {"English": "🏠 Start", "Polski": "🏠 Start", "Русский": "🏠 Главная"},
    "📁 Pliki": {"English": "📁 Files", "Polski": "📁 Pliki", "Русский": "📁 Файлы"},
    "💻 System": {"English": "💻 System", "Polski": "💻 System", "Русский": "💻 Система"},
    "🔧 Hardware": {"English": "🔧 Hardware", "Polski": "🔧 Hardware", "Русский": "🔧 Аппаратное обеспечение"},
    "🌐 Sieć": {"English": "🌐 Network", "Polski": "🌐 Sieć", "Русский": "🌐 Сеть"},
    "🛡 Bezpieczeństwo": {"English": "🛡 Security", "Polski": "🛡 Bezpieczeństwo", "Русский": "🛡 Безопасность"},
    "💾 Backup": {"English": "💾 Backup", "Polski": "💾 Backup", "Русский": "💾 Резерв"},
    "🛠 Narzędzia": {"English": "🛠 Tools", "Polski": "🛠 Narzędzia", "Русский": "🛠 Инструменты"},
    "👨‍💻 Developer": {"English": "👨‍💻 Developer", "Polski": "👨‍💻 Developer", "Русский": "👨‍💻 Разработчик"},
    "⚙ Admin": {"English": "⚙ Admin", "Polski": "⚙ Admin", "Русский": "⚙ Админ"},
    "👑 GodMode": {"English": "👑 GodMode", "Polski": "👑 GodMode", "Русский": "👑 GodMode"},
    "🌐 Język": {"English": "🌐 Language", "Polski": "🌐 Język", "Русский": "🌐 Язык"},

    # === PLIKI (File) ===
    "📁 Eksplorator": {"English": "📁 Explorer", "Polski": "📁 Eksplorator", "Русский": "📁 Проводник"},
    "📋 Kopiuj": {"English": "📋 Copy", "Polski": "📋 Kopiuj", "Русский": "📋 Копировать"},
    "🚚 Przenieś": {"English": "🚚 Move", "Polski": "🚚 Przenieś", "Русский": "🚚 Переместить"},
    "🗑 Usuń": {"English": "🗑 Delete", "Polski": "🗑 Usuń", "Русский": "🗑 Удалить"},
    "Brak baterii": {"English": "No battery", "Polski": "Brak baterii", "Русский": "Нет батареи"},
    "System nie udostępnia temperatur": {"English": "The system does not provide temperature data", "Polski": "System nie udostępnia temperatur", "Русский": "Система не предоставляет данные о температуре"},
    "Wersja:": {"English": "Version:", "Polski": "Wersja:", "Русский": "Версия:"},
    "Python:": {"English": "Python:", "Polski": "Python:", "Русский": "Python:"},
    "Procesor:": {"English": "Processor:", "Polski": "Procesor:", "Русский": "Процессор:"},
    "Data:": {"English": "Date:", "Polski": "Data:", "Русский": "Дата:"},
    "CPU:": {"English": "CPU:", "Polski": "CPU:", "Русский": "ЦП:"},
    "Brak duplikatów": {"English": "No duplicates", "Polski": "Brak duplikatów", "Русский": "Дубликаты не найдены"},
    "Utworzono archiwum": {"English": "Archive created", "Polski": "Utworzono archiwum", "Русский": "Архив создан"},
    "Brak internetu": {"English": "No internet connection", "Polski": "Brak internetu", "Русский": "Нет подключения к Интернету"},
    "Domena": {"English": "Domain", "Polski": "Domena", "Русский": "Домен"},
    "Adres IP / Host": {"English": "IP address / Host", "Polski": "Adres IP / Host", "Русский": "IP-адрес / Хост"},
    "Zakres np. 192.168.1.0/24": {"English": "Range e.g. 192.168.1.0/24", "Polski": "Zakres np. 192.168.1.0/24", "Русский": "Диапазон, например 192.168.1.0/24"},
    "OTWARTY": {"English": "OPEN", "Polski": "OTWARTY", "Русский": "ОТКРЫТ"},
    "ZAMKNIĘTY": {"English": "CLOSED", "Polski": "ZAMKNIĘTY", "Русский": "ЗАКРЫТ"},
    "Brak dostępu": {"English": "Access denied", "Polski": "Brak dostępu", "Русский": "Нет доступа"},
    "Wysłano pakiet": {"English": "Packet sent", "Polski": "Wysłano pakiet", "Русский": "Пакет отправлен"},
    "Pakiet wysłany": {"English": "Packet sent", "Polski": "Pakiet wysłany", "Русский": "Пакет отправлен"},
    "Nazwa pluginu:": {"English": "Plugin name:", "Polski": "Nazwa pluginu:", "Русский": "Имя плагина:"},
    "Brak konfiguracji.": {"English": "No configuration.", "Polski": "Brak konfiguracji.", "Русский": "Конфигурация отсутствует."},
    "Ustawienia zapisane.": {"English": "Settings saved.", "Polski": "Ustawienia zapisane.", "Русский": "Настройки сохранены."},
    "Ustawienia wczytane.": {"English": "Settings loaded.", "Polski": "Ustawienia wczytane.", "Русский": "Настройки загружены."},
    "Włączono tryb ciemny.": {"English": "Dark mode enabled.", "Polski": "Włączono tryb ciemny.", "Русский": "Темный режим включен."},
    "Przywrócono motyw.": {"English": "Theme restored.", "Polski": "Przywrócono motyw.", "Русский": "Тема восстановлена."},
    "Proces": {"English": "Process", "Polski": "Proces", "Русский": "Процесс"},
    "Proces:": {"English": "Process:", "Polski": "Proces:", "Русский": "Процесс:"},
    "Usługa": {"English": "Service", "Polski": "Usługa", "Русский": "Служба"},
    "UŻYTKOWNICY": {"English": "USERS", "Polski": "UŻYTKOWNICY", "Русский": "ПОЛЬЗОВАТЕЛИ"},
    "Utworzono": {"English": "Created", "Polski": "Utworzono", "Русский": "Создано"},
    "Poprawny": {"English": "Valid", "Polski": "Poprawny", "Русский": "Корректный"},
    "Sformatowano": {"English": "Formatted", "Polski": "Sformatowano", "Русский": "Отформатировано"},
    "Skrypt uruchomiony.": {"English": "Script started.", "Polski": "Skrypt uruchomiony.", "Русский": "Скрипт запущен."},
    "Czas zakończony.": {"English": "Time elapsed.", "Polski": "Czas zakończony.", "Русский": "Время истекло."},
    "Automatyzacja": {"English": "Automation", "Polski": "Automatyzacja", "Русский": "Автоматизация"},
    "Brak zapisanych.": {"English": "Nothing saved.", "Polski": "Brak zapisanych.", "Русский": "Сохраненных элементов нет."},
    "Skan procesów": {"English": "Process scan", "Polski": "Skan procesów", "Русский": "Сканирование процессов"},
    "Nie wykryto dużego użycia": {"English": "No high usage detected", "Polski": "Nie wykryto dużego użycia", "Русский": "Высокая нагрузка не обнаружена"},
    "Python Editor": {"English": "Python Editor", "Polski": "Edytor Python", "Русский": "Редактор Python"},
    "Terminal": {"English": "Terminal", "Polski": "Terminal", "Русский": "Терминал"},
    "💾 Zapisz": {"English": "💾 Save", "Polski": "💾 Zapisz", "Русский": "💾 Сохранить"},
    "▶ Wykonaj": {"English": "▶ Execute", "Polski": "▶ Wykonaj", "Русский": "▶ Выполнить"},
    "📊 Informacje": {"English": "📊 Info", "Polski": "📊 Informacje", "Русский": "📊 Инфо"},
    "📦 ZIP": {"English": "📦 ZIP", "Polski": "📦 ZIP", "Русский": "📦 ZIP"},
    "📤 Rozpakuj": {"English": "📤 Unpack", "Polski": "📤 Rozpakuj", "Русский": "📤 Распаковать"},
    "🔎 Szukaj": {"English": "🔎 Search", "Polski": "🔎 Szukaj", "Русский": "🔎 Поиск"},
    "📈 Rozszerzenia": {"English": "📈 Extensions", "Polski": "📈 Rozszerzenia", "Русский": "📈 Расширения"},
    "💾 Największe": {"English": "💾 Biggest", "Polski": "💾 Największe", "Русский": "💾 Самые большие"},
    "♻ Duplikaty": {"English": "♻ Duplicates", "Polski": "♻ Duplikaty", "Русский": "♻ Дубликаты"},
    "✏ Zmień nazwy": {"English": "✏ Rename", "Polski": "✏ Zmień nazwy", "Русский": "✏ Переименовать"},

    # === SYSTEM ===
    "💻 Windows Info": {"English": "💻 Windows Info", "Polski": "💻 Windows Info", "Русский": "💻 Сведения Windows"},
    "🐍 Python Info": {"English": "🐍 Python Info", "Polski": "🐍 Python Info", "Русский": "🐍 Python Info"},
    "⚡ CPU": {"English": "⚡ CPU", "Polski": "⚡ CPU", "Русский": "⚡ CPU"},
    "🧠 RAM": {"English": "🧠 RAM", "Polski": "🧠 RAM", "Русский": "🧠 RAM"},
    "💾 Dyski": {"English": "💾 Disks", "Polski": "💾 Dyski", "Русский": "💾 Диски"},
    "📋 Procesy": {"English": "📋 Processes", "Polski": "📋 Procesy", "Русский": "📋 Процессы"},
    "⚙ Usługi": {"English": "⚙ Services", "Polski": "⚙ Usługi", "Русский": "⚙ Службы"},
    "🚀 Autostart": {"English": "🚀 Startup", "Polski": "🚀 Autostart", "Русский": "🚀 Автозапуск"},
    "🌐 Environment": {"English": "🌐 Environment", "Polski": "🌐 Environment", "Русский": "🌐 Окружение"},
    "👤 Użytkownicy": {"English": "👤 Users", "Polski": "👤 Użytkownicy", "Русский": "👤 Пользователи"},
    "🔧 Sterowniki": {"English": "🔧 Drivers", "Polski": "🔧 Sterowniki", "Русский": "🔧 Драйверы"},
    "📜 Logi": {"English": "📜 Logs", "Polski": "📜 Logi", "Русский": "📜 Логи"},
    "📈 Monitor": {"English": "📈 Monitor", "Polski": "📈 Monitor", "Русский": "📈 Монитор"},

    # === HARDWARE ===
    "🎮 GPU": {"English": "🎮 GPU", "Polski": "🎮 GPU", "Русский": "🎮 GPU"},
    "🧬 BIOS": {"English": "🧬 BIOS", "Polski": "🧬 BIOS", "Русский": "🧬 BIOS"},
    "🖥 Płyta główna": {"English": "🖥 Motherboard", "Polski": "🖥 Płyta główna", "Русский": "🖥 Материнская плата"},
    "⚡ CPU Info": {"English": "⚡ CPU Info", "Polski": "⚡ CPU Info", "Русский": "⚡ CPU Info"},
    "🧠 RAM Moduły": {"English": "🧠 RAM Modules", "Polski": "🧠 RAM Moduły", "Русский": "🧠 Модули RAM"},
    "💽 Dyski fizyczne": {"English": "💽 Physical Disks", "Polski": "💽 Dyski fizyczne", "Русский": "💽 Физические диски"},
    "💚 SMART": {"English": "💚 SMART", "Polski": "💚 SMART", "Русский": "💚 SMART"},
    "🔌 USB": {"English": "🔌 USB", "Polski": "🔌 USB", "Русский": "🔌 USB"},
    "🖥 Monitory": {"English": "🖥 Monitors", "Polski": "🖥 Monitory", "Русский": "🖥 Мониторы"},
    "🔊 Audio": {"English": "🔊 Audio", "Polski": "🔊 Audio", "Русский": "🔊 Аудио"},
    "📷 Kamera": {"English": "📷 Camera", "Polski": "📷 Kamera", "Русский": "📷 Камера"},
    "🔋 Bateria": {"English": "🔋 Battery", "Polski": "🔋 Bateria", "Русский": "🔋 Батарея"},
    "🔧 PCI": {"English": "🔧 PCI", "Polski": "🔧 PCI", "Русский": "🔧 PCI"},
    "🌡 Temperatury": {"English": "🌡 Temperatures", "Polski": "🌡 Temperatury", "Русский": "🌡 Температуры"},
    "⚙ Kontrolery": {"English": "⚙ Controllers", "Polski": "⚙ Kontrolery", "Русский": "⚙ Контроллеры"},
    "⚡ CPU Live": {"English": "⚡ CPU Live", "Polski": "⚡ CPU Live", "Русский": "⚡ CPU Live"},
    "🌀 Wentylatory": {"English": "🌀 Fans", "Polski": "🌀 Wentylatory", "Русский": "🌀 Вентиляторы"},
    "❤️ SMART": {"English": "❤️ SMART", "Polski": "❤️ SMART", "Русский": "❤️ SMART"},
    "🏁 CPU Test": {"English": "🏁 CPU Test", "Polski": "🏁 CPU Test", "Русский": "🏁 CPU Test"},
    "🏁 RAM Test": {"English": "🏁 RAM Test", "Polski": "🏁 RAM Test", "Русский": "🏁 RAM Test"},
    "🔥 CPU Stress": {"English": "🔥 CPU Stress", "Polski": "🔥 CPU Stress", "Русский": "🔥 CPU Stress"},
    "🖥 Płyta": {"English": "🖥 Motherboard", "Polski": "🖥 Płyta", "Русский": "🖥 Материнская плата"},

    # === NETWORK ===
    "🌐 Karty sieciowe": {"English": "🌐 Network Adapters", "Polski": "🌐 Karty sieciowe", "Русский": "🌐 Сетевые адаптеры"},
    "📍 Lokalny IP": {"English": "📍 Local IP", "Polski": "📍 Lokalny IP", "Русский": "📍 Локальный IP"},
    "🌍 Publiczne IP": {"English": "🌍 Public IP", "Polski": "🌍 Publiczne IP", "Русский": "🌍 Внешний IP"},
    "🔎 DNS Lookup": {"English": "🔎 DNS Lookup", "Polski": "🔎 DNS Lookup", "Русский": "🔎 DNS Lookup"},
    "📡 Ping": {"English": "📡 Ping", "Polski": "📡 Ping", "Русский": "📡 Ping"},
    "🛰 Traceroute": {"English": "🛰 Traceroute", "Polski": "🛰 Traceroute", "Русский": "🛰 Traceroute"},
    "🔌 Test portu": {"English": "🔌 Port Test", "Polski": "🔌 Test portu", "Русский": "🔌 Тест порта"},
    "📶 Skan LAN": {"English": "📶 LAN Scan", "Polski": "📶 Skan LAN", "Русский": "📶 LAN Scan"},
    "📋 ARP": {"English": "📋 ARP", "Polski": "📋 ARP", "Русский": "📋 ARP"},
    "📡 WiFi": {"English": "📡 WiFi", "Polski": "📡 WiFi", "Русский": "📡 WiFi"},
    "🔗 Połączenia": {"English": "🔗 Connections", "Polski": "🔗 Połączenia", "Русский": "🔗 Соединения"},
    "📊 Netstat": {"English": "📊 Netstat", "Polski": "📊 Netstat", "Русский": "📊 Netstat"},
    "♻ Flush DNS": {"English": "♻ Flush DNS", "Polski": "♻ Flush DNS", "Русский": "♻ Flush DNS"},
    "🌍 Test Internetu": {"English": "🌍 Internet Test", "Polski": "🌍 Test Internetu", "Русский": "🌍 Тест интернета"},
    "📡 Ping Host": {"English": "📡 Ping Host", "Polski": "📡 Ping Host", "Русский": "📡 Ping Host"},
    "🔎 Skan sieci": {"English": "🔎 Network Scan", "Polski": "🔎 Skan sieci", "Русский": "🔎 Сканирование сети"},
    "⚡ Wake LAN": {"English": "⚡ Wake LAN", "Polski": "⚡ Wake LAN", "Русский": "⚡ Wake LAN"},
    "🔢 Generator MAC": {"English": "🔢 MAC Generator", "Polski": "🔢 Generator MAC", "Русский": "🔢 Генератор MAC"},
    "🌐 Generator IP": {"English": "🌐 IP Generator", "Polski": "🌐 Generator IP", "Русский": "🌐 Генератор IP"},
    "🔐 SSH": {"English": "🔐 SSH", "Polski": "🔐 SSH", "Русский": "🔐 SSH"},
    "🖥 RDP": {"English": "🖥 RDP", "Polski": "🖥 RDP", "Русский": "🖥 RDP"},
    "🔌 Port Scan": {"English": "🔌 Port Scan", "Polski": "🔌 Port Scan", "Русский": "🔌 Port Scan"},
    "🌍 DNS": {"English": "🌍 DNS", "Polski": "🌍 DNS", "Русский": "🌍 DNS"},
    "↩ Reverse DNS": {"English": "↩ Reverse DNS", "Polski": "↩ Reverse DNS", "Русский": "↩ Reverse DNS"},
    "📄 Raport sieci": {"English": "📄 Network Report", "Polski": "📄 Raport sieci", "Русский": "📄 Отчет о сети"},

    # === SECURITY ===
    "🛡 Defender": {"English": "🛡 Defender", "Polski": "🛡 Defender", "Русский": "🛡 Defender"},
    "🔥 Firewall": {"English": "🔥 Firewall", "Polski": "🔥 Firewall", "Русский": "🔥 Firewall"},
    "🔍 Procesy": {"English": "🔍 Processes", "Polski": "🔍 Procesy", "Русский": "🔍 Процессы"},
    "🔌 Porty": {"English": "🔌 Ports", "Polski": "🔌 Porty", "Русский": "🔌 Порты"},
    "⭐ Administratorzy": {"English": "⭐ Administrators", "Polski": "⭐ Administratorzy", "Русский": "⭐ Администраторы"},
    "🔐 UAC": {"English": "🔐 UAC", "Polski": "🔐 UAC", "Русский": "🔐 UAC"},
    "# SHA256": {"English": "# SHA256", "Polski": "# SHA256", "Русский": "# SHA256"},
    "📄 Integralność": {"English": "📄 Integrity", "Polski": "📄 Integralność", "Русский": "📄 Целостность"},
    "📋 Audyt": {"English": "📋 Audit", "Polski": "📋 Audyt", "Русский": "📋 Аудит"},
    "🕵 Logowania": {"English": "🕵 Logins", "Polski": "🕵 Logowania", "Русский": "🕵 Логины"},
    "🔄 Update": {"English": "🔄 Update", "Polski": "🔄 Update", "Русский": "🔄 Update"},
    "👨 Konto": {"English": "👨 Account", "Polski": "👨 Konto", "Русский": "👨 Учетная запись"},
    "📑 Raport": {"English": "📑 Report", "Polski": "📑 Raport", "Русский": "📑 Отчет"},
    "🔑 Hash pliku": {"English": "🔑 File Hash", "Polski": "🔑 Hash pliku", "Русский": "🔑 Хэш файла"},
    "⚖ Porównaj hash": {"English": "⚖ Compare hash", "Polski": "⚖ Porównaj hash", "Русский": "⚖ Сравнить хэш"},
    "🧬 Integralność": {"English": "🧬 Integrity", "Polski": "🧬 Integralność", "Русский": "🧬 Целостность"},
    "👁 Monitor zmian": {"English": "👁 Change Monitor", "Polski": "👁 Monitor zmian", "Русский": "👁 Монитор изменений"},
    "🔐 Uprawnienia": {"English": "🔐 Permissions", "Polski": "🔐 Uprawnienia", "Русский": "🔐 Разрешения"},
    "👥 Grupy": {"English": "👥 Groups", "Polski": "👥 Grupy", "Русский": "👥 Группы"},
    "📜 Logi": {"English": "📜 Logs", "Polski": "📜 Logi", "Русский": "📜 Логи"},
    "🎲 Token": {"English": "🎲 Token", "Polski": "🎲 Token", "Русский": "🎲 Токен"},

    # === BACKUP ===
    "📁 Backup folderu": {"English": "📁 Backup Folder", "Polski": "📁 Backup folderu", "Русский": "📁 Папка резервных копий"},
    "♻ Przywróć": {"English": "♻ Restore", "Polski": "♻ Przywróć", "Русский": "♻ Восстановить"},
    "📦 ZIP Backup": {"English": "📦 ZIP Backup", "Polski": "📦 ZIP Backup", "Русский": "📦 ZIP Backup"},
    "👤 Profil użytkownika": {"English": "👤 User Profile", "Polski": "👤 Profil użytkownika", "Русский": "👤 Профиль пользователя"},
    "🖥 Pulpit": {"English": "🖥 Desktop", "Polski": "🖥 Pulpit", "Русский": "🖥 Рабочий стол"},
    "📄 Dokumenty": {"English": "📄 Documents", "Polski": "📄 Dokumenty", "Русский": "📄 Документы"},
    "⚙ Ustawienia": {"English": "⚙ Settings", "Polski": "⚙ Ustawienia", "Русский": "⚙ Настройки"},
    "📜 Rejestr": {"English": "📜 Registry", "Polski": "📜 Rejestr", "Русский": "📜 Реестр"},
    "📋 Lista kopii": {"English": "📋 Backup List", "Polski": "📋 Lista kopii", "Русский": "📋 Список резервных"},
    "🗑 Wyczyść": {"English": "🗑 Clean", "Polski": "🗑 Wyczyść", "Русский": "🗑 Очистить"},
    "🔄 Synchronizacja": {"English": "🔄 Sync", "Polski": "🔄 Synchronizacja", "Русский": "🔄 Синхронизация"},
    "🔍 Porównaj": {"English": "🔍 Compare", "Polski": "🔍 Porównaj", "Русский": "🔍 Сравнить"},
    "📁 Utwórz folder backup": {"English": "📁 Create backup folder", "Polski": "📁 Utwórz folder backup", "Русский": "📁 Создать папку резерва"},
    "📂 Kopia folderu": {"English": "📂 Copy folder", "Polski": "📂 Kopia folderu", "Русский": "📂 Копия папки"},
    "📤 Przywróć ZIP": {"English": "📤 Restore ZIP", "Polski": "📤 Przywróć ZIP", "Русский": "📤 Восстановить ZIP"},
    "🔄 Synchronizacja": {"English": "🔄 Synchronization", "Polski": "🔄 Synchronizacja", "Русский": "🔄 Синхронизация"},
    "🗑 Usuń stare kopie": {"English": "🗑 Delete old copies", "Polski": "🗑 Usuń stare kopie", "Русский": "🗑 Удалить старые копии"},
    "⚙ Export konfiguracji": {"English": "⚙ Export config", "Polski": "⚙ Export konfiguracji", "Русский": "⚙ Экспорт конфигурации"},
    "🧪 Test ZIP": {"English": "🧪 Test ZIP", "Polski": "🧪 Test ZIP", "Русский": "🧪 Тест ZIP"},

    # === VAULT / TOOLS ===
    "🔐 Otwórz sejf": {"English": "🔐 Open Vault", "Polski": "🔐 Otwórz sejf", "Русский": "🔐 Открыть сейф"},
    "➕ Nowy sejf": {"English": "➕ New Vault", "Polski": "➕ Nowy sejf", "Русский": "➕ Новый сейф"},
    "🔑 Generator haseł": {"English": "🔑 Password Generator", "Polski": "🔑 Generator haseł", "Русский": "🔑 Генератор паролей"},
    "📝 Prywatna notatka": {"English": "📝 Private note", "Polski": "📝 Prywatna notatka", "Русский": "📝 Личная заметка"},
    "🆔 UUID": {"English": "🆔 UUID", "Polski": "🆔 UUID", "Русский": "🆔 UUID"},
    "🔑 GUID": {"English": "🔑 GUID", "Polski": "🔑 GUID", "Русский": "🔑 GUID"},
    "# MD5": {"English": "# MD5", "Polski": "# MD5", "Русский": "# MD5"},
    "# SHA1": {"English": "# SHA1", "Polski": "# SHA1", "Русский": "# SHA1"},
    "🔒 Szyfruj plik": {"English": "🔒 Encrypt file", "Polski": "🔒 Szyfruj plik", "Русский": "🔒 Шифровать файл"},
    "🎯 Random": {"English": "🎯 Random", "Polski": "🎯 Random", "Русский": "🎯 Random"},
    "🔤 Base64 Encode": {"English": "🔤 Base64 Encode", "Polski": "🔤 Base64 Encode", "Русский": "🔤 Base64 Encode"},
    "🔡 Base64 Decode": {"English": "🔡 Base64 Decode", "Polski": "🔡 Base64 Decode", "Русский": "🔡 Base64 Decode"},
    "📊 Analizator tekstu": {"English": "📊 Text analyzer", "Polski": "📊 Analizator tekstu", "Русский": "📊 Анализатор текста"},
    "📋 Schowek": {"English": "📋 Clipboard", "Polski": "📋 Schowek", "Русский": "📋 Буфер обмена"},
    "🧹 Temp Cleaner": {"English": "🧹 Temp Cleaner", "Polski": "🧹 Temp Cleaner", "Русский": "🧹 Temp Cleaner"},
    "⚡ Cache Cleaner": {"English": "⚡ Cache Cleaner", "Polski": "⚡ Cache Cleaner", "Русский": "⚡ Cache Cleaner"},
    "📁 Info folderu": {"English": "📁 Folder info", "Polski": "📁 Info folderu", "Русский": "📁 Инфо папки"},

    # === DEVELOPER ===
    "📝 Edytor Python": {"English": "📝 Python Editor", "Polski": "📝 Edytor Python", "Русский": "📝 Редактор Python"},
    "▶ Uruchom Python": {"English": "▶ Run Python", "Polski": "▶ Uruchom Python", "Русский": "▶ Запустить Python"},
    "📦 pip install": {"English": "📦 pip install", "Polski": "📦 pip install", "Русский": "📦 pip install"},
    "📚 pip list": {"English": "📚 pip list", "Polski": "📚 pip list", "Русский": "📚 pip list"},
    "🏗 Generator projektu": {"English": "🏗 Project generator", "Polski": "🏗 Generator projektu", "Русский": "🏗 Генератор проекта"},
    "✔ JSON Check": {"English": "✔ JSON Check", "Polski": "✔ JSON Check", "Русский": "✔ JSON Check"},
    "✨ JSON Format": {"English": "✨ JSON Format", "Polski": "✨ JSON Format", "Русский": "✨ JSON Format"},
    "🔎 Regex": {"English": "🔎 Regex", "Polski": "🔎 Regex", "Русский": "🔎 Regex"},
    "🌐 ENV": {"English": "🌐 ENV", "Polski": "🌐 ENV", "Русский": "🌐 ENV"},
    "📄 .gitignore": {"English": "📄 .gitignore", "Polski": "📄 .gitignore", "Русский": "📄 .gitignore"},
    "📘 README": {"English": "📘 README", "Polski": "📘 README", "Русский": "📘 README"},
    "💻 Terminal": {"English": "💻 Terminal", "Polski": "💻 Terminal", "Русский": "💻 Терминал"},

    # === ADMIN ===
    "❌ Zabij proces": {"English": "❌ Kill process", "Polski": "❌ Zabij proces", "Русский": "❌ Убить процесс"},
    "▶ Start usługi": {"English": "▶ Start service", "Polski": "▶ Start usługi", "Русский": "▶ Запустить службу"},
    "⏹ Stop usługi": {"English": "⏹ Stop service", "Polski": "⏹ Stop usługi", "Русский": "⏹ Остановить службу"},
    "🖥 Urządzenia": {"English": "🖥 Devices", "Polski": "🖥 Urządzenia", "Русский": "🖥 Устройства"},
    "🌐 Zmienne": {"English": "🌐 Variables", "Polski": "🌐 Zmienne", "Русский": "🌐 Переменные"},
    "🔗 PATH": {"English": "🔗 PATH", "Polski": "🔗 PATH", "Русский": "🔗 PATH"},
    "🔑 Licencja": {"English": "🔑 License", "Polski": "🔑 Licencja", "Русский": "🔑 Лицензия"},
    "✅ Aktywacja": {"English": "✅ Activation", "Polski": "✅ Aktywacja", "Русский": "✅ Активация"},
    "📜 Polityki": {"English": "📜 Policies", "Polski": "📜 Polityki", "Русский": "📜 Политики"},
    "📊 System Info": {"English": "📊 System Info", "Polski": "📊 System Info", "Русский": "📊 Сведения системы"},

    # === GODMODE ===
    "📁 Utwórz folder GodMode": {"English": "📁 Create GodMode folder", "Polski": "📁 Utwórz folder GodMode", "Русский": "📁 Создать папку GodMode"},
    "🛠 Panele administracyjne": {"English": "🛠 Admin panels", "Polski": "🛠 Panele administracyjne", "Русский": "🛠 Административные панели"},
    "💻 CMD": {"English": "💻 CMD", "Polski": "💻 CMD", "Русский": "💻 CMD"},
    "🧠 PowerShell": {"English": "🧠 PowerShell", "Polski": "🧠 PowerShell", "Русский": "🧠 PowerShell"},
    "📊 Menedżer zadań": {"English": "📊 Task Manager", "Polski": "📊 Menedżer zadań", "Русский": "📊 Диспетчер задач"},
    "🖥 Menedżer urządzeń": {"English": "🖥 Device Manager", "Polski": "🖥 Menedżer urządzeń", "Русский": "🖥 Диспетчер устройств"},
    "🗂 Rejestr": {"English": "🗂 Registry", "Polski": "🗂 Rejestr", "Русский": "🗂 Реестр"},
    "🎛 Panel sterowania": {"English": "🎛 Control Panel", "Polski": "🎛 Panel sterowania", "Русский": "🎛 Панель управления"},
    "🎮 Informacje DirectX": {"English": "🎮 DirectX Info", "Polski": "🎮 Informacje DirectX", "Русский": "🎮 Информация DirectX"},
    "🧰 Zarządzanie komputerem": {"English": "🧰 Computer Management", "Polski": "🧰 Zarządzanie komputerem", "Русский": "🧰 Управление компьютером"},
    "🛠 SFC /Scannow": {"English": "🛠 SFC /Scannow", "Polski": "🛠 SFC /Scannow", "Русский": "🛠 SFC /Scannow"},
    "🧱 DISM Repair": {"English": "🧱 DISM Repair", "Polski": "🧱 DISM Repair", "Русский": "🧱 Восстановление DISM"},

    # === CORE / DODATKOWE ===
    "ℹ Informacje": {"English": "ℹ Info", "Polski": "ℹ Informacje", "Русский": "ℹ Инфо"},
    "💾 Zapisz ustawienia": {"English": "💾 Save settings", "Polski": "💾 Zapisz ustawienia", "Русский": "💾 Сохранить настройки"},
    "📂 Wczytaj ustawienia": {"English": "📂 Load settings", "Polski": "📂 Wczytaj ustawienia", "Русский": "📂 Загрузить настройки"},
    "ℹ O ToolKit": {"English": "ℹ About ToolKit", "Polski": "ℹ O ToolKit", "Русский": "ℹ О ToolKit"},
    "📦 Moduły": {"English": "📦 Modules", "Polski": "📦 Moduły", "Русский": "📦 Модули"},
    "🧩 Utwórz plugin": {"English": "🧩 Create plugin", "Polski": "🧩 Utwórz plugin", "Русский": "🧩 Создать плагин"},
    "📋 Lista pluginów": {"English": "📋 Plugin list", "Polski": "📋 Lista pluginów", "Русский": "📋 Список плагинов"},
    "🌑 Tryb ciemny": {"English": "🌑 Dark mode", "Polski": "🌑 Tryb ciemny", "Русский": "🌑 Темный режим"},
    "☀ Tryb normalny": {"English": "☀ Normal mode", "Polski": "☀ Tryb normalny", "Русский": "☀ Обычный режим"},
    "🔄 Restart": {"English": "🔄 Restart", "Polski": "🔄 Restart", "Русский": "🔄 Перезапуск"},
    "❌ Wyjście": {"English": "❌ Exit", "Polski": "❌ Wyjście", "Русский": "❌ Выход"},
    "⚙ Skrypt Admin": {"English": "⚙ Admin Script", "Polski": "⚙ Skrypt Admin", "Русский": "⚙ Административный скрипт"},

    # === AUTOMATION ===
    "▶ Uruchom program": {"English": "▶ Run program", "Polski": "▶ Uruchom program", "Русский": "▶ Запустить программу"},
    "📁 Otwórz folder": {"English": "📁 Open folder", "Polski": "📁 Otwórz folder", "Русский": "📁 Открыть папку"},
    "⌨ Wykonaj CMD": {"English": "⌨ Execute CMD", "Polski": "⌨ Wykonaj CMD", "Русский": "⌨ Выполнить CMD"},
    "🐍 Uruchom skrypt Python": {"English": "🐍 Run Python script", "Polski": "🐍 Uruchom skrypt Python", "Русский": "🐍 Запустить скрипт Python"},
    "⏱ Timer": {"English": "⏱ Timer", "Polski": "⏱ Timer", "Русский": "⏱ Таймер"},
    "💾 Zapisz zadanie": {"English": "💾 Save task", "Polski": "💾 Zapisz zadanie", "Русский": "💾 Сохранить задание"},
    "📋 Lista zadań": {"English": "📋 Task list", "Polski": "📋 Lista zadań", "Русский": "📋 Список задач"},
    "🧹 Czyść TEMP": {"English": "🧹 Clean TEMP", "Polski": "🧹 Czyść TEMP", "Русский": "🧹 Очистить TEMP"},
    "🐍 Informacje Python": {"English": "🐍 Python Info", "Polski": "🐍 Informacje Python", "Русский": "🐍 Информация Python"},

    # === MONITORING ===
    "📄 Raport systemu": {"English": "📄 System Report", "Polski": "📄 Raport systemu", "Русский": "📄 Отчет системы"},
    "📈 Monitor Live": {"English": "📈 Live Monitor", "Polski": "📈 Monitor Live", "Русский": "📈 Живой монитор"},

    # === ADVANCED ===
    "🛠 SFC Scan": {"English": "🛠 SFC Scan", "Polski": "🛠 SFC Scan", "Русский": "🛠 SFC Scan"},
    "🔧 DISM Repair": {"English": "🔧 DISM Repair", "Polski": "🔧 DISM Repair", "Русский": "🔧 Восстановление DISM"},
    "💿 Sterowniki": {"English": "💿 Drivers", "Polski": "💿 Sterowniki", "Русский": "💿 Драйверы"},
    "📤 Export Drivers": {"English": "📤 Export Drivers", "Polski": "📤 Export Drivers", "Русский": "📤 Экспорт драйверов"},
    "🌱 Zmienne": {"English": "🌱 Variables", "Polski": "🌱 Zmienne", "Русский": "🌱 Переменные"},
    "📦 Programy": {"English": "📦 Programs", "Polski": "📦 Programy", "Русский": "📦 Программы"},
    "🧰 Admin Tools": {"English": "🧰 Admin Tools", "Polski": "🧰 Admin Tools", "Русский": "🧰 Административные инструменты"},
    "🧹 TEMP Clean": {"English": "🧹 TEMP Clean", "Polski": "🧹 TEMP Clean", "Русский": "🧹 Очистка TEMP"},
    "🌐 IP Config": {"English": "🌐 IP Config", "Polski": "🌐 IP Config", "Русский": "🌐 IP Config"},
    "📋 Tasklist": {"English": "📋 Tasklist", "Polski": "📋 Tasklist", "Русский": "📋 Список задач"},
}

# add tabs and buttons translations
extra = {
    # tabs
    "🏠 Start": {"English": "🏠 Start", "Polski": "🏠 Start", "Русский": "🏠 Главная"},
    "📁 Pliki": {"English": "📁 Files", "Polski": "📁 Pliki", "Русский": "📁 Файлы"},
    "💻 System": {"English": "💻 System", "Polski": "💻 System", "Русский": "💻 Система"},
    "🔧 Hardware": {"English": "🔧 Hardware", "Polski": "🔧 Hardware", "Русский": "🔧 Аппаратное обеспечение"},
    "🌐 Sieć": {"English": "🌐 Network", "Polski": "🌐 Sieć", "Русский": "🌐 Сеть"},
    "🛡 Bezpieczeństwo": {"English": "🛡 Security", "Polski": "🛡 Bezpieczeństwo", "Русский": "🛡 Безопасность"},
    "💾 Backup": {"English": "💾 Backup", "Polski": "💾 Backup", "Русский": "💾 Резерв"},
    "🛠 Narzędzia": {"English": "🛠 Tools", "Polski": "🛠 Narzędzia", "Русский": "🛠 Инструменты"},
    "👨‍💻 Developer": {"English": "👨‍💻 Developer", "Polski": "👨‍💻 Developer", "Русский": "👨‍💻 Разработчик"},
    "⚙ Admin": {"English": "⚙ Admin", "Polski": "⚙ Admin", "Русский": "⚙ Админ"},
    "👑 GodMode": {"English": "👑 GodMode", "Polski": "👑 GodMode", "Русский": "👑 GodMode"},
    # file buttons
    "📁 Eksplorator": {"English": "📁 Explorer", "Polski": "📁 Eksplorator", "Русский": "📁 Проводник"},
    "📋 Kopiuj": {"English": "📋 Copy", "Polski": "📋 Kopiuj", "Русский": "📋 Копировать"},
    "🚚 Przenieś": {"English": "🚚 Move", "Polski": "🚚 Przenieś", "Русский": "🚚 Переместить"},
    "🗑 Usuń": {"English": "🗑 Delete", "Polski": "🗑 Usuń", "Русский": "🗑 Удалить"},
    "📊 Informacje": {"English": "📊 Info", "Polski": "📊 Informacje", "Русский": "📊 Инфо"},
    "📦 ZIP": {"English": "📦 ZIP", "Polski": "📦 ZIP", "Русский": "📦 ZIP"},
    "📤 Rozpakuj": {"English": "📤 Unpack", "Polski": "📤 Rozpakuj", "Русский": "📤 Распаковать"},
    "🔎 Szukaj": {"English": "🔎 Search", "Polski": "🔎 Szukaj", "Русский": "🔎 Поиск"},
    "📈 Rozszerzenia": {"English": "📈 Extensions", "Polski": "📈 Rozszerzenia", "Русский": "📈 Расширения"},
    "💾 Największe": {"English": "💾 Biggest", "Polski": "💾 Największe", "Русский": "💾 Самые большие"},
    "♻ Duplikaty": {"English": "♻ Duplicates", "Polski": "♻ Duplikaty", "Русский": "♻ Дубликаты"},
    "✏ Zmień nazwy": {"English": "✏ Rename", "Polski": "✏ Zmień nazwy", "Русский": "✏ Переименовать"},
    # system buttons
    "💻 Windows Info": {"English": "💻 Windows Info", "Polski": "💻 Windows Info", "Русский": "💻 Сведения Windows"},
    "🐍 Python Info": {"English": "🐍 Python Info", "Polski": "🐍 Python Info", "Русский": "🐍 Python Info"},
    "⚡ CPU": {"English": "⚡ CPU", "Polski": "⚡ CPU", "Русский": "⚡ CPU"},
    "🧠 RAM": {"English": "🧠 RAM", "Polski": "🧠 RAM", "Русский": "🧠 RAM"},
    "💾 Dyski": {"English": "💾 Disks", "Polski": "💾 Dyski", "Русский": "💾 Диски"},
    "📋 Procesy": {"English": "📋 Processes", "Polski": "📋 Procesy", "Русский": "📋 Процессы"},
    "⚙ Usługi": {"English": "⚙ Services", "Polski": "⚙ Usługi", "Русский": "⚙ Службы"},
    "🚀 Autostart": {"English": "🚀 Startup", "Polski": "🚀 Autostart", "Русский": "🚀 Автозапуск"},
    "🌐 Environment": {"English": "🌐 Environment", "Polski": "🌐 Environment", "Русский": "🌐 Окружение"},
    "👤 Użytkownicy": {"English": "👤 Users", "Polski": "👤 Użytkownicy", "Русский": "👤 Пользователи"},
    "🔧 Sterowniki": {"English": "🔧 Drivers", "Polski": "🔧 Sterowniki", "Русский": "🔧 Драйверы"},
    "📜 Logi": {"English": "📜 Logs", "Polski": "📜 Logi", "Русский": "📜 Логи"},
    "📈 Monitor": {"English": "📈 Monitor", "Polski": "📈 Monitor", "Русский": "📈 Монитор"},
    # hardware buttons
    "🎮 GPU": {"English": "🎮 GPU", "Polski": "🎮 GPU", "Русский": "🎮 GPU"},
    "🧬 BIOS": {"English": "🧬 BIOS", "Polski": "🧬 BIOS", "Русский": "🧬 BIOS"},
    "🖥 Płyta główna": {"English": "🖥 Motherboard", "Polski": "🖥 Płyta główna", "Русский": "🖥 Материнская плата"},
    "⚡ CPU Info": {"English": "⚡ CPU Info", "Polski": "⚡ CPU Info", "Русский": "⚡ CPU Info"},
    "🧠 RAM Moduły": {"English": "🧠 RAM Modules", "Polski": "🧠 RAM Moduły", "Русский": "🧠 Модули RAM"},
    "💽 Dyski fizyczne": {"English": "💽 Physical Disks", "Polski": "💽 Dyski fizyczne", "Русский": "💽 Физические диски"},
    "💚 SMART": {"English": "💚 SMART", "Polski": "💚 SMART", "Русский": "💚 SMART"},
    "🔌 USB": {"English": "🔌 USB", "Polski": "🔌 USB", "Русский": "🔌 USB"},
    "🖥 Monitory": {"English": "🖥 Monitors", "Polski": "🖥 Monitory", "Русский": "🖥 Мониторы"},
    "🔊 Audio": {"English": "🔊 Audio", "Polski": "🔊 Audio", "Русский": "🔊 Аудио"},
    "📷 Kamera": {"English": "📷 Camera", "Polski": "📷 Kamera", "Русский": "📷 Камера"},
    "🔋 Bateria": {"English": "🔋 Battery", "Polski": "🔋 Bateria", "Русский": "🔋 Батарея"},
    "🔧 PCI": {"English": "🔧 PCI", "Polski": "🔧 PCI", "Русский": "🔧 PCI"},
    "🌡 Temperatury": {"English": "🌡 Temperatures", "Polski": "🌡 Temperatury", "Русский": "🌡 Температуры"},
    "⚙ Kontrolery": {"English": "⚙ Controllers", "Polski": "⚙ Kontrolery", "Русский": "⚙ Контроллеры"},
    # network buttons
    "🌐 Karty sieciowe": {"English": "🌐 Network Adapters", "Polski": "🌐 Karty sieciowe", "Русский": "🌐 Сетевые адаптеры"},
    "📍 Lokalny IP": {"English": "📍 Local IP", "Polski": "📍 Lokalny IP", "Русский": "📍 Локальный IP"},
    "🌍 Publiczne IP": {"English": "🌍 Public IP", "Polski": "🌍 Publiczne IP", "Русский": "🌍 Внешний IP"},
    "🔎 DNS Lookup": {"English": "🔎 DNS Lookup", "Polski": "🔎 DNS Lookup", "Русский": "🔎 DNS Lookup"},
    "📡 Ping": {"English": "📡 Ping", "Polski": "📡 Ping", "Русский": "📡 Ping"},
    "🛰 Traceroute": {"English": "🛰 Traceroute", "Polski": "🛰 Traceroute", "Русский": "🛰 Traceroute"},
    "🔌 Test portu": {"English": "🔌 Port Test", "Polski": "🔌 Test portu", "Русский": "🔌 Тест порта"},
    "📶 Skan LAN": {"English": "📶 LAN Scan", "Polski": "📶 Skan LAN", "Русский": "📶 LAN Scan"},
    "📋 ARP": {"English": "📋 ARP", "Polski": "📋 ARP", "Русский": "📋 ARP"},
    "📡 WiFi": {"English": "📡 WiFi", "Polski": "📡 WiFi", "Русский": "📡 WiFi"},
    "🔗 Połączenia": {"English": "🔗 Connections", "Polski": "🔗 Połączenia", "Русский": "🔗 Соединения"},
    "📊 Netstat": {"English": "📊 Netstat", "Polski": "📊 Netstat", "Русский": "📊 Netstat"},
    "♻ Flush DNS": {"English": "♻ Flush DNS", "Polski": "♻ Flush DNS", "Русский": "♻ Flush DNS"},
    "🌍 Test Internetu": {"English": "🌍 Internet Test", "Polski": "🌍 Test Internetu", "Русский": "🌍 Тест интернета"},
    # security buttons
    "🛡 Defender": {"English": "🛡 Defender", "Polski": "🛡 Defender", "Русский": "🛡 Defender"},
    "🔥 Firewall": {"English": "🔥 Firewall", "Polski": "🔥 Firewall", "Русский": "🔥 Firewall"},
    "🔍 Procesy": {"English": "🔍 Processes", "Polski": "🔍 Procesy", "Русский": "🔍 Процессы"},
    "🔌 Porty": {"English": "🔌 Ports", "Polski": "🔌 Porty", "Русский": "🔌 Порты"},
    "👤 Użytkownicy": {"English": "👤 Users", "Polski": "👤 Użytkownicy", "Русский": "👤 Пользователи"},
    "⭐ Administratorzy": {"English": "⭐ Administrators", "Polski": "⭐ Administratorzy", "Русский": "⭐ Администраторы"},
    "🔐 UAC": {"English": "🔐 UAC", "Polski": "🔐 UAC", "Русский": "🔐 UAC"},
    "# SHA256": {"English": "# SHA256", "Polski": "# SHA256", "Русский": "# SHA256"},
    "📄 Integralność": {"English": "📄 Integrity", "Polski": "📄 Integralność", "Русский": "📄 Целостность"},
    "📋 Audyt": {"English": "📋 Audit", "Polski": "📋 Audyt", "Русский": "📋 Аудит"},
    "🕵 Logowania": {"English": "🕵 Logins", "Polski": "🕵 Logowania", "Русский": "🕵 Логины"},
    "🔄 Update": {"English": "🔄 Update", "Polski": "🔄 Update", "Русский": "🔄 Update"},
    "👨 Konto": {"English": "👨 Account", "Polski": "👨 Konto", "Русский": "👨 Учетная запись"},
    "📑 Raport": {"English": "📑 Report", "Polski": "📑 Raport", "Русский": "📑 Отчет"},
    # backup buttons
    "📁 Backup folderu": {"English": "📁 Backup Folder", "Polski": "📁 Backup folderu", "Русский": "📁 Папка резервных копий"},
    "♻ Przywróć": {"English": "♻ Restore", "Polski": "♻ Przywróć", "Русский": "♻ Восстановить"},
    "📦 ZIP Backup": {"English": "📦 ZIP Backup", "Polski": "📦 ZIP Backup", "Русский": "📦 ZIP Backup"},
    "👤 Profil użytkownika": {"English": "👤 User Profile", "Polski": "👤 Profil użytkownika", "Русский": "👤 Профиль пользователя"},
    "🖥 Pulpit": {"English": "🖥 Desktop", "Polski": "🖥 Pulpit", "Русский": "🖥 Рабочий стол"},
    "📄 Dokumenty": {"English": "📄 Documents", "Polski": "📄 Dokumenty", "Русский": "📄 Документы"},
    "⚙ Ustawienia": {"English": "⚙ Settings", "Polski": "⚙ Ustawienia", "Русский": "⚙ Настройки"},
    "📜 Rejestr": {"English": "📜 Registry", "Polski": "📜 Rejestr", "Русский": "📜 Реестр"},
    "📋 Lista kopii": {"English": "📋 Backup List", "Polski": "📋 Lista kopii", "Русский": "📋 Список резервных"},
    "🗑 Wyczyść": {"English": "🗑 Clean", "Polski": "🗑 Wyczyść", "Русский": "🗑 Очистить"},
    "🔄 Synchronizacja": {"English": "🔄 Sync", "Polski": "🔄 Synchronizacja", "Русский": "🔄 Синхронизация"},
    "🔍 Porównaj": {"English": "🔍 Compare", "Polski": "🔍 Porównaj", "Русский": "🔍 Сравнить"},
    # vault buttons
    "🔐 Otwórz sejf": {"English": "🔐 Open Vault", "Polski": "🔐 Otwórz sejf", "Русский": "🔐 Открыть сейф"},
    "➕ Nowy sejf": {"English": "➕ New Vault", "Polski": "➕ Nowy sejf", "Русский": "➕ Новый сейф"},
    "🔑 Generator haseł": {"English": "🔑 Password Generator", "Polski": "🔑 Generator haseł", "Русский": "🔑 Генератор паролей"},
    "📝 Prywatna notatka": {"English": "📝 Private note", "Polski": "📝 Prywatna notatka", "Русский": "📝 Личная заметка"},
    # tools
    "🆔 UUID": {"English": "🆔 UUID", "Polski": "🆔 UUID", "Русский": "🆔 UUID"},
    "🔑 GUID": {"English": "🔑 GUID", "Polski": "🔑 GUID", "Русский": "🔑 GUID"},
    "# MD5": {"English": "# MD5", "Polski": "# MD5", "Русский": "# MD5"},
    "# SHA1": {"English": "# SHA1", "Polski": "# SHA1", "Русский": "# SHA1"},
    "# SHA256": {"English": "# SHA256", "Polski": "# SHA256", "Русский": "# SHA256"},
    "⚖ Porównaj hash": {"English": "⚖ Compare hash", "Polski": "⚖ Porównaj hash", "Русский": "⚖ Сравнить хэш"},
    "🔒 Szyfruj plik": {"English": "🔒 Encrypt file", "Polski": "🔒 Szyfruj plik", "Русский": "🔒 Шифровать файл"},
    "🎲 Token": {"English": "🎲 Token", "Polski": "🎲 Token", "Русский": "🎲 Токен"},
    "🎯 Random": {"English": "🎯 Random", "Polski": "🎯 Random", "Русский": "🎯 Random"},
    "🔤 Base64 Encode": {"English": "🔤 Base64 Encode", "Polski": "🔤 Base64 Encode", "Русский": "🔤 Base64 Encode"},
    "🔡 Base64 Decode": {"English": "🔡 Base64 Decode", "Polski": "🔡 Base64 Decode", "Русский": "🔡 Base64 Decode"},
    "📊 Analizator tekstu": {"English": "📊 Text analyzer", "Polski": "📊 Analizator tekstu", "Русский": "📊 Анализатор текста"},
    "🧹 Temp Cleaner": {"English": "🧹 Temp Cleaner", "Polski": "🧹 Temp Cleaner", "Русский": "🧹 Temp Cleaner"},
    "⚡ Cache Cleaner": {"English": "⚡ Cache Cleaner", "Polski": "⚡ Cache Cleaner", "Русский": "⚡ Cache Cleaner"},
    "📁 Info folderu": {"English": "📁 Folder info", "Polski": "📁 Info folderu", "Русский": "📁 Инфо папки"},
    # developer
    "📝 Edytor Python": {"English": "📝 Python Editor", "Polski": "📝 Edytor Python", "Русский": "📝 Редактор Python"},
    "▶ Uruchom Python": {"English": "▶ Run Python", "Polski": "▶ Uruchom Python", "Русский": "▶ Запустить Python"},
    "📦 pip install": {"English": "📦 pip install", "Polski": "📦 pip install", "Русский": "📦 pip install"},
    "📚 pip list": {"English": "📚 pip list", "Polski": "📚 pip list", "Русский": "📚 pip list"},
    "🏗 Generator projektu": {"English": "🏗 Project generator", "Polski": "🏗 Generator projektu", "Русский": "🏗 Генератор проекта"},
    "✔ JSON Check": {"English": "✔ JSON Check", "Polski": "✔ JSON Check", "Русский": "✔ JSON Check"},
    "✨ JSON Format": {"English": "✨ JSON Format", "Polski": "✨ JSON Format", "Русский": "✨ JSON Format"},
    "🔎 Regex": {"English": "🔎 Regex", "Polski": "🔎 Regex", "Русский": "🔎 Regex"},
    "🌐 ENV": {"English": "🌐 ENV", "Polski": "🌐 ENV", "Русский": "🌐 ENV"},
    "📄 .gitignore": {"English": "📄 .gitignore", "Polski": "📄 .gitignore", "Русский": "📄 .gitignore"},
    "📘 README": {"English": "📘 README", "Polski": "📘 README", "Русский": "📘 README"},
}

PHRASES.update(extra)

# Runtime messages used by the Tools, Security and Backup actions.
PHRASES.update({
    "Użytkownicy": {"English": "Users", "Polski": "Użytkownicy", "Русский": "Пользователи"},
    "Administratorzy": {"English": "Administrators", "Polski": "Administratorzy", "Русский": "Администраторы"},
    "Kontrola": {"English": "Check", "Polski": "Kontrola", "Русский": "Проверка"},
    "Aktualizacje": {"English": "Updates", "Polski": "Aktualizacje", "Русский": "Обновления"},
    "Konto": {"English": "Account", "Polski": "Konto", "Русский": "Учетная запись"},
    "Backup": {"English": "Backup", "Polski": "Backup", "Русский": "Резервная копия"},
    "Restore": {"English": "Restore", "Polski": "Przywracanie", "Русский": "Восстановление"},
    "ZIP": {"English": "ZIP", "Polski": "ZIP", "Русский": "ZIP"},
    "Backup ZIP gotowy": {"English": "ZIP backup ready", "Polski": "Backup ZIP gotowy", "Русский": "ZIP-резервная копия готова"},
    "Profil": {"English": "Profile", "Polski": "Profil", "Русский": "Профиль"},
    "Skopiowano profil": {"English": "Profile copied", "Polski": "Skopiowano profil", "Русский": "Профиль скопирован"},
    "Pulpit": {"English": "Desktop", "Polski": "Pulpit", "Русский": "Рабочий стол"},
    "Backup pulpitu gotowy": {"English": "Desktop backup ready", "Polski": "Backup pulpitu gotowy", "Русский": "Резервная копия рабочего стола готова"},
    "Dokumenty": {"English": "Documents", "Polski": "Dokumenty", "Русский": "Документы"},
    "Backup wykonany": {"English": "Backup completed", "Polski": "Backup wykonany", "Русский": "Резервное копирование завершено"},
    "Settings": {"English": "Settings", "Polski": "Ustawienia", "Русский": "Настройки"},
    "Ustawienia zapisane": {"English": "Settings saved", "Polski": "Ustawienia zapisane", "Русский": "Настройки сохранены"},
    "Rejestr": {"English": "Registry", "Polski": "Rejestr", "Русский": "Реестр"},
    "Backup rejestru gotowy": {"English": "Registry backup ready", "Polski": "Backup rejestru gotowy", "Русский": "Резервная копия реестра готова"},
    "Backup Lista": {"English": "Backup list", "Polski": "Backup Lista", "Русский": "Список резервных копий"},
    "📋 Lista backupów": {"English": "📋 Backup list", "Polski": "📋 Lista backupów", "Русский": "📋 Список резервных копий"},
    "📦 Backup ZIP": {"English": "📦 ZIP backup", "Polski": "📦 Backup ZIP", "Русский": "📦 ZIP-резервная копия"},
    "UUID": {"English": "UUID", "Polski": "UUID", "Русский": "UUID"},
    "GUID": {"English": "GUID", "Polski": "GUID", "Русский": "GUID"},
    "Base64": {"English": "Base64", "Polski": "Base64", "Русский": "Base64"},
    "Plik:": {"English": "File:", "Polski": "Plik:", "Русский": "Файл:"},
    "Rozmiar:": {"English": "Size:", "Polski": "Rozmiar:", "Русский": "Размер:"},
    "Utworzono:": {"English": "Created:", "Polski": "Utworzono:", "Русский": "Создано:"},
    "Zmodyfikowano:": {"English": "Modified:", "Polski": "Zmodyfikowano:", "Русский": "Изменено:"},
    "bajtów": {"English": "bytes", "Polski": "bajtów", "Русский": "байт"},
    "SYSTEM:": {"English": "SYSTEM:", "Polski": "SYSTEM:", "Русский": "СИСТЕМА:"},
    "WERSJA:": {"English": "VERSION:", "Polski": "WERSJA:", "Русский": "ВЕРСИЯ:"},
    "RELEASE:": {"English": "RELEASE:", "Polski": "RELEASE:", "Русский": "ВЫПУСК:"},
    "ARCHITEKTURA:": {"English": "ARCHITECTURE:", "Polski": "ARCHITEKTURA:", "Русский": "АРХИТЕКТУРА:"},
    "PROCESOR:": {"English": "PROCESSOR:", "Polski": "PROCESOR:", "Русский": "ПРОЦЕССОР:"},
    "Użycie:": {"English": "Usage:", "Polski": "Użycie:", "Русский": "Использование:"},
    "Rdzenie:": {"English": "Cores:", "Polski": "Rdzenie:", "Русский": "Ядра:"},
    "Całość:": {"English": "Total:", "Polski": "Całość:", "Русский": "Всего:"},
    "Dostępne:": {"English": "Available:", "Polski": "Dostępne:", "Русский": "Доступно:"},
    "Wolne:": {"English": "Free:", "Polski": "Wolne:", "Русский": "Свободно:"},
    "Dysk:": {"English": "Disk:", "Polski": "Dysk:", "Русский": "Диск:"},
    "System:": {"English": "System:", "Polski": "System:", "Русский": "Система:"},
    "PID:": {"English": "PID:", "Polski": "PID:", "Русский": "PID:"},
    "Nazwa:": {"English": "Name:", "Polski": "Nazwa:", "Русский": "Имя:"},
    "RAM:": {"English": "RAM:", "Polski": "RAM:", "Русский": "ОЗУ:"},
    "Czas:": {"English": "Time:", "Polski": "Czas:", "Русский": "Время:"},
    "Elementy:": {"English": "Items:", "Polski": "Elementy:", "Русский": "Элементы:"},
    "Tylko A:": {"English": "A only:", "Polski": "Tylko A:", "Русский": "Только A:"},
    "Tylko B:": {"English": "B only:", "Polski": "Tylko B:", "Русский": "Только B:"},
    "Lokalizacja:": {"English": "Location:", "Polski": "Lokalizacja:", "Русский": "Расположение:"},
    "Zawartość:": {"English": "Contents:", "Polski": "Zawartość:", "Русский": "Содержимое:"},
    "Dodane:": {"English": "Added:", "Polski": "Dodane:", "Русский": "Добавлено:"},
    "Usunięte:": {"English": "Removed:", "Polski": "Usunięte:", "Русский": "Удалено:"},
    "Znaki:": {"English": "Characters:", "Polski": "Znaki:", "Русский": "Символы:"},
    "Słowa:": {"English": "Words:", "Polski": "Słowa:", "Русский": "Слова:"},
    "Linie:": {"English": "Lines:", "Polski": "Linie:", "Русский": "Строки:"},
    "HOST:": {"English": "HOST:", "Polski": "HOST:", "Русский": "ХОСТ:"},
    "IPCONFIG:": {"English": "IPCONFIG:", "Polski": "IPCONFIG:", "Русский": "IPCONFIG:"},
    "NETSTAT:": {"English": "NETSTAT:", "Polski": "NETSTAT:", "Русский": "NETSTAT:"},
    "Wyniki": {"English": "Results", "Polski": "Wyniki", "Русский": "Результаты"},
    "Statystyka": {"English": "Statistics", "Polski": "Statystyka", "Русский": "Статистика"},
    "Największe": {"English": "Largest", "Polski": "Największe", "Русский": "Самые большие"},
    "Duplikaty": {"English": "Duplicates", "Polski": "Duplikaty", "Русский": "Дубликаты"},
    "Gotowe": {"English": "Done", "Polski": "Gotowe", "Русский": "Готово"},
    "Windows Info": {"English": "Windows Info", "Polski": "Windows Info", "Русский": "Сведения Windows"},
    "Logi Windows": {"English": "Windows Logs", "Polski": "Logi Windows", "Русский": "Журналы Windows"},
    "CPU Monitor": {"English": "CPU Monitor", "Polski": "Monitor CPU", "Русский": "Монитор ЦП"},
    "Procesy Windows": {"English": "Windows Processes", "Polski": "Procesy Windows", "Русский": "Процессы Windows"},
    "Procesy": {"English": "Processes", "Polski": "Procesy", "Русский": "Процессы"},
    "Monitor Live": {"English": "Live Monitor", "Polski": "Monitor Live", "Русский": "Монитор в реальном времени"},
    "Brak dostępu": {"English": "Access denied", "Polski": "Brak dostępu", "Русский": "Нет доступа"},
    "OTWARTY": {"English": "OPEN", "Polski": "OTWARTY", "Русский": "ОТКРЫТ"},
    "ZAMKNIĘTY": {"English": "CLOSED", "Polski": "ZAMKNIĘTY", "Русский": "ЗАКРЫТ"},
    "Połączenie działa": {"English": "Connection is working", "Polski": "Połączenie działa", "Русский": "Соединение работает"},
    "Brak internetu": {"English": "No internet connection", "Polski": "Brak internetu", "Русский": "Нет подключения к Интернету"},
    "Niepoprawny MAC": {"English": "Invalid MAC", "Polski": "Niepoprawny MAC", "Русский": "Неверный MAC"},
    "Pakiet wysłany": {"English": "Packet sent", "Polski": "Pakiet wysłany", "Русский": "Пакет отправлен"},
    "Analiza dysku": {"English": "Disk analysis", "Polski": "Analiza dysku", "Русский": "Анализ диска"},
    "Minimum MB": {"English": "Minimum MB", "Polski": "Minimum MB", "Русский": "Минимум МБ"},
    "Duże pliki": {"English": "Large files", "Polski": "Duże pliki", "Русский": "Большие файлы"},
    "Zakończono": {"English": "Completed", "Polski": "Zakończono", "Русский": "Завершено"},
    "Konta użytkowników": {"English": "User accounts", "Polski": "Konta użytkowników", "Русский": "Учетные записи пользователей"},
    "Procesy CMD": {"English": "CMD processes", "Polski": "Procesy CMD", "Русский": "Процессы CMD"},
    "Plugin utworzony.": {"English": "Plugin created.", "Polski": "Plugin utworzony.", "Русский": "Плагин создан."},
    "Czyszczenie": {"English": "Cleanup", "Polski": "Czyszczenie", "Русский": "Очистка"},
    "Sync": {"English": "Sync", "Polski": "Synchronizacja", "Русский": "Синхронизация"},
    "Synchronizacja zakończona": {"English": "Synchronization completed", "Polski": "Synchronizacja zakończona", "Русский": "Синхронизация завершена"},
    "Porównanie": {"English": "Comparison", "Polski": "Porównanie", "Русский": "Сравнение"},
    "Tylko A": {"English": "A only", "Polski": "Tylko A", "Русский": "Только A"},
    "Tylko B": {"English": "B only", "Polski": "Tylko B", "Русский": "Только B"},
    "Lokalizacja": {"English": "Location", "Polski": "Lokalizacja", "Русский": "Расположение"},
    "Zawartość": {"English": "Contents", "Polski": "Zawartość", "Русский": "Содержимое"},
    "Hash": {"English": "Hash", "Polski": "Hash", "Русский": "Хэш"},
    "Wynik": {"English": "Result", "Polski": "Wynik", "Русский": "Результат"},
    "Hashy są identyczne": {"English": "Hashes are identical", "Polski": "Hashy są identyczne", "Русский": "Хэши совпадают"},
    "Hashy różne": {"English": "Hashes are different", "Polski": "Hashy różne", "Русский": "Хэши отличаются"},
    "Szyfrowanie": {"English": "Encryption", "Polski": "Szyfrowanie", "Русский": "Шифрование"},
    "Ilość znaków": {"English": "Character count", "Polski": "Ilość znaków", "Русский": "Количество символов"},
    "Dane": {"English": "Data", "Polski": "Dane", "Русский": "Данные"},
    "Analizator": {"English": "Analyzer", "Polski": "Analizator", "Русский": "Анализатор"},
    "Analiza": {"English": "Analysis", "Polski": "Analiza", "Русский": "Анализ"},
    "Schowek pusty": {"English": "Clipboard is empty", "Polski": "Schowek pusty", "Русский": "Буфер обмена пуст"},
    "Cleaner": {"English": "Cleaner", "Polski": "Cleaner", "Русский": "Очистка"},
    "Cache": {"English": "Cache", "Polski": "Cache", "Русский": "Кэш"},
    "Wyczyszczono": {"English": "Cleaned", "Polski": "Wyczyszczono", "Русский": "Очищено"},
    "Folder": {"English": "Folder", "Polski": "Folder", "Русский": "Папка"},
    "Rozmiar": {"English": "Size", "Polski": "Rozmiar", "Русский": "Размер"},
    "Folder backup został utworzony.": {"English": "Backup folder created.", "Polski": "Folder backup został utworzony.", "Русский": "Папка резервных копий создана."},
    "Kopia folderu wykonana.": {"English": "Folder backup completed.", "Polski": "Kopia folderu wykonana.", "Русский": "Резервная копия папки создана."},
    "Backup ZIP utworzony.": {"English": "ZIP backup created.", "Polski": "Backup ZIP utworzony.", "Русский": "ZIP-резервная копия создана."},
    "Pliki przywrócone.": {"English": "Files restored.", "Polski": "Pliki przywrócone.", "Русский": "Файлы восстановлены."},
    "Brak folderu backup.": {"English": "Backup folder does not exist.", "Polski": "Brak folderu backup.", "Русский": "Папка резервных копий отсутствует."},
    "Brak kopii.": {"English": "No backups found.", "Polski": "Brak kopii.", "Русский": "Резервные копии не найдены."},
    "Konfiguracja zapisana.": {"English": "Configuration saved.", "Polski": "Konfiguracja zapisana.", "Русский": "Конфигурация сохранена."},
    "Archiwum OK": {"English": "Archive OK", "Polski": "Archiwum OK", "Русский": "Архив в порядке"},
    "Synchronizacja": {"English": "Synchronization", "Polski": "Synchronizacja", "Русский": "Синхронизация"},
    "Skopiowano": {"English": "Copied", "Polski": "Skopiowano", "Русский": "Скопировано"},
    "plików": {"English": "files", "Polski": "plików", "Русский": "файлов"},
    "Usunięto": {"English": "Deleted", "Polski": "Usunięto", "Русский": "Удалено"},
    "Takie same": {"English": "Identical", "Polski": "Takie same", "Русский": "Одинаковые"},
    "Różne": {"English": "Different", "Polski": "Różne", "Русский": "Разные"},
    "Utworzono bazę": {"English": "Database created", "Polski": "Utworzono bazę", "Русский": "База данных создана"},
    "Dodane": {"English": "Added", "Polski": "Dodane", "Русский": "Добавлено"},
    "Usunięte": {"English": "Removed", "Polski": "Usunięte", "Русский": "Удалено"},
    "Raport bezpieczeństwa": {"English": "Security report", "Polski": "Raport bezpieczeństwa", "Русский": "Отчет безопасности"},
    "Lista backupów": {"English": "Backup list", "Polski": "Lista backupów", "Русский": "Список резервных копий"},
    "Export": {"English": "Export", "Polski": "Eksport", "Русский": "Экспорт"},
    "ZIP Test": {"English": "ZIP test", "Polski": "Test ZIP", "Русский": "Тест ZIP"},
    "Zmiany": {"English": "Changes", "Polski": "Zmiany", "Русский": "Изменения"},
    "Uprawnienia": {"English": "Permissions", "Polski": "Uprawnienia", "Русский": "Разрешения"},
    "Grupy": {"English": "Groups", "Polski": "Grupy", "Русский": "Группы"},
    "Połączenia": {"English": "Connections", "Polski": "Połączenia", "Русский": "Соединения"},
    "Porty": {"English": "Ports", "Polski": "Porty", "Русский": "Порты"},
    "Firewall": {"English": "Firewall", "Polski": "Firewall", "Русский": "Брандмауэр"},
    "Defender": {"English": "Defender", "Polski": "Defender", "Русский": "Defender"},
    "Logi": {"English": "Logs", "Polski": "Logi", "Русский": "Журналы"},
    "Znaki": {"English": "Characters", "Polski": "Znaki", "Русский": "Символы"},
    "Słowa": {"English": "Words", "Polski": "Słowa", "Русский": "Слова"},
    "Linie": {"English": "Lines", "Polski": "Linie", "Русский": "Строки"},
    "Brak danych": {"English": "No data", "Polski": "Brak danych", "Русский": "Нет данных"},
    "Brak danych temperatury": {"English": "No temperature data", "Polski": "Brak danych temperatury", "Русский": "Нет данных о температуре"},
    "Nie wykryto dużego użycia": {"English": "No high usage detected", "Polski": "Nie wykryto dużego użycia", "Русский": "Высокая нагрузка не обнаружена"},
    "Vault": {"English": "Vault", "Polski": "Sejf", "Русский": "Сейф"},
    "🔐 ToolKit Vault": {"English": "🔐 ToolKit Vault", "Polski": "🔐 Sejf ToolKit", "Русский": "🔐 Сейф ToolKit"},
    "Utworzono sejf": {"English": "Vault created", "Polski": "Utworzono sejf", "Русский": "Сейф создан"},
    "Błędne hasło": {"English": "Incorrect password", "Polski": "Błędne hasło", "Русский": "Неверный пароль"},
    "Generator": {"English": "Generator", "Polski": "Generator", "Русский": "Генератор"},
    "Notatka": {"English": "Note", "Polski": "Notatka", "Русский": "Заметка"},
    "Treść": {"English": "Content", "Polski": "Treść", "Русский": "Содержимое"},
    "Hasło / tekst": {"English": "Password / text", "Polski": "Hasło / tekst", "Русский": "Пароль / текст"},
    "Zapisano": {"English": "Saved", "Polski": "Zapisano", "Русский": "Сохранено"},
    "➕ Dodaj": {"English": "➕ Add", "Polski": "➕ Dodaj", "Русский": "➕ Добавить"},
    "👁 Pokaż": {"English": "👁 Show", "Polski": "👁 Pokaż", "Русский": "👁 Показать"},
    "🗑 Usuń": {"English": "🗑 Delete", "Polski": "🗑 Usuń", "Русский": "🗑 Удалить"},
})

# Normalize PHRASES: ensure that every language variant is also a lookup key
for key, mapping in list(PHRASES.items()):
    for lang_label in mapping.values():
        if isinstance(lang_label, str) and lang_label not in PHRASES:
            PHRASES[lang_label] = mapping

# ensure the language label exists
PHRASES.setdefault("Język:", {"English": "Language:", "Polski": "Język:", "Русский": "Язык:"})


def t(text):
    """Translate a phrase if available, otherwise return original."""
    if not isinstance(text, str):
        return text
    entry = PHRASES.get(text)
    if entry:
        return entry.get(current_lang, text)
    return text


def refresh_localized_widgets(parent):
    """Refresh buttons and labels created outside the shared button factory."""
    for widget in parent.winfo_children():
        widget_class = widget.winfo_class()
        if widget_class in {"Button", "TButton", "Label", "TLabel"}:
            try:
                original = getattr(widget, "_orig_text", widget.cget("text"))
                widget._orig_text = original
                widget.config(text=t(original))
            except Exception:
                pass
        refresh_localized_widgets(widget)


# Wrap simpledialog and messagebox to auto-translate prompts
_orig_askstring = simpledialog.askstring
def _askstring_wrapped(title, prompt, **kwargs):
    return _orig_askstring(t(title), t(prompt), **kwargs)
simpledialog.askstring = _askstring_wrapped

_orig_askinteger = simpledialog.askinteger
def _askinteger_wrapped(title, prompt, **kwargs):
    return _orig_askinteger(t(title), t(prompt), **kwargs)
simpledialog.askinteger = _askinteger_wrapped

_orig_askyesno = messagebox.askyesno
def _askyesno_wrapped(title, message, **kwargs):
    return _orig_askyesno(t(title), t(message), **kwargs)
messagebox.askyesno = _askyesno_wrapped


def change_language(lang):
    global current_lang
    current_lang = lang
    data = translations.get(lang, translations["English"])

    try:
        subtitle.config(text=data.get("subtitle", ""))
        welcome.config(text=data.get("welcome", ""))
    except Exception:
        pass

    # update the language label using PHRASES
    try:
        new_label = PHRASES.get("Język:", {}).get(lang, "Język:")
        lang_label.config(text=new_label)
    except Exception:
        pass

    # update tab labels
    for frame, orig in list(tab_texts.items()):
        try:
            new = PHRASES.get(orig, {}).get(lang, orig)
            tabs.tab(frame, text=new)
        except Exception:
            pass

    # update button texts
    for btn in list(translatable_buttons):
        try:
            orig = getattr(btn, "_orig_text", None)
            if not orig:
                continue
            new = PHRASES.get(orig, {}).get(lang, orig)
            btn.config(text=new)
        except Exception:
            pass

    try:
        refresh_localized_widgets(root)
    except Exception:
        pass

    tools_labels = globals().get("TOOLS_LABELS", {})
    for button, original in list(tools_button_registry):
        try:
            button.config(
                text=tools_labels.get(original, {}).get(lang, original)
            )
        except Exception:
            pass


# Language controls moved to the '🌐 Język' tab

language_var = tk.StringVar(value="English")

lang_frame = tk.Frame(tab_language, bg=BG)
lang_frame.pack(anchor="nw", padx=20, pady=20)

lang_label = ttk.Label(lang_frame, text=t("Język:"), background=BG, foreground=TEXT)
lang_label.pack(side="left", padx=(0,6))

lang_combo = ttk.Combobox(lang_frame, textvariable=language_var, values=["English", "Polski", "Русский"], width=12)
lang_combo.pack(side="left")
lang_combo.bind("<<ComboboxSelected>>", lambda e: change_language(language_var.get()))

# Ensure default language is English on startup
change_language("English")



# ============================================================
# TESTOWE KAFELKI
# ============================================================


def about():

    popup(

        "ToolKit 2.0",

        "Nowa generacja Toolkit GUI"

    )



add_button(

    tab_dashboard,

    "ℹ Informacje",

    about,

    0,

    0

)



# ============================================================
# START
# ============================================================


# ============================================================
# ToolKit 2.0
# CZĘŚĆ 2 — FILE MANAGER PRO
# ============================================================


import zipfile
import collections



# ============================================================
# OKNO TEKSTOWE
# ============================================================


def toolkit_text_window(title, text):


    window=tk.Toplevel(

        root

    )


    window.title(

        translate_ui_text(title)

    )


    window.geometry(

        "800x500"

    )


    box=tk.Text(

        window,

        bg="#111827",

        fg="white",

        font=(

            "Consolas",

            11

        )

    )


    box.pack(

        expand=True,

        fill="both"

    )


    box.insert(

        tk.END,

        translate_ui_text(text)

    )



# ============================================================
# EKSPLORATOR
# ============================================================


def file_explorer():


    folder=choose_folder()



    if not folder:

        return



    data=""


    for item in os.listdir(folder):


        path=os.path.join(

            folder,

            item

        )


        if os.path.isdir(path):

            data+="📁 "


        else:

            data+="📄 "



        data+=item+"\n"



    toolkit_text_window(

        t("Eksplorator"),

        data

    )



# ============================================================
# KOPIOWANIE
# ============================================================


def file_copy():


    source=choose_file()



    if not source:

        return



    destination=filedialog.askdirectory()



    if destination:


        shutil.copy(

            source,

            destination

        )


        popup(

            t("Pliki"),

            t("Skopiowano")

        )



# ============================================================
# PRZENOSZENIE
# ============================================================


def file_move():


    source=choose_file()



    if not source:

        return



    destination=filedialog.askdirectory()



    if destination:


        shutil.move(

            source,

            destination

        )


        popup(

            t("Pliki"),

            t("Przeniesiono")

        )



# ============================================================
# USUWANIE
# ============================================================


def file_delete():


    file=choose_file()



    if file:


        if messagebox.askyesno(

            t("Usuń"),

            t("Usunąć plik?")

        ):


            os.remove(

                file

            )


            popup(

                t("OK"),

                t("Usunięto")

            )



# ============================================================
# INFORMACJE
# ============================================================


def file_info():


    file=choose_file()



    if not file:

        return



    size=os.path.getsize(

        file

    )


    created=datetime.datetime.fromtimestamp(

        os.path.getctime(file)

    )


    modified=datetime.datetime.fromtimestamp(

        os.path.getmtime(file)

    )



    popup(

        "Informacje",

        f"""

Plik:

{file}


Rozmiar:

{size} bajtów


Utworzono:

{created}


Zmodyfikowano:

{modified}

"""

    )



# ============================================================
# ZIP
# ============================================================


def file_zip():


    folder=choose_folder()



    if not folder:

        return



    output=filedialog.asksaveasfilename(

        defaultextension=".zip"

    )



    if output:


        shutil.make_archive(

            output.replace(

                ".zip",

                ""

            ),

            "zip",

            folder

        )


        popup(

            "ZIP",

            "Utworzono archiwum"

        )



# ============================================================
# ROZPAKOWANIE
# ============================================================


def file_unzip():


    archive=choose_file()



    if not archive:

        return



    folder=choose_folder()



    if folder:


        with zipfile.ZipFile(

            archive

        ) as z:


            z.extractall(

                folder

            )


        popup(

            "ZIP",

            "Rozpakowano"

        )



# ============================================================
# SZUKAJ
# ============================================================


def file_search():


    folder=choose_folder()



    if not folder:

        return



    query=simpledialog.askstring(

        "Szukaj",

        "Nazwa pliku"

    )



    if not query:

        return



    result=""


    for root_dir,dirs,files in os.walk(folder):


        for f in files:


            if query.lower() in f.lower():


                result+=os.path.join(

                    root_dir,

                    f

                )+"\n"



    toolkit_text_window(

        "Wyniki",

        result

    )



# ============================================================
# ROZSZERZENIA
# ============================================================


def file_extensions():


    folder=choose_folder()



    if not folder:

        return



    counter=collections.Counter()



    for root_dir,dirs,files in os.walk(folder):


        for f in files:


            ext=os.path.splitext(

                f

            )[1]


            counter[ext]+=1



    text=""


    for k,v in counter.items():


        text+=f"{k}: {v}\n"



    toolkit_text_window(

        "Statystyka",

        text

    )



# ============================================================
# NAJWIĘKSZE PLIKI
# ============================================================


def file_biggest():


    folder=choose_folder()



    if not folder:

        return



    files=[]



    for root_dir,dirs,fs in os.walk(folder):


        for f in fs:


            try:


                path=os.path.join(

                    root_dir,

                    f

                )


                files.append(

                    (

                        os.path.getsize(path),

                        path

                    )

                )


            except:

                pass



    files.sort(

        reverse=True

    )


    result=""


    for size,path in files[:20]:


        result+=f"{round(size/1024/1024,2)} MB | {path}\n"



    toolkit_text_window(

        "Największe",

        result

    )



# ============================================================
# DUPLIKATY
# ============================================================


def file_duplicates():


    folder=choose_folder()



    hashes={}

    result=""


    for root_dir,dirs,files in os.walk(folder):


        for f in files:


            path=os.path.join(

                root_dir,

                f

            )


            try:


                h=hashlib.md5()



                with open(

                    path,

                    "rb"

                ) as file:


                    h.update(

                        file.read()

                    )



                key=h.hexdigest()



                if key in hashes:


                    result+=path+"\n"


                else:


                    hashes[key]=path



            except:

                pass



    if not result:

        result="Brak duplikatów"



    toolkit_text_window(

        "Duplikaty",

        result

    )



# ============================================================
# MASOWA ZMIANA NAZW
# ============================================================


def file_mass_rename():


    folder=choose_folder()



    prefix=simpledialog.askstring(

        "Nazwa",

        "Prefix"

    )



    if not prefix:

        return



    i=1



    for f in os.listdir(folder):


        old=os.path.join(

            folder,

            f

        )


        new=os.path.join(

            folder,

            prefix+"_"+str(i)+"_"+f

        )


        os.rename(

            old,

            new

        )


        i+=1



    popup(

        "Rename",

        "Gotowe"

    )



# ============================================================
# KAFELKI PLIKÓW
# ============================================================


file_buttons=[


("📁 Eksplorator",file_explorer),

("📋 Kopiuj",file_copy),

("🚚 Przenieś",file_move),

("🗑 Usuń",file_delete),

("📊 Informacje",file_info),

("📦 ZIP",file_zip),

("📤 Rozpakuj",file_unzip),

("🔎 Szukaj",file_search),

("📈 Rozszerzenia",file_extensions),

("💾 Największe",file_biggest),

("♻ Duplikaty",file_duplicates),

("✏ Zmień nazwy",file_mass_rename)

]



row=0
col=0


for text,cmd in file_buttons:


    add_button(

        tab_files,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 3 — SYSTEM PRO
# ============================================================


try:

    import psutil

except Exception:

    psutil=None


# ============================================================
# INFORMACJE WINDOWS
# ============================================================


def system_windows_info():


    text=f"""

SYSTEM:

{platform.system()}


WERSJA:

{platform.version()}


RELEASE:

{platform.release()}


ARCHITEKTURA:

{platform.machine()}


PROCESOR:

{platform.processor()}

"""


    toolkit_text_window(

        "Windows Info",

        text

    )



# ============================================================
# PYTHON INFO
# ============================================================


def system_python_info():


    text=f"""

Python:

{sys.version}


Interpreter:

{sys.executable}

"""


    toolkit_text_window(

        "Python",

        text

    )



# ============================================================
# CPU
# ============================================================


def system_cpu():


    cpu=psutil.cpu_percent(

        interval=1

    )


    cores=psutil.cpu_count()



    popup(

        "CPU",

        f"""

Użycie:

{cpu}%


Rdzenie:

{cores}

"""

    )



# ============================================================
# RAM
# ============================================================


def system_ram():


    ram=psutil.virtual_memory()



    popup(

        "RAM",

        f"""

Użycie:

{ram.percent}%


Całość:

{round(ram.total/1024**3,2)} GB


Dostępne:

{round(ram.available/1024**3,2)} GB

"""

    )



# ============================================================
# DYSKI
# ============================================================


def system_disks():


    text=""


    for d in psutil.disk_partitions():


        try:


            usage=psutil.disk_usage(

                d.mountpoint

            )


            text+=f"""

Dysk:

{d.device}


System:

{d.fstype}


Użycie:

{usage.percent}%


Wolne:

{round(usage.free/1024**3,2)} GB


----------------

"""


        except:

            pass



    toolkit_text_window(

        "Dyski",

        text

    )



# ============================================================
# PROCESY
# ============================================================


def system_processes():


    text=""


    for p in psutil.process_iter(

        [

            "pid",

            "name",

            "memory_percent"

        ]

    ):


        try:


            text+=f"""

PID:

{p.info['pid']}


Nazwa:

{p.info['name']}


RAM:

{round(p.info['memory_percent'],2)}%


----------------

"""


        except:

            pass



    toolkit_text_window(

        "Procesy",

        text

    )



# ============================================================
# USŁUGI WINDOWS
# ============================================================


def system_services():


    result=run_command(

        "sc query"

    )


    toolkit_text_window(

        "Usługi",

        result

    )



# ============================================================
# AUTOSTART
# ============================================================


def system_startup():


    result=run_command(

        "wmic startup get caption,command"

    )


    toolkit_text_window(

        "Autostart",

        result

    )



# ============================================================
# ZMIENNE ŚRODOWISKOWE
# ============================================================


def system_environment():


    text=""


    for k,v in os.environ.items():


        text+=f"{k}={v}\n"



    toolkit_text_window(

        "Environment",

        text

    )



# ============================================================
# UŻYTKOWNICY
# ============================================================


def system_users():


    result=run_command(

        "net user"

    )


    toolkit_text_window(

        "Użytkownicy",

        result

    )



# ============================================================
# STEROWNIKI
# ============================================================


def system_drivers():


    result=run_command(

        "driverquery"

    )


    toolkit_text_window(

        "Sterowniki",

        result

    )



# ============================================================
# LOGI SYSTEMOWE
# ============================================================


def system_logs():


    result=run_command(

        "wevtutil el"

    )


    toolkit_text_window(

        "Logi Windows",

        result

    )



# ============================================================
# MONITOR ZASOBÓW
# ============================================================


def system_monitor():


    window=tk.Toplevel(

        root

    )


    window.title(

        t("Monitor")

    )


    window.geometry(

        "500x400"

    )


    label=tk.Label(

        window,

        bg=BG,

        fg=TEXT,

        font=(

            "Segoe UI",

            14

        )

    )


    label.pack(

        expand=True

    )



    def update():


        cpu=psutil.cpu_percent()

        ram=psutil.virtual_memory().percent



        label.config(

            text=f"""

CPU:

{cpu}%


RAM:

{ram}%

"""

        )


        window.after(

            1000,

            update

        )



    update()



# ============================================================
# KAFELKI SYSTEM
# ============================================================


system_buttons=[


("💻 Windows Info",system_windows_info),

("🐍 Python Info",system_python_info),

("⚡ CPU",system_cpu),

("🧠 RAM",system_ram),

("💾 Dyski",system_disks),

("📋 Procesy",system_processes),

("⚙ Usługi",system_services),

("🚀 Autostart",system_startup),

("🌐 Environment",system_environment),

("👤 Użytkownicy",system_users),

("🔧 Sterowniki",system_drivers),

("📜 Logi",system_logs),

("📈 Monitor",system_monitor)

]



row=0
col=0


for text,cmd in system_buttons:


    add_button(

        tab_system,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 4 — HARDWARE PRO
# ============================================================



# ============================================================
# GPU
# ============================================================


def hardware_gpu():


    result=run_command(

        "wmic path win32_VideoController get name,driverVersion"

    )


    toolkit_text_window(

        "GPU",

        result

    )



# ============================================================
# BIOS
# ============================================================


def hardware_bios():


    result=run_command(

        "wmic bios get manufacturer,name,version,releasedate"

    )


    toolkit_text_window(

        "BIOS",

        result

    )



# ============================================================
# PŁYTA GŁÓWNA
# ============================================================


def hardware_board():


    result=run_command(

        "wmic baseboard get manufacturer,product,serialnumber"

    )


    toolkit_text_window(

        "Płyta główna",

        result

    )



# ============================================================
# CPU SZCZEGÓŁY
# ============================================================


def hardware_cpu_detail():


    result=run_command(

        "wmic cpu get name,maxclockspeed,numberofcores"

    )


    toolkit_text_window(

        "CPU",

        result

    )



# ============================================================
# RAM MODUŁY
# ============================================================


def hardware_ram_modules():


    result=run_command(

        "wmic memorychip get manufacturer,capacity,speed"

    )


    toolkit_text_window(

        "RAM",

        result

    )



# ============================================================
# DYSKI FIZYCZNE
# ============================================================


def hardware_physical_disk():


    result=run_command(

        "wmic diskdrive get model,size,serialnumber"

    )


    toolkit_text_window(

        "Dyski",

        result

    )



# ============================================================
# SMART
# ============================================================


def hardware_smart():


    result=run_command(

        "wmic diskdrive get model,status"

    )


    toolkit_text_window(

        "SMART",

        result

    )



# ============================================================
# USB
# ============================================================


def hardware_usb():


    result=run_command(

        "wmic path Win32_USBHub get Name"

    )


    toolkit_text_window(

        "USB",

        result

    )



# ============================================================
# MONITORY
# ============================================================


def hardware_monitors():


    result=run_command(

        "wmic desktopmonitor get screenheight,screenwidth,name"

    )


    toolkit_text_window(

        "Monitory",

        result

    )



# ============================================================
# AUDIO
# ============================================================


def hardware_audio():


    result=run_command(

        "wmic sounddev get name"

    )


    toolkit_text_window(

        "Audio",

        result

    )



# ============================================================
# KAMERA
# ============================================================


def hardware_camera():


    result=run_command(

        "wmic path Win32_PnPEntity where \"Name like '%Camera%'\" get Name"

    )


    toolkit_text_window(

        "Kamera",

        result

    )



# ============================================================
# BATERIA
# ============================================================


def hardware_battery():


    result=run_command(

        "wmic battery get status,estimatedChargeRemaining"

    )


    toolkit_text_window(

        "Bateria",

        result

    )



# ============================================================
# PCI
# ============================================================


def hardware_pci():


    result=run_command(

        "wmic path Win32_PnPEntity get Name"

    )


    toolkit_text_window(

        "Urządzenia",

        result

    )



# ============================================================
# TEMPERATURY
# ============================================================


def hardware_temperature():


    if hasattr(

        psutil,

        "sensors_temperatures"

    ):


        try:


            data=psutil.sensors_temperatures()



            popup(

                "Temperatury",

                str(data)

            )


        except:


            error(

                "Brak danych"

            )


    else:


        error(

            "System nie udostępnia temperatur"

        )



# ============================================================
# KONTROLERY
# ============================================================


def hardware_controllers():


    result=run_command(

        "wmic path Win32_Controller get Name"

    )


    toolkit_text_window(

        "Kontrolery",

        result

    )



# ============================================================
# KAFELKI HARDWARE
# ============================================================


hardware_buttons=[


("🎮 GPU",hardware_gpu),

("🧬 BIOS",hardware_bios),

("🖥 Płyta główna",hardware_board),

("⚡ CPU Info",hardware_cpu_detail),

("🧠 RAM Moduły",hardware_ram_modules),

("💽 Dyski fizyczne",hardware_physical_disk),

("💚 SMART",hardware_smart),

("🔌 USB",hardware_usb),

("🖥 Monitory",hardware_monitors),

("🔊 Audio",hardware_audio),

("📷 Kamera",hardware_camera),

("🔋 Bateria",hardware_battery),

("🔧 PCI",hardware_pci),

("🌡 Temperatury",hardware_temperature),

("⚙ Kontrolery",hardware_controllers)

]



row=0
col=0


for text,cmd in hardware_buttons:


    add_button(

        tab_hardware,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 5 — NETWORK PRO
# ============================================================


import socket
import urllib.request



# ============================================================
# KARTY SIECIOWE
# ============================================================


def network_adapters():


    text=""


    if psutil:


        adapters=psutil.net_if_addrs()



        for name,data in adapters.items():


            text+=f"\n{name}\n"

            text+="-"*30+"\n"



            for item in data:


                text+=str(item)+"\n"



    toolkit_text_window(

        "Karty sieciowe",

        text

    )



# ============================================================
# IP LOKALNE
# ============================================================


def network_local_ip():


    try:


        hostname=socket.gethostname()


        ip=socket.gethostbyname(

            hostname

        )


        popup(

            "IP",

            ip

        )


    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# PUBLIC IP
# ============================================================


def network_public_ip():


    try:


        ip=urllib.request.urlopen(

            "https://api.ipify.org",

            timeout=5

        ).read().decode()



        popup(

            "Publiczne IP",

            ip

        )


    except:


        error(

            "Brak dostępu"

        )



# ============================================================
# DNS LOOKUP
# ============================================================


def network_dns_lookup():


    host=simpledialog.askstring(

        "DNS",

        "Domena"

    )



    if not host:

        return



    try:


        result=socket.gethostbyname_ex(

            host

        )


        popup(

            "DNS",

            str(result)

        )


    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# PING
# ============================================================


def network_ping():


    host=simpledialog.askstring(

        "Ping",

        "Adres"

    )


    if not host:

        return



    result=run_command(

        f"ping {host}"

    )



    toolkit_text_window(

        "Ping",

        result

    )



# ============================================================
# TRACEROUTE
# ============================================================


def network_traceroute():


    host=simpledialog.askstring(

        "Traceroute",

        "Adres"

    )



    if not host:

        return



    if os.name=="nt":


        cmd=f"tracert {host}"


    else:


        cmd=f"traceroute {host}"



    result=run_command(

        cmd

    )


    toolkit_text_window(

        "Traceroute",

        result

    )



# ============================================================
# TEST PORTU
# ============================================================


def network_port_test():


    host=simpledialog.askstring(

        "Host",

        "Adres"

    )


    port=simpledialog.askinteger(

        "Port",

        "Numer"

    )



    if not host or not port:

        return



    sock=socket.socket()



    sock.settimeout(

        3

    )



    result=sock.connect_ex(

        (

            host,

            port

        )

    )



    sock.close()



    if result==0:


        popup(

            "Port",

            "OTWARTY"

        )


    else:


        popup(

            "Port",

            "ZAMKNIĘTY"

        )



# ============================================================
# SKAN LAN
# ============================================================


def network_lan_scan():


    subnet=simpledialog.askstring(

        "LAN",

        "Prefix np. 192.168.1"

    )



    if not subnet:

        return



    result=""


    for i in range(1,255):


        ip=f"{subnet}.{i}"



        try:


            socket.gethostbyaddr(

                ip

            )


            result+=ip+"\n"



        except:

            pass



    toolkit_text_window(

        "LAN Scan",

        result

    )



# ============================================================
# ARP
# ============================================================


def network_arp():


    result=run_command(

        "arp -a"

    )


    toolkit_text_window(

        "ARP",

        result

    )



# ============================================================
# WIFI
# ============================================================


def network_wifi():


    result=run_command(

        "netsh wlan show interfaces"

    )


    toolkit_text_window(

        "WiFi",

        result

    )



# ============================================================
# POŁĄCZENIA
# ============================================================


def network_connections():


    if not psutil:

        return



    text=""


    for c in psutil.net_connections():


        text+=str(c)+"\n"



    toolkit_text_window(

        "Połączenia",

        text

    )



# ============================================================
# NETSTAT
# ============================================================


def network_netstat():


    result=run_command(

        "netstat -ano"

    )


    toolkit_text_window(

        "Netstat",

        result

    )



# ============================================================
# RESET DNS
# ============================================================


def network_flush_dns():


    result=run_command(

        "ipconfig /flushdns"

    )


    popup(

        "DNS",

        result

    )



# ============================================================
# TEST INTERNETU
# ============================================================


def network_internet_test():


    try:


        socket.create_connection(

            (

                "8.8.8.8",

                53

            ),

            timeout=5

        )


        popup(

            "Internet",

            "Połączenie działa"

        )


    except:


        error(

            "Brak internetu"

        )



# ============================================================
# KAFELKI NETWORK
# ============================================================


network_buttons=[


("🌐 Karty sieciowe",network_adapters),

("📍 Lokalny IP",network_local_ip),

("🌍 Publiczne IP",network_public_ip),

("🔎 DNS Lookup",network_dns_lookup),

("📡 Ping",network_ping),

("🛰 Traceroute",network_traceroute),

("🔌 Test portu",network_port_test),

("📶 Skan LAN",network_lan_scan),

("📋 ARP",network_arp),

("📡 WiFi",network_wifi),

("🔗 Połączenia",network_connections),

("📊 Netstat",network_netstat),

("♻ Flush DNS",network_flush_dns),

("🌍 Test Internetu",network_internet_test)

]



row=0
col=0


for text,cmd in network_buttons:


    add_button(

        tab_network,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 6 — SECURITY PRO
# ============================================================


# ============================================================
# WINDOWS DEFENDER
# ============================================================


def security_defender():


    result=run_command(

        "powershell Get-MpComputerStatus"

    )


    toolkit_text_window(

        "Windows Defender",

        result

    )



# ============================================================
# FIREWALL
# ============================================================


def security_firewall():


    result=run_command(

        "netsh advfirewall show allprofiles"

    )


    toolkit_text_window(

        "Firewall",

        result

    )



# ============================================================
# SKAN PROCESÓW
# ============================================================


def security_process_scan():


    if not psutil:

        return



    text=""


    for p in psutil.process_iter(

        [

            "pid",

            "name",

            "cpu_percent",

            "memory_percent"

        ]

    ):


        try:


            info=p.info



            if (

                info["cpu_percent"] > 50

                or

                info["memory_percent"] > 10

            ):


                text+=f"""

PID:

{info['pid']}


Proces:

{info['name']}


CPU:

{info['cpu_percent']}%


RAM:

{round(info['memory_percent'],2)}%


-------------------

"""



        except:

            pass



    if not text:

        text=t("Nie wykryto dużego użycia")



    toolkit_text_window(

        "Skan procesów",

        text

    )



# ============================================================
# OTWARTE PORTY
# ============================================================


def security_ports():


    result=run_command(

        "netstat -ano"

    )


    toolkit_text_window(

        "Porty",

        result

    )



# ============================================================
# UŻYTKOWNICY
# ============================================================


def security_users():


    result=run_command(

        "net user"

    )


    toolkit_text_window(

        "Użytkownicy",

        result

    )



# ============================================================
# ADMINISTRATORZY
# ============================================================


def security_admins():


    result=run_command(

        "net localgroup administrators"

    )


    toolkit_text_window(

        "Administratorzy",

        result

    )



# ============================================================
# UAC
# ============================================================


def security_uac():


    result=run_command(

        "reg query HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA"

    )


    popup(

        "UAC",

        result

    )



# ============================================================
# SHA256
# ============================================================


def security_sha256():


    file=choose_file()



    if not file:

        return



    sha=hashlib.sha256()



    with open(

        file,

        "rb"

    ) as f:


        while True:


            data=f.read(

                8192

            )


            if not data:

                break



            sha.update(

                data

            )



    popup(

        "SHA256",

        sha.hexdigest()

    )



# ============================================================
# INTEGRALNOŚĆ PLIKU
# ============================================================


def security_file_check():


    file=choose_file()



    if not file:

        return



    size=os.path.getsize(

        file

    )



    modified=datetime.datetime.fromtimestamp(

        os.path.getmtime(file)

    )



    popup(

        "Kontrola",

        f"""

Plik:

{file}


Rozmiar:

{size} bajtów


Zmodyfikowano:

{modified}

"""

    )



# ============================================================
# AUDYT SYSTEMU
# ============================================================


def security_audit():


    report=""


    report+="SYSTEM\n"

    report+=platform.platform()

    report+="\n\n"



    report+="UŻYTKOWNICY\n"

    report+=run_command(

        "net user"

    )


    report+="\n\nFIREWALL\n"

    report+=run_command(

        "netsh advfirewall show allprofiles"

    )



    toolkit_text_window(

        "Audyt",

        report

    )



# ============================================================
# HISTORIA LOGOWANIA
# ============================================================


def security_login_history():


    result=run_command(

        "wevtutil qe Security /c:20 /rd:true"

    )


    toolkit_text_window(

        "Logowania",

        result

    )



# ============================================================
# WINDOWS UPDATE
# ============================================================


def security_updates():


    result=run_command(

        "powershell Get-HotFix"

    )


    toolkit_text_window(

        "Aktualizacje",

        result

    )



# ============================================================
# STATUS KONTA
# ============================================================


def security_account_status():


    result=run_command(

        "whoami /all"

    )


    toolkit_text_window(

        "Konto",

        result

    )



# ============================================================
# RAPORT
# ============================================================


def security_report():


    filename="security_report.txt"



    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:


        f.write(

            "ToolKit 2.0 Security Report\n\n"

        )


        f.write(

            platform.platform()

        )


    popup(

        "Raport",

        "Zapisano raport"

    )



# ============================================================
# The Security UI is built once by the consolidated Security Center block below.


# ============================================================
# ToolKit 2.0
# CZĘŚĆ 7 — BACKUP PRO
# ============================================================


import pathlib



BACKUP_FOLDER="ToolKit_Backups"



# ============================================================
# TWORZENIE FOLDERU BACKUP
# ============================================================


def backup_prepare():


    if not os.path.exists(

        BACKUP_FOLDER

    ):


        os.makedirs(

            BACKUP_FOLDER

        )



# ============================================================
# BACKUP FOLDERU
# ============================================================


def backup_folder():


    source=choose_folder()



    if not source:

        return



    backup_prepare()



    name=os.path.basename(

        source

    )


    destination=os.path.join(

        BACKUP_FOLDER,

        name+"_"+datetime.datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

    )



    shutil.copytree(

        source,

        destination

    )



    popup(

        "Backup",

        "Utworzono kopię"

    )



# ============================================================
# PRZYWRACANIE
# ============================================================


def backup_restore():


    backup=choose_folder()



    if not backup:

        return



    destination=filedialog.askdirectory()



    if destination:


        shutil.copytree(

            backup,

            destination,

            dirs_exist_ok=True

        )


        popup(

            "Restore",

            "Przywrócono"

        )



# ============================================================
# ZIP BACKUP
# ============================================================


def backup_zip():


    folder=choose_folder()



    if not folder:

        return



    output=filedialog.asksaveasfilename(

        defaultextension=".zip"

    )



    if output:


        shutil.make_archive(

            output.replace(

                ".zip",

                ""

            ),

            "zip",

            folder

        )



        popup(

            "ZIP",

            "Backup ZIP gotowy"

        )



# ============================================================
# PROFIL UŻYTKOWNIKA
# ============================================================


def backup_user_profile():


    source=os.path.expanduser(

        "~"

    )



    backup_prepare()



    destination=os.path.join(

        BACKUP_FOLDER,

        "User_Profile"

    )



    shutil.copytree(

        source,

        destination,

        dirs_exist_ok=True

    )


    popup(

        "Profil",

        "Skopiowano profil"

    )



# ============================================================
# PULPIT
# ============================================================


def backup_desktop():


    desktop=os.path.join(

        os.path.expanduser("~"),

        "Desktop"

    )


    backup_prepare()



    shutil.copytree(

        desktop,

        os.path.join(

            BACKUP_FOLDER,

            "Desktop"

        ),

        dirs_exist_ok=True

    )


    popup(

        "Pulpit",

        "Backup pulpitu gotowy"

    )



# ============================================================
# DOKUMENTY
# ============================================================


def backup_documents():


    folder=os.path.join(

        os.path.expanduser("~"),

        "Documents"

    )



    backup_prepare()



    shutil.copytree(

        folder,

        os.path.join(

            BACKUP_FOLDER,

            "Documents"

        ),

        dirs_exist_ok=True

    )


    popup(

        "Dokumenty",

        "Backup wykonany"

    )



# ============================================================
# USTAWIENIA APLIKACJI
# ============================================================


def backup_app_settings():


    paths=[

        os.path.expanduser(

            "~/AppData/Roaming"

        ),

        os.path.expanduser(

            "~/AppData/Local"

        )

    ]



    backup_prepare()



    for p in paths:


        if os.path.exists(p):


            shutil.copytree(

                p,

                os.path.join(

                    BACKUP_FOLDER,

                    os.path.basename(p)

                ),

                dirs_exist_ok=True

            )



    popup(

        "Settings",

        "Ustawienia zapisane"

    )



# ============================================================
# REJESTR WINDOWS
# ============================================================


def backup_registry():


    backup_prepare()



    file=os.path.join(

        BACKUP_FOLDER,

        "registry_backup.reg"

    )



    run_command(

        f"reg export HKCU {file} /y"

    )



    popup(

        "Rejestr",

        "Backup rejestru gotowy"

    )



# ============================================================
# LISTA BACKUPÓW
# ============================================================


def backup_list():


    backup_prepare()



    text=""


    for item in os.listdir(

        BACKUP_FOLDER

    ):


        text+=item+"\n"



    toolkit_text_window(

        "Backup Lista",

        text

    )



# ============================================================
# USUWANIE STARYCH
# ============================================================


def backup_clean():


    folder=choose_folder()



    if not folder:

        return



    for item in os.listdir(folder):


        path=os.path.join(

            folder,

            item

        )


        if os.path.isdir(path):


            shutil.rmtree(

                path

            )


        else:


            os.remove(

                path

            )



    popup(

        "Czyszczenie",

        "Usunięto"

    )



# ============================================================
# SYNCHRONIZACJA
# ============================================================


def backup_sync():


    source=choose_folder()



    destination=filedialog.askdirectory()



    if source and destination:


        shutil.copytree(

            source,

            destination,

            dirs_exist_ok=True

        )


        popup(

            "Sync",

            "Synchronizacja zakończona"

        )



# ============================================================
# PORÓWNANIE
# ============================================================


def backup_compare():


    a=choose_folder()



    b=filedialog.askdirectory()



    if not a or not b:

        return



    files_a=set(

        os.listdir(a)

    )


    files_b=set(

        os.listdir(b)

    )


    result=f"""

Tylko A:

{files_a-files_b}


Tylko B:

{files_b-files_a}

"""



    toolkit_text_window(

        "Porównanie",

        result

    )



# ============================================================
# RAPORT BACKUP
# ============================================================


def backup_report():


    backup_prepare()



    text="ToolKit 2.0 Backup Report\n\n"



    text+=f"Lokalizacja:\n{BACKUP_FOLDER}\n\n"



    text+="Zawartość:\n"



    for x in os.listdir(BACKUP_FOLDER):


        text+=x+"\n"



    toolkit_text_window(

        "Raport",

        text

    )



# ============================================================
# KAFELKI BACKUP
# ============================================================


# Legacy Backup UI removed; the active panel is defined below.

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 8 — VAULT PRO
# ============================================================


import base64
import importlib.util
import secrets
import string


Fernet=None


if importlib.util.find_spec("cryptography") is not None:

    try:

        Fernet=importlib.import_module("cryptography.fernet").Fernet

    except Exception:

        Fernet=None



VAULT_FILE="toolkit_vault.dat"



# ============================================================
# KLUCZ
# ============================================================


def vault_key(password):


    return base64.urlsafe_b64encode(

        hashlib.sha256(

            password.encode()

        ).digest()

    )



# ============================================================
# SZYFROWANIE
# ============================================================


def vault_encrypt(data,password):


    if not Fernet:


        error(

            "Brak cryptography"

        )

        return



    f=Fernet(

        vault_key(password)

    )


    return f.encrypt(

        data.encode()

    )



# ============================================================
# DESZYFROWANIE
# ============================================================


def vault_decrypt(data,password):


    f=Fernet(

        vault_key(password)

    )


    return f.decrypt(

        data

    ).decode()



# ============================================================
# TWORZENIE SEJFU
# ============================================================


def vault_create():


    password=simpledialog.askstring(

        "Vault",

        "Hasło główne",

        show="*"

    )



    if not password:

        return



    data={

        "entries":[]

    }



    encrypted=vault_encrypt(

        json.dumps(data),

        password

    )



    with open(

        VAULT_FILE,

        "wb"

    ) as f:


        f.write(

            encrypted

        )



    popup(

        "Vault",

        "Utworzono sejf"

    )



# ============================================================
# OTWIERANIE
# ============================================================


def vault_open():


    if not os.path.exists(

        VAULT_FILE

    ):


        vault_create()

        return



    password=simpledialog.askstring(

        "Vault",

        "Hasło",

        show="*"

    )



    if not password:

        return



    try:


        with open(

            VAULT_FILE,

            "rb"

        ) as f:


            encrypted=f.read()



        data=json.loads(

            vault_decrypt(

                encrypted,

                password

            )

        )



        vault_window(

            data,

            password

        )



    except:


        error(

            "Błędne hasło"

        )



# ============================================================
# OKNO SEJFU
# ============================================================


def vault_window(data,password):


    win=tk.Toplevel(

        root

    )


    win.title(

        t("🔐 ToolKit Vault")

    )


    win.geometry(

        "700x500"

    )



    box=tk.Listbox(

        win,

        bg="#111827",

        fg="white"

    )


    box.pack(

        expand=True,

        fill="both",

        padx=10,

        pady=10

    )



    def refresh():


        box.delete(

            0,

            tk.END

        )


        for item in data["entries"]:


            box.insert(

                tk.END,

                item["name"]

            )



    def save():


        encrypted=vault_encrypt(

            json.dumps(data),

            password

        )


        with open(

            VAULT_FILE,

            "wb"

        ) as f:


            f.write(

                encrypted

            )



    def add():


        name=simpledialog.askstring(

            "Nazwa",

            "Nazwa"

        )



        value=simpledialog.askstring(

            "Wartość",

            "Hasło / tekst",

            show="*"

        )



        if name and value:


            data["entries"].append(

                {

                    "name":name,

                    "value":value

                }

            )


            save()

            refresh()



    def remove():


        selected=box.curselection()



        if selected:


            data["entries"].pop(

                selected[0]

            )


            save()

            refresh()



    def show():


        selected=box.curselection()



        if selected:


            item=data["entries"][

                selected[0]

            ]



            popup(

                item["name"],

                item["value"]

            )



    ttk.Button(

        win,

        text=t("➕ Dodaj"),

        command=add,

        style="Tool.TButton"

    ).pack()



    ttk.Button(

        win,

        text=t("👁 Pokaż"),

        command=show,

        style="Tool.TButton"

    ).pack()



    ttk.Button(

        win,

        text=t("🗑 Usuń"),

        command=remove,

        style="Tool.TButton"

    ).pack()



    refresh()



# ============================================================
# GENERATOR HASŁA
# ============================================================


def vault_password_generator():


    length=simpledialog.askinteger(

        "Generator",

        "Długość"

    )


    if not length:

        return



    chars=(

        string.ascii_letters

        +

        string.digits

        +

        "!@#$%^&*"

    )



    password="".join(

        secrets.choice(chars)

        for _ in range(length)

    )



    popup(

        "Hasło",

        password

    )



# ============================================================
# NOTATKA
# ============================================================


def vault_private_note():


    text=simpledialog.askstring(

        "Notatka",

        "Treść"

    )



    if text:


        encrypted=vault_encrypt(

            text,

            "toolkit"

        )



        with open(

            "private_note.dat",

            "wb"

        ) as f:


            f.write(

                encrypted

            )


        popup(

            "Notatka",

            "Zapisano"

        )



# ============================================================
# KAFELKI VAULT
# ============================================================


vault_buttons=[


("🔐 Otwórz sejf",vault_open),

("➕ Nowy sejf",vault_create),

("🔑 Generator haseł",vault_password_generator),

("📝 Prywatna notatka",vault_private_note)

]



row=0
col=0


for text,cmd in vault_buttons:


    add_button(

        tab_tools,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 9 — ADVANCED TOOLS
# ============================================================


import uuid
import secrets
import base64



# ============================================================
# UUID
# ============================================================


def tool_uuid():


    popup(

        "UUID",

        str(uuid.uuid4())

    )



# ============================================================
# GUID
# ============================================================


def tool_guid():


    popup(

        "GUID",

        str(uuid.uuid1())

    )



# ============================================================
# HASH FUNKCJA
# ============================================================


def calculate_hash(algorithm):


    file=choose_file()



    if not file:

        return



    h=algorithm()



    with open(

        file,

        "rb"

    ) as f:


        while True:


            data=f.read(

                8192

            )


            if not data:

                break



            h.update(

                data

            )



    popup(

        "Hash",

        h.hexdigest()

    )



# ============================================================
# MD5
# ============================================================


def tool_md5():

    calculate_hash(

        hashlib.md5

    )



# ============================================================
# SHA1
# ============================================================


def tool_sha1():

    calculate_hash(

        hashlib.sha1

    )



# ============================================================
# SHA256
# ============================================================


def tool_sha256():

    calculate_hash(

        hashlib.sha256

    )



# ============================================================
# PORÓWNANIE HASH
# ============================================================


def tool_compare_hash():


    a=simpledialog.askstring(

        "Hash",

        "Pierwszy hash"

    )


    b=simpledialog.askstring(

        "Hash",

        "Drugi hash"

    )



    if a==b:


        popup(

            "Wynik",

            "Hashy są identyczne"

        )


    else:


        popup(

            "Wynik",

            "Hashy różne"

        )



# ============================================================
# SZYFROWANIE PLIKU
# ============================================================


def tool_encrypt_file():


    file=choose_file()



    if not file:

        return



    password=simpledialog.askstring(

        "Szyfrowanie",

        "Hasło",

        show="*"

    )


    if not password:

        return



    with open(

        file,

        "rb"

    ) as f:


        data=f.read()



    key=hashlib.sha256(

        password.encode()

    ).digest()



    encrypted=bytes(

        [

            b ^ key[i % len(key)]

            for i,b in enumerate(data)

        ]

    )



    output=file+".enc"



    with open(

        output,

        "wb"

    ) as f:


        f.write(

            encrypted

        )



    popup(

        "Szyfrowanie",

        output

    )



# ============================================================
# TOKEN
# ============================================================


def tool_token():


    token=secrets.token_hex(

        32

    )


    popup(

        "Token",

        token

    )



# ============================================================
# RANDOM
# ============================================================


def tool_random_data():


    size=simpledialog.askinteger(

        "Random",

        "Ilość znaków"

    )


    if size:


        data=secrets.token_urlsafe(

            size

        )


        popup(

            "Dane",

            data

        )



# ============================================================
# BASE64
# ============================================================


def tool_base64_encode():


    text=simpledialog.askstring(

        "Base64",

        "Tekst"

    )


    if text:


        result=base64.b64encode(

            text.encode()

        ).decode()



        popup(

            "Base64",

            result

        )



def tool_base64_decode():


    text=simpledialog.askstring(

        "Base64",

        "Kod"

    )


    if text:


        result=base64.b64decode(

            text

        ).decode()



        popup(

            "Tekst",

            result

        )



# ============================================================
# ANALIZA TEKSTU
# ============================================================


def tool_text_analyzer():


    text=simpledialog.askstring(

        "Analizator",

        "Tekst"

    )



    if text:


        result=f"""

Znaki:

{len(text)}


Słowa:

{len(text.split())}


Linie:

{len(text.splitlines())}

"""



        popup(

            "Analiza",

            result

        )



# ============================================================
# SCHOWEK
# ============================================================


def tool_clipboard():


    try:


        data=root.clipboard_get()



        popup(

            "Schowek",

            data

        )


    except:


        error(

            "Schowek pusty"

        )



# ============================================================
# CZYSZCZENIE TEMP
# ============================================================


def tool_clean_temp():


    temp=os.getenv(

        "TEMP"

    )



    count=0



    for item in os.listdir(temp):


        try:


            path=os.path.join(

                temp,

                item

            )


            if os.path.isdir(path):


                shutil.rmtree(

                    path

                )

            else:


                os.remove(

                    path

                )


            count+=1



        except:

            pass



    popup(

        "Cleaner",

        f"Usunięto: {count}"

    )



# ============================================================
# CACHE WINDOWS
# ============================================================


def tool_clean_cache():


    commands=[

        "ipconfig /flushdns",

        "cleanmgr"

    ]



    for cmd in commands:


        run_command(

            cmd

        )



    popup(

        "Cache",

        "Wyczyszczono"

    )



# ============================================================
# INFORMACJE FOLDERU
# ============================================================


def tool_folder_info():


    folder=choose_folder()



    if not folder:

        return



    files=0

    size=0



    for root_dir,dirs,fs in os.walk(folder):


        for f in fs:


            files+=1


            try:


                size+=os.path.getsize(

                    os.path.join(

                        root_dir,

                        f

                    )

                )

            except:

                pass



    popup(

        "Folder",

        f"""

Pliki:

{files}


Rozmiar:

{round(size/1024/1024,2)} MB

"""

    )



# ============================================================
# KAFELKI TOOLS
# ============================================================


tools_buttons=[


("🆔 UUID",tool_uuid),

("🔑 GUID",tool_guid),

("# MD5",tool_md5),

("# SHA1",tool_sha1),

("# SHA256",tool_sha256),

("⚖ Porównaj hash",tool_compare_hash),

("🔒 Szyfruj plik",tool_encrypt_file),

("🎲 Token",tool_token),

("🎯 Random",tool_random_data),

("🔤 Base64 Encode",tool_base64_encode),

("🔡 Base64 Decode",tool_base64_decode),

("📊 Analizator tekstu",tool_text_analyzer),

("📋 Schowek",tool_clipboard),

("🧹 Temp Cleaner",tool_clean_temp),

("⚡ Cache Cleaner",tool_clean_cache),

("📁 Info folderu",tool_folder_info)

]



row=0
col=0


for text,cmd in tools_buttons:


    add_button(

        tab_tools,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 10 — DEVELOPER MODE
# ============================================================


import subprocess
import re



# ============================================================
# EDYTOR PYTHON
# ============================================================


def dev_editor():


    window=tk.Toplevel(

        root

    )


    window.title(

        t("Python Editor")

    )


    window.geometry(

        "800x600"

    )


    text=tk.Text(

        window,

        font=(

            "Consolas",

            12

        )

    )


    text.pack(

        expand=True,

        fill="both"

    )



    def save():


        file=filedialog.asksaveasfilename(

            defaultextension=".py"

        )


        if file:


            with open(

                file,

                "w",

                encoding="utf-8"

            ) as f:


                f.write(

                    text.get(

                        "1.0",

                        tk.END

                    )

                )



            popup(

                "Editor",

                "Zapisano"

            )



    ttk.Button(

        window,

        text=t("💾 Zapisz"),

        command=save,

        style="Tool.TButton"

    ).pack()



# ============================================================
# URUCHAMIANIE PYTHON
# ============================================================


def dev_run_python():


    file=choose_file()



    if not file:

        return



    result=run_command(

        f"python {file}"

    )



    toolkit_text_window(

        "Python Output",

        result

    )



# ============================================================
# TERMINAL GUI
# ============================================================


def dev_terminal():


    window=tk.Toplevel(

        root

    )


    window.title(

        t("Terminal")

    )


    window.geometry(

        "800x500"

    )


    output=tk.Text(

        window

    )


    output.pack(

        expand=True,

        fill="both"

    )


    entry=ttk.Entry(

        window

    )


    entry.pack(

        fill="x"

    )



    def execute():


        cmd=entry.get()


        result=run_command(

            cmd

        )


        output.insert(

            tk.END,

            result+"\n"

        )


        entry.delete(

            0,

            tk.END

        )



    ttk.Button(

        window,

        text=t("▶ Wykonaj"),

        command=execute,

        style="Tool.TButton"

    ).pack()



# ============================================================
# PIP INSTALL
# ============================================================


def dev_pip_install():


    package=simpledialog.askstring(

        "pip",

        "Nazwa pakietu"

    )



    if package:


        result=run_command(

            f"pip install {package}"

        )


        toolkit_text_window(

            "pip",

            result

        )



# ============================================================
# LISTA PAKIETÓW
# ============================================================


def dev_pip_list():


    result=run_command(

        "pip list"

    )


    toolkit_text_window(

        "Pakiety",

        result

    )



# ============================================================
# GENERATOR PROJEKTU
# ============================================================


def dev_project_generator():


    folder=filedialog.askdirectory()



    if not folder:

        return



    name=simpledialog.askstring(

        "Projekt",

        "Nazwa"

    )



    if not name:

        return



    path=os.path.join(

        folder,

        name

    )



    os.makedirs(

        path,

        exist_ok=True

    )



    files=[

        "main.py",

        "README.md",

        ".gitignore"

    ]



    for file in files:


        open(

            os.path.join(

                path,

                file

            ),

            "w"

        ).close()



    popup(

        "Projekt",

        "Utworzono"

    )



# ============================================================
# JSON VALIDATOR
# ============================================================


def dev_json_check():


    file=choose_file()



    if not file:

        return



    try:


        with open(

            file,

            encoding="utf-8"

        ) as f:


            json.load(

                f

            )



        popup(

            "JSON",

            "Poprawny"

        )


    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# JSON FORMAT
# ============================================================


def dev_json_format():


    file=choose_file()



    if not file:

        return



    with open(

        file,

        encoding="utf-8"

    ) as f:


        data=json.load(

            f

        )



    with open(

        file,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )


    popup(

        "JSON",

        "Sformatowano"

    )



# ============================================================
# REGEX TESTER
# ============================================================


def dev_regex():


    pattern=simpledialog.askstring(

        "Regex",

        "Wyrażenie"

    )


    text=simpledialog.askstring(

        "Tekst",

        "Tekst"

    )



    if pattern and text:


        result=re.findall(

            pattern,

            text

        )


        popup(

            "Regex",

            str(result)

        )



# ============================================================
# ENV
# ============================================================


def dev_environment():


    text=""


    for key,value in os.environ.items():


        text+=f"{key}={value}\n"



    toolkit_text_window(

        "Environment",

        text

    )



# ============================================================
# PYTHON INFO
# ============================================================


def dev_python_info():


    text=f"""

Python:

{platform.python_version()}


Interpreter:

{sys.executable}


System:

{platform.platform()}

"""


    popup(

        "Python",

        text

    )



# ============================================================
# GITIGNORE
# ============================================================


def dev_gitignore():


    file=filedialog.asksaveasfilename(

        defaultextension=".gitignore"

    )



    if file:


        with open(

            file,

            "w"

        ) as f:


            f.write(

"""__pycache__/
*.pyc
.env
.vscode/
"""

            )


        popup(

            "Git",

            "Utworzono"

        )



# ============================================================
# README
# ============================================================


def dev_readme():


    file=filedialog.asksaveasfilename(

        defaultextension=".md"

    )


    if file:


        with open(

            file,

            "w"

        ) as f:


            f.write(

"# Projekt\n\nOpis projektu"

            )


        popup(

            "README",

            "Gotowe"

        )



# ============================================================
# KAFELKI DEVELOPER
# ============================================================


developer_buttons=[


("📝 Edytor Python",dev_editor),

("▶ Uruchom Python",dev_run_python),

("💻 Terminal",dev_terminal),

("📦 pip install",dev_pip_install),

("📚 pip list",dev_pip_list),

("🏗 Generator projektu",dev_project_generator),

("✔ JSON Check",dev_json_check),

("✨ JSON Format",dev_json_format),

("🔎 Regex",dev_regex),

("🌐 ENV",dev_environment),

("🐍 Python Info",dev_python_info),

("📄 .gitignore",dev_gitignore),

("📘 README",dev_readme)

]



row=0
col=0


for text,cmd in developer_buttons:


    add_button(

        tab_developer,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 11 — HARDWARE MONITOR PRO
# ============================================================


import threading



# ============================================================
# CPU LIVE MONITOR
# ============================================================


def hardware_cpu_monitor():


    window=tk.Toplevel(

        root

    )


    window.title(

        t("CPU Monitor")

    )


    window.geometry(

        "500x300"

    )



    label=ttk.Label(

        window,

        font=(

            "Arial",

            20

        )

    )


    label.pack(

        expand=True

    )



    running=True



    def update():


        if not running:

            return



        if psutil:


            cpu=psutil.cpu_percent(

                interval=1

            )


            label.config(

                text=f"CPU\n{cpu}%"

            )



        window.after(

            1000,

            update

        )



    def close():


        nonlocal running


        running=False


        window.destroy()



    window.protocol(

        "WM_DELETE_WINDOW",

        close

    )



    update()



# ============================================================
# RAM MONITOR
# ============================================================


def hardware_ram_monitor():


    if not psutil:

        return



    ram=psutil.virtual_memory()



    popup(

        "RAM",

        f"""

Użycie:

{ram.percent}%


Całość:

{round(ram.total/1024**3,2)} GB


Wolne:

{round(ram.available/1024**3,2)} GB

"""

    )



# ============================================================
# TEMPERATURA
# ============================================================


def hardware_temperature():


    if not psutil:

        return



    try:


        temps=psutil.sensors_temperatures()



        text=""


        for name,data in temps.items():


            text+=name+"\n"


            for item in data:


                text+=str(item)+"\n"



        toolkit_text_window(

            "Temperatury",

            text

        )



    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# WENTYLATORY
# ============================================================


def hardware_fans():


    if not psutil:

        return



    try:


        fans=psutil.sensors_fans()


        toolkit_text_window(

            "Wentylatory",

            str(fans)

        )


    except:


        error(

            "Brak danych"

        )



# ============================================================
# BATERIA
# ============================================================


def hardware_battery():


    if not psutil:

        return



    battery=psutil.sensors_battery()



    if battery:


        popup(

            "Bateria",

            f"""

Poziom:

{battery.percent}%


Ładowanie:

{battery.power_plugged}

"""

        )


    else:


        popup(

            "Bateria",

            "Brak baterii"

        )



# ============================================================
# GPU
# ============================================================


def hardware_gpu():


    result=run_command(

        "wmic path win32_VideoController get name"

    )


    toolkit_text_window(

        "GPU",

        result

    )



# ============================================================
# DYSKI
# ============================================================


def hardware_physical_disks():


    result=run_command(

        "wmic diskdrive get model,size"

    )


    toolkit_text_window(

        "Dyski",

        result

    )



# ============================================================
# SMART
# ============================================================


def hardware_smart():


    result=run_command(

        "wmic diskdrive get status"

    )


    popup(

        "SMART",

        result

    )



# ============================================================
# BENCH CPU
# ============================================================


def hardware_cpu_benchmark():


    start=time.time()



    total=0


    for i in range(

        10000000

    ):


        total+=i*i



    end=time.time()



    popup(

        "CPU Benchmark",

        f"Czas:\n{round(end-start,3)}s"

    )



# ============================================================
# BENCH RAM
# ============================================================


def hardware_ram_benchmark():


    start=time.time()



    data=[0]*10000000



    end=time.time()



    size=len(data)



    popup(

        "RAM Benchmark",

        f"""

Elementy:

{size}


Czas:

{round(end-start,3)}s

"""

    )



# ============================================================
# CPU STRESS
# ============================================================


def hardware_cpu_load():


    def load():


        while True:


            x=0


            for i in range(

                1000000

            ):

                x+=i*i



    threading.Thread(

        target=load,

        daemon=True

    ).start()



    popup(

        "Stress",

        "Uruchomiono test CPU"

    )



# ============================================================
# USB
# ============================================================


def hardware_usb():


    result=run_command(

        "wmic path Win32_USBControllerDevice"

    )


    toolkit_text_window(

        "USB",

        result

    )



# ============================================================
# BIOS
# ============================================================


def hardware_bios():


    result=run_command(

        "wmic bios get manufacturer,version"

    )


    popup(

        "BIOS",

        result

    )



# ============================================================
# PŁYTA GŁÓWNA
# ============================================================


def hardware_motherboard():


    result=run_command(

        "wmic baseboard get product,manufacturer"

    )


    popup(

        "Płyta",

        result

    )



# ============================================================
# KAFELKI HARDWARE
# ============================================================


hardware_buttons=[


("⚡ CPU Live",hardware_cpu_monitor),

("🧠 RAM",hardware_ram_monitor),

("🌡 Temperatury",hardware_temperature),

("🌀 Wentylatory",hardware_fans),

("🔋 Bateria",hardware_battery),

("🎮 GPU",hardware_gpu),

("💽 Dyski",hardware_physical_disks),

("❤️ SMART",hardware_smart),

("🏁 CPU Test",hardware_cpu_benchmark),

("🏁 RAM Test",hardware_ram_benchmark),

("🔥 CPU Stress",hardware_cpu_load),

("🔌 USB",hardware_usb),

("⚙ BIOS",hardware_bios),

("🖥 Płyta",hardware_motherboard)

]



row=0
col=0


for text,cmd in hardware_buttons:


    add_button(

        tab_hardware,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 12 — SYSTEM CLEANER PRO
# ============================================================


import glob



# ============================================================
# ANALIZA DYSKU
# ============================================================


def cleaner_disk_usage():


    if not psutil:

        return



    text=""


    for disk in psutil.disk_partitions():


        try:


            usage=psutil.disk_usage(

                disk.mountpoint

            )


            text+=f"""

Dysk:

{disk.device}


Całość:

{round(usage.total/1024**3,2)} GB


Zajęte:

{usage.percent}%


Wolne:

{round(usage.free/1024**3,2)} GB


-------------------

"""



        except:

            pass



    toolkit_text_window(

        "Analiza dysku",

        text

    )



# ============================================================
# DUŻE PLIKI
# ============================================================


def cleaner_big_files():


    folder=choose_folder()



    if not folder:

        return



    limit=simpledialog.askinteger(

        "Rozmiar",

        "Minimum MB"

    )



    if not limit:

        return



    result=""


    for root_dir,dirs,files in os.walk(folder):


        for file in files:


            try:


                path=os.path.join(

                    root_dir,

                    file

                )


                size=os.path.getsize(

                    path

                )



                if size > limit*1024*1024:


                    result+=f"""

{path}

{round(size/1024/1024,2)} MB


"""



            except:

                pass



    toolkit_text_window(

        "Duże pliki",

        result

    )



# ============================================================
# DUPLIKATY
# ============================================================


def cleaner_duplicates():


    folder=choose_folder()



    if not folder:

        return



    hashes={}

    duplicates=""


    for root_dir,dirs,files in os.walk(folder):


        for file in files:


            try:


                path=os.path.join(

                    root_dir,

                    file

                )


                h=hashlib.md5()



                with open(

                    path,

                    "rb"

                ) as f:


                    h.update(

                        f.read()

                    )



                value=h.hexdigest()



                if value in hashes:


                    duplicates+=f"""

DUPE:

{path}


ORYGINAŁ:

{hashes[value]}



"""


                else:


                    hashes[value]=path



            except:

                pass



    if not duplicates:


        duplicates="Brak duplikatów"



    toolkit_text_window(

        "Duplikaty",

        duplicates

    )



# ============================================================
# TEMP CLEAN
# ============================================================


def cleaner_temp():


    folders=[

        os.getenv("TEMP"),

        os.path.join(

            os.getenv("WINDIR"),

            "Temp"

        )

    ]



    count=0



    for folder in folders:


        if not folder:

            continue



        for item in glob.glob(

            folder+"\\*"

        ):


            try:


                if os.path.isdir(item):


                    shutil.rmtree(

                        item

                    )

                else:


                    os.remove(

                        item

                    )



                count+=1



            except:

                pass



    popup(

        "Cleaner",

        f"Usunięto: {count}"

    )



# ============================================================
# CACHE PRZEGLĄDAREK
# ============================================================


def cleaner_browser_cache():


    paths=[

        os.path.expanduser(

            "~/AppData/Local/Google/Chrome/User Data/Default/Cache"

        ),

        os.path.expanduser(

            "~/AppData/Local/Microsoft/Edge/User Data/Default/Cache"

        )

    ]



    count=0



    for path in paths:


        if os.path.exists(path):


            try:


                shutil.rmtree(

                    path

                )

                count+=1



            except:

                pass



    popup(

        "Cache",

        f"Usunięto: {count}"

    )



# ============================================================
# MINIATURY WINDOWS
# ============================================================


def cleaner_thumbnails():


    path=os.path.expanduser(

        "~/AppData/Local/Microsoft/Windows/Explorer"

    )


    count=0



    for file in glob.glob(

        path+"\\thumbcache*"

    ):


        try:


            os.remove(

                file

            )

            count+=1



        except:

            pass



    popup(

        "Miniatury",

        f"Usunięto: {count}"

    )



# ============================================================
# AUTOSTART
# ============================================================


def cleaner_startup():


    result=run_command(

        "wmic startup get caption,command"

    )


    toolkit_text_window(

        "Autostart",

        result

    )



# ============================================================
# USŁUGI
# ============================================================


def cleaner_services():


    result=run_command(

        "sc query"

    )


    toolkit_text_window(

        "Usługi",

        result

    )



# ============================================================
# APLIKACJE
# ============================================================


def cleaner_apps():


    result=run_command(

        "wmic product get name"

    )


    toolkit_text_window(

        "Programy",

        result

    )



# ============================================================
# LOGI WINDOWS
# ============================================================


def cleaner_logs():


    path=os.path.join(

        os.getenv("WINDIR"),

        "Logs"

    )


    try:


        shutil.rmtree(

            path

        )


        popup(

            "Logi",

            "Usunięto"

        )


    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# KOSZ
# ============================================================


def cleaner_recycle_bin():


    run_command(

        "PowerShell Clear-RecycleBin -Force"

    )


    popup(

        "Kosz",

        "Wyczyszczono"

    )



# ============================================================
# RAPORT
# ============================================================


def cleaner_report():


    text=""


    text+="ToolKit Cleaner Report\n\n"


    text+=run_command(

        "systeminfo"

    )



    toolkit_text_window(

        "Raport",

        text

    )



# ============================================================
# KAFELKI CLEANER
# ============================================================


cleaner_buttons=[


("💽 Analiza dysku",cleaner_disk_usage),

("📦 Duże pliki",cleaner_big_files),

("♻ Duplikaty",cleaner_duplicates),

("🧹 TEMP",cleaner_temp),

("🌐 Cache przeglądarek",cleaner_browser_cache),

("🖼 Miniatury",cleaner_thumbnails),

("🚀 Autostart",cleaner_startup),

("⚙ Usługi",cleaner_services),

("📦 Programy",cleaner_apps),

("📜 Logi",cleaner_logs),

("🗑 Kosz",cleaner_recycle_bin),

("📑 Raport",cleaner_report)

]



row=0
col=0


for text,cmd in cleaner_buttons:


    add_button(

        tab_cleaner,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 13 — WINDOWS MANAGEMENT PRO
# ============================================================


# ============================================================
# MENEDŻER PROCESÓW
# ============================================================


def win_process_manager():


    if not psutil:

        error(

            "Brak psutil"

        )

        return



    window=tk.Toplevel(

        root

    )


    window.title(

        t("Procesy Windows")

    )


    window.geometry(

        "700x500"

    )



    box=tk.Listbox(

        window,

        width=90

    )


    box.pack(

        expand=True,

        fill="both"

    )



    for p in psutil.process_iter(

        [

            "pid",

            "name",

            "cpu_percent",

            "memory_percent"

        ]

    ):


        try:


            info=p.info



            box.insert(

                tk.END,

                f"{info['pid']} | {info['name']} | CPU {info['cpu_percent']}%"

            )



        except:

            pass



# ============================================================
# ZABIJANIE PROCESU
# ============================================================


def win_kill_process():


    pid=simpledialog.askinteger(

        "Proces",

        "PID"

    )



    if not pid:

        return



    try:


        os.kill(

            pid,

            9

        )


        popup(

            "Proces",

            "Zakończono"

        )



    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# USŁUGI
# ============================================================


def win_services():


    result=run_command(

        "sc query type= service"

    )


    toolkit_text_window(

        "Usługi",

        result

    )



# ============================================================
# START USŁUGI
# ============================================================


def win_start_service():


    service=simpledialog.askstring(

        "Usługa",

        "Nazwa"

    )



    if service:


        result=run_command(

            f"net start {service}"

        )


        popup(

            "Start",

            result

        )



# ============================================================
# STOP USŁUGI
# ============================================================


def win_stop_service():


    service=simpledialog.askstring(

        "Usługa",

        "Nazwa"

    )



    if service:


        result=run_command(

            f"net stop {service}"

        )


        popup(

            "Stop",

            result

        )



# ============================================================
# STEROWNIKI
# ============================================================


def win_drivers():


    result=run_command(

        "driverquery"

    )


    toolkit_text_window(

        "Sterowniki",

        result

    )



# ============================================================
# URZĄDZENIA
# ============================================================


def win_devices():


    result=run_command(

        "pnputil /enum-devices"

    )


    toolkit_text_window(

        "Urządzenia",

        result

    )



# ============================================================
# MENEDŻER URZĄDZEŃ
# ============================================================


def win_device_manager():


    run_command(

        "start devmgmt.msc"

    )



# ============================================================
# ENVIRONMENT
# ============================================================


def win_environment():


    text=""


    for key,value in os.environ.items():


        text+=f"""

{key}

{value}


"""


    toolkit_text_window(

        "Zmienne",

        text

    )



# ============================================================
# PATH
# ============================================================


def win_path():


    path=os.environ.get(

        "PATH"

    )


    toolkit_text_window(

        "PATH",

        path

    )



# ============================================================
# LICENCJA WINDOWS
# ============================================================


def win_license():


    result=run_command(

        "slmgr /dli"

    )


    popup(

        "Licencja",

        result

    )



# ============================================================
# AKTYWACJA
# ============================================================


def win_activation():


    result=run_command(

        "slmgr /xpr"

    )


    popup(

        "Aktywacja",

        result

    )



# ============================================================
# POLITYKI
# ============================================================


def win_policy():


    result=run_command(

        "gpresult /r"

    )


    toolkit_text_window(

        "Polityki",

        result

    )



# ============================================================
# KONTO
# ============================================================


def win_account():


    result=run_command(

        "whoami /all"

    )


    toolkit_text_window(

        "Konto",

        result

    )



# ============================================================
# HISTORIA SYSTEMU
# ============================================================


def win_history():


    result=run_command(

        "systeminfo"

    )


    toolkit_text_window(

        "Historia",

        result

    )



# ============================================================
# KAFELKI WINDOWS
# ============================================================


windows_buttons=[


("📋 Procesy",win_process_manager),

("❌ Zabij proces",win_kill_process),

("⚙ Usługi",win_services),

("▶ Start usługi",win_start_service),

("⏹ Stop usługi",win_stop_service),

("🔧 Sterowniki",win_drivers),

("🖥 Urządzenia",win_devices),

("🛠 Device Manager",win_device_manager),

("🌐 Zmienne",win_environment),

("🔗 PATH",win_path),

("🔑 Licencja",win_license),

("✅ Aktywacja",win_activation),

("📜 Polityki",win_policy),

("👤 Konto",win_account),

("📊 System Info",win_history)

]



row=0
col=0


for text,cmd in windows_buttons:


    add_button(

        tab_windows,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 14 — REMOTE & ADMIN TOOLS
# ============================================================


import ipaddress
import subprocess



# ============================================================
# PING HOSTA
# ============================================================


def remote_ping_host():


    host=simpledialog.askstring(

        "Ping",

        "Adres IP / Host"

    )



    if not host:

        return



    result=run_command(

        f"ping {host}"

    )


    toolkit_text_window(

        "Ping",

        result

    )



# ============================================================
# SKAN SIECI LOKALNEJ
# ============================================================


def remote_network_scan():


    network=simpledialog.askstring(

        "Sieć",

        "Zakres np. 192.168.1.0/24"

    )



    if not network:

        return



    result=""


    try:


        net=ipaddress.ip_network(

            network,

            strict=False

        )


        for ip in net.hosts():


            response=subprocess.call(

                [

                    "ping",

                    "-n",

                    "1",

                    str(ip)

                ],

                stdout=subprocess.DEVNULL

            )



            if response==0:


                result+=f"{ip} ONLINE\n"



    except Exception as e:


        result=str(e)



    toolkit_text_window(

        "Skan sieci",

        result

    )



# ============================================================
# WAKE ON LAN
# ============================================================


def remote_wol():


    mac=simpledialog.askstring(

        "Wake On LAN",

        "MAC"

    )



    if not mac:

        return



    mac=mac.replace(

        "-",

        ""

    ).replace(

        ":",

        ""

    )



    if len(mac)!=12:


        error(

            "Niepoprawny MAC"

        )

        return



    packet=bytes.fromhex(

        "FF"*6 + mac*16

    )



    import socket as sock



    s=sock.socket(

        sock.AF_INET,

        sock.SOCK_DGRAM

    )


    s.setsockopt(

        sock.SOL_SOCKET,

        sock.SO_BROADCAST,

        1

    )



    s.sendto(

        packet,

        (

            "<broadcast>",

            9

        )

    )



    popup(

        "Wake ON LAN",

        "Pakiet wysłany"

    )



# ============================================================
# GENERATOR MAC
# ============================================================


def remote_mac_generator():


    mac=":".join(

        "%02x"%random.randint(

            0,

            255

        )

        for _ in range(6)

    )


    popup(

        "MAC",

        mac

    )



# ============================================================
# GENERATOR IP
# ============================================================


def remote_ip_generator():


    ip=".".join(

        str(

            random.randint(

                0,

                255

            )

        )

        for _ in range(4)

    )


    popup(

        "IP",

        ip

    )



# ============================================================
# SSH
# ============================================================


def remote_ssh():


    host=simpledialog.askstring(

        "SSH",

        "Host"

    )


    if host:


        os.system(

            f"start ssh {host}"

        )



# ============================================================
# RDP
# ============================================================


def remote_rdp():


    host=simpledialog.askstring(

        "RDP",

        "Adres"

    )


    if host:


        os.system(

            f"mstsc /v:{host}"

        )



# ============================================================
# PORT CHECK
# ============================================================


def remote_port_scan():


    host=simpledialog.askstring(

        "Host",

        "Adres"

    )


    if not host:

        return



    ports=[

        21,

        22,

        23,

        25,

        53,

        80,

        443,

        3389

    ]



    result=""


    for port in ports:


        s=socket.socket()


        s.settimeout(

            0.5

        )


        if s.connect_ex(

            (

                host,

                port

            )

        )==0:


            result+=f"{port} OPEN\n"



        s.close()



    toolkit_text_window(

        "Porty",

        result

    )



# ============================================================
# DNS LOOKUP
# ============================================================


def remote_dns():


    host=simpledialog.askstring(

        "DNS",

        "Host"

    )


    if host:


        try:


            ip=socket.gethostbyname(

                host

            )


            popup(

                "DNS",

                ip

            )


        except Exception as e:


            error(

                str(e)

            )



# ============================================================
# REVERSE DNS
# ============================================================


def remote_reverse_dns():


    ip=simpledialog.askstring(

        "Reverse DNS",

        "IP"

    )


    if ip:


        try:


            name=socket.gethostbyaddr(

                ip

            )


            popup(

                "Reverse DNS",

                str(name)

            )


        except Exception as e:


            error(

                str(e)

            )



# ============================================================
# TRACEROUTE
# ============================================================


def remote_trace():


    host=simpledialog.askstring(

        "Traceroute",

        "Host"

    )


    if host:


        result=run_command(

            f"tracert {host}"

        )


        toolkit_text_window(

            "Traceroute",

            result

        )



# ============================================================
# NETSTAT
# ============================================================


def remote_netstat():


    result=run_command(

        "netstat -ano"

    )


    toolkit_text_window(

        "Netstat",

        result

    )



# ============================================================
# ARP
# ============================================================


def remote_arp():


    result=run_command(

        "arp -a"

    )


    toolkit_text_window(

        "ARP",

        result

    )



# ============================================================
# RAPORT SIECI
# ============================================================


def remote_network_report():


    text=""


    text+="HOST:\n"

    text+=run_command(

        "hostname"

    )


    text+="\n\nIPCONFIG:\n"

    text+=run_command(

        "ipconfig"

    )


    text+="\n\nNETSTAT:\n"

    text+=run_command(

        "netstat -ano"

    )



    toolkit_text_window(

        "Raport",

        text

    )



# ============================================================
# SKRYPT ADMIN
# ============================================================


def remote_script_generator():


    file=filedialog.asksaveasfilename(

        defaultextension=".bat"

    )


    if file:


        with open(

            file,

            "w"

        ) as f:


            f.write(

"""@echo off
echo ToolKit Admin Script
systeminfo
pause
"""

            )


        popup(

            "Script",

            "Utworzono"

        )



# ============================================================
# KAFELKI REMOTE
# ============================================================


remote_buttons=[


("📡 Ping Host",remote_ping_host),

("🔎 Skan sieci",remote_network_scan),

("⚡ Wake LAN",remote_wol),

("🔢 Generator MAC",remote_mac_generator),

("🌐 Generator IP",remote_ip_generator),

("🔐 SSH",remote_ssh),

("🖥 RDP",remote_rdp),

("🔌 Port Scan",remote_port_scan),

("🌍 DNS",remote_dns),

("↩ Reverse DNS",remote_reverse_dns),

("🛰 Traceroute",remote_trace),

("📊 Netstat",remote_netstat),

("📋 ARP",remote_arp),

("📄 Raport sieci",remote_network_report),

("⚙ Skrypt Admin",remote_script_generator)

]


row=0
col=0


for text,cmd in remote_buttons:


    add_button(

        tab_remote,

        text,

        cmd,

        row,

        col

    )


    col+=1


    if col==4:

        col=0

        row+=1

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 15 — SECURITY CENTER PRO
# ============================================================


import secrets



# ============================================================
# HASH PLIKU
# ============================================================


def security_hash_file():


    file=choose_file()



    if not file:

        return



    sha256=hashlib.sha256()

    md5=hashlib.md5()

    sha1=hashlib.sha1()



    with open(

        file,

        "rb"

    ) as f:


        while True:


            data=f.read(

                4096

            )


            if not data:

                break



            sha256.update(

                data

            )


            md5.update(

                data

            )


            sha1.update(

                data

            )



    popup(

        "Hash",

        f"""

MD5:

{md5.hexdigest()}


SHA1:

{sha1.hexdigest()}


SHA256:

{sha256.hexdigest()}

"""

    )



# ============================================================
# PORÓWNYWANIE HASHY
# ============================================================


def security_compare_hash():


    first=simpledialog.askstring(

        "Hash",

        "Pierwszy hash"

    )


    second=simpledialog.askstring(

        "Hash",

        "Drugi hash"

    )



    if first and second:


        if first==second:


            popup(

                "Hash",

                "Takie same"

            )


        else:


            popup(

                "Hash",

                "Różne"

            )



# ============================================================
# INTEGRITY CHECK
# ============================================================


def security_integrity_scan():


    folder=choose_folder()



    if not folder:

        return



    database={}



    for root_dir,dirs,files in os.walk(folder):


        for file in files:


            try:


                path=os.path.join(

                    root_dir,

                    file

                )


                h=hashlib.sha256()



                with open(

                    path,

                    "rb"

                ) as f:


                    h.update(

                        f.read()

                    )



                database[path]=h.hexdigest()



            except:

                pass



    save=filedialog.asksaveasfilename(

        defaultextension=".json"

    )



    if save:


        with open(

            save,

            "w"

        ) as f:


            json.dump(

                database,

                f,

                indent=4

            )



    popup(

        "Integralność",

        "Utworzono bazę"

    )



# ============================================================
# MONITOR ZMIAN
# ============================================================


def security_file_monitor():


    folder=choose_folder()



    if not folder:

        return



    before=set()



    for root_dir,dirs,files in os.walk(folder):


        for file in files:


            before.add(

                os.path.join(

                    root_dir,

                    file

                )

            )



    time.sleep(

        5

    )



    after=set()



    for root_dir,dirs,files in os.walk(folder):


        for file in files:


            after.add(

                os.path.join(

                    root_dir,

                    file

                )

            )



    added=after-before

    removed=before-after



    toolkit_text_window(

        "Zmiany",

        f"""

Dodane:

{added}


Usunięte:

{removed}

"""

    )



# ============================================================
# UPRAWNIENIA
# ============================================================


def security_permissions():


    file=choose_file()



    if file:


        result=run_command(

            f"icacls \"{file}\""

        )


        toolkit_text_window(

            "Uprawnienia",

            result

        )



# ============================================================
# UŻYTKOWNICY
# ============================================================


def security_users():


    result=run_command(

        "net user"

    )


    toolkit_text_window(

        "Użytkownicy",

        result

    )



# ============================================================
# GRUPY
# ============================================================


def security_groups():


    result=run_command(

        "net localgroup"

    )


    toolkit_text_window(

        "Grupy",

        result

    )



# ============================================================
# POŁĄCZENIA
# ============================================================


def security_connections():


    result=run_command(

        "netstat -ano"

    )


    toolkit_text_window(

        "Połączenia",

        result

    )



# ============================================================
# OTWARTE PORTY
# ============================================================


def security_ports():


    result=run_command(

        "netstat -an"

    )


    toolkit_text_window(

        "Porty",

        result

    )



# ============================================================
# FIREWALL STATUS
# ============================================================


def security_firewall():


    result=run_command(

        "netsh advfirewall show allprofiles"

    )


    toolkit_text_window(

        "Firewall",

        result

    )



# ============================================================
# DEFENDER
# ============================================================


def security_defender():


    result=run_command(

        "powershell Get-MpComputerStatus"

    )


    toolkit_text_window(

        "Defender",

        result

    )



# ============================================================
# LOGI
# ============================================================


def security_logs():


    result=run_command(

        "wevtutil el"

    )


    toolkit_text_window(

        "Logi",

        result

    )



# ============================================================
# RAPORT
# ============================================================


def security_report():


    text=""


    text+="SECURITY REPORT\n\n"


    text+=run_command(

        "whoami"

    )


    text+="\n\n"


    text+=run_command(

        "netstat -ano"

    )


    text+="\n\n"


    text+=run_command(

        "systeminfo"

    )



    toolkit_text_window(

        "Raport bezpieczeństwa",

        text

    )



# ============================================================
# TOKEN
# ============================================================


def security_token():


    token=secrets.token_hex(

        32

    )


    popup(

        "Token",

        token

    )



# ============================================================
# KAFELKI SECURITY
# ============================================================


security_buttons = [
    ("🔑 Hash pliku", security_hash_file),
    ("⚖ Porównaj hash", security_compare_hash),
    ("🧬 Integralność", security_integrity_scan),
    ("👁 Monitor zmian", security_file_monitor),
    ("🔐 Uprawnienia", security_permissions),
    ("👤 Użytkownicy", security_users),
    ("👥 Grupy", security_groups),
    ("🌐 Połączenia", security_connections),
    ("🔌 Porty", security_ports),
    ("🔥 Firewall", security_firewall),
    ("🛡 Defender", security_defender),
    ("📜 Logi", security_logs),
    ("📄 Raport", security_report),
    ("🎲 Token", security_token),
]

for index, (text, command) in enumerate(security_buttons):
    add_button(
        tab_security,
        text,
        command,
        index // 4,
        index % 4,
    )

# ============================================================
# ToolKit 2.0
# CZĘŚĆ 16 — 💾 BACKUP & RECOVERY PRO
# POPRAWIONA WERSJA
# ============================================================

import glob


BACKUP_FOLDER = "ToolKit_Backups"



# ============================================================
# UTWORZENIE FOLDERU BACKUP
# ============================================================

def backup_create_folder():

    try:

        os.makedirs(
            BACKUP_FOLDER,
            exist_ok=True
        )

        popup(
            "Backup",
            "Folder backup został utworzony."
        )

    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# KOPIA FOLDERU
# ============================================================

def backup_copy_folder():

    source = choose_folder()

    if not source:
        return


    destination = choose_folder()

    if not destination:
        return


    name = os.path.basename(source)

    target = os.path.join(
        destination,
        name + "_backup"
    )


    try:

        shutil.copytree(
            source,
            target,
            dirs_exist_ok=True
        )


        popup(
            "Backup",
            "Kopia folderu wykonana."
        )


    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# BACKUP ZIP
# ============================================================

def backup_create_zip():

    folder = choose_folder()

    if not folder:
        return


    output = filedialog.asksaveasfilename(
        defaultextension=".zip"
    )


    if not output:
        return


    try:

        with zipfile.ZipFile(
            output,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archive:


            for root_dir, dirs, files in os.walk(folder):

                for file in files:

                    path = os.path.join(
                        root_dir,
                        file
                    )

                    archive.write(
                        path,
                        os.path.relpath(
                            path,
                            folder
                        )
                    )


        popup(
            "ZIP",
            "Backup ZIP utworzony."
        )


    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# ODZYSKIWANIE ZIP
# ============================================================

def backup_extract_zip():

    archive = choose_file()

    if not archive:
        return


    destination = choose_folder()

    if not destination:
        return


    try:

        with zipfile.ZipFile(
            archive,
            "r"
        ) as zip_file:


            zip_file.extractall(
                destination
            )


        popup(
            "Restore",
            "Pliki przywrócone."
        )


    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# SYNCHRONIZACJA
# ============================================================

def backup_sync_folder():

    source = choose_folder()

    if not source:
        return


    target = choose_folder()

    if not target:
        return


    copied = 0


    try:

        for root_dir, dirs, files in os.walk(source):

            for file in files:

                src = os.path.join(
                    root_dir,
                    file
                )


                relative = os.path.relpath(
                    src,
                    source
                )


                dst = os.path.join(
                    target,
                    relative
                )


                os.makedirs(
                    os.path.dirname(dst),
                    exist_ok=True
                )


                shutil.copy2(
                    src,
                    dst
                )


                copied += 1



        popup(
            "Synchronizacja",
            f"Skopiowano: {copied} plików"
        )


    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# LISTA BACKUPÓW
# ============================================================

def backup_show_list():

    if not os.path.exists(
        BACKUP_FOLDER
    ):

        popup(
            "Backup",
            "Brak folderu backup."
        )

        return


    files = os.listdir(
        BACKUP_FOLDER
    )


    if not files:

        files_text = "Brak kopii."

    else:

        files_text = "\n".join(files)


    popup(
        "Lista backupów",
        files_text
    )



# ============================================================
# USUWANIE STARYCH BACKUPÓW
# ============================================================

def backup_clean_old():

    folder = choose_folder()

    if not folder:
        return


    deleted = 0


    for file in glob.glob(
        folder + "/*"
    ):

        try:

            if os.path.isfile(file):

                os.remove(
                    file
                )

                deleted += 1


        except:

            pass


    popup(
        "Czyszczenie",
        f"Usunięto: {deleted}"
    )



# ============================================================
# EXPORT KONFIGURACJI
# ============================================================

def backup_export_config():

    output = filedialog.asksaveasfilename(
        defaultextension=".json"
    )


    if not output:
        return


    data = {

        "ToolKit":

        "2.0",

        "backup":

        str(datetime.datetime.now())

    }


    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            data,
            file,
            indent=4
        )


    popup(
        "Export",
        "Konfiguracja zapisana."
    )



# ============================================================
# TEST ZIP
# ============================================================

def backup_test_zip():

    file = choose_file()

    if not file:
        return


    try:

        with zipfile.ZipFile(
            file,
            "r"
        ) as archive:


            result = archive.testzip()



        popup(
            "ZIP Test",
            result if result else "Archiwum OK"
        )


    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# PRZYCISKI BACKUP
# ============================================================


backup_buttons = [
    ("📁 Utwórz folder backup", backup_create_folder),
    ("📂 Kopia folderu", backup_copy_folder),
    ("📦 Backup ZIP", backup_create_zip),
    ("📤 Przywróć ZIP", backup_extract_zip),
    ("🔄 Synchronizacja", backup_sync_folder),
    ("📋 Lista backupów", backup_show_list),
    ("🗑 Usuń stare kopie", backup_clean_old),
    ("⚙ Export konfiguracji", backup_export_config),
    ("🧪 Test ZIP", backup_test_zip),
]

for index, (text, command) in enumerate(backup_buttons):
    add_button(
        tab_backup,
        text,
        command,
        index // 4,
        index % 4,
    )

# ============================================================
# AUTOMATION CENTER PRO
# ============================================================


AUTOMATION_FILE = "automation_tasks.json"



# ============================================================
# OTWARCIE PROGRAMU
# ============================================================


def automation_open_program():

    file = filedialog.askopenfilename()

    if not file:
        return


    try:

        os.startfile(
            file
        )


    except Exception as e:

        error(
            str(e)
        )



# ============================================================
# OTWARCIE FOLDERU
# ============================================================


def automation_open_folder():

    folder = choose_folder()


    if folder:

        try:

            os.startfile(
                folder
            )


        except Exception as e:

            error(
                str(e)
            )



# ============================================================
# URUCHOM KOMENDĘ
# ============================================================


def automation_command():


    command = simpledialog.askstring(

        "Komenda",

        "Wpisz polecenie CMD:"

    )


    if not command:

        return



    try:

        result = subprocess.check_output(

            command,

            shell=True,

            stderr=subprocess.STDOUT

        ).decode(

            errors="ignore"

        )


        popup(

            "CMD",

            result

        )


    except Exception as e:

        error(

            str(e)

        )



# ============================================================
# INFORMACJE O PROCESIE
# ============================================================


def automation_run_script():


    file = filedialog.askopenfilename(

        filetypes=[

            (
                "Python",

                "*.py"

            )

        ]

    )


    if not file:

        return



    try:

        subprocess.Popen(

            [

                sys.executable,

                file

            ]

        )


        popup(

            "Python",

            "Skrypt uruchomiony."

        )


    except Exception as e:

        error(

            str(e)

        )



# ============================================================
# TIMER
# ============================================================


def automation_timer():


    seconds = simpledialog.askinteger(

        "Timer",

        "Sekundy:"

    )


    if not seconds:

        return



    def finish():

        popup(

            "Timer",

            "Czas zakończony."

        )



    root.after(

        seconds * 1000,

        finish

    )



# ============================================================
# ZAPIS ZADANIA
# ============================================================


def automation_save_task():


    name = simpledialog.askstring(

        "Zadanie",

        "Nazwa:"

    )


    command = simpledialog.askstring(

        "Zadanie",

        "Komenda:"

    )


    if not name or not command:

        return



    data = []



    if os.path.exists(

        AUTOMATION_FILE

    ):


        with open(

            AUTOMATION_FILE,

            encoding="utf-8"

        ) as file:

            data=json.load(file)



    data.append(

        {

            "name":

            name,

            "command":

            command

        }

    )



    with open(

        AUTOMATION_FILE,

        "w",

        encoding="utf-8"

    ) as file:


        json.dump(

            data,

            file,

            indent=4,

            ensure_ascii=False

        )



    popup(

        "Automatyzacja",

        "Zapisano zadanie."

    )



# ============================================================
# LISTA ZADAŃ
# ============================================================


def automation_tasks():


    if not os.path.exists(

        AUTOMATION_FILE

    ):

        popup(

            "Zadania",

            "Brak zapisanych."

        )

        return



    with open(

        AUTOMATION_FILE,

        encoding="utf-8"

    ) as file:


        data=json.load(file)



    text=""


    for item in data:


        text += (

            item["name"]

            +

            " -> "

            +

            item["command"]

            +

            "\n"

        )



    popup(

        "Zadania",

        text

    )



# ============================================================
# CZYSZCZENIE TEMP
# ============================================================


def automation_clean_temp():


    folders=[


        tempfile.gettempdir(),


        r"C:\Windows\Temp"


    ]



    count=0



    for folder in folders:


        try:


            for item in os.listdir(folder):


                path=os.path.join(

                    folder,

                    item

                )


                if os.path.isfile(path):


                    os.remove(

                        path

                    )

                    count+=1


        except:

            pass



    popup(

        "Cleaner",

        f"Usunięto: {count}"

    )



# ============================================================
# INFORMACJE O URUCHOMIONYM PYTHONIE
# ============================================================


def automation_python_info():


    text=f"""

Python:

{sys.version}


Interpreter:

{sys.executable}


Folder:

{os.getcwd()}

"""


    popup(

        "Python",

        text

    )



# ============================================================
# PRZYCISKI AUTOMATYZACJI
# ============================================================


automation_buttons=[


    (
        "▶ Uruchom program",
        automation_open_program
    ),


    (
        "📁 Otwórz folder",
        automation_open_folder
    ),


    (
        "⌨ Wykonaj CMD",
        automation_command
    ),


    (
        "🐍 Uruchom skrypt Python",
        automation_run_script
    ),


    (
        "⏱ Timer",
        automation_timer
    ),


    (
        "💾 Zapisz zadanie",
        automation_save_task
    ),


    (
        "📋 Lista zadań",
        automation_tasks
    ),


    (
        "🧹 Czyść TEMP",
        automation_clean_temp
    ),


    (
        "🐍 Informacje Python",
        automation_python_info
    )

]



for text, command in automation_buttons:


    btn = ttk.Button(

        tab_automation,

        text=t(text),

        command=command,

        style="Tool.TButton"

    )
    btn._orig_text = text
    translatable_buttons.append(btn)
    btn.pack(

        pady=5,

        padx=10,

        fill="x"

    )

# ============================================================
# MONITORING CENTER PRO
# ============================================================


MONITOR_REFRESH = 2000



# ============================================================
# CPU
# ============================================================


def monitor_cpu():


    if not psutil:

        error(
            "Brak biblioteki psutil"
        )

        return



    value = psutil.cpu_percent(
        interval=1
    )



    popup(

        "CPU",

        f"Użycie procesora:\n{value}%"

    )



# ============================================================
# RAM
# ============================================================


def monitor_ram():


    if not psutil:

        error(
            "Brak psutil"
        )

        return



    ram = psutil.virtual_memory()



    text=f"""

RAM:


Użycie:

{ram.percent}%


Całkowita:

{round(ram.total/1024**3,2)} GB


Dostępna:

{round(ram.available/1024**3,2)} GB

"""


    popup(

        "RAM",

        text

    )



# ============================================================
# DYSKI
# ============================================================


def monitor_disks():


    if not psutil:

        return



    text=""



    for disk in psutil.disk_partitions():


        try:


            usage = psutil.disk_usage(

                disk.mountpoint

            )


            text += f"""

Dysk:

{disk.device}


Zajęte:

{usage.percent}%


Wolne:

{round(usage.free/1024**3,2)} GB


-----------------

"""


        except:

            pass



    popup(

        "Dyski",

        text

    )



# ============================================================
# BATERIA
# ============================================================


def monitor_battery():


    if not psutil:

        return



    try:


        battery = psutil.sensors_battery()



        if battery:


            popup(

                "Bateria",

                f"""

Poziom:

{battery.percent}%


Ładowanie:

{battery.power_plugged}

"""

            )


        else:


            popup(

                "Bateria",

                "Brak baterii"

            )


    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# PROCESY
# ============================================================


def monitor_processes():


    if not psutil:

        return



    window=tk.Toplevel(

        root

    )


    window.title(

        t("Procesy")

    )


    window.geometry(

        "600x500"

    )



    box=tk.Listbox(

        window,

        width=80,

        height=25

    )


    box.pack(

        expand=True,

        fill="both"

    )



    for process in psutil.process_iter(

        [

            "pid",

            "name",

            "cpu_percent"

        ]

    ):


        try:


            box.insert(

                tk.END,

                f"{process.info['pid']} | {process.info['name']}"

            )


        except:

            pass



# ============================================================
# SIEĆ
# ============================================================


def monitor_network():


    if not psutil:

        return



    connections = psutil.net_connections()



    popup(

        "Sieć",

        f"Liczba połączeń:\n{len(connections)}"

    )



# ============================================================
# TEMPERATURA
# ============================================================


def monitor_temperature():


    if not psutil:

        return



    try:


        temps = psutil.sensors_temperatures()



        text=str(

            temps

        )



        popup(

            "Temperatura",

            text

        )



    except Exception as e:


        error(

            "Brak danych temperatury"

        )



# ============================================================
# RAPORT SYSTEMU
# ============================================================


def monitor_report():


    filename=filedialog.asksaveasfilename(

        defaultextension=".txt"

    )



    if not filename:

        return



    text=""




    text+="ToolKit 2.0 RAPORT\n"

    text+="=================\n\n"



    text+=f"""

System:

{platform.system()}


Wersja:

{platform.version()}


Python:

{platform.python_version()}


Procesor:

{platform.processor()}


Data:

{datetime.datetime.now()}

"""



    if psutil:


        text+=f"""

CPU:

{psutil.cpu_percent()}%


RAM:

{psutil.virtual_memory().percent}%


"""



    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:


        file.write(

            text

        )



    popup(

        "Raport",

        "Zapisano raport."

    )



# ============================================================
# MONITOR LIVE
# ============================================================


def monitor_live():


    window=tk.Toplevel(

        root

    )


    window.title(

        t("Monitor Live")

    )


    window.geometry(

        "400x300"

    )



    label=tk.Label(

        window,

        font=(

            "Arial",

            14

        )

    )


    label.pack(

        pady=40

    )



    def update():


        if psutil:


            text=f"""

CPU:

{psutil.cpu_percent()}%


RAM:

{psutil.virtual_memory().percent}%


"""

            label.config(

                text=text

            )


        window.after(

            MONITOR_REFRESH,

            update

        )



    update()



# ============================================================
# PRZYCISKI MONITORING
# ============================================================


monitor_buttons=[


    (
        "⚡ CPU",
        monitor_cpu
    ),


    (
        "🧠 RAM",
        monitor_ram
    ),


    (
        "💾 Dyski",
        monitor_disks
    ),


    (
        "🔋 Bateria",
        monitor_battery
    ),


    (
        "📋 Procesy",
        monitor_processes
    ),


    (
        "🌐 Połączenia",
        monitor_network
    ),


    (
        "🌡 Temperatura",
        monitor_temperature
    ),


    (
        "📄 Raport systemu",
        monitor_report
    ),


    (
        "📈 Monitor Live",
        monitor_live
    )

]



for text, command in monitor_buttons:


    btn = ttk.Button(

        tab_monitor,

        text=t(text),

        command=command,

        style="Tool.TButton"

    )
    btn._orig_text = text
    translatable_buttons.append(btn)
    btn.pack(

        pady=5,

        padx=10,

        fill="x"

    )

# ============================================================
# ADVANCED SYSTEM TOOLS PRO
# ============================================================


# ============================================================
# URUCHAMIANIE KOMEND
# ============================================================


def advanced_run(command):

    try:

        result = subprocess.check_output(

            command,

            shell=True,

            stderr=subprocess.STDOUT

        )


        return result.decode(

            errors="ignore"

        )


    except Exception as e:

        return str(e)



# ============================================================
# SFC
# ============================================================


def advanced_sfc():


    result = advanced_run(

        "sfc /scannow"

    )


    toolkit_text_window(

        "SFC",

        result

    )



# ============================================================
# DISM
# ============================================================


def advanced_dism():


    result = advanced_run(

        "DISM /Online /Cleanup-Image /RestoreHealth"

    )


    toolkit_text_window(

        "DISM",

        result

    )



# ============================================================
# STEROWNIKI
# ============================================================


def advanced_drivers():


    result = advanced_run(

        "driverquery"

    )


    toolkit_text_window(

        "Sterowniki",

        result

    )



# ============================================================
# EXPORT STEROWNIKÓW
# ============================================================


def advanced_export_drivers():


    folder=choose_folder()



    if not folder:

        return



    result=advanced_run(

        f'dism /online /export-driver /destination:"{folder}"'

    )


    popup(

        "Sterowniki",

        result

    )



# ============================================================
# USŁUGI
# ============================================================


def advanced_services():


    result=advanced_run(

        "sc query"

    )


    toolkit_text_window(

        "Usługi",

        result

    )



# ============================================================
# UŻYTKOWNICY
# ============================================================


def advanced_users():


    result=advanced_run(

        "net user"

    )


    toolkit_text_window(

        "Konta użytkowników",

        result

    )



# ============================================================
# BIOS
# ============================================================


def advanced_bios():


    result=advanced_run(

        "wmic bios get manufacturer,name,version"

    )


    toolkit_text_window(

        "BIOS",

        result

    )



# ============================================================
# PŁYTA GŁÓWNA
# ============================================================


def advanced_board():


    result=advanced_run(

        "wmic baseboard get manufacturer,product,serialnumber"

    )


    toolkit_text_window(

        "Płyta główna",

        result

    )



# ============================================================
# ZMIENNE ŚRODOWISKOWE
# ============================================================


def advanced_environment():


    text=""


    for key,value in os.environ.items():


        text+=f"""

{key}

{value}

----------------

"""



    toolkit_text_window(

        "Environment",

        text

    )



# ============================================================
# LISTA PROGRAMÓW
# ============================================================


def advanced_programs():


    result=advanced_run(

        "wmic product get name,version"

    )


    toolkit_text_window(

        "Programy",

        result

    )



# ============================================================
# PANEL ADMINISTRACYJNY
# ============================================================


def advanced_admin_panel():


    try:

        os.system(

            "control admintools"

        )


    except Exception as e:

        error(

            str(e)

        )



# ============================================================
# CZYSZCZENIE TEMP
# ============================================================


def advanced_temp_clean():


    folders=[


        tempfile.gettempdir(),


        r"C:\Windows\Temp"


    ]



    removed=0



    for folder in folders:


        try:


            for file in os.listdir(folder):


                path=os.path.join(

                    folder,

                    file

                )



                if os.path.isfile(path):


                    os.remove(

                        path

                    )


                    removed+=1



        except:

            pass



    popup(

        "TEMP",

        f"Usunięto plików: {removed}"

    )



# ============================================================
# INFORMACJE WINDOWS
# ============================================================


def advanced_windows_info():


    result=advanced_run(

        "systeminfo"

    )


    toolkit_text_window(

        "Windows Info",

        result

    )



# ============================================================
# IP CONFIG
# ============================================================


def advanced_ipconfig():


    result=advanced_run(

        "ipconfig /all"

    )


    toolkit_text_window(

        "IP Config",

        result

    )



# ============================================================
# TASKLIST
# ============================================================


def advanced_tasklist():


    result=advanced_run(

        "tasklist"

    )


    toolkit_text_window(

        "Procesy CMD",

        result

    )



# ============================================================
# PRZYCISKI ADVANCED
# ============================================================


advanced_buttons=[


    (
        "🛠 SFC Scan",
        advanced_sfc
    ),


    (
        "🔧 DISM Repair",
        advanced_dism
    ),


    (
        "💿 Sterowniki",
        advanced_drivers
    ),


    (
        "📤 Export Drivers",
        advanced_export_drivers
    ),


    (
        "⚙ Usługi",
        advanced_services
    ),


    (
        "👤 Użytkownicy",
        advanced_users
    ),


    (
        "BIOS",
        advanced_bios
    ),


    (
        "🖥 Płyta główna",
        advanced_board
    ),


    (
        "🌱 Zmienne",
        advanced_environment
    ),


    (
        "📦 Programy",
        advanced_programs
    ),


    (
        "🧰 Admin Tools",
        advanced_admin_panel
    ),


    (
        "🧹 TEMP Clean",
        advanced_temp_clean
    ),


    (
        "💻 Windows Info",
        advanced_windows_info
    ),


    (
        "🌐 IP Config",
        advanced_ipconfig
    ),


    (
        "📋 Tasklist",
        advanced_tasklist
    )

]



for text, command in advanced_buttons:


    btn = ttk.Button(

        tab_advanced,

        text=t(text),

        command=command,

        style="Tool.TButton"

    )
    btn._orig_text = text
    translatable_buttons.append(btn)
    btn.pack(

        pady=5,

        padx=10,

        fill="x"

    )

# ============================================================
# FINAL CORE
# ============================================================


TOOLKIT_VERSION = "2.0"

CORE_CONFIG = "toolkit_config.json"

PLUGIN_FOLDER = "plugins"



# ============================================================
# ZAPIS USTAWIEŃ
# ============================================================


def core_save_settings():


    data = {

        "version":

        TOOLKIT_VERSION,


        "window":

        root.geometry(),


        "created":

        str(datetime.datetime.now())

    }



    try:

        with open(

            CORE_CONFIG,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )


        popup(

            "Core",

            "Zapisano ustawienia."

        )


    except Exception as e:

        error(

            str(e)

        )



# ============================================================
# WCZYTYWANIE USTAWIEŃ
# ============================================================


def core_load_settings():


    if not os.path.exists(

        CORE_CONFIG

    ):


        popup(

            "Core",

            "Brak konfiguracji."

        )

        return



    try:

        with open(

            CORE_CONFIG,

            encoding="utf-8"

        ) as file:


            data=json.load(file)



        if "window" in data:


            root.geometry(

                data["window"]

            )



        popup(

            "Core",

            "Ustawienia wczytane."

        )


    except Exception as e:


        error(

            str(e)

        )



# ============================================================
# INFORMACJE TOOLKIT
# ============================================================


def core_about():


    text=f"""

ToolKit 2.0


Wersja:

{TOOLKIT_VERSION}


System:

{platform.system()}


Python:

{platform.python_version()}


Data:

{datetime.datetime.now()}


"""



    popup(

        "O programie",

        text

    )



# ============================================================
# LISTA MODUŁÓW
# ============================================================


def core_modules():


    modules="""

📁 File Manager

💻 System Tools

🌐 Network Tools

🔐 Vault

🛠 Developer

💾 Backup

🤖 Automation

📊 Monitoring

🧩 Advanced

🚀 Core

"""



    popup(

        "Moduły",

        modules

    )



# ============================================================
# TWORZENIE PLUGINU
# ============================================================


def core_create_plugin():


    os.makedirs(

        PLUGIN_FOLDER,

        exist_ok=True

    )



    name=simpledialog.askstring(

        "Plugin",

        "Nazwa pluginu:"

    )



    if not name:

        return



    filename=os.path.join(

        PLUGIN_FOLDER,

        name+".py"

    )



    content=f'''

# ToolKit 2.0 Plugin


PLUGIN_NAME="{name}"


def start():

    print("Plugin {name} działa")

'''



    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:


        file.write(

            content

        )



    popup(

        "Plugin",

        "Plugin utworzony."

    )



# ============================================================
# LISTA PLUGINÓW
# ============================================================


def core_list_plugins():


    if not os.path.exists(

        PLUGIN_FOLDER

    ):


        popup(

            "Pluginy",

            "Brak pluginów."

        )

        return



    plugins=os.listdir(

        PLUGIN_FOLDER

    )



    popup(

        "Pluginy",

        "\n".join(plugins)

    )



# ============================================================
# MOTYW CIEMNY
# ============================================================


def core_dark_mode():


    try:


        style.theme_use(

            "clam"

        )


        popup(

            "Motyw",

            "Włączono tryb ciemny."

        )


    except:

        pass



# ============================================================
# MOTYW NORMALNY
# ============================================================


def core_default_mode():


    try:


        style.theme_use(

            "default"

        )


        popup(

            "Motyw",

            "Przywrócono motyw."

        )


    except:

        pass



# ============================================================
# RESTART
# ============================================================


def core_restart():


    python=sys.executable


    os.execl(

        python,

        python,

        *sys.argv

    )



# ============================================================
# ZAMKNIĘCIE
# ============================================================


def core_exit():


    root.destroy()



# ============================================================
# PRZYCISKI CORE
# ============================================================


core_buttons=[


    (
        "💾 Zapisz ustawienia",
        core_save_settings
    ),


    (
        "📂 Wczytaj ustawienia",
        core_load_settings
    ),


    (
        "ℹ O ToolKit",
        core_about
    ),


    (
        "📦 Moduły",
        core_modules
    ),


    (
        "🧩 Utwórz plugin",
        core_create_plugin
    ),


    (
        "📋 Lista pluginów",
        core_list_plugins
    ),


    (
        "🌑 Tryb ciemny",
        core_dark_mode
    ),


    (
        "☀ Tryb normalny",
        core_default_mode
    ),


    (
        "🔄 Restart",
        core_restart
    ),


    (
        "❌ Wyjście",
        core_exit
    )

]



for text, command in core_buttons:


    btn = ttk.Button(

        tab_core,

        text=t(text),

        command=command,

        style="Tool.TButton"

    )
    btn._orig_text = text
    translatable_buttons.append(btn)
    btn.pack(

        pady=5,

        padx=10,

        fill="x"

    )



# ============================================================
# START TOOLKIT 2.0
# ============================================================


TOOLS_LABELS = {
    "🔐 Otwórz sejf": {"English": "🔐 Open Vault", "Polski": "🔐 Otwórz sejf", "Русский": "🔐 Открыть сейф"},
    "➕ Nowy sejf": {"English": "➕ New Vault", "Polski": "➕ Nowy sejf", "Русский": "➕ Новый сейф"},
    "🔑 Generator haseł": {"English": "🔑 Password Generator", "Polski": "🔑 Generator haseł", "Русский": "🔑 Генератор паролей"},
    "📝 Prywatna notatka": {"English": "📝 Private Note", "Polski": "📝 Prywatna notatka", "Русский": "📝 Личная заметка"},
    "🆔 UUID": {"English": "🆔 UUID", "Polski": "🆔 UUID", "Русский": "🆔 UUID"},
    "🔑 GUID": {"English": "🔑 GUID", "Polski": "🔑 GUID", "Русский": "🔑 GUID"},
    "# MD5": {"English": "# MD5", "Polski": "# MD5", "Русский": "# MD5"},
    "# SHA1": {"English": "# SHA1", "Polski": "# SHA1", "Русский": "# SHA1"},
    "# SHA256": {"English": "# SHA256", "Polski": "# SHA256", "Русский": "# SHA256"},
    "⚖ Porównaj hash": {"English": "⚖ Compare Hash", "Polski": "⚖ Porównaj hash", "Русский": "⚖ Сравнить хэш"},
    "🔒 Szyfruj plik": {"English": "🔒 Encrypt File", "Polski": "🔒 Szyfruj plik", "Русский": "🔒 Зашифровать файл"},
    "🎲 Token": {"English": "🎲 Token", "Polski": "🎲 Token", "Русский": "🎲 Токен"},
    "🎯 Random": {"English": "🎯 Random Data", "Polski": "🎯 Random", "Русский": "🎯 Случайные данные"},
    "🔤 Base64 Encode": {"English": "🔤 Base64 Encode", "Polski": "🔤 Base64 Encode", "Русский": "🔤 Кодировать Base64"},
    "🔡 Base64 Decode": {"English": "🔡 Base64 Decode", "Polski": "🔡 Base64 Decode", "Русский": "🔡 Декодировать Base64"},
    "📊 Analizator tekstu": {"English": "📊 Text Analyzer", "Polski": "📊 Analizator tekstu", "Русский": "📊 Анализатор текста"},
    "📋 Schowek": {"English": "📋 Clipboard", "Polski": "📋 Schowek", "Русский": "📋 Буфер обмена"},
    "🧹 Temp Cleaner": {"English": "🧹 Temp Cleaner", "Polski": "🧹 Temp Cleaner", "Русский": "🧹 Очистка TEMP"},
    "⚡ Cache Cleaner": {"English": "⚡ Cache Cleaner", "Polski": "⚡ Cache Cleaner", "Русский": "⚡ Очистка кэша"},
    "📁 Info folderu": {"English": "📁 Folder Info", "Polski": "📁 Info folderu", "Русский": "📁 Информация о папке"},
    "▶ Uruchom program": {"English": "▶ Run Program", "Polski": "▶ Uruchom program", "Русский": "▶ Запустить программу"},
    "📁 Otwórz folder": {"English": "📁 Open Folder", "Polski": "📁 Otwórz folder", "Русский": "📁 Открыть папку"},
    "⌨ Wykonaj CMD": {"English": "⌨ Execute CMD", "Polski": "⌨ Wykonaj CMD", "Русский": "⌨ Выполнить CMD"},
    "🐍 Uruchom skrypt Python": {"English": "🐍 Run Python Script", "Polski": "🐍 Uruchom skrypt Python", "Русский": "🐍 Запустить скрипт Python"},
    "⏱ Timer": {"English": "⏱ Timer", "Polski": "⏱ Timer", "Русский": "⏱ Таймер"},
    "💾 Zapisz zadanie": {"English": "💾 Save Task", "Polski": "💾 Zapisz zadanie", "Русский": "💾 Сохранить задачу"},
    "📋 Lista zadań": {"English": "📋 Task List", "Polski": "📋 Lista zadań", "Русский": "📋 Список задач"},
    "🧹 Czyść TEMP": {"English": "🧹 Clean TEMP", "Polski": "🧹 Czyść TEMP", "Русский": "🧹 Очистить TEMP"},
    "🐍 Informacje Python": {"English": "🐍 Python Info", "Polski": "🐍 Informacje Python", "Русский": "🐍 Информация Python"},
    "💽 Analiza dysku": {"English": "💽 Disk Analysis", "Polski": "💽 Analiza dysku", "Русский": "💽 Анализ диска"},
    "📦 Duże pliki": {"English": "📦 Large Files", "Polski": "📦 Duże pliki", "Русский": "📦 Большие файлы"},
    "♻ Duplikaty": {"English": "♻ Duplicates", "Polski": "♻ Duplikaty", "Русский": "♻ Дубликаты"},
    "🧹 TEMP": {"English": "🧹 TEMP", "Polski": "🧹 TEMP", "Русский": "🧹 TEMP"},
    "🌐 Cache przeglądarek": {"English": "🌐 Browser Cache", "Polski": "🌐 Cache przeglądarek", "Русский": "🌐 Кэш браузеров"},
    "🖼 Miniatury": {"English": "🖼 Thumbnails", "Polski": "🖼 Miniatury", "Русский": "🖼 Миниатюры"},
    "🚀 Autostart": {"English": "🚀 Startup", "Polski": "🚀 Autostart", "Русский": "🚀 Автозапуск"},
    "⚙ Usługi": {"English": "⚙ Services", "Polski": "⚙ Usługi", "Русский": "⚙ Службы"},
    "📦 Programy": {"English": "📦 Programs", "Polski": "📦 Programy", "Русский": "📦 Программы"},
    "📜 Logi": {"English": "📜 Logs", "Polski": "📜 Logi", "Русский": "📜 Журналы"},
    "🗑 Kosz": {"English": "🗑 Recycle Bin", "Polski": "🗑 Kosz", "Русский": "🗑 Корзина"},
    "📑 Raport": {"English": "📑 Report", "Polski": "📑 Raport", "Русский": "📑 Отчет"},
}


def rebuild_tools_tab():
    """Build one stable, localized Tools grid from the canonical actions."""
    tools_button_registry.clear()

    for child in tab_tools.winfo_children():
        child.destroy()

    host = tk.Frame(tab_tools, bg=BG)
    host.pack(fill="both", expand=True, padx=8, pady=8)

    for column in range(4):
        host.columnconfigure(column, weight=1)

    button_groups = (
        vault_buttons,
        tools_buttons,
        cleaner_buttons,
        automation_buttons,
    )

    index = 0
    for group in button_groups:
        for original, command in group:
            row = index // 4
            column = index % 4
            tile = tk.Frame(
                host,
                bg=CARD if index % 2 == 0 else "#263549",
                highlightthickness=1,
                highlightbackground="#475569",
            )
            tile.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")
            button = ttk.Button(
                tile,
                text=TOOLS_LABELS.get(original, {}).get(current_lang, original),
                command=command,
                style="Tool.TButton",
            )
            button.pack(fill="both", expand=True, padx=10, pady=10)
            button._orig_text = original
            tools_button_registry.append((button, original))
            translatable_buttons.append(button)
            index += 1


rebuild_tools_tab()
print(
    "ToolKit 2.0 uruchomiony"
)



change_language(current_lang)
root.mainloop()