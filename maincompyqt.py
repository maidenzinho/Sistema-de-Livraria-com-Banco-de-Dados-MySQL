import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QListWidget, QFormLayout, QComboBox
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

URL_BANCO = "mysql+pymysql://root:@localhost/tde"
engine = create_engine(URL_BANCO)
Base = declarative_base()

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    biografia = Column(Text)
    livros = relationship('Livro', back_populates='autor')

class Editora(Base):
    __tablename__ = 'editoras'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    endereco = Column(String(255))
    livros = relationship('Livro', back_populates='editora')

class Frete(Base):
    __tablename__ = 'fretes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    custo = Column(Numeric(10, 2))
    metodo = Column(String(255))
    livros = relationship('Livro', back_populates='frete')

class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    sinopse = Column(Text)
    preco = Column(Numeric(10, 2))
    autor_id = Column(Integer, ForeignKey('autores.id'), nullable=False)
    editora_id = Column(Integer, ForeignKey('editoras.id'), nullable=False)
    frete_id = Column(Integer, ForeignKey('fretes.id'))

    autor = relationship('Autor', back_populates='livros')
    editora = relationship('Editora', back_populates='livros')
    frete = relationship('Frete', back_populates='livros')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sessao = Session()

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Sistema de Gerenciamento de Livros')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.botao_autores = QPushButton('Gerenciar Autores', self)
        self.botao_editoras = QPushButton('Gerenciar Editoras', self)
        self.botao_livros = QPushButton('Gerenciar Livros', self)
        self.botao_fretes = QPushButton('Gerenciar Fretes', self)

        self.botao_autores.clicked.connect(self.abrir_autores)
        self.botao_editoras.clicked.connect(self.abrir_editoras)
        self.botao_livros.clicked.connect(self.abrir_livros)
        self.botao_fretes.clicked.connect(self.abrir_fretes)

        layout.addWidget(self.botao_autores)
        layout.addWidget(self.botao_editoras)
        layout.addWidget(self.botao_livros)
        layout.addWidget(self.botao_fretes)

        self.setLayout(layout)

    def abrir_autores(self):
        self.autor_window = AutorApp()
        self.autor_window.show()

    def abrir_editoras(self):
        self.editora_window = EditoraApp()
        self.editora_window.show()

    def abrir_livros(self):
        self.livro_window = LivroApp()
        self.livro_window.show()

    def abrir_fretes(self):
        self.frete_window = FreteApp()
        self.frete_window.show()

class AutorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Gerenciar Autores')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.nome_input = QLineEdit(self)
        self.biografia_input = QLineEdit(self)

        nome_label = QLabel('Nome do Autor:')
        biografia_label = QLabel('Biografia do Autor:')

        self.lista_autores = QListWidget(self)
        self.lista_autores.itemClicked.connect(self.preencher_campos)

        botao_adicionar = QPushButton('Adicionar Autor', self)
        botao_atualizar = QPushButton('Atualizar Autor', self)
        botao_deletar = QPushButton('Deletar Autor', self)

        botao_adicionar.clicked.connect(self.adicionar_autor)
        botao_atualizar.clicked.connect(self.atualizar_autor)
        botao_deletar.clicked.connect(self.deletar_autor)

        form_layout = QFormLayout()
        form_layout.addRow(nome_label, self.nome_input)
        form_layout.addRow(biografia_label, self.biografia_input)

        layout.addLayout(form_layout)
        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(QLabel('Lista de Autores:'))
        layout.addWidget(self.lista_autores)

        self.setLayout(layout)
        self.carregar_autores()

    def carregar_autores(self):
        self.lista_autores.clear()
        autores = sessao.query(Autor).all()
        for autor in autores:
            self.lista_autores.addItem(f"{autor.id} - {autor.nome}")

    def preencher_campos(self, item):
        autor_id = int(item.text().split(' ')[0])
        autor = sessao.query(Autor).filter_by(id=autor_id).first()

        if autor:
            self.nome_input.setText(autor.nome)
            self.biografia_input.setText(autor.biografia)

    def adicionar_autor(self):
        nome = self.nome_input.text()
        biografia = self.biografia_input.text()

        if nome:
            novo_autor = Autor(nome=nome, biografia=biografia)
            sessao.add(novo_autor)
            sessao.commit()
            self.carregar_autores()
            self.limpar_campos()
            QMessageBox.information(self, 'Sucesso', 'Autor adicionado com sucesso!')
        else:
            QMessageBox.warning(self, 'Erro', 'O nome do autor não pode ser vazio!')

    def atualizar_autor(self):
        item_selecionado = self.lista_autores.currentItem()

        if item_selecionado:
            autor_id = int(item_selecionado.text().split(' ')[0])
            autor = sessao.query(Autor).filter_by(id=autor_id).first()

            if autor:
                autor.nome = self.nome_input.text()
                autor.biografia = self.biografia_input.text()
                sessao.commit()
                self.carregar_autores()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Autor atualizado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Autor não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum autor selecionado!')

    def deletar_autor(self):
        item_selecionado = self.lista_autores.currentItem()

        if item_selecionado:
            autor_id = int(item_selecionado.text().split(' ')[0])
            autor = sessao.query(Autor).filter_by(id=autor_id).first()

            if autor:
                sessao.delete(autor)
                sessao.commit()
                self.carregar_autores()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Autor deletado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Autor não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum autor selecionado!')

    def limpar_campos(self):
        self.nome_input.clear()
        self.biografia_input.clear()

class EditoraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Gerenciar Editoras')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.nome_input = QLineEdit(self)
        self.endereco_input = QLineEdit(self)

        nome_label = QLabel('Nome da Editora:')
        endereco_label = QLabel('Endereço da Editora:')

        self.lista_editoras = QListWidget(self)
        self.lista_editoras.itemClicked.connect(self.preencher_campos)

        botao_adicionar = QPushButton('Adicionar Editora', self)
        botao_atualizar = QPushButton('Atualizar Editora', self)
        botao_deletar = QPushButton('Deletar Editora', self)

        botao_adicionar.clicked.connect(self.adicionar_editora)
        botao_atualizar.clicked.connect(self.atualizar_editora)
        botao_deletar.clicked.connect(self.deletar_editora)

        form_layout = QFormLayout()
        form_layout.addRow(nome_label, self.nome_input)
        form_layout.addRow(endereco_label, self.endereco_input)

        layout.addLayout(form_layout)
        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(QLabel('Lista de Editoras:'))
        layout.addWidget(self.lista_editoras)

        self.setLayout(layout)
        self.carregar_editoras()

    def carregar_editoras(self):
        self.lista_editoras.clear()
        editoras = sessao.query(Editora).all()
        for editora in editoras:
            self.lista_editoras.addItem(f"{editora.id} - {editora.nome}")

    def preencher_campos(self, item):
        editora_id = int(item.text().split(' ')[0])
        editora = sessao.query(Editora).filter_by(id=editora_id).first()

        if editora:
            self.nome_input.setText(editora.nome)
            self.endereco_input.setText(editora.endereco)

    def adicionar_editora(self):
        nome = self.nome_input.text()
        endereco = self.endereco_input.text()

        if nome:
            nova_editora = Editora(nome=nome, endereco=endereco)
            sessao.add(nova_editora)
            sessao.commit()
            self.carregar_editoras()
            self.limpar_campos()
            QMessageBox.information(self, 'Sucesso', 'Editora adicionada com sucesso!')
        else:
            QMessageBox.warning(self, 'Erro', 'O nome da editora não pode ser vazio!')

    def atualizar_editora(self):
        item_selecionado = self.lista_editoras.currentItem()

        if item_selecionado:
            editora_id = int(item_selecionado.text().split(' ')[0])
            editora = sessao.query(Editora).filter_by(id=editora_id).first()

            if editora:
                editora.nome = self.nome_input.text()
                editora.endereco = self.endereco_input.text()
                sessao.commit()
                self.carregar_editoras()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Editora atualizada com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Editora não encontrada!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhuma editora selecionada!')

    def deletar_editora(self):
        item_selecionado = self.lista_editoras.currentItem()

        if item_selecionado:
            editora_id = int(item_selecionado.text().split(' ')[0])
            editora = sessao.query(Editora).filter_by(id=editora_id).first()

            if editora:
                sessao.delete(editora)
                sessao.commit()
                self.carregar_editoras()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Editora deletada com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Editora não encontrada!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhuma editora selecionada!')

    def limpar_campos(self):
        self.nome_input.clear()
        self.endereco_input.clear()

class FreteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Gerenciar Fretes')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.custo_input = QLineEdit(self)
        self.metodo_input = QLineEdit(self)

        custo_label = QLabel('Custo do Frete:')
        metodo_label = QLabel('Método do Frete:')

        self.lista_fretes = QListWidget(self)
        self.lista_fretes.itemClicked.connect(self.preencher_campos)

        botao_adicionar = QPushButton('Adicionar Frete', self)
        botao_atualizar = QPushButton('Atualizar Frete', self)
        botao_deletar = QPushButton('Deletar Frete', self)

        botao_adicionar.clicked.connect(self.adicionar_frete)
        botao_atualizar.clicked.connect(self.atualizar_frete)
        botao_deletar.clicked.connect(self.deletar_frete)

        form_layout = QFormLayout()
        form_layout.addRow(custo_label, self.custo_input)
        form_layout.addRow(metodo_label, self.metodo_input)

        layout.addLayout(form_layout)
        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(QLabel('Lista de Fretes:'))
        layout.addWidget(self.lista_fretes)

        self.setLayout(layout)
        self.carregar_fretes()

    def carregar_fretes(self):
        self.lista_fretes.clear()
        fretes = sessao.query(Frete).all()
        for frete in fretes:
            self.lista_fretes.addItem(f"{frete.id} - {frete.metodo}")

    def preencher_campos(self, item):
        frete_id = int(item.text().split(' ')[0])
        frete = sessao.query(Frete).filter_by(id=frete_id).first()

        if frete:
            self.custo_input.setText(str(frete.custo))
            self.metodo_input.setText(frete.metodo)

    def adicionar_frete(self):
        custo = self.custo_input.text()
        metodo = self.metodo_input.text()

        if metodo and custo:
            novo_frete = Frete(custo=custo, metodo=metodo)
            sessao.add(novo_frete)
            sessao.commit()
            self.carregar_fretes()
            self.limpar_campos()
            QMessageBox.information(self, 'Sucesso', 'Frete adicionado com sucesso!')
        else:
            QMessageBox.warning(self, 'Erro', 'Os campos não podem ser vazios!')

    def atualizar_frete(self):
        item_selecionado = self.lista_fretes.currentItem()

        if item_selecionado:
            frete_id = int(item_selecionado.text().split(' ')[0])
            frete = sessao.query(Frete).filter_by(id=frete_id).first()

            if frete:
                frete.custo = self.custo_input.text()
                frete.metodo = self.metodo_input.text()
                sessao.commit()
                self.carregar_fretes()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Frete atualizado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Frete não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum frete selecionado!')

    def deletar_frete(self):
        item_selecionado = self.lista_fretes.currentItem()

        if item_selecionado:
            frete_id = int(item_selecionado.text().split(' ')[0])
            frete = sessao.query(Frete).filter_by(id=frete_id).first()

            if frete:
                sessao.delete(frete)
                sessao.commit()
                self.carregar_fretes()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Frete deletado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Frete não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum frete selecionado!')

    def limpar_campos(self):
        self.custo_input.clear()
        self.metodo_input.clear()

class LivroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Gerenciar Livros')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.titulo_input = QLineEdit(self)
        self.sinopse_input = QLineEdit(self)
        self.preco_input = QLineEdit(self)
        self.autor_input = QComboBox(self)
        self.editora_input = QComboBox(self)
        self.frete_input = QComboBox(self)

        titulo_label = QLabel('Título do Livro:')
        sinopse_label = QLabel('Sinopse do Livro:')
        preco_label = QLabel('Preço do Livro:')
        autor_label = QLabel('Autor:')
        editora_label = QLabel('Editora:')
        frete_label = QLabel('Frete:')

        self.lista_livros = QListWidget(self)
        self.lista_livros.itemClicked.connect(self.preencher_campos)

        botao_adicionar = QPushButton('Adicionar Livro', self)
        botao_atualizar = QPushButton('Atualizar Livro', self)
        botao_deletar = QPushButton('Deletar Livro', self)

        botao_adicionar.clicked.connect(self.adicionar_livro)
        botao_atualizar.clicked.connect(self.atualizar_livro)
        botao_deletar.clicked.connect(self.deletar_livro)

        form_layout = QFormLayout()
        form_layout.addRow(titulo_label, self.titulo_input)
        form_layout.addRow(sinopse_label, self.sinopse_input)
        form_layout.addRow(preco_label, self.preco_input)
        form_layout.addRow(autor_label, self.autor_input)
        form_layout.addRow(editora_label, self.editora_input)
        form_layout.addRow(frete_label, self.frete_input)

        layout.addLayout(form_layout)
        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(QLabel('Lista de Livros:'))
        layout.addWidget(self.lista_livros)

        self.setLayout(layout)
        self.carregar_livros()
        self.carregar_autores()
        self.carregar_editoras()
        self.carregar_fretes()

    def carregar_livros(self):
        self.lista_livros.clear()
        livros = sessao.query(Livro).all()
        for livro in livros:
            self.lista_livros.addItem(f"{livro.id} - {livro.titulo}")

    def carregar_autores(self):
        self.autor_input.clear()
        autores = sessao.query(Autor).all()
        for autor in autores:
            self.autor_input.addItem(f"{autor.id} - {autor.nome}")

    def carregar_editoras(self):
        self.editora_input.clear()
        editoras = sessao.query(Editora).all()
        for editora in editoras:
            self.editora_input.addItem(f"{editora.id} - {editora.nome}")

    def carregar_fretes(self):
        self.frete_input.clear()
        fretes = sessao.query(Frete).all()
        for frete in fretes:
            self.frete_input.addItem(f"{frete.id} - {frete.metodo}")

    def preencher_campos(self, item):
        livro_id = int(item.text().split(' ')[0])
        livro = sessao.query(Livro).filter_by(id=livro_id).first()

        if livro:
            self.titulo_input.setText(livro.titulo)
            self.sinopse_input.setText(livro.sinopse)
            self.preco_input.setText(str(livro.preco))

            index_autor = self.autor_input.findText(f"{livro.autor.id} - {livro.autor.nome}")
            index_editora = self.editora_input.findText(f"{livro.editora.id} - {livro.editora.nome}")
            index_frete = self.frete_input.findText(f"{livro.frete.id} - {livro.frete.metodo}" if livro.frete else "")

            self.autor_input.setCurrentIndex(index_autor)
            self.editora_input.setCurrentIndex(index_editora)
            self.frete_input.setCurrentIndex(index_frete)

    def adicionar_livro(self):
        titulo = self.titulo_input.text()
        sinopse = self.sinopse_input.text()
        preco = self.preco_input.text()

        autor_id = int(self.autor_input.currentText().split(' ')[0])
        editora_id = int(self.editora_input.currentText().split(' ')[0])
        frete_id = int(self.frete_input.currentText().split(' ')[0])

        if titulo and preco and autor_id and editora_id:
            novo_livro = Livro(titulo=titulo, sinopse=sinopse, preco=preco, autor_id=autor_id, editora_id=editora_id, frete_id=frete_id)
            sessao.add(novo_livro)
            sessao.commit()
            self.carregar_livros()
            self.limpar_campos()
            QMessageBox.information(self, 'Sucesso', 'Livro adicionado com sucesso!')
        else:
            QMessageBox.warning(self, 'Erro', 'Os campos obrigatórios não podem ser vazios!')

    def atualizar_livro(self):
        item_selecionado = self.lista_livros.currentItem()

        if item_selecionado:
            livro_id = int(item_selecionado.text().split(' ')[0])
            livro = sessao.query(Livro).filter_by(id=livro_id).first()

            if livro:
                livro.titulo = self.titulo_input.text()
                livro.sinopse = self.sinopse_input.text()
                livro.preco = self.preco_input.text()

                livro.autor_id = int(self.autor_input.currentText().split(' ')[0])
                livro.editora_id = int(self.editora_input.currentText().split(' ')[0])
                livro.frete_id = int(self.frete_input.currentText().split(' ')[0])

                sessao.commit()
                self.carregar_livros()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Livro atualizado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Livro não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum livro selecionado!')

    def deletar_livro(self):
        item_selecionado = self.lista_livros.currentItem()

        if item_selecionado:
            livro_id = int(item_selecionado.text().split(' ')[0])
            livro = sessao.query(Livro).filter_by(id=livro_id).first()

            if livro:
                sessao.delete(livro)
                sessao.commit()
                self.carregar_livros()
                self.limpar_campos()
                QMessageBox.information(self, 'Sucesso', 'Livro deletado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Livro não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum livro selecionado!')

    def limpar_campos(self):
        self.titulo_input.clear()
        self.sinopse_input.clear()
        self.preco_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())