import sqlite3
import sqlite3 as sq
from tkinter import messagebox
from datetime import date
from customtkinter import *

conn_estoque = sq.connect('estoque.db')
cur_estoque = conn_estoque.cursor()

conn_catalogo = sq.connect('itens_de_cadastro.db')
cur_catalogo = conn_catalogo.cursor()

conn_log = sq.connect('log_posicao.db')
cur_log = conn_log.cursor()

conn_user = sq.connect('usuarios.db')
cur_user = conn_user.cursor()


class Posicao:

    def __init__(self, codigo_posicao):
        self._codigo_posicao = codigo_posicao
        self._itens = []

    # FUNÇÕES DE MANIPULAÇÃO DE POSIÇÃO;
    def __str__(self):
        print(f'Posição : {self._codigo_posicao}'
              f'Itens : {self._itens}')

    @staticmethod
    def retorna_catalogo_posicoes():

        catalogo_posicoes = []

        cur_estoque.execute(f'SELECT name FROM sqlite_master WHERE type="table"; ')
        resultado = cur_estoque.fetchall()

        for x in resultado:
            catalogo_posicoes.append(x[0])

        return catalogo_posicoes

    # Cria as tabelas de log de posição no banco de dados "log_posicao";
    @staticmethod
    def cria_log_posicao(codigo_posicao):
        cur_log.execute(f'''CREATE TABLE "{codigo_posicao}" ("codigo_item" TEXT NOT NULL, 
                                                             "transacao" TEXT NOT NULL, 
                                                             "quantidade" INTEGER NOT NULL,
                                                             "data" DATE NOT NULL,
                                                             "identificador" NUMERIC NOT NULL
                                                             ); ''')
        conn_log.commit()

    # Exclui as tabelas de log de posição no banco de dados "log_posicao";
    @staticmethod
    def exclui_log_posicao(codigo_posicao):
        cur_log.execute(f'DROP TABLE IF EXISTS {codigo_posicao}')
        conn_log.commit()

    @staticmethod
    def cria_posicao(codigo):
        # Cria a posição(ou tabela) no banco de dados "estoque";
        try:
            posicao_criada = Posicao(codigo)
            cur_estoque.execute(f'''CREATE TABLE "{posicao_criada._codigo_posicao.strip().upper()}" ("codigo" TEXT NOT NULL UNIQUE, 
                                                               "descricao" TEXT NOT NULL UNIQUE, 
                                                               "quantidade" INTEGER NOT NULL, 
                                                                PRIMARY KEY("codigo")); ''')
            conn_estoque.commit()

            # Cria a tabela com o nome da posição no banco de dados "log_posicao";
            Posicao.cria_log_posicao(posicao_criada._codigo_posicao)
        except sqlite3.OperationalError:
            messagebox.showerror("Erro", "Posição já cadastrada no sistema.")
    @staticmethod
    def exclui_posicao():
        # Exclui a tabela referente a posição no banco de dados "estoque";
        codigo_posicao = input('Digite o código da posição que deseja excluir.\n'
                               ' Digite: ')
        cur_estoque.execute(f'DROP TABLE IF EXISTS {codigo_posicao}')
        conn_estoque.commit()

        # Exclui a tabela referente ao log da posição no banco de dados "log_posicao";
        Posicao.exclui_log_posicao(codigo_posicao)


    # FUNÇÕES DE MANIPULAÇÃO DE ITENS;
    @staticmethod
    def aloca_item(codigo_item, quantidade_de_alocagem, nota_fiscal, codigo_posicao):

        # Realiza a seleção do item no banco de dados que possui todos os itens de uso cadastrados;
        cur_catalogo.execute(f'SELECT * FROM itens WHERE codigo = "{codigo_item}"')
        resultado_query = cur_catalogo.fetchone()

        # Cria um objeto do tipo "Item" que servirá de base para a alocagem do item na posição;
        item_de_alocagem = Item(resultado_query[0], resultado_query[1])

        # Cria um objeto "Posicao" que será responsável por representar a posição que alocará o item;
        posicao_de_alocagem = Posicao(codigo_posicao)

        # Verifica se a posição ja possui alguma quantidade deste item específico alocado nela;
        cur_estoque.execute(f'SELECT * FROM "{codigo_posicao}" WHERE codigo = "{item_de_alocagem.codigo_item}"; ')

        # Caso possua o item alocado;
        if cur_estoque.fetchone():

            # Realiza a soma das quantidades no banco de dados no registro do item específico;
            cur_estoque.execute(
                f'UPDATE "{posicao_de_alocagem._codigo_posicao}"'
                f'SET quantidade = quantidade + "{quantidade_de_alocagem}" '
                f'WHERE codigo = "{item_de_alocagem.codigo_item}"')

            conn_estoque.commit()
            cur_log.execute(
                f'INSERT INTO "{codigo_posicao}" (codigo_item, transacao, quantidade, data, identificador) VALUES '
                f'("{codigo_item}", "Adiciona", "{quantidade_de_alocagem}", "{date.today()}", "{nota_fiscal}"); ')
            conn_log.commit()
            messagebox.showinfo("Sucesso!", f"Item alocado com sucesso na posição {codigo_posicao}.")
        # caso não possua o item previamente alocado;
        else:

            # Insere o item na posição de alocagem selecionada;
            cur_estoque.execute(f'INSERT INTO "{posicao_de_alocagem._codigo_posicao}" '
                                f'(codigo, descricao, quantidade) VALUES '
                                f'("{item_de_alocagem.codigo_item}", '
                                f'"{item_de_alocagem.descricao}", '
                                f'"{quantidade_de_alocagem}"); ')
            conn_estoque.commit()
            conn_estoque.close()

            cur_log.execute(f'INSERT INTO "{codigo_posicao}" (codigo_item, transacao, quantidade, data, identificador) '
                            f'VALUES ("{codigo_item}", "Adiciona", "{quantidade_de_alocagem}", CURRENT_DATE, "{nota_fiscal}"); ')
            conn_log.commit()
            messagebox.showinfo("Sucesso!", f"Item alocado com sucesso na posição {codigo_posicao}.")
    @staticmethod
    def localiza_item(codigo_do_item: str) -> list:

        # Seleciono todas as tabelas existentes no meu banco de dados;
        cur_estoque.execute('SELECT name FROM sqlite_master WHERE type="table"; ')
        catalogo_posicoes = cur_estoque.fetchall()

        # Crio uma lista a qual armazenará todas as tabelas (ou posições) do meu banco de dados;
        posicoes_com_item = []

        # Realizo um loop por todo o catálogo de posições;
        for posicao in catalogo_posicoes:
            nome_posicao = posicao[0]
            cur_estoque.execute(f'SELECT * FROM "{nome_posicao}" WHERE codigo = "{codigo_do_item}"; ')
            tem_item = cur_estoque.fetchall()

            if tem_item:
                for x in tem_item:
                    posicao = {'posicao': nome_posicao,
                               'codigo': x[0],
                               'descricao': x[1],
                               'quantidade': x[2]}

                posicoes_com_item.append(posicao)
        return posicoes_com_item

    @staticmethod
    def localiza_posicao(codigo_posicao: str) -> dict:
        posicao = {"posicao": codigo_posicao,
                   "itens": []}
        cur_estoque.execute(f"SELECT * FROM '{codigo_posicao}'; ")
        resultado = cur_estoque.fetchall()

        if resultado:
            for it in resultado:
                item = {"codigo": it[0],
                        "descricao": it[1],
                        "quantidade": it[2]}
                posicao["itens"].append(item)

        return posicao

    @staticmethod
    def retira_item(codigo_posicao_retirada, codigo_do_item, quantidade_de_retirada, identificador):

        # Faço a verificação das informações do registro do item que desejo realizar a retirada;
        cur_estoque.execute(f'SELECT * FROM "{codigo_posicao_retirada}" WHERE codigo = "{codigo_do_item}"; ')
        resultado = cur_estoque.fetchone()

        # Realizo uma validação para apenas realizar a retirada de itens, caso a quantidade a ser retirada seja menor ou
        # igual a quantidade de itens que possui alocado a posição;
        if int(quantidade_de_retirada) <= int(resultado[2]):

            cur_estoque.execute(f'UPDATE "{codigo_posicao_retirada}" SET quantidade = quantidade - "{quantidade_de_retirada}" WHERE codigo = "{codigo_do_item}"; ')
            conn_estoque.commit()

            cur_estoque.execute(f'SELECT quantidade FROM "{codigo_posicao_retirada}" WHERE codigo = "{codigo_do_item}"; ')
            result = cur_estoque.fetchall()
            if result[0][0] == 0:
                cur_estoque.execute(f'DELETE FROM "{codigo_posicao_retirada}" WHERE codigo = "{codigo_do_item}"; ')
                conn_estoque.commit()

            # Operações do banco de dados log;
            cur_log.execute(f'INSERT INTO "{codigo_posicao_retirada}" (codigo_item, transacao, quantidade, data, identificador)'
                            f'VALUES ( "{codigo_do_item}", "Retira", "{quantidade_de_retirada}", CURRENT_DATE, "{identificador}"); ')
            conn_log.commit()

    @staticmethod
    def retorna_log_posicao(posicao):

        cur_log.execute(f'SELECT * FROM "{posicao.upper()}"')
        resultado = cur_log.fetchall()
        posicoes = []

        for registro in resultado:
            log = {'codigo': registro[0],
                   'transacao': registro[1],
                   'quantidade': registro[2],
                   'data': registro[3],
                   'identificador': registro[4]}
            posicoes.append(log)
        return posicoes

