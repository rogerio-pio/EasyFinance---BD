import tkinter as tk
from tkinter import messagebox
import psycopg2

# Função para conectar ao banco
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

# Função para inserir um novo usuário
def insert_user():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            query = """INSERT INTO usuario (tipo, nomeCompleto, cpf, idUsuario, email, senha, fixo, celular) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            data = (entry_tipo.get(), entry_nome.get(), entry_cpf.get(), entry_id.get(), entry_email.get(), entry_senha.get(), entry_fixo.get(), entry_celular.get())
            cur.execute(query, data)
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário inserido com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir usuário: {e}")
        finally:
            conn.close()

# Função para consultar usuários
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

# Função para remover um usuário
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

# Interface gráfica
root = tk.Tk()
root.title("EasyFinance - Gerenciamento de Usuários")

# Labels e Entradas
tk.Label(root, text="Tipo").grid(row=0, column=0)
entry_tipo = tk.Entry(root)
entry_tipo.grid(row=0, column=1)

tk.Label(root, text="Nome Completo").grid(row=1, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1)

tk.Label(root, text="CPF").grid(row=2, column=0)
entry_cpf = tk.Entry(root)
entry_cpf.grid(row=2, column=1)

tk.Label(root, text="ID do Usuário").grid(row=3, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=3, column=1)

tk.Label(root, text="Email").grid(row=4, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=4, column=1)

tk.Label(root, text="Senha").grid(row=5, column=0)
entry_senha = tk.Entry(root, show="*")
entry_senha.grid(row=5, column=1)

tk.Label(root, text="Fixo").grid(row=6, column=0)
entry_fixo = tk.Entry(root)
entry_fixo.grid(row=6, column=1)

tk.Label(root, text="Celular").grid(row=7, column=0)
entry_celular = tk.Entry(root)
entry_celular.grid(row=7, column=1)

# Botões
btn_insert = tk.Button(root, text="Inserir Usuário", command=insert_user)
btn_insert.grid(row=8, column=0)

btn_query = tk.Button(root, text="Consultar Usuários", command=query_users)
btn_query.grid(row=8, column=1)

btn_delete = tk.Button(root, text="Remover Usuário", command=delete_user)
btn_delete.grid(row=8, column=2)

root.mainloop()
