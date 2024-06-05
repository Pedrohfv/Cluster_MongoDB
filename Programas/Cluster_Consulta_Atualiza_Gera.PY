import pymongo
import random
import string
from faker import Faker
from pymongo import MongoClient
import time

# Conectar ao servidor MongoDB (ajuste a URL de conexão conforme necessário)
conexao = MongoClient("mongodb://localhost:27017/")
admin_db = conexao.admin

def criar_indice_hashed(collection):
    collection.create_index([("id_produto", "hashed")])
    print(f"Índice 'id_produto' criado na coleção {collection.name}")

def shard_collection(nome_banco, nome_colecao):
    comando = {
        'shardCollection': f"{nome_banco}.{nome_colecao}",
        'key': {'id_produto': 'hashed'}
    }
    admin_db.command(comando)
    print(f"Shard configurado para {nome_banco}.{nome_colecao}")

def gerar_numero_lote():
    letras = ''.join(random.choices(string.ascii_uppercase, k=5))  # Gera 5 letras maiúsculas aleatórias
    numeros = ''.join(random.choices(string.digits, k=5))  # Gera 5 números aleatórios
    return letras + numeros

def gerar_dados():
    faker = Faker()

    # Perguntar ao usuário se deseja adicionar uma nova filial ou usar uma existente
    novo = input("Deseja adicionar uma nova filial (S/N)? ").lower()

    if novo == "s":
        # Verificar o número da última filial existente e criar o nome da nova filial
        filiais_existentes = [db for db in conexao.list_database_names() if "varejo_filial_" in db]
        if filiais_existentes:
            numero_ultima_filial = max(int(f.split("_")[-1]) for f in filiais_existentes)
        else:
            numero_ultima_filial = 0
        nome_banco = f"varejo_filial_{numero_ultima_filial + 1}"
        print(f"Nova filial criada: {nome_banco}")

        # Definir o nome da coleção com base na filial
        nome_colecao = f"estoque_produtos_filial_{numero_ultima_filial + 1}"

    else:
        # Perguntar ao usuário qual banco de dados existente deseja usar
        print("Escolha o banco de dados onde deseja inserir os dados (digite o número correspondente): ")
        filiais_existentes = [db for db in conexao.list_database_names() if "varejo_filial_" in db]
        for i, nome in enumerate(filiais_existentes, start=1):
            print(f"{i}. {nome}")

        opcao = int(input("Opção: "))

        if 1 <= opcao <= len(filiais_existentes):
            nome_banco = filiais_existentes[opcao - 1]
            print(f"Banco de dados selecionado: {nome_banco}")
        else:
            print("Opção inválida.")
            return

        # Definir o nome da coleção com base na filial
        numero_filial = int(nome_banco.split("_")[-1])
        nome_colecao = f"estoque_produtos_filial_{numero_filial}"

    # Acessar o banco de dados escolhido
    db = conexao[nome_banco]

    # Criar ou acessar a coleção com o nome definido
    collection = db[nome_colecao]

    # Verificar se a coleção existe
    if nome_colecao not in db.list_collection_names():
        print("A coleção não existe. Criando...")
        criar_indice_hashed(collection)
        shard_collection(nome_banco, nome_colecao)
    
    # Lista de 300 itens de supermercado
    itens_supermercado = [
        # Bebidas
        ("Água mineral", "Bebidas"), ("Refrigerante de cola", "Bebidas"), ("Refrigerante de laranja", "Bebidas"),
        ("Suco de laranja", "Bebidas"), ("Suco de uva", "Bebidas"), ("Cerveja", "Bebidas"), ("Vinho tinto", "Bebidas"),
        ("Vinho branco", "Bebidas"), ("Whisky", "Bebidas"), ("Vodka", "Bebidas"), ("Cachaça", "Bebidas"), ("Chá preto", "Bebidas"),
        ("Chá verde", "Bebidas"), ("Café", "Bebidas"), ("Achocolatado", "Bebidas"), ("Água de coco", "Bebidas"),
        ("Leite de soja", "Bebidas"), ("Suco de maçã", "Bebidas"), ("Suco de abacaxi", "Bebidas"), ("Energético", "Bebidas"),
        
        # Frios
        ("Presunto", "Frios"), ("Queijo mussarela", "Frios"), ("Queijo prato", "Frios"), ("Mortadela", "Frios"),
        ("Salame", "Frios"), ("Peito de peru", "Frios"), ("Queijo parmesão", "Frios"), ("Queijo provolone", "Frios"),
        ("Queijo gorgonzola", "Frios"), ("Requeijão", "Frios"), ("Manteiga", "Frios"), ("Margarina", "Frios"),
        ("Patê de atum", "Frios"), ("Patê de presunto", "Frios"), ("Ricota", "Frios"), ("Cream cheese", "Frios"),
        ("Queijo cottage", "Frios"), ("Queijo brie", "Frios"), ("Queijo camembert", "Frios"), ("Patê de frango", "Frios"),
        
        # Laticínios
        ("Leite integral", "Laticínios"), ("Leite desnatado", "Laticínios"), ("Leite semidesnatado", "Laticínios"),
        ("Iogurte natural", "Laticínios"), ("Iogurte de morango", "Laticínios"), ("Iogurte de pêssego", "Laticínios"),
        ("Iogurte grego", "Laticínios"), ("Creme de leite", "Laticínios"), ("Leite condensado", "Laticínios"),
        ("Leite em pó", "Laticínios"), ("Queijo ralado", "Laticínios"), ("Chantilly", "Laticínios"), ("Manteiga com sal", "Laticínios"),
        ("Manteiga sem sal", "Laticínios"), ("Coalhada", "Laticínios"), ("Iogurte com mel", "Laticínios"),
        ("Iogurte com granola", "Laticínios"), ("Bebida láctea", "Laticínios"), ("Kefir", "Laticínios"),
        ("Leite fermentado", "Laticínios"),
        
        # Mercearia
        ("Arroz branco", "Mercearia"), ("Arroz integral", "Mercearia"), ("Feijão preto", "Mercearia"), ("Feijão carioca", "Mercearia"),
        ("Macarrão espaguete", "Mercearia"), ("Macarrão penne", "Mercearia"), ("Macarrão parafuso", "Mercearia"),
        ("Farinha de trigo", "Mercearia"), ("Farinha de mandioca", "Mercearia"), ("Farinha de milho", "Mercearia"),
        ("Açúcar refinado", "Mercearia"), ("Açúcar mascavo", "Mercearia"), ("Sal", "Mercearia"), ("Óleo de soja", "Mercearia"),
        ("Óleo de canola", "Mercearia"), ("Óleo de girassol", "Mercearia"), ("Azeite de oliva", "Mercearia"), ("Vinagre de maçã", "Mercearia"),
        ("Vinagre balsâmico", "Mercearia"), ("Molho de tomate", "Mercearia"), ("Molho de pimenta", "Mercearia"), ("Mostarda", "Mercearia"),
        ("Ketchup", "Mercearia"), ("Maionese", "Mercearia"), ("Molho barbecue", "Mercearia"), ("Shoyu", "Mercearia"),
        ("Molho inglês", "Mercearia"), ("Atum enlatado", "Mercearia"), ("Sardinha enlatada", "Mercearia"), ("Milho enlatado", "Mercearia"),
        ("Ervilha enlatada", "Mercearia"), ("Palmito", "Mercearia"), ("Azeitona verde", "Mercearia"), ("Azeitona preta", "Mercearia"),
        ("Pepino em conserva", "Mercearia"), ("Champignon", "Mercearia"), ("Massa para pastel", "Mercearia"), ("Massa para pizza", "Mercearia"),
        ("Pão de forma", "Mercearia"), ("Pão francês", "Mercearia"),
        
        # Hortifruti
        ("Maçã", "Hortifruti"), ("Banana", "Hortifruti"), ("Laranja", "Hortifruti"), ("Limão", "Hortifruti"), ("Abacaxi", "Hortifruti"),
        ("Uva", "Hortifruti"), ("Morango", "Hortifruti"), ("Melancia", "Hortifruti"), ("Melão", "Hortifruti"), ("Mamão", "Hortifruti"),
        ("Kiwi", "Hortifruti"), ("Pera", "Hortifruti"), ("Manga", "Hortifruti"), ("Abacate", "Hortifruti"), ("Tomate", "Hortifruti"),
        ("Alface", "Hortifruti"), ("Rúcula", "Hortifruti"), ("Agrião", "Hortifruti"), ("Espinafre", "Hortifruti"), ("Couve", "Hortifruti"),
        ("Brócolis", "Hortifruti"), ("Cenoura", "Hortifruti"), ("Beterraba", "Hortifruti"), ("Batata", "Hortifruti"), ("Batata-doce", "Hortifruti"),
        ("Cebola", "Hortifruti"), ("Alho", "Hortifruti"), ("Pimentão", "Hortifruti"), ("Abobrinha", "Hortifruti"), ("Berinjela", "Hortifruti"),
        ("Chuchu", "Hortifruti"), ("Pepino", "Hortifruti"), ("Abóbora", "Hortifruti"), ("Quiabo", "Hortifruti"), ("Vagem", "Hortifruti"),
        ("Milho verde", "Hortifruti"), ("Coentro", "Hortifruti"), ("Salsa", "Hortifruti"), ("Cebolinha", "Hortifruti"), ("Hortelã", "Hortifruti"),
        
        # Carnes
        ("Carne bovina", "Carnes"), ("Carne suína", "Carnes"), ("Frango", "Carnes"), ("Peixe", "Carnes"), ("Carne de cordeiro", "Carnes"),
        ("Carne moída", "Carnes"), ("Filé mignon", "Carnes"), ("Picanha", "Carnes"), ("Alcatra", "Carnes"), ("Costela bovina", "Carnes"),
        ("Bife de fígado", "Carnes"), ("Linguiça", "Carnes"), ("Salsicha", "Carnes"), ("Hambúrguer", "Carnes"), ("Bacon", "Carnes"),
        ("Peito de frango", "Carnes"), ("Coxa de frango", "Carnes"), ("Asa de frango", "Carnes"), ("Filé de tilápia", "Carnes"), ("Salmão", "Carnes"),
        
        # Padaria
        ("Pão francês", "Padaria"), ("Pão de forma", "Padaria"), ("Pão integral", "Padaria"), ("Pão de queijo", "Padaria"), ("Croissant", "Padaria"),
        ("Baguete", "Padaria"), ("Pão de batata", "Padaria"), ("Pão doce", "Padaria"), ("Pão de centeio", "Padaria"), ("Pão sírio", "Padaria"),
        ("Pão australiano", "Padaria"), ("Pão de hambúrguer", "Padaria"), ("Pão de hot dog", "Padaria"), ("Biscoito de polvilho", "Padaria"),
        ("Biscoito cream cracker", "Padaria"), ("Biscoito de maizena", "Padaria"), ("Biscoito recheado", "Padaria"), ("Biscoito amanteigado", "Padaria"),
        ("Torta salgada", "Padaria"), ("Torta doce", "Padaria"),
        
        # Limpeza
        ("Detergente", "Limpeza"), ("Sabão em pó", "Limpeza"), ("Sabão líquido", "Limpeza"), ("Água sanitária", "Limpeza"), ("Amaciante de roupas", "Limpeza"),
        ("Desinfetante", "Limpeza"), ("Limpador multiuso", "Limpeza"), ("Limpador de vidro", "Limpeza"), ("Limpador de banheiro", "Limpeza"),
        ("Esponja de aço", "Limpeza"), ("Esponja de cozinha", "Limpeza"), ("Escova de lavar", "Limpeza"), ("Vassoura", "Limpeza"), ("Rodo", "Limpeza"),
        ("Pano de chão", "Limpeza"), ("Pano de prato", "Limpeza"), ("Balde", "Limpeza"), ("Saco de lixo", "Limpeza"), ("Luvas de limpeza", "Limpeza"),
        ("Álcool em gel", "Limpeza"),
        
        # Higiene Pessoal
        ("Sabonete", "Higiene Pessoal"), ("Shampoo", "Higiene Pessoal"), ("Condicionador", "Higiene Pessoal"), ("Creme dental", "Higiene Pessoal"),
        ("Escova de dentes", "Higiene Pessoal"), ("Fio dental", "Higiene Pessoal"), ("Desodorante", "Higiene Pessoal"), ("Papel higiênico", "Higiene Pessoal"),
        ("Absorvente", "Higiene Pessoal"), ("Fralda descartável", "Higiene Pessoal"), ("Cotonete", "Higiene Pessoal"), ("Algodão", "Higiene Pessoal"),
        ("Lâmina de barbear", "Higiene Pessoal"), ("Creme de barbear", "Higiene Pessoal"), ("Loção pós-barba", "Higiene Pessoal"), ("Hidratante corporal", "Higiene Pessoal"),
        ("Protetor solar", "Higiene Pessoal"), ("Repelente", "Higiene Pessoal"), ("Perfume", "Higiene Pessoal"), ("Sabonete líquido", "Higiene Pessoal"),
        
        # Pet Shop
        ("Ração para cães", "Pet Shop"), ("Ração para gatos", "Pet Shop"), ("Petiscos para cães", "Pet Shop"), ("Petiscos para gatos", "Pet Shop"),
        ("Areia para gatos", "Pet Shop"), ("Shampoo para cães", "Pet Shop"), ("Shampoo para gatos", "Pet Shop"), ("Antipulgas", "Pet Shop"),
        ("Ossinhos para cães", "Pet Shop"), ("Brinquedos para cães", "Pet Shop"), ("Brinquedos para gatos", "Pet Shop"), ("Cama para cães", "Pet Shop"),
        ("Cama para gatos", "Pet Shop"), ("Coleira para cães", "Pet Shop"), ("Coleira para gatos", "Pet Shop"), ("Guia para cães", "Pet Shop"),
        ("Bebedouro para cães", "Pet Shop"), ("Bebedouro para gatos", "Pet Shop"), ("Comedouro para cães", "Pet Shop"), ("Comedouro para gatos", "Pet Shop"),
        
        # Produtos de Cozinha
        ("Filme plástico", "Produtos de Cozinha"), ("Papel alumínio", "Produtos de Cozinha"), ("Papel manteiga", "Produtos de Cozinha"),
        ("Guardanapo", "Produtos de Cozinha"), ("Prato descartável", "Produtos de Cozinha"), ("Copo descartável", "Produtos de Cozinha"),
        ("Talheres descartáveis", "Produtos de Cozinha"), ("Toalha de papel", "Produtos de Cozinha"), ("Esponja de limpeza", "Produtos de Cozinha"),
        ("Saco plástico", "Produtos de Cozinha"), ("Rolo de massa", "Produtos de Cozinha"), ("Assadeira", "Produtos de Cozinha"),
        ("Forma de bolo", "Produtos de Cozinha"), ("Panela de pressão", "Produtos de Cozinha"), ("Panela antiaderente", "Produtos de Cozinha"),
        ("Frigideira", "Produtos de Cozinha"), ("Espátula", "Produtos de Cozinha"), ("Concha", "Produtos de Cozinha"), ("Escumadeira", "Produtos de Cozinha"),
        ("Abridor de latas", "Produtos de Cozinha"),
        
        # Diversos
        ("Pilhas", "Diversos"), ("Lâmpadas", "Diversos"), ("Vela", "Diversos"), ("Isqueiro", "Diversos"), ("Fósforos", "Diversos"),
        ("Inseticida", "Diversos"), ("Repelente de insetos", "Diversos"), ("Fita adesiva", "Diversos"), ("Super cola", "Diversos"),
        ("Pilha alcalina", "Diversos"), ("Extensão elétrica", "Diversos"), ("Adaptador de tomada", "Diversos"), ("Carregador de celular", "Diversos"),
        ("Cabo USB", "Diversos"), ("Bateria de lítio", "Diversos"), ("Tomada elétrica", "Diversos"), ("Benjamim (T)", "Diversos"),
        ("Fita isolante", "Diversos"), ("Lanterna", "Diversos"), ("Rolo de fita", "Diversos"),
        
        # Bebidas Alcoólicas
        ("Cerveja", "Bebidas Alcoólicas"), ("Cerveja artesanal", "Bebidas Alcoólicas"), ("Vodka", "Bebidas Alcoólicas"),
        ("Whisky", "Bebidas Alcoólicas"), ("Vinho tinto", "Bebidas Alcoólicas"), ("Vinho branco", "Bebidas Alcoólicas"),
        ("Champanhe", "Bebidas Alcoólicas"), ("Cachaça", "Bebidas Alcoólicas"), ("Licor", "Bebidas Alcoólicas"), ("Gin", "Bebidas Alcoólicas"),
        ("Tequila", "Bebidas Alcoólicas"), ("Rum", "Bebidas Alcoólicas"), ("Conhaque", "Bebidas Alcoólicas"), ("Cerveja sem álcool", "Bebidas Alcoólicas"),
        ("Sidra", "Bebidas Alcoólicas"), ("Vinho rosé", "Bebidas Alcoólicas"), ("Espumante", "Bebidas Alcoólicas"), ("Aperol", "Bebidas Alcoólicas"),
        ("Fernet", "Bebidas Alcoólicas"), ("Cerveja IPA", "Bebidas Alcoólicas")
    ]

     # Perguntar quantos itens deseja adicionar
    quantidade = int(input("Quantos itens deseja adicionar ao estoque? "))

    # Verificar se a quantidade solicitada é maior que o total de itens disponíveis
    if quantidade > len(itens_supermercado):
        print("A quantidade solicitada excede o total de itens disponíveis. Serão adicionados itens aleatórios com repetição.")

    # Selecionar itens aleatórios da lista
    itens_selecionados = random.choices(itens_supermercado, k=quantidade)

    # Preparar uma lista de documentos a serem inseridos
    documentos = []

    for item, categoria in itens_selecionados:
        numero_lote = gerar_numero_lote()

        documento = {
            "id_produto": random.randint(0, 999999999),  # Gerar um novo ID se o produto não existir
            "nome_produto": item,
            "categoria": categoria,
            "preco": round(random.uniform(1.0, 100.0), 2),
            "validade": faker.date_between(start_date='today', end_date='+1y').strftime("%Y-%m-%d"),
            "quantidade": random.randint(1, 100),
            "lote": numero_lote,
        }
        documentos.append(documento)
    start_time = time.time()
    collection.insert_many(documentos)
    end_time = time.time()
    tempo_execucao = end_time - start_time
    print(f"Tempo de execução para inserção: {tempo_execucao:.4f} segundos")
        

    print("Itens inseridos no banco de dados com sucesso!")

