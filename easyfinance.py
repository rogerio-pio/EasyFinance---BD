import tkinter as tk
from tkinter import messagebox
import psycopg2

# Funções para conectar ao banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="EASYFINANCE", 
            user="admin_user", 
            password="admin_password", 
            host="localhost", 
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na conexão com o banco de dados: {e}")
        return None

# Funções para usuários
def insert_user():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            query = """INSERT INTO usuario (tipo, nomeCompleto, cpf, idUsuario, email, senha, fixo, celular) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            data = (entry_tipo.get(), entry_nome.get(), entry_cpf.get(), entry_id.get(), entry_email.get(), 
                    entry_senha.get(), entry_fixo.get(), entry_celular.get())
            cur.execute(query, data)
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário inserido com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir usuário: {e}")
        finally:
            conn.close()

def query_users():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario")
            users = cur.fetchall()
            output = ""
            for user in users:
                output += f"ID: {user[3]}, Nome: {user[1]}, CPF: {user[2]}\n"
            messagebox.showinfo("Usuários", output)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar usuários: {e}")
        finally:
            conn.close()

def delete_user():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            query = "DELETE FROM usuario WHERE idUsuario = %s"
            cur.execute(query, (entry_id.get(),))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário removido com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover usuário: {e}")
        finally:
            conn.close()

# Funções para contas
def insert_conta():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            query = """INSERT INTO conta (idConta, senha, chavesPIX, saldo, tipoConta) 
                       VALUES (%s, %s, %s, %s, %s)"""
            data = (entry_idConta.get(), entry_senhaConta.get(), entry_chavesPIX.get(), entry_saldoConta.get(), entry_tipoConta.get())
            cur.execute(query, data)
            conn.commit()
            messagebox.showinfo("Sucesso", "Conta inserida com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir conta: {e}")
        finally:
            conn.close()

def query_conta():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM conta")
            contas = cur.fetchall()
            output = ""
            for conta in contas:
                output += f"ID Conta: {conta[0]}, Saldo: {conta[3]}\n"
            messagebox.showinfo("Contas", output)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar contas: {e}")
        finally:
            conn.close()

# Interface gráfica principal com frames para diferentes seções
class EasyFinanceApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("EasyFinance - Gerenciamento")
        self.geometry("600x500")

        # Container para as páginas
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Inicializa todas as páginas
        for F in (MenuInicial, GerenciarUsuarios, GerenciarContas):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostra o menu inicial
        self.show_frame("MenuInicial")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Página do menu inicial
class MenuInicial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Bem-vindo ao EasyFinance!", font=("Helvetica", 16)).pack(pady=20)

        btn_gerenciar_usuarios = tk.Button(self, text="Gerenciar Usuários", font=("Helvetica", 12),
                                           command=lambda: controller.show_frame("GerenciarUsuarios"))
        btn_gerenciar_usuarios.pack(pady=10)

        btn_gerenciar_contas = tk.Button(self, text="Gerenciar Contas", font=("Helvetica", 12),
                                         command=lambda: controller.show_frame("GerenciarContas"))
        btn_gerenciar_contas.pack(pady=10)

# Página para gerenciar usuários
class GerenciarUsuarios(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        font_medium = ("Helvetica", 12)

        tk.Label(self, text="Gerenciar Usuários", font=("Helvetica", 16)).grid(row=0, column=1, pady=20)

        tk.Label(self, text="Tipo", font=font_medium).grid(row=1, column=0, padx=8, pady=8)
        global entry_tipo
        entry_tipo = tk.Entry(self, font=font_medium)
        entry_tipo.grid(row=1, column=1, padx=8, pady=8)

        tk.Label(self, text="Nome Completo", font=font_medium).grid(row=2, column=0, padx=8, pady=8)
        global entry_nome
        entry_nome = tk.Entry(self, font=font_medium)
        entry_nome.grid(row=2, column=1, padx=8, pady=8)

        tk.Label(self, text="CPF", font=font_medium).grid(row=3, column=0, padx=8, pady=8)
        global entry_cpf
        entry_cpf = tk.Entry(self, font=font_medium)
        entry_cpf.grid(row=3, column=1, padx=8, pady=8)

        tk.Label(self, text="ID do Usuário", font=font_medium).grid(row=4, column=0, padx=8, pady=8)
        global entry_id
        entry_id = tk.Entry(self, font=font_medium)
        entry_id.grid(row=4, column=1, padx=8, pady=8)

        tk.Label(self, text="Email", font=font_medium).grid(row=5, column=0, padx=8, pady=8)
        global entry_email
        entry_email = tk.Entry(self, font=font_medium)
        entry_email.grid(row=5, column=1, padx=8, pady=8)

        tk.Label(self, text="Senha", font=font_medium).grid(row=6, column=0, padx=8, pady=8)
        global entry_senha
        entry_senha = tk.Entry(self, show="*", font=font_medium)
        entry_senha.grid(row=6, column=1, padx=8, pady=8)

        tk.Label(self, text="Fixo", font=font_medium).grid(row=7, column=0, padx=8, pady=8)
        global entry_fixo
        entry_fixo = tk.Entry(self, font=font_medium)
        entry_fixo.grid(row=7, column=1, padx=8, pady=8)

        tk.Label(self, text="Celular", font=font_medium).grid(row=8, column=0, padx=8, pady=8)
        global entry_celular
        entry_celular = tk.Entry(self, font=font_medium)
        entry_celular.grid(row=8, column=1, padx=8, pady=8)

        # Botões
        btn_insert = tk.Button(self, text="Inserir Usuário", font=font_medium, command=insert_user)
        btn_insert.grid(row=9, column=0, pady=10)

        btn_query = tk.Button(self, text="Consultar Usuários", font=font_medium, command=query_users)
        btn_query.grid(row=9, column=1, pady=10)

        btn_delete = tk.Button(self, text="Remover Usuário", font=font_medium, command=delete_user)
        btn_delete.grid(row=9, column=2, pady=10)

        btn_voltar = tk.Button(self, text="Voltar", font=font_medium, command=lambda: controller.show_frame("MenuInicial"))
        btn_voltar.grid(row=10, column=1, pady=20)

# Página para gerenciar contas
class GerenciarContas(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        font_medium = ("Helvetica", 12)

        tk.Label(self, text="Gerenciar Contas", font=("Helvetica", 16)).grid(row=0, column=1, pady=20)

        tk.Label(self, text="ID Conta", font=font_medium).grid(row=1, column=0, padx=8, pady=8)
        global entry_idConta
        entry_idConta = tk.Entry(self, font=font_medium)
        entry_idConta.grid(row=1, column=1, padx=8, pady=8)

        tk.Label(self, text="Senha", font=font_medium).grid(row=2, column=0, padx=8, pady=8)
        global entry_senhaConta
        entry_senhaConta = tk.Entry(self, show="*", font=font_medium)
        entry_senhaConta.grid(row=2, column=1, padx=8, pady=8)

        tk.Label(self, text="Chaves PIX", font=font_medium).grid(row=3, column=0, padx=8, pady=8)
        global entry_chavesPIX
        entry_chavesPIX = tk.Entry(self, font=font_medium)
        entry_chavesPIX.grid(row=3, column=1, padx=8, pady=8)

        tk.Label(self, text="Saldo", font=font_medium).grid(row=4, column=0, padx=8, pady=8)
        global entry_saldoConta
        entry_saldoConta = tk.Entry(self, font=font_medium)
        entry_saldoConta.grid(row=4, column=1, padx=8, pady=8)

        tk.Label(self, text="Tipo de Conta", font=font_medium).grid(row=5, column=0, padx=8, pady=8)
        global entry_tipoConta
        entry_tipoConta = tk.Entry(self, font=font_medium)
        entry_tipoConta.grid(row=5, column=1, padx=8, pady=8)

        # Botões
        btn_insert_conta = tk.Button(self, text="Inserir Conta", font=font_medium, command=insert_conta)
        btn_insert_conta.grid(row=6, column=0, pady=10)

        btn_query_conta = tk.Button(self, text="Consultar Contas", font=font_medium, command=query_conta)
        btn_query_conta.grid(row=6, column=1, pady=10)

        btn_voltar = tk.Button(self, text="Voltar", font=font_medium, command=lambda: controller.show_frame("MenuInicial"))
        btn_voltar.grid(row=7, column=1, pady=20)

# Executa a aplicação
if __name__ == "__main__":
    app = EasyFinanceApp()
    app.mainloop()
