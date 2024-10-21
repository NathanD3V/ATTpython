import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345", 
            database="bancopy"  
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(err)}")
        return None

# Função de login para verificar o tipo de usuário
def login():
    username = entry_username.get().strip()
    senha = entry_senha.get().strip()

    if not (username and senha):
        messagebox.showwarning("Aviso", "Nome de usuário e senha não podem estar vazios.")
        return

    conexao = conectar_banco()
    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        # Consultar usuário no banco de dados
        cursor.execute("SELECT role FROM tb_usuarios WHERE username=%s AND senha=%s", (username, senha))
        result = cursor.fetchone()

        if result:
            role = result[0]
            messagebox.showinfo("Sucesso", f"Login bem-sucedido como {username}!")
            root.destroy()
            open_main_window(username, role)  # Abre a janela principal com base no papel do usuário
        else:
            messagebox.showwarning("Aviso", "Usuário ou senha incorretos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar login: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

# Função para abrir a janela principal de acordo com o tipo de usuário
def open_main_window(username, role):
    main_window = tk.Tk()
    main_window.title("Gerenciador de Resíduos")
    main_window.geometry("400x300")
    main_window.configure(bg="#91bd8f")

    def insert_data():
        residuos = entry_residuo.get().strip().lower()
        estado = entry_estado.get().strip().capitalize()
        quantidade = entry_quantidade.get()

        if not (residuos and estado and quantidade.isdigit()):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos corretamente.")
            return

        quantidade = int(quantidade)

        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()

            # Inserir os resíduos no banco de dados, relacionado ao usuário logado
            sql = "INSERT INTO tb_residuos (residuos, estado, quantidade, usuario_id) VALUES (%s, %s, %s, (SELECT id FROM tb_usuarios WHERE username = %s))"
            valores = (residuos, estado, quantidade, username)
            cursor.execute(sql, valores)

            conexao.commit()

            messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir dados: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

        clear_entries()

    def delete_data():
        residuos = entry_residuo.get().strip().lower()

        if role != 'admin':
            messagebox.showwarning("Aviso", "Somente o engenheiro chefe pode remover resíduos.")
            return

        if not residuos:
            messagebox.showwarning("Aviso", "Digite o código do resíduo a ser removido.")
            return

        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM tb_residuos WHERE residuos = %s"
            valores = (residuos,)
            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Sucesso", f"Dados deletados com sucesso para {residuos}")
            else:
                messagebox.showwarning("Aviso", f"Nenhum resíduo encontrado com o nome {residuos}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar dados: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

        clear_entries()

    def view_data():
        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tb_residuos")
            registros = cursor.fetchall()

            dados = "\n".join([f"ID: {row[0]}, Resíduo: {row[1]}, Estado: {row[2]}, Quantidade: {row[3]}" for row in registros])
            if dados:
                messagebox.showinfo("Dados", dados)
            else:
                messagebox.showinfo("Dados", "Nenhum dado encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

    def clear_entries():
        entry_residuo.delete(0, tk.END)
        entry_estado.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

    label_style = {"bg": "#14341f", "fg": "white", "font": ("Helvetica", 10, "bold")}

    tk.Label(main_window, text="Resíduo:", **label_style).grid(row=0, column=0, pady=5, padx=10, sticky="e")
    entry_residuo = tk.Entry(main_window, font=("Helvetica", 10))
    entry_residuo.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Estado:", **label_style).grid(row=1, column=0, pady=5, padx=10, sticky="e")
    entry_estado = tk.Entry(main_window, font=("Helvetica", 10))
    entry_estado.grid(row=1, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Quantidade:", **label_style).grid(row=2, column=0, pady=5, padx=10, sticky="e")
    entry_quantidade = tk.Entry(main_window, font=("Helvetica", 10))
    entry_quantidade.grid(row=2, column=1, pady=5, padx=10, sticky="w")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", 
                    background="#30833f",  
                    foreground="white",    
                    font=("Helvetica", 10, "bold"),
                    padding=5)

    ttk.Button(main_window, text="Adicionar Resíduo", command=insert_data).grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="n")

    if role == 'admin':  # Apenas engenheiro chefe (admin) pode remover
        ttk.Button(main_window, text="Remover Resíduo", command=delete_data).grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="n")
    
    ttk.Button(main_window, text="Visualizar Status", command=view_data).grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="n")
    ttk.Button(main_window, text="Sair", command=main_window.quit).grid(row=6, column=0, columnspan=2, pady=5, padx=10, sticky="n")

    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=1)

    main_window.mainloop()

# Interface de login
root = tk.Tk()
root.title("Login")
root.geometry("400x300")
root.configure(bg="#91bd8f")

label_username = tk.Label(root, text="Nome de Usuário:", font=("Helvetica", 12, "bold"), bg="#30833f", fg="white")
label_username.grid(row=0, column=0, pady=20, padx=20)

entry_username = tk.Entry(root, font=("Helvetica", 12))
entry_username.grid(row=0, column=1, pady=10, padx=20)

label_senha = tk.Label(root, text="Senha:", font=("Helvetica", 12, "bold"), bg="#30833f", fg="white")
label_senha.grid(row=1, column=0, pady=20, padx=20)

entry_senha = tk.Entry(root, font=("Helvetica", 12), show='*')
entry_senha.grid(row=1, column=1, pady=10, padx=20)

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", 
                background="#4CAF50", 
                foreground="white",
                font=("Helvetica", 12, "bold"),
                padding=10)

style.map("TButton", 
          background=[("active", "#45a049")], 
          foreground=[("active", "white")])

btn_login = ttk.Button(root, text="Login", command=login)
btn_login.grid(row=2, column=0, columnspan=2, pady=20)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