def consulta():
    def consulta_de_produtos(banco_dados, nome_colecao):
        collection = banco_dados[nome_colecao]

        def consultar_por_lote(numero_lote):
            start_time = time.time()
            resultado = collection.find_one({"lote": numero_lote})
            end_time = time.time()
            tempo_execucao = end_time - start_time
            if resultado:
                print("Produto encontrado:")
                print("Tempo de execução: " + str(tempo_execucao))
                print(resultado)
            else:
                print("Nenhum produto encontrado com esse número de lote.")

        def consultar_por_nome(nome_produto):
            start_time = time.time()
            resultado = collection.find_one({"nome_produto": nome_produto})
            end_time = time.time()
            tempo_execucao = end_time - start_time
            if resultado:
                print("Produto encontrado:")
                print("Tempo de execução: " + str(tempo_execucao))
                print(resultado)
            else:
                print("Nenhum produto encontrado com esse nome.")

        opcao = input("Deseja consultar por lote (L) ou por nome do produto (N)? ").upper()

        if opcao == "L":
            numero_lote = input("Digite o número de lote do produto que deseja consultar: ")
            consultar_por_lote(numero_lote)
        elif opcao == "N":
            nome_produto = input("Digite o nome do produto que deseja consultar: ")
            consultar_por_nome(nome_produto)
        else:
            print("Opção inválida. Por favor, escolha 'L' para consultar por lote ou 'N' para consultar por nome do produto.")

    def consultar_filiais_matrizes(conexao):
        #nomes_bancos = conexao.list_database_names()
        nomes_bancos = [db for db in conexao.list_database_names() if db not in ["admin", "config"]]
        if not nomes_bancos:
            print("Nenhum banco de dados encontrado no servidor MongoDB.")
            return

        consulta = input("Deseja realizar uma consulta? (S/N): ").upper()

        if consulta == "S":
            print("Bancos de dados encontrados:")
            for i, nome_banco in enumerate(nomes_bancos, start=1):
                print(f"{i}. {nome_banco}")
            
            escolha_banco = int(input("Escolha o número correspondente ao banco de dados que deseja usar: "))
            if escolha_banco < 1 or escolha_banco > len(nomes_bancos):
                print("Escolha inválida.")
                return

            nome_banco_escolhido = nomes_bancos[escolha_banco - 1]
            banco_dados = conexao[nome_banco_escolhido]
            colecoes = banco_dados.list_collection_names()

            if not colecoes:
                print(f"Nenhuma coleção encontrada no banco de dados '{nome_banco_escolhido}'.")
            else:
                print(f"Coleções encontradas no banco de dados '{nome_banco_escolhido}':")
                for i, colecao in enumerate(colecoes, start=1):
                    print(f"{i}. {colecao}")

                escolha_colecao = int(input("Escolha o número correspondente à coleção que deseja usar: ")) - 1
                if escolha_colecao < 0 or escolha_colecao >= len(colecoes):
                    print("Coleção inválida.")
                    return

                nome_colecao_escolhida = colecoes[escolha_colecao]
                consulta_de_produtos(banco_dados, nome_colecao_escolhida)
        else:
            print("Consulta não realizada.")

    consultar_filiais_matrizes(conexao)

def atualizar_produto():
    def atualizar_por_id_produto(banco_dados, nome_colecao):
        collection = banco_dados[nome_colecao]
        id_produto = int(input("Digite o ID do produto que deseja atualizar: "))
        start_time = time.time()
        produto = collection.find_one({"id_produto": id_produto})
        end_time = time.time()
        tempo_execucao = end_time - start_time
        print("Tempo de execução: " + str(tempo_execucao))
        if produto:
            print("Produto encontrado:")
            print(produto)

            opcao = input("Deseja atualizar a quantidade (Q) ou o preço (P)? ").upper()
            if opcao == "Q":
                nova_quantidade = int(input("Digite a nova quantidade: "))
                start_time = time.time()
                collection.update_one({"id_produto": id_produto}, {"$set": {"quantidade": nova_quantidade}})
                end_time = time.time()
                tempo_execucao = end_time - start_time
                print("Quantidade atualizada com sucesso! Tempo de execução: " + str(tempo_execucao))
            elif opcao == "P":
                novo_preco = float(input("Digite o novo preço: "))
                start_time = time.time()
                collection.update_one({"id_produto": id_produto}, {"$set": {"preco": novo_preco}})
                end_time = time.time()
                tempo_execucao = end_time - start_time
                print("Preço atualizado com sucesso! Tempo de execução: " + str(tempo_execucao))
            else:
                print("Opção inválida.")
        else:
            print("Nenhum produto encontrado com esse ID.")


    def atualizar_filiais_matrizes(conexao):
        #nomes_bancos = conexao.list_database_names()
        nomes_bancos = [db for db in conexao.list_database_names() if db not in ["admin", "config"]]

        if not nomes_bancos:
            print("Nenhum banco de dados encontrado no servidor MongoDB.")
            return

        atualizar = input("Deseja realizar uma atualização? (S/N): ").upper()

        if atualizar == "S":
            print("Bancos de dados encontrados:")
            for i, nome_banco in enumerate(nomes_bancos, start=1):
                print(f"{i}. {nome_banco}")
            
            escolha_banco = int(input("Escolha o número correspondente ao banco de dados que deseja usar: "))
            if escolha_banco < 1 or escolha_banco > len(nomes_bancos):
                print("Escolha inválida.")
                return

            nome_banco_escolhido = nomes_bancos[escolha_banco - 1]
            banco_dados = conexao[nome_banco_escolhido]
            colecoes = banco_dados.list_collection_names()

            if not colecoes:
                print(f"Nenhuma coleção encontrada no banco de dados '{nome_banco_escolhido}'.")
            else:
                print(f"Coleções encontradas no banco de dados '{nome_banco_escolhido}':")
                for i, colecao in enumerate(colecoes, start=1):
                    print(f"{i}. {colecao}")

                escolha_colecao = int(input("Escolha o número correspondente à coleção que deseja usar: ")) - 1
                if escolha_colecao < 0 or escolha_colecao >= len(colecoes):
                    print("Coleção inválida.")
                    return

                nome_colecao_escolhida = colecoes[escolha_colecao]
                atualizar_por_id_produto(banco_dados, nome_colecao_escolhida)
        else:
            print("Atualização não realizada.")

    atualizar_filiais_matrizes(conexao)

# Executar o menu
while True:
    print("\nMenu:")
    print("1. Gerar dados")
    print("2. Consultar dados")
    print("3. Atualizar dados")
    print("4. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        gerar_dados()
    elif escolha == "2":
        consulta()
    elif escolha == "3":
        atualizar_produto()
    elif escolha == "4":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")





