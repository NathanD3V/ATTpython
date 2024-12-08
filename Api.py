import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def conectar_banco():
    try:
        return mysql.connector.connect(
            host="mysql://root:VHvYAqxlVbYqkioAUmuBMejOIDTvtPWb@junction.proxy.rlwy.net:13556/railwayt",
            user="root",
            password="12345",
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

def open_third_window():
    third_window = tk.Toplevel()
    third_window.title("Registrar Novo Funcionário")
    third_window.geometry("600x400")
    third_window.configure(bg="#91bd8f")

    def view_users():
        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tb_usuarios")
            registros = cursor.fetchall()

            dados = "\n".join([f"ID: {row[0]}, Usuário: {row[1]}, Função: {row[3]}" for row in registros])
            if dados:
                messagebox.showinfo("Usuários Cadastrados", dados)
            else:
                messagebox.showinfo("Usuários Cadastrados", "Nenhum usuário encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuários: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

    def delete_user():
        username = entry_delete_username.get().strip()
        if not username:
            messagebox.showwarning("Aviso", "Por favor, insira um nome de usuário para deletar.")
            return

        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM tb_usuarios WHERE username = %s", (username,))
            conexao.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Sucesso", f"Usuário '{username}' deletado com sucesso!")
            else:
                messagebox.showwarning("Aviso", f"Usuário '{username}' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar usuário: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

        entry_delete_username.delete(0, tk.END)

    def add_employee():
        new_username = entry_new_username.get().strip()
        new_password = entry_new_password.get().strip()
        new_role = entry_new_role.get().strip().lower()

        if not (new_username and new_password and new_role):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            sql = "INSERT INTO tb_usuarios (username, senha, role) VALUES (%s, %s, %s)"
            cursor.execute(sql, (new_username, new_password, new_role))
            conexao.commit()
            messagebox.showinfo("Sucesso", f"Funcionário {new_username} registrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar funcionário: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

        entry_new_username.delete(0, tk.END)
        entry_new_password.delete(0, tk.END)
        entry_new_role.delete(0, tk.END)

    label_style = {
        "bg": "#a2d5ab",
        "fg": "#333333",
        "font": ("Helvetica", 10, "bold")
    }

    tk.Label(third_window, text="Nome de Usuário:", **label_style).grid(row=0, column=0, pady=5, padx=10, sticky="e")
    entry_new_username = tk.Entry(third_window, font=("Helvetica", 10))
    entry_new_username.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    tk.Label(third_window, text="Senha:", **label_style).grid(row=1, column=0, pady=5, padx=10, sticky="e")
    entry_new_password = tk.Entry(third_window, font=("Helvetica", 10), show='*')
    entry_new_password.grid(row=1, column=1, pady=5, padx=10, sticky="w")

    tk.Label(third_window, text="Função (ex: admin, user):", **label_style).grid(row=2, column=0, pady=5, padx=10, sticky="e")
    entry_new_role = tk.Entry(third_window, font=("Helvetica", 10))
    entry_new_role.grid(row=2, column=1, pady=5, padx=10, sticky="w")

    ttk.Button(third_window, text="Adicionar Funcionário", command=add_employee).grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Button(third_window, text="Visualizar Usuários", command=view_users).grid(row=4, column=0, columnspan=2, pady=5)
    ttk.Button(third_window, text="Deletar Usuário", command=delete_user).grid(row=6, column=0, columnspan=2, pady=5)

    tk.Label(third_window, text="Deletar Usuário:", **label_style).grid(row=5, column=0, pady=5, padx=10, sticky="e")
    entry_delete_username = tk.Entry(third_window, font=("Helvetica", 10))
    entry_delete_username.grid(row=5, column=1, pady=5, padx=10, sticky="w")

    ttk.Button(third_window, text="Voltar", command=third_window.destroy).grid(row=7, column=0, pady=10)
    ttk.Button(third_window, text="Sair", command=third_window.quit).grid(row=7, column=1, pady=10)

    third_window.grid_columnconfigure(0, weight=1)
    third_window.grid_columnconfigure(1, weight=1)

    third_window.grid_columnconfigure(0, weight=1)
    third_window.grid_columnconfigure(1, weight=1)
    
def open_main_window(username, role):
    main_window = tk.Tk()
    main_window.title("Gerenciador da ideonella sakaiensis")
    main_window.geometry("600x400")
    main_window.configure(bg="#91bd8f")

    def update_capacity_chart():
        """Atualiza o gráfico de capacidade do banco de dados."""
        conexao = conectar_banco()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT SUM(quantidade) FROM tb_crioprotetores")
            total = cursor.fetchone()[0] or 0

            cursor.close()
            conexao.close()

            ocupado = min(total, 1000)
            livre = max(0, 1000 - ocupado)

            ax.clear()
            ax.pie(
                [ocupado, livre],
                labels=["Ocupado", "Disponível"],
                autopct='%1.1f%%',
                colors=["#ff9999", "#99ff99"],
                startangle=90,
            )
            ax.set_title("Capacidade do Biodigestor (Máx: 1000)")
            canvas.draw()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {str(e)}")
    
    def insert_data():
        """Insere dados no banco, respeitando o limite máximo de 1000 unidades."""
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
            cursor.execute("SELECT SUM(quantidade) FROM tb_crioprotetores")
            total_atual = cursor.fetchone()[0] or 0

            if total_atual + quantidade > 1000:
                messagebox.showwarning("Aviso", "A quantidade excederia o limite máximo de 1000 unidades no biodigestor.")
                return

            sql = "INSERT INTO tb_crioprotetores (crioprotetores, temperatura, quantidade, usuario_id) VALUES (%s, %s, %s, (SELECT id FROM tb_usuarios WHERE username = %s))"
            valores = (crioprotetores, temperatura, quantidade, username)
            cursor.execute(sql, valores)
            conexao.commit()
            messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")

            update_capacity_chart()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir dados: {str(e)}")
        finally:
            cursor.close()
            conexao.close()

        clear_entries()

    def delete_data():
        crioprotetores = entry_crioprotetor.get().strip().lower()

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

    label_style = {
        "bg": "#a2d5ab",
        "fg": "#333333",
        "font": ("Helvetica", 10, "bold")
    }

    ttk.Button(main_window, text="Atualizar Gráfico", command=update_capacity_chart).grid(row=8, column=2, pady=5)
    tk.Label(main_window, text="Crioprotetor:", bg="#a2d5ab", font=("Helvetica", 10, "bold")).grid(row=0, column=0, pady=5, padx=10, sticky="e")
    entry_crioprotetor = tk.Entry(main_window, font=("Helvetica", 10))
    entry_crioprotetor.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Temperatura:", bg="#a2d5ab", font=("Helvetica", 10, "bold")).grid(row=1, column=0, pady=5, padx=10, sticky="e")
    entry_temperatura = tk.Entry(main_window, font=("Helvetica", 10))
    entry_temperatura.grid(row=1, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Quantidade:", bg="#a2d5ab", font=("Helvetica", 10, "bold")).grid(row=2, column=0, pady=5, padx=10, sticky="e")
    entry_quantidade = tk.Entry(main_window, font=("Helvetica", 10))
    entry_quantidade.grid(row=2, column=1, pady=5, padx=10, sticky="w")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton",
                    background="#30833f",
                    foreground="white",
                    font=("Helvetica", 10, "bold"),
                    padding=5)

    tk.Label(main_window, text="Crioprotetor:", bg="#a2d5ab", font=("Helvetica", 10, "bold")).grid(row=0, column=0, pady=5, padx=10, sticky="e")
    entry_crioprotetor = tk.Entry(main_window, font=("Helvetica", 10))
    entry_crioprotetor.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Temperatura:", bg="#a2d5ab", font=("Helvetica", 10, "bold")).grid(row=1, column=0, pady=5, padx=10, sticky="e")
    entry_temperatura = tk.Entry(main_window, font=("Helvetica", 10))
    entry_temperatura.grid(row=1, column=1, pady=5, padx=10, sticky="w")

    tk.Label(main_window, text="Quantidade:", bg="#a2d5ab", font=("Helvetica", 10, "bold")).grid(row=2, column=0, pady=5, padx=10, sticky="e")
    entry_quantidade = tk.Entry(main_window, font=("Helvetica", 10))
    entry_quantidade.grid(row=2, column=1, pady=5, padx=10, sticky="w")

    ttk.Button(main_window, text="Adicionar bactéria", command=insert_data).grid(row=3, column=0, columnspan=2, pady=5)
    ttk.Button(main_window, text="Visualizar Status", command=view_data).grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Button(main_window, text="Remover bactéria", command=delete_data).grid(row=4, column=0, columnspan=2, pady=5)
    if role == 'admin':
        ttk.Button(main_window, text="Registro", command=open_third_window).grid(row=6, column=0, columnspan=2, pady=5)
    ttk.Button(main_window, text="Sair", command=main_window.quit).grid(row=7, column=0, columnspan=2, pady=5)

    fig = Figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, main_window)
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=8, padx=20, pady=10)

    ttk.Button(main_window, text="Atualizar Gráfico", command=update_capacity_chart).grid(row=8, column=2, pady=5)

    update_capacity_chart()

    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=1)
    main_window.grid_columnconfigure(2, weight=1)

    main_window.mainloop()

root = tk.Tk()
root.title("Login")
root.geometry("400x300")
root.configure(bg="#91bd8f")

label_style = {
    "bg": "#a2d5ab",
    "fg": "#333333",
    "font": ("Helvetica", 10, "bold")
}

tk.Label(root, text="Nome de Usuário:", **label_style).grid(row=0, column=0, pady=20, padx=20, sticky="e")
entry_username = tk.Entry(root, font=("Helvetica", 10))
entry_username.grid(row=0, column=1, pady=10, padx=20, sticky="w")

tk.Label(root, text="Senha:", **label_style).grid(row=1, column=0, pady=20, padx=20, sticky="e")
entry_senha = tk.Entry(root, font=("Helvetica", 10), show='*')
entry_senha.grid(row=1, column=1, pady=10, padx=20, sticky="w")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                background="#30833f",
                foreground="white",
                font=("Helvetica", 10, "bold"),
                padding=5)
style.map("TButton",
        background=[("active", "#45a049")],
        foreground=[("active", "white")])

btn_login = ttk.Button(root, text="Entrar", command=login)
btn_login.grid(row=2, column=0, columnspan=2, pady=20)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()