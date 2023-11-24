import tkinter as tk
from tkinter import ttk, filedialog
import os
import webbrowser

def save_data():
    animal_name = animal_name_entry.get()
    owner_name = owner_name_entry.get()
    animal_species = species_entry.get()
    animal_age = age_entry.get()
    entry_date = entry_date_entry.get()
    procedures = procedures_entry.get()
    payment_method = payment_method_entry.get()
    medications = medications_entry.get()
    attending_vet = attending_vet_entry.get()
    medical_record = medical_record_entry.get()
    value = value_entry.get()
    status = status_entry.get()

    data_table.insert("", "end", values=(animal_name, animal_species, owner_name, animal_age, entry_date, procedures, payment_method, medications, attending_vet, medical_record, value, status))

    animal_name_entry.delete(0, tk.END)
    owner_name_entry.delete(0, tk.END)
    species_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    entry_date_entry.delete(0, tk.END)
    procedures_entry.delete(0, tk.END)
    payment_method_entry.delete(0, tk.END)
    medications_entry.delete(0, tk.END)
    attending_vet_entry.delete(0, tk.END)
    medical_record_entry.delete(0, tk.END)
    value_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

def choose_medical_record():
    file_path = filedialog.askopenfilename(
        title="Selecione o Arquivo de Prontuário",
        filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os Arquivos", "*.*"))
    )
    if file_path:
        medical_record_entry.delete(0, tk.END)
        medical_record_entry.insert(0, file_path)

def open_medical_record(event):
    selected_item = data_table.focus()
    item_values = data_table.item(selected_item, 'values')
    medical_record_path = item_values[9]  # Assuming the medical record is in the 10th column
    if os.path.exists(medical_record_path):
        webbrowser.open(medical_record_path)

def create_vet_clinic_gui():
    window = tk.Tk()
    window.title("Sistema de Registro de Clínica Veterinária")
    window.geometry("800x600")

    # Define a responsividade da janela principal.
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    # Cria o PanedWindow para dividir a tela entre o menu e o conteúdo.
    main_pane = ttk.PanedWindow(window, orient=tk.HORIZONTAL)
    main_pane.pack(fill=tk.BOTH, expand=True)

    # Menu lateral
    menu_frame = ttk.Frame(main_pane, width=200, relief=tk.RAISED, borderwidth=2)
    main_pane.add(menu_frame)

    # Botões do menu lateral
    ttk.Button(menu_frame, text="Cadastro", command=lambda: show_frame(registration_frame)).pack(fill=tk.BOTH)
    ttk.Button(menu_frame, text="Registros", command=lambda: show_frame(records_frame)).pack(fill=tk.BOTH)

    # Conteúdo principal
    content_frame = ttk.Frame(main_pane, relief=tk.RAISED, borderwidth=2)
    main_pane.add(content_frame)
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # Frames para cadastro e visualização de registros
    registration_frame = ttk.Frame(content_frame)
    registration_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    registration_frame.grid_columnconfigure(1, weight=1)

    records_frame = ttk.Frame(content_frame)
    records_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    records_frame.grid_columnconfigure(0, weight=1)
    records_frame.grid_rowconfigure(0, weight=1)

    # Função para alternar entre os frames.
    def show_frame(frame):
        frame.tkraise()

    # Configuração dos widgets de cadastro
    labels_texts = ["Nome do Animal", "Espécie", "Nome do Dono", "Idade", "Data de Entrada",
                    "Procedimentos e Serviços", "Método de Pagamento", "Medicamentos", 
                    "Médico que Atendeu", "Prontuário", "Valor", "Status"]
    global animal_name_entry, species_entry, owner_name_entry, age_entry
    global entry_date_entry, procedures_entry, payment_method_entry, medications_entry
    global attending_vet_entry, medical_record_entry, value_entry, status_entry

    entries = []
    for i, text in enumerate(labels_texts):
        label = ttk.Label(registration_frame, text=text)
        label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entry = ttk.Entry(registration_frame, width=30)
        entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
        entries.append(entry)

    animal_name_entry, species_entry, owner_name_entry, age_entry, entry_date_entry, procedures_entry, payment_method_entry, medications_entry, attending_vet_entry, medical_record_entry, value_entry, status_entry = entries

    # Botão para salvar os dados de cadastro.
    save_button = ttk.Button(registration_frame, text="Salvar", command=save_data)
    save_button.grid(row=12, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    # Botão para selecionar o arquivo de prontuário.
    medical_record_button = ttk.Button(registration_frame, text="Escolher Prontuário", command=choose_medical_record)
    medical_record_button.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

    # Tabela de visualização dos registros
    columns = ["Animal", "Espécie", "Dono", "Idade", "Data de Entrada", 
               "Procedimentos e Serviços", "Método de Pagamento", "Medicamentos", 
               "Médico", "Prontuário", "Valor", "Status"]
    global data_table
    data_table = ttk.Treeview(records_frame, columns=columns, show="headings")
    data_table.grid(row=0, column=0, sticky="nsew")
    for col in columns:
        data_table.heading(col, text=col)
        data_table.column(col, anchor="center")

    # Adiciona a barra de rolagem à tabela.
    scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=data_table.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    data_table.configure(yscrollcommand=scrollbar.set)

    # Define a função de abertura do arquivo de prontuário ao clicar duas vezes no registro.
    data_table.bind("<Double-1>", open_medical_record)

    # Define o frame de cadastro para ser mostrado inicialmente.
    show_frame(registration_frame)

    # Inicia a aplicação.
    window.mainloop()

# Executar a criação da GUI
create_vet_clinic_gui()
