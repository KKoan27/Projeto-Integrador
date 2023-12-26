import sys
import typing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMessageBox, QLabel, QMainWindow
from PyQt5.uic import loadUi
import os
import time
import mysql.connector
from mysql.connector import Error

class SQLOps():
    def conectarBD(host, usuario, senha, DB, porta):
        try:
            connection = mysql.connector.connect(
                host=host,
                user=usuario,
                password=senha,
                database=DB,
                port=porta
            )
            print("Conexão estabelecida com sucesso!")
            return connection
        except Error as err:
            print("Erro ao estabelecer conexão com o banco de dados: ", err)
            exit()  
    

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.btnLogin.clicked.connect(self.loginfunction)
        self.txtSenha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.nivel = ""

    def loginfunction(self):
        nome = self.txtUsuario.text()
        senha = self.txtSenha.text()
        self.loginn(nome, senha, connection)

    def loginn(self,nome, senha, conn):
        connection = conn
        cursor = connection.cursor()
        
        sql = f"SELECT * FROM contas where usuario = '{nome}' and senha = '{senha}'"

        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        tup = results[0]
        tupList = list(tup)
        self.nivel = tupList[3]
        

        if results:
            self.gotomain()
        else:    
            
            self.labIncorreta.setText("Usuário ou senha incorretos!")

    def gotomain(self):
        mainselect = MainSelect(self.nivel)
        widget.addWidget(mainselect)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotomain2(self):
       
        mainselect = MainSelect("2")
        widget.addWidget(mainselect)
        widget.setCurrentIndex(widget.currentIndex() + 1)    


