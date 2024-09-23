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
root.geometry("600x400")


# Labels e Entradas
font_medium = ("Helvetica", 12)

# Labels e Entradas com espaçamento moderado (padx e pady)
tk.Label(root, text="Tipo", font=font_medium).grid(row=0, column=0, padx=8, pady=8)
entry_tipo = tk.Entry(root, font=font_medium)
entry_tipo.grid(row=0, column=1, padx=8, pady=8)

tk.Label(root, text="Nome Completo", font=font_medium).grid(row=1, column=0, padx=8, pady=8)
entry_nome = tk.Entry(root, font=font_medium)
entry_nome.grid(row=1, column=1, padx=8, pady=8)

tk.Label(root, text="CPF", font=font_medium).grid(row=2, column=0, padx=8, pady=8)
entry_cpf = tk.Entry(root, font=font_medium)
entry_cpf.grid(row=2, column=1, padx=8, pady=8)

tk.Label(root, text="ID do Usuário", font=font_medium).grid(row=3, column=0, padx=8, pady=8)
entry_id = tk.Entry(root, font=font_medium)
entry_id.grid(row=3, column=1, padx=8, pady=8)

tk.Label(root, text="Email", font=font_medium).grid(row=4, column=0, padx=8, pady=8)
entry_email = tk.Entry(root, font=font_medium)
entry_email.grid(row=4, column=1, padx=8, pady=8)

tk.Label(root, text="Senha", font=font_medium).grid(row=5, column=0, padx=8, pady=8)
entry_senha = tk.Entry(root, show="*", font=font_medium)
entry_senha.grid(row=5, column=1, padx=8, pady=8)

tk.Label(root, text="Fixo", font=font_medium).grid(row=6, column=0, padx=8, pady=8)
entry_fixo = tk.Entry(root, font=font_medium)
entry_fixo.grid(row=6, column=1, padx=8, pady=8)

tk.Label(root, text="Celular", font=font_medium).grid(row=7, column=0, padx=8, pady=8)
entry_celular = tk.Entry(root, font=font_medium)
entry_celular.grid(row=7, column=1, padx=8, pady=8)

# Botões com tamanho mais moderado
btn_insert = tk.Button(root, text="Inserir Usuário", font=font_medium, width=12, height=1, command=insert_user)
btn_insert.grid(row=8, column=0, padx=10, pady=20)

btn_query = tk.Button(root, text="Consultar Usuários", font=font_medium, width=17, height=1, command=query_users)
btn_query.grid(row=8, column=1, padx=10, pady=20)

btn_delete = tk.Button(root, text="Remover Usuário", font=font_medium, width=17, height=1, command=delete_user)
btn_delete.grid(row=8, column=2, padx=10, pady=20)

root.mainloop()
