import os
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

class Frete(Base):
    __tablename__ = 'fretes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    custo = Column(Numeric(10, 2))
    metodo = Column(String(255))
    livros = relationship('Livro', back_populates='frete')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
sessao = Session()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def adicionar_autor(nome, biografia):
    autor_novo = Autor(nome=nome, biografia=biografia)
    sessao.add(autor_novo)
    sessao.commit()
    print("Autor adicionado com sucesso")

def adicionar_editora(nome, endereco):
    editora_nova = Editora(nome=nome, endereco=endereco)
    sessao.add(editora_nova)
    sessao.commit()
    print("Editora adicionada com sucesso")

def adicionar_livro(titulo, sinopse, preco, autor_id, editora_id, frete_id):
    livro_novo = Livro(titulo=titulo, sinopse=sinopse, preco=preco, autor_id=autor_id, editora_id=editora_id, frete_id=frete_id)
    sessao.add(livro_novo)
    sessao.commit()
    print("Livro adicionado com sucesso")

def adicionar_frete(custo, metodo):
    frete_novo = Frete(custo=custo, metodo=metodo)
    sessao.add(frete_novo)
    sessao.commit()
    print("Frete adicionado com sucesso")

def consultar_autores():
    autores = sessao.query(Autor).all()
    for autor in autores:
        print(f"ID: {autor.id}, Nome: {autor.nome}, Biografia: {autor.biografia}")

def consultar_editoras():
    editoras = sessao.query(Editora).all()
    for editora in editoras:
        print(f"ID: {editora.id}, Nome: {editora.nome}, Endereço: {editora.endereco}")

def consultar_livros():
    livros = sessao.query(Livro).all()
    for livro in livros:
        print(f"ID: {livro.id}, Título: {livro.titulo}, Sinopse: {livro.sinopse}, Preço: {livro.preco}")

def consultar_fretes():
    fretes = sessao.query(Frete).all()
    for frete in fretes:
        print(f"ID: {frete.id}, Custo: {frete.custo}, Método: {frete.metodo}")

def atualizar_autor(id, nome=None, biografia=None):
    autor = sessao.query(Autor).filter_by(id=id).first()
    if autor:
        if nome:
            autor.nome = nome
        if biografia:
            autor.biografia = biografia
        sessao.commit()
        print("Autor atualizado com sucesso")
    else:
        print("Autor não encontrado")

def atualizar_editora(id, nome=None, endereco=None):
    editora = sessao.query(Editora).filter_by(id=id).first()
    if editora:
        if nome:
            editora.nome = nome
        if endereco:
            editora.endereco = endereco
        sessao.commit()
        print("Editora atualizada com sucesso")
    else:
        print("Editora não encontrada")

def atualizar_livro(id, titulo=None, sinopse=None, preco=None):
    livro = sessao.query(Livro).filter_by(id=id).first()
    if livro:
        if titulo:
            livro.titulo = titulo
        if sinopse:
            livro.sinopse = sinopse
        if preco is not None:
            livro.preco = preco
        sessao.commit()
        print("Livro atualizado com sucesso")
    else:
        print("Livro não encontrado")

def atualizar_frete(id, custo=None, metodo=None):
    frete = sessao.query(Frete).filter_by(id=id).first()
    if frete:
        if custo is not None:
            frete.custo = custo
        if metodo:
            frete.metodo = metodo
        sessao.commit()
        print("Frete atualizado com sucesso")
    else:
        print("Frete não encontrado")

def deletar_autor(id):
    autor = sessao.query(Autor).filter_by(id=id).first()
    if autor:
        sessao.delete(autor)
        sessao.commit()
        print("Autor deletado com sucesso")
    else:
        print("Autor não encontrado")

def deletar_editora(id):
    editora = sessao.query(Editora).filter_by(id=id).first()
    if editora:
        if editora.livros:
            print("Não é possível deletar a editora porque há livros associados a ela.")
        else:
            sessao.delete(editora)
            sessao.commit()
            print("Editora deletada com sucesso")
    else:
        print("Editora não encontrada")