class MainSelect(QtWidgets.QMainWindow):
    def __init__(self, nivel):
        super(MainSelect, self).__init__()
        loadUi("MainSelect.ui", self)
        self.nivel = nivel
        if self.nivel == "1":
            self.btnCadastro.hide()
            self.btnUpdate.hide()
            self.btnDelete.hide()
        #Declaração da lista contendo todos os frames disponíveis para update
        self.frames = [self.frameAluno, self.frameApp, self.frameComputadores, self.frameContas, self.frameCurso, self.frameFuncionarios, self.framePacote_Internet, self.frameProjetor, self.frameSala_Lab, self.frameServidor, self.frameSetor, self.frameSwitch, self.frameWebsite]
        self.btnUpdate.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.comboTabelasJoin2.setEnabled(False)
        self.btnLogout.clicked.connect(self.logout)
        self.gotoConsultas()
        self.btnCancel.hide()
        self.btnSave.hide()
        self.comboTabelasJoin.hide()
        self.btnConsultarJoin.hide()
        self.comboTabelasJoin.hide()
        self.btnConsultarJoin.clicked.connect(lambda:self.mainJoin(connection, self.tableWidget))
        self.checkJoin.stateChanged.connect(self.displayJoin)
        self.btnConsultar.clicked.connect(self.consultar)
        self.btnCadastro.clicked.connect(self.gotoInsert)
        self.btnDelete.clicked.connect(self.obterID) 
        self.tableWidget.cellClicked.connect(self.obterDadosColunas)
        self.btnUpdate.clicked.connect(self.displayUpdate)
        self.btnConsultas.clicked.connect(self.gotoConsultas)
        self.btnCancel.clicked.connect(self.gotoConsultas)
        self.nomesColunas = []
        self.dadosColunas = []



    def consultar(self):
        self.nomesColunas = [] #Resetar coluna atual e dados atuais para evitar erros
        self.dadosColunas = []
        self.table = self.comboTabelas.currentText()
        self.read_BD(connection, self.table, self.tableWidget)

    def read_BD(self, conn, table, tableWidget):
        connection = conn
        cursor = connection.cursor()
        
        if self.txtBusca.text() == "":
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)
        else:
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            colunas = [column[0] for column in cursor.fetchall()]

            condicoes = [f"{coluna} LIKE %s" for coluna in colunas]  
            where = " OR ".join(condicoes) 

            sql = f"SELECT * FROM {table} WHERE {where}"

            comLike = f"%{self.txtBusca.text()}%"
             
            cursor.execute(sql, (comLike,)*len(colunas))
        results = cursor.fetchall()
        

        tableWidget.setRowCount(0)

        # Configurar o cabeçalho da tabela
        if results:
            tableWidget.setColumnCount(len(results[0]))
            tableWidget.setRowCount(len(results))
            headers = [description[0] for description in cursor.description]
            tableWidget.setHorizontalHeaderLabels(headers)
            cursor.close()

            # Preencher a tabela com os dados
            for row_num, row_data in enumerate(results):
                for col_num, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    tableWidget.setItem(row_num, col_num, item)    

    def mainJoin(self, conn, tableWidget):
        table1 = self.comboTabelasJoin.currentText()
        table2 = self.comboTabelasJoin2.currentText()
        connection = conn
        cursor = connection.cursor()

        sqlPrimaria = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = 'techmark' AND TABLE_NAME = '{table2}' AND CONSTRAINT_NAME = 'PRIMARY'"
        cursor.execute(sqlPrimaria)
        chavePrimaria = cursor.fetchone()
        chavePrimariaStr = str(chavePrimaria[0])

        
        sqlEstrangeira = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = 'techmark' AND TABLE_NAME = '{table1}' AND REFERENCED_TABLE_NAME IS NOT NULL"
        cursor.execute(sqlEstrangeira)
        chaveEstrangeira = cursor.fetchone()
        
        if chaveEstrangeira is not None:
            chaveEstrangeiraStr = str(chaveEstrangeira[0])
            

            try:
            
                sql = f"select * from {table1} join {table2} on {chavePrimariaStr} = {chaveEstrangeiraStr}" 
                cursor.execute(sql)
                results = cursor.fetchall()

                tableWidget.setRowCount(0)

            # Configurar o cabeçalho da tabela
                if results:
                    tableWidget.setColumnCount(len(results[0]))
                    tableWidget.setRowCount(len(results))
                    headers = [description[0] for description in cursor.description]
                    tableWidget.setHorizontalHeaderLabels(headers)
                    
                    

                # Preencher a tabela com os dados
                    for row_num, row_data in enumerate(results):
                        for col_num, col_data in enumerate(row_data):
                            item = QtWidgets.QTableWidgetItem(str(col_data))
                            tableWidget.setItem(row_num, col_num, item)

            except Error as err:
                str(err)
                txtErro = f"Erro ao realizar consulta relacionada: {err}"
                self.labOp.setText(txtErro)
                print(txtErro)             
        else:
            print("Ih")
        


        cursor.close()


    def displayJoin(self):
        if self.checkJoin.isChecked():
            self.comboTabelasJoin2.setEnabled(True)
            self.txtBusca.setEnabled(False)
            self.btnUpdate.setEnabled(False)
            self.btnDelete.setEnabled(False) 
            self.comboTabelasJoin.show()
            self.btnConsultarJoin.show()
            self.comboTabelasJoin.show()
            self.comboTabelas.hide()
            self.btnConsultar.hide()
        else:
            self.comboTabelasJoin2.setEnabled(False)
            self.txtBusca.setEnabled(True)
            self.btnUpdate.setEnabled(True)
            self.btnDelete.setEnabled(True)   
            self.comboTabelasJoin.hide()
            self.btnConsultarJoin.hide()
            self.comboTabelasJoin.hide()
            self.comboTabelas.show()
            self.btnConsultar.show()

    def deleteRow(self, table, idD, conn):
        
        resposta = self.caixaConfirma()

        if resposta == QMessageBox.Yes:
            try:
                connection = conn
                cursor = connection.cursor()

                sqlPrimaria = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = 'techmark' AND TABLE_NAME = '{table}' AND CONSTRAINT_NAME = 'PRIMARY'"
                cursor.execute(sqlPrimaria)
                chavePrimaria = cursor.fetchone()
                chavePrimariaStr = str(chavePrimaria[0])

                sql = f"DELETE FROM {table} WHERE {chavePrimariaStr} = {idD}"
            

                cursor.execute(sql)
                connection.commit()

                cursor.close()

                self.labOp.setText(f"O cadastro da tabela {table} com id {idD} foi deletado com sucesso")
            except Error as err:
                str(err)
                txtErro = f"Erro ao tentar apagar a linha {idD} da tabela {table}: {err}"
                self.labOp.setText(txtErro)
        else:
            self.labOp.setText("Exclusão cancelada.")        
    
    def obterID(self):
            
        linhaAtual = self.tableWidget.currentRow()
        if linhaAtual >= 0:
            idColuna = 0
            celula = self.tableWidget.item(linhaAtual, idColuna)
            if celula is not None:
                idD = celula.text()
                self.deleteRow(self.table, idD, connection)

    def obterDadosColunas(self, row, col):

        self.btnUpdate.setEnabled(True)
        self.btnDelete.setEnabled(True)

        if self.checkJoin.isChecked():
            self.btnUpdate.setEnabled(False)
            self.btnDelete.setEnabled(False)

        totalColunas = self.tableWidget.columnCount()

        self.nomesColunas = [self.tableWidget.horizontalHeaderItem(c).text() for c in range(totalColunas)]      #Comando para armazenar os nomes de colunas em uma lista

        self.dadosColunas = [self.tableWidget.item(row, c).text() for c in range(totalColunas)]                 #Comando para armazenar os dados em uma lista

        print(self.nomesColunas)
        print(self.dadosColunas)  

    def displayUpdate(self):
        self.tableWidget.hide()
        self.btnSave.show()
        self.btnCancel.show()
        self.comboTabelas.setEnabled(False)
        self.btnConsultar.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.btnSave.clicked.connect(lambda:self.mainUpdate(connection))  
        
        if self.table == "Aluno":
            self.frameAluno.show()
            self.txtANome.setText(self.dadosColunas[1])
            self.txtAIdade.setText(self.dadosColunas[2])
            self.txtAMatricula.setText(self.dadosColunas[3])
            self.txtACpf.setText(self.dadosColunas[4])
            self.txtARg.setText(self.dadosColunas[5])
            self.txtAIdCurso.setText(self.dadosColunas[6])

        elif self.table == "App":
            self.frameApp.show()
            self.txtAppNome.setText(self.dadosColunas[1])
            self.txtAppEstado.setText(self.dadosColunas[2])
            self.txtAppVers.setText(self.dadosColunas[3])
            self.txtAppVenc.setText(self.dadosColunas[4])

        elif self.table == "Computadores":
            self.frameComputadores.show()
            self.txtComNome.setText(self.dadosColunas[1])
            self.txtComConf.setText(self.dadosColunas[2])
            self.txtComEstado.setText(self.dadosColunas[3])
            self.txtComSala.setText(self.dadosColunas[4])
            self.txtComSetor.setText(self.dadosColunas[5])
            if self.dadosColunas[4] == "None":
                self.txtComSala.setText("null")
            elif self.dadosColunas[5] == "None":
                self.txtComSetor.setText("null")
            

        elif self.table == "Contas":
            self.frameContas.show()
            self.txtCoUser_2.setText(self.dadosColunas[1])
            self.txtCoSenha_2.setText(self.dadosColunas[2])
            self.txtCoNivel_2.setText(self.dadosColunas[3])
            self.txtCoIdFun.setText(self.dadosColunas[4])

        elif self.table == "Curso":
            self.frameCurso.show()
            self.txtCNome.setText(self.dadosColunas[1])
            self.txtCDuracao.setText(self.dadosColunas[2])
            self.txtCNMaterias.setText(self.dadosColunas[3])

        elif self.table == "Funcionarios":
            self.frameFuncionarios.show()
            self.txtFunNome.setText(self.dadosColunas[1])
            self.txtFunCpf.setText(self.dadosColunas[2])
            self.txtFunRg.setText(self.dadosColunas[3])
            self.txtFunFun.setText(self.dadosColunas[4])
            self.txtFunSalario.setText(self.dadosColunas[5])
            self.txtFunSetor.setText(self.dadosColunas[6])
            self.txtFunLeciona.setText(self.dadosColunas[7])
            if self.dadosColunas[7] == "None":
                self.txtFunLeciona.setText("null")
    
        elif self.table == "Pacote_Internet":
            self.framePacote_Internet.show()
            self.txtInterVeloci.setText(self.dadosColunas[1])
            self.txtInterEstado.setText(self.dadosColunas[2])

        elif self.table == "Projetor":
            self.frameProjetor.show()
            self.txtProjEstado.setText(self.dadosColunas[1])
            self.txtProjModelo.setText(self.dadosColunas[2])
            self.txtProjLocal.setText(self.dadosColunas[3])      
            
        elif self.table == "Sala_Lab":
            self.frameSala_Lab.show()
            self.txtSalaAndar.setText(self.dadosColunas[1])
            self.txtSalaNum.setText(self.dadosColunas[2])
            self.txtSalaTipo.setText(self.dadosColunas[3])
            self.txtSalaCap.setText(self.dadosColunas[4])
            self.txtSalaReserva.setText(self.dadosColunas[5])
            self.txtSalaQuantPC.setText(self.dadosColunas[6])

        elif self.table == "Servidor":
            self.frameServidor.show()
            self.txtServNome.setText(self.dadosColunas[1])
            self.txtServEstado.setText(self.dadosColunas[2])
            self.txtServCap.setText(self.dadosColunas[3])
        
        elif self.table == "Setor":
            self.frameSetor.show()
            self.txtSetorNome.setText(self.dadosColunas[1])
            self.txtSetorAndar.setText(self.dadosColunas[2])
            self.txtSetorNFun.setText(self.dadosColunas[3])
            self.txtSetorNPcs.setText(self.dadosColunas[4])
            
        elif self.table == "Switch":
            self.frameSwitch.show()
            self.txtSwitchLocal.setText(self.dadosColunas[1])
            self.txtSwitchEstado.setText(self.dadosColunas[2]) 

        elif self.table == "Website":
            self.frameWebsite.show()
            self.txtWebNome.setText(self.dadosColunas[1])
            self.txtWebEstado.setText(self.dadosColunas[2]) 
            self.txtWebVers.setText(self.dadosColunas[3])       

    def mainUpdate(self, conn):
       
        resposta = self.caixaConfirma()
        
        
        if resposta == QMessageBox.Yes:
            try:
                    connection = conn
                    cursor = connection.cursor()

                    if self.table == "Aluno":
                        nome = self.txtANome.text()
                        idade = self.txtAIdade.text()
                        matricula = self.txtAMatricula.text()
                        cpf = self.txtACpf.text()
                        rg = self.txtARg.text()
                        estuda = self.txtAIdCurso.text()

                        sql = f"update aluno set nome='{nome}', idade={idade}, matricula='{matricula}', cpf='{cpf}', rg='{rg}', estuda={estuda} where id_aluno = {self.dadosColunas[0]}"

                    elif self.table == "App":
                        
                        nome = self.txtAppNome.text()
                        estado = self.txtAppEstado.text()
                        versao = self.txtAppVers.text()
                        vencimento = self.txtAppVenc.text()

                        sql = f"update app set nome='{nome}', estado='{estado}', versão='{versao}', vencimento_licença='{vencimento}' where id_app = {self.dadosColunas[0]}"

                    elif self.table == "Computadores":
                        
                        nome = self.txtComNome.text()
                        config = self.txtComConf.text()
                        estado = self.txtComEstado.text()
                        sala = self.txtComSala.text()
                        setor = self.txtComSetor.text()

                        sql = f"update computadores set nome_pc='{nome}', conf='{config}', estado='{estado}', localização_sala_lab={sala}, localização_setor = {setor} where id_computadores = {self.dadosColunas[0]}"

                    elif self.table == "Contas":

                        user = self.txtCoUser_2.text()
                        senha = self.txtCoSenha_2.text()
                        nivel = self.txtCoNivel_2.text()
                        fId = self.txtCoIdFun.text()
                        
                        sql = f"update contas set usuario='{user}', senha='{senha}', nivel='{nivel}', funcionario_id='{fId}'  where id_contas = {self.dadosColunas[0]}"

                    elif self.table == "Curso":

                        nome = self.txtCNome.text()
                        tempo = self.txtCDuracao.text()
                        nMaterias = self.txtCNMaterias.text()
                        
                        sql = f"update curso set nome='{nome}', tempo='{tempo}', n°_materias='{nMaterias}'  where id_curso = {self.dadosColunas[0]}"    
                    
                    elif self.table == "Funcionarios":
                        
                        nome = self.txtFunNome.text()
                        cpf = self.txtFunCpf.text()
                        rg = self.txtFunRg.text()
                        funcao = self.txtFunFun.text()
                        salario = self.txtFunSalario.text()
                        setor = self.txtFunSetor.text()
                        leciona = self.txtFunLeciona.text()


                        sql = f"update funcionarios set nome='{nome}', cpf='{cpf}', rg='{rg}', função='{funcao}', salarioRS = {salario}, leciona = {leciona} where id_funcionarios = {self.dadosColunas[0]}"
                    
                    elif self.table == "Pacote_Internet":
                        
                        velocidade = self.txtInterVeloci.text()
                        estado = self.txtInterEstado.text()

                        sql = f"update pacote_internet set velocidade='{velocidade}', estado='{estado}' where id_pacote_internet = {self.dadosColunas[0]}"

                    elif self.table == "Projetor":
                        
                        estado = self.txtProjEstado.text()
                        modelo = self.txtProjModelo.text()
                        local = self.txtProjLocal.text()

                        sql = f"update projetor set estado='{estado}', modelo='{modelo}', localização = '{local}' where id_projetor = {self.dadosColunas[0]}"

                    elif self.table == "Sala_Lab":
                        
                        andar = self.txtSalaAndar.text()
                        numero = self.txtSalaNum.text()
                        tipo = self.txtSalaTipo.text()
                        capacidade = self.txtSalaCap.text()
                        reserva = self.txtSalaReserva.text()
                        quantPc = self.txtSalaQuantPC.text()


                        sql = f"update sala_lab set andar='{andar}', numero={numero}, tipo='{tipo}', capacidade='{capacidade}', reserva = '{reserva}', quant_pc = {quantPc} where id_sala_lab = {self.dadosColunas[0]}"

                    elif self.table == "Servidor":
                        
                        nome = self.txtServNome.text()
                        estado = self.txtServEstado.text()
                        capacidade = self.txtServCap.text()

                        sql = f"update servidor set nome='{nome}', estado='{estado}', capacidade = '{capacidade}' where id_servidor = {self.dadosColunas[0]}"

                    elif self.table == "Setor":
                        
                        nome = self.txtSetorNome.text()
                        andar = self.txtSetorAndar.text()
                        numeroF = self.txtSetorNFun.text()
                        numeroP = self.txtSetorNPcs.text()

                        sql = f"update setor set nome='{nome}', andar='{andar}', quant_funcionarios = {numeroF}, quant_pc = {numeroP} where id_setor = {self.dadosColunas[0]}"

                    elif self.table == "Switch":
                        
                        local = self.txtSwitchLocal.text()
                        estado = self.txtSwitchEstado.text()

                        sql = f"update switch set localização='{local}', estado='{estado}' where id_switch = {self.dadosColunas[0]}"

                    elif self.table == "Website":
                        
                        nome = self.txtWebNome.text()
                        estado = self.txtWebEstado.text()
                        versao = self.txtWebVers.text()

                        sql = f"update website set nome='{nome}', estado='{estado}', versão = '{versao}' where id_website = {self.dadosColunas[0]}"

                    cursor.execute(sql)
                    connection.commit()

                    cursor.close()

                    self.labOp.setText(f"Alteração no id {self.dadosColunas[0]} na tabela {self.table} foi realizada com sucesso!")
            except Error as err:
                    str(err)
                    txtErro = f"Erro ao tentar aalterar a linha {self.dadosColunas[0]} da tabela {self.table}: {err}"
                    self.labOp.setText(txtErro)
        else:
                self.labOp.setText("Alteração cancelada")


    def caixaConfirma(self):
        resposta = QMessageBox.question(
            self,
            'Confirmar Alteração',
            f'Tem certeza que deseja alterar o registro com ID {self.dadosColunas[0]} da tabela {self.table}?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        
        
        return resposta
    
    
        

    def gotoConsultas(self):
        self.tableWidget.show()
        self.btnSave.hide()
        self.btnCancel.hide()
        self.comboTabelas.setEnabled(True)
        self.btnConsultar.setEnabled(True)
        for f in self.frames:
            f.hide()
        

    def gotoInsert(self):
        maininsert = MainInsert()
        widget.addWidget(maininsert)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

    def logout(self):
        logout = Login()
        widget.addWidget(logout)
        widget.setCurrentIndex(widget.currentIndex() + 1)
                 




class MainInsert(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainInsert, self).__init__()
        loadUi("MainInsert.ui", self)

        self.btnConsultas.clicked.connect(Login.gotomain2)                       #Função para voltar à tela de consulta
        self.frames = [self.frameAluno, self.frameApp, self.frameComputadores, self.frameContas, self.frameCurso, self.frameFuncionarios, self.framePacote_Internet, self.frameProjetor, self.frameSala_Lab, self.frameServidor, self.frameSetor, self.frameSwitch, self.frameWebsite]
        self.comboTabelas.currentIndexChanged.connect(self.visibilidade)        #Executa a função visibilidade toda vez que a opção da combo box é alterada
        self.visibilidade()                                                     #Execução inicial da função de visibilidade
        self.txtComSala.textChanged.connect(self.salaSetor)
        self.txtComSetor.textChanged.connect(self.salaSetor)

        self.btnInsert.clicked.connect(lambda:self.inserirCadastro(connection)) #Uso da função lambda para que possam ser passados parâmetros na função do botão
       

    def salaSetor(self):
        if self.txtComSala.text() != "":
            self.txtComSetor.setEnabled(False)
           
        else:
            self.txtComSetor.setEnabled(True)

        if self.txtComSetor.text() != "":
            self.txtComSala.setEnabled(False)
           
        else:
            self.txtComSala.setEnabled(True)
    def inserirCadastro(self, conn):
        atual = self.comboTabelas.currentText() 
        resposta = self.caixaConfirma()
        if resposta == QMessageBox.Yes:
            try:
                connection = conn
                cursor = connection.cursor()
                if atual == "Aluno":
                    nome = self.txtANome.text()
                    idade = self.txtAIdade.text()
                    matricula = self.txtAMatricula.text()
                    cpf = self.txtACpf.text()
                    rg = self.txtARg.text()
                    curso = self.txtAIdCurso.text()

                    sql = F"INSERT INTO ALUNO VALUES (null, '{nome}', {idade}, '{matricula}', '{cpf}', '{rg}', {curso})"

                elif atual == "App":
                    nome = self.txtAppNome.text()
                    estado = self.txtAppEstado.text()
                    versao = self.txtAppVers.text()  
                    vencimento = self.txtAppVenc.text()

                    sql = F"INSERT INTO App VALUES (null, '{nome}', '{estado}', '{versao}', '{vencimento}')"

                elif atual == "Computadores":
                    nome = self.txtComNome.text()
                    config = self.txtComConf.text()
                    estado = self.txtComEstado.text()
                    sala = self.txtComSala.text()
                    setor = self.txtComSetor.text() 
                    if setor != "":
                        sql = F"INSERT INTO computadores VALUES (null, '{nome}', '{config}', '{estado}', null, {setor})"
                    elif sala != "":
                        sql = F"INSERT INTO computadores VALUES (null, '{nome}', '{config}', '{estado}', {sala}, null)"
                       

                    
                    
                
                elif atual == "Contas":
                    user = self.txtCoUser_2.text()
                    senha = self.txtCoSenha_2.text()
                    nivel = self.txtCoNivel_2.text()
                    funcionario = self.txtCoIdFun.text()   

                    sql = F"INSERT INTO contas VALUES (null, '{user}', '{senha}', '{nivel}', {funcionario})"

                elif atual == "Curso":
                    nome = self.txtCNome.text()
                    tempo = self.txtCDuracao.text()
                    materias = self.txtCNMaterias.text()  

                    sql = F"INSERT INTO curso VALUES (null, '{nome}', '{tempo}', {materias})"
                
                elif atual == "Funcionarios":
                    nome = self.txtFunNome.text()
                    cpf = self.txtFunCpf.text()
                    rg = self.txtFunRg.text()
                    funcao = self.txtFunFun.text() 
                    salario = self.txtFunSalario.text() 
                    setor = self.txtFunSetor.text() 
                    leciona = self.txtFunLeciona.text() 
                    if leciona != "":
                        sql = F"INSERT INTO funcionarios VALUES (null, '{nome}', '{cpf}', '{rg}', '{funcao}', {salario}, {setor}, {leciona})"
                    else:     
                        sql = F"INSERT INTO funcionarios VALUES (null, '{nome}', '{cpf}', '{rg}', '{funcao}', {salario}, {setor}, null)"
                


                elif atual == "Pacote_Internet":
                    velocidade = self.txtInterVeloci.text()
                    estado = self.txtInterEstado.text() 

                    sql = F"INSERT INTO pacote_internet VALUES (null, '{velocidade}', '{estado}')"

                elif atual == "Projetor":
                    estado = self.txtProjEstado.text()
                    modelo = self.txtProjModelo.text()
                    local = self.txtProjLocal.text()  

                    sql = F"INSERT INTO projetor VALUES (null, '{estado}', '{modelo}', {local})"

                elif atual == "Sala_Lab":
                    andar = self.txtSalaAndar.text()
                    numero = self.txtSalaNum.text()
                    tipo = self.txtSalaTipo.text()
                    capacidade = self.txtSalaCap.text() 
                    reserva = self.txtSalaReserva.text() 
                    quantidadeP = self.txtSalaQuantPC.text()   

                    sql = F"INSERT INTO sala_lab VALUES (null, '{andar}', {numero}, '{tipo}', '{capacidade}', '{reserva}', {quantidadeP})"

                elif atual == "Servidor":
                    nome = self.txtServNome.text()
                    estado = self.txtServEstado.text()
                    capacidade = self.txtServCap.text()  

                    sql = F"INSERT INTO servidor VALUES (null, '{nome}', '{estado}', '{capacidade}')"

                elif atual == "Setor":
                    nome = self.txtSetorNome.text()
                    andar = self.txtSetorAndar.text()
                    quantF = self.txtSetorNFun.text() 
                    quantP = self.txtSetorNPcs.text() 

                    sql = F"INSERT INTO setor VALUES (null, '{nome}', '{andar}', {quantF}, {quantP})"

                elif atual == "Switch":
                    local = self.txtSwitchLocal.text()
                    estado = self.txtSwitchEstado.text()  

                    sql = F"INSERT INTO switch VALUES (null, '{local}', '{estado}')"

                elif atual == "Website":
                    nome = self.txtWebNome.text()
                    estado = self.txtWebEstado.text()
                    versao = self.txtWebVers.text()  

                    sql = F"INSERT INTO website VALUES (null, '{nome}', '{estado}', '{versao}')"

                cursor.execute(sql)
                connection.commit()
                id = cursor.lastrowid

                cursor.close()

                self.labOp.setText(f"O cadastro do id {id} na tabela {atual} foi realizado com sucesso!")

            except Error as err:
                str(err)
                txtErro = f"Erro ao tentar realizar o cadastro: {err}"
                self.labOp.setText(txtErro)   
           
    def visibilidade(self):
        for frame in self.frames:                                               #Aqui estamos escondendo todos os frames para que somente a opção selecionada apareça
            frame.hide()   
        atual = self.comboTabelas.currentText()                                 #Variável que contem o texto da opção selecionada pela combo box
        if atual == "Aluno":                                                    #Aqui podemos adicionar as opções do menu para que elas apareçam quando selecionadas
            self.frameAluno.show()
        elif atual == "App":   
            self.frameApp.show()
        elif atual == "Computadores":
            self.frameComputadores.show()
        elif atual == "Contas":
            self.frameContas.show()
        elif atual == "Curso":
            self.frameCurso.show()
        elif atual == "Funcionarios":
            self.frameFuncionarios.show()
        elif atual == "Pacote_Internet":
            self.framePacote_Internet.show()
        elif atual == "Projetor":
            self.frameProjetor.show()
        elif atual == "Sala_Lab":
            self.frameSala_Lab.show()
        elif atual == "Servidor":
            self.frameServidor.show()
        elif atual == "Setor":
            self.frameSetor.show()
        elif atual == "Switch":
            self.frameSwitch.show()
        elif atual == "Website":
            self.frameWebsite.show()
    def caixaConfirma(self):
        resposta = QMessageBox.question(
            self,
            'Confirmar Alteração',
            f'Tem certeza que deseja realizar o cadastro na tabela {self.comboTabelas.currentText()}?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        return resposta

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)


# Conectar ao banco de dados
connection = SQLOps.conectarBD("localhost", "root", "luan", "techmark", "3306")

widget.show()
app.exec_()
