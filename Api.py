import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def conectar_banco():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="sua senha",
            database="bancopy"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(err)}")
        return None

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
        cursor.execute("SELECT role FROM tb_usuarios WHERE username=%s AND senha=%s", (username, senha))
        result = cursor.fetchone()

        if result:
            role = result[0]
            messagebox.showinfo("Sucesso", f"Login bem-sucedido como {username}!")
            root.destroy()
            open_main_window(username, role)
        else:
            messagebox.showwarning("Aviso", "Usuário ou senha incorretos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar login: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

def open_main_window(username, role):
    main_window = tk.Tk()
    main_window.title("Gerenciador da ideonella sakaiensis")
    main_window.geometry("400x300")
    main_window.configure(bg="#91bd8f")

    def insert_data():
        crioprotetores = entry_crioprotetor.get().strip().lower()
        temperatura = entry_temperatura.get().strip().capitalize()
        quantidade = entry_quantidade.get()

        if not (crioprotetores and temperatura and quantidade.isdigit()):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos corretamente.")
            return

        quantidade = int(quantidade)
        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            sql = "INSERT INTO tb_crioprotetores (crioprotetores, temperatura, quantidade, usuario_id) VALUES (%s, %s, %s, (SELECT id FROM tb_usuarios WHERE username = %s))"
            valores = (crioprotetores, temperatura, quantidade, username)
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
        crioprotetores = entry_crioprotetor.get().strip().lower()

        if role != 'admin':
            messagebox.showwarning("Aviso", "Somente o engenheiro chefe pode remover crioprotetores.")
            return

        if not crioprotetores:
            messagebox.showwarning("Aviso", "Digite o nome do crioprotetor a ser removido.")
            return

        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            sql = "DELETE FROM tb_crioprotetores WHERE crioprotetores = %s"
            valores = (crioprotetores,)
            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Sucesso", f"Dados deletados com sucesso para {crioprotetores}")
            else:
                messagebox.showwarning("Aviso", f"Nenhum crioprotetor encontrado com o nome {crioprotetores}")
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
            cursor.execute("SELECT * FROM tb_crioprotetores")
            registros = cursor.fetchall()

            dados = "\n".join([f"ID: {row[0]}, Crioprotetor: {row[1]}, Temperatura: {row[2]}, Quantidade: {row[3]}" for row in registros])
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
        entry_crioprotetor.delete(0, tk.END)
        entry_temperatura.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

    label_style = {"bg": "#14341f", "fg": "white", "font": ("Helvetica", 10, "bold")}

    tk.Label(main_window, text="Crioprotetor:", **label_style).grid(row=0, column=0, pady=5, padx=10, sticky="e")
    entry_crioprotetor = tk.Entry(main_window, font=("Helvetica", 10))
    entry_crioprotetor.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Temperatura:", **label_style).grid(row=1, column=0, pady=5, padx=10, sticky="e")
    entry_temperatura = tk.Entry(main_window, font=("Helvetica", 10))
    entry_temperatura.grid(row=1, column=1, pady=5, padx=10, sticky="w")

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

    ttk.Button(main_window, text="Adicionar bactéria", command=insert_data).grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="n")

    if role == 'admin':
        ttk.Button(main_window, text="Remover bactéria", command=delete_data).grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="n")
    
    ttk.Button(main_window, text="Visualizar Status", command=view_data).grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="n")
    ttk.Button(main_window, text="Sair", command=main_window.quit).grid(row=6, column=0, columnspan=2, pady=5, padx=10, sticky="n")

    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=1)

    main_window.mainloop()

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