def deletar_livro(id):
    livro = sessao.query(Livro).filter_by(id=id).first()
    if livro:
        sessao.delete(livro)
        sessao.commit()
        print("Livro deletado com sucesso")
    else:
        print("Livro não encontrado")

def deletar_frete(id):
    frete = sessao.query(Frete).filter_by(id=id).first()
    if frete:
        if frete.livros:
            print("Não é possível deletar o frete porque há livros associados a ele.")
        else:
            sessao.delete(frete)
            sessao.commit()
            print("Frete deletado com sucesso")
    else:
        print("Frete não encontrado")

def main():
    limpar_tela()
    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar Autor")
        print("2. Adicionar Editora")
        print("3. Adicionar Livro")
        print("4. Adicionar Frete")
        print("5. Consultar Autores")
        print("6. Consultar Editoras")
        print("7. Consultar Livros")
        print("8. Consultar Fretes")
        print("9. Atualizar Autor")
        print("10. Atualizar Editora")
        print("11. Atualizar Livro")
        print("12. Atualizar Frete")
        print("13. Deletar Autor")
        print("14. Deletar Editora")
        print("15. Deletar Livro")
        print("16. Deletar Frete")
        print("17. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            nome = input("Nome do Autor: ")
            biografia = input("Biografia do Autor: ")
            adicionar_autor(nome, biografia)
        elif opcao == '2':
            nome = input("Nome da Editora: ")
            endereco = input("Endereço da Editora: ")
            adicionar_editora(nome, endereco)
        elif opcao == '3':
            titulo = input("Título do Livro: ")
            sinopse = input("Sinopse do Livro: ")
            preco = float(input("Preço do Livro: "))
            autor_id = int(input("ID do Autor: "))
            editora_id = int(input("ID da Editora: "))
            frete_id = int(input("ID do Frete: "))
            adicionar_livro(titulo, sinopse, preco, autor_id, editora_id, frete_id)
        elif opcao == '4':
            custo = float(input("Custo do Frete: "))
            metodo = input("Método do Frete: ")
            adicionar_frete(custo, metodo)
        elif opcao == '5':
            consultar_autores()
        elif opcao == '6':
            consultar_editoras()
        elif opcao == '7':
            consultar_livros()
        elif opcao == '8':
            consultar_fretes()
        elif opcao == '9':
            id = int(input("ID do Autor a ser atualizado: "))
            nome = input("Novo Nome (deixe em branco para não alterar): ")
            biografia = input("Nova Biografia (deixe em branco para não alterar): ")
            atualizar_autor(id, nome if nome else None, biografia if biografia else None)
        elif opcao == '10':
            id = int(input("ID da Editora a ser atualizada: "))
            nome = input("Novo Nome (deixe em branco para não alterar): ")
            endereco = input("Novo Endereço (deixe em branco para não alterar): ")
            atualizar_editora(id, nome if nome else None, endereco if endereco else None)
        elif opcao == '11':
            id = int(input("ID do Livro a ser atualizado: "))
            titulo = input("Novo Título (deixe em branco para não alterar): ")
            sinopse = input("Nova Sinopse (deixe em branco para não alterar): ")
            preco = input("Novo Preço (deixe em branco para não alterar): ")
            atualizar_livro(id, titulo if titulo else None, sinopse if sinopse else None, float(preco) if preco else None)
        elif opcao == '12':
            id = int(input("ID do Frete a ser atualizado: "))
            custo = input("Novo Custo (deixe em branco para não alterar): ")
            metodo = input("Novo Método (deixe em branco para não alterar): ")
            atualizar_frete(id, float(custo) if custo else None, metodo if metodo else None)
        elif opcao == '13':
            id = int(input("ID do Autor a ser deletado: "))
            deletar_autor(id)
        elif opcao == '14':
            id = int(input("ID da Editora a ser deletada: "))
            deletar_editora(id)
        elif opcao == '15':
            id = int(input("ID do Livro a ser deletado: "))
            deletar_livro(id)
        elif opcao == '16':
            id = int(input("ID do Frete a ser deletado: "))
            deletar_frete(id)
        elif opcao == '17':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        input("Pressione Enter para continuar...")
        limpar_tela()

if __name__ == '__main__':
    main()