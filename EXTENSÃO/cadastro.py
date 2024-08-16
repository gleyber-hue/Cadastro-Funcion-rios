from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
import pandas as pd

numero_id = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Gl90Th93@",
    database="cadastro_funcionarios"
)


def exportar_tabela_para_excel():
     cursor = banco.cursor()
     comando_SQL = "SELECT * FROM cadastro"
     cursor.execute(comando_SQL)
    

     colunas = [desc[0] for desc in cursor.description]
     dados = cursor.fetchall()
     df = pd.DataFrame(dados, columns=colunas)
     df.to_excel('exportar_tabela_para_excel.xlsx', index=False)

    
     print("EXCEL GERADO COM SUCESSO!")


def editar_dados():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM cadastro")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM cadastro WHERE id="+ str(valor_id))
    cadastro = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(cadastro[0][0]))
    tela_editar.lineEdit_2.setText(str(cadastro[0][1]))
    tela_editar.lineEdit_4.setText(str(cadastro[0][2]))
    tela_editar.lineEdit_5.setText(str(cadastro[0][3]))
    tela_editar.lineEdit_3.setText(str(cadastro[0][4]))
    tela_editar.lineEdit_6.setText(str(cadastro[0][5]))
    tela_editar.lineEdit_7.setText(str(cadastro[0][6]))
    tela_editar.lineEdit_8.setText(str(cadastro[0][7]))
    numero_id = valor_id


def salvar_valor_editado():
    global numero_id

    # ler dados do lineEdit
    nome = tela_editar.lineEdit_2.text()
    data = tela_editar.lineEdit_4.text()
    sexo = tela_editar.lineEdit_5.text()
    telefone = tela_editar.lineEdit_3.text()
    email = tela_editar.lineEdit_6.text()
    cargo = tela_editar.lineEdit_7.text()
    salario = tela_editar.lineEdit_8.text()

    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE cadastro SET nome = '{}', data = '{}', sexo = '{}', telefone ='{}', email ='{}', cargo ='{}', salario ='{}' WHERE id = {}".format(nome,data,sexo,telefone,email,cargo,salario,numero_id))
    banco.commit()
    #atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()    


def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM cadastro")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM cadastro WHERE id="+ str(valor_id))


def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM cadastro"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_funcionarios.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Funcionarios Cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10,750, "ID")
    pdf.drawString(70,750, "NOME")
    pdf.drawString(270,750, "DATA")
    pdf.drawString(380,750, "SEXO")
    pdf.drawString(470,750, "TELEFONE")
    pdf.drawString(600,750, "E-MAIL")
    pdf.drawString(770,750, "CARGO")
    pdf.drawString(900,750, "SALARIO")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(70,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(270,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(380,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(470,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(600,750 - y, str(dados_lidos[i][5]))
        pdf.drawString(770,750 - y, str(dados_lidos[i][6]))
        pdf.drawString(9000,750 - y, str(dados_lidos[i][7]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")


def funcao_principal():
    linha1 = cadastro.lineEdit.text()
    linha2 = cadastro.lineEdit_3.text()
    linha3 = cadastro.lineEdit_2.text()
    linha4 = cadastro.lineEdit_4.text()
    linha5 = cadastro.lineEdit_5.text()
    linha6 = cadastro.lineEdit_6.text()
    linha7 = cadastro.lineEdit_7.text()

    print("Nome",linha1)
    print("Data de Nascimento",linha2)
    print("Sexo",linha3)
    print("Telefone",linha4)
    print("E-mail",linha5)
    print("Cargo",linha6)
    print("Salario",linha7)
    print("Cadastro Realizado")

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO cadastro (nome, data, sexo, telefone, email, cargo, salario) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5),str(linha6),str(linha7))
    cursor.execute(comando_SQL,dados)         
    banco.commit()
    cadastro.lineEdit.setText("")
    cadastro.lineEdit_3.setText("")
    cadastro.lineEdit_2.setText("")
    cadastro.lineEdit_4.setText("")
    cadastro.lineEdit_5.setText("")
    cadastro.lineEdit_6.setText("")
    cadastro.lineEdit_7.setText("")
    
def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM cadastro"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(8)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 8):
           segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                   

app=QtWidgets.QApplication([])
cadastro=uic.loadUi("cadastro.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
tela_editar=uic.loadUi("menu_editar.ui")
cadastro.pushButton.clicked.connect(funcao_principal)
cadastro.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton_4.clicked.connect(exportar_tabela_para_excel)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)


cadastro.show()
app.exec()

#criando a tabela

""" CREATE TABLE cadastro (id INT NOT NULL AUTO_INCREMENT,
nome VARCHAR(100),
data DATE,
sexo ENUM('Masculino', 'Feminino'),
telefone VARCHAR(15),
email VARCHAR(100),
cargo VARCHAR(50),
salario DECIMAL(10, 2),
PRIMARY KEY (id)
);
"""
# inserindo registros na tabela

#INSERT INTO cadastro (nome, data, sexo, telefone, email, cargo, salario) VALUES ('Gleyber Lima Soares', '1990-11-29', 'Masculino', '34992014824', 'gleyberlimasoares@gmail.com', 'Analista de Sistemas', 2700.00);