''' A classe "Item" somente opera suas funções no banco de dados "itens_de_cadastro". Sendo assim, qualquer atividade de 
manipulação de itens, seja transferência, retirada, exclusão ou localização de itens de uma posição, deve ser realizada através
de funções da classe "Posicao" '''


class Item:

    def __init__(self, codigo_item, descricao):
        self._codigo_item = codigo_item
        self._descricao = descricao
        self.quantidade = 0

    def __str__(self):
        return (f'Código : {self._codigo_item}\n'
                f'Descrição : {self._descricao}')

    # funções do banco de dados "Itens";
    @staticmethod
    def cadastra_item(codigo, descricao):

        if codigo and descricao:
            try:
                item_de_cadastro = Item(codigo, descricao)
                cur_catalogo.execute(
                    f'INSERT INTO itens VALUES ("{item_de_cadastro._codigo_item}", "{item_de_cadastro._descricao}"); ')
                conn_catalogo.commit()
                messagebox.showinfo("Sucesso", "Item cadastrado com sucesso.")

            except sq.IntegrityError:
                messagebox.showerror("Erro", "Erro no cadastro do item.")
        else:
            messagebox.showerror("Erro", "Impossível cadastrar itens sem código ou descrição.")

    @staticmethod
    def exclui_item(codigo):
        try:
            cur_catalogo.execute(f'DELETE FROM itens WHERE codigo = "{codigo}"; ')
            conn_catalogo.commit()

            if cur_catalogo.rowcount == 0:
                print('Nenhum item com esse código encontrado no sistema.')
            else:
                print('Item removido com sucesso.')

        except sq.Error as e:
            print(f'Erro ao remover o registro {e}')
            raise

        finally:
            if conn_catalogo:
                conn_catalogo.close()

    @staticmethod
    def retorna_catalogo_de_itens():
        itens = []
        try:
            cur_catalogo.execute('SELECT * FROM itens')
            catalogo = cur_catalogo.fetchall()
            for item in catalogo:
                item_atual = {"codigo":item[0],
                              "descricao":item[1]}
                itens.append(item_atual)
            return itens

        except:
            messagebox.showerror("Erro", "Erro no sistema")

    # Setters;
    @property
    def codigo_item(self):
        return self._codigo_item

    @property
    def descricao(self):
        return self._descricao


class Usuario:

    def __init__(self, login, senha):
        self._login = login
        self._senha = senha
        self._status = False

    @staticmethod
    def cadastra_usuario(login, senha):
        try:
            if not login or not senha:
                return messagebox.showerror("Erro", "Os campos de usuário e senha não podem ser cadastrados vazios")

            cur_user.execute(f'INSERT INTO login_senha ("login", "senha") VALUES ("{login}", "{senha}")')
            conn_user.commit()
            messagebox.showinfo("Sucesso!", "Usuário cadastrado com sucesso.")

        except sq.IntegrityError:
            messagebox.showerror("Erro", "Usuário não disponível")


    @staticmethod
    def loga_usuario(login, senha):

        cur_user.execute(f'SELECT * FROM login_senha WHERE ("login", "senha") = ("{login}", "{senha}")')
        resultado = cur_user.fetchall()
        if resultado:
            messagebox.showinfo('Sucesso', 'Login efetuado com sucesso')
            return True
        else:
            messagebox.showerror('Erro', 'Login ou Senha incorretos')
            return False

    def desloga_usuario(self):
        print('Logout efetuado com sucesso.')
        self._status = False

    def login(self):
        return self._login

    def senha(self):
        return self._senha
