import random
import string
from faker import Faker
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# Inicializações
faker = Faker()

# Conectar ao MongoDB
conexao = MongoClient("mongodb://localhost:27017/")

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

# Função para gerar um número de lote no formato 5 letras maiúsculas e 5 números
def gerar_numero_lote():
    letras = random.choices(string.ascii_uppercase, k=5)
    numeros = random.choices(string.digits, k=5)
    return ''.join(letras + numeros)

def operacao_insert(db, itens_supermercado):
    item, categoria = random.choice(itens_supermercado)
    numero_lote = gerar_numero_lote()

    documento = {
        "id_produto": random.randint(0, 999999999),
        "nome_produto": item,
        "categoria": categoria,
        "preco": round(random.uniform(1.0, 100.0), 2),
        "validade": faker.date_between(start_date='today', end_date='+1y').strftime("%Y-%m-%d"),
        "quantidade": random.randint(1, 100),
        "lote": numero_lote,
    }

    collection = db[random.choice(db.list_collection_names())]
    collection.insert_one(documento)
    print("Documento inserido")

def operacao_delete(db):
    collection = db[random.choice(db.list_collection_names())]
    cursor = collection.aggregate([{ "$sample": { "size": 1 } }])
    documento = next(cursor, None)
    
    if documento:
        id_produto = documento["id_produto"]
        collection.delete_one({"id_produto": id_produto})
        print(f"Produto com id_produto {id_produto} deletado com sucesso.")
    else:
        print("Nenhum documento encontrado na coleção.")

def operacao_update(db):
    collection = db[random.choice(db.list_collection_names())]
    cursor = collection.aggregate([{ "$sample": { "size": 1 } }])
    documento = next(cursor, None)
    
    if documento:
        if 'lote' in documento:
            novo_preco = round(random.uniform(1.0, 100.0), 2)
            nova_quantidade = random.randint(1, 100)
            collection.update_one({"_id": documento["_id"]}, {"$set": {"preco": novo_preco, "quantidade": nova_quantidade}})
            print(f"Atualização de produto - Banco: {db.name}, Coleção: {collection.name}, id_produto {documento['id_produto']}, Novo Preço: {novo_preco}, Nova Quantidade: {nova_quantidade}")
        else:
            print("Documento não possui a chave 'lote'.")
    else:
        print("Nenhum documento encontrado na coleção.")

def estresse_banco_dados(num_loops):
    print(f"Iniciando programa de estresse do banco de dados com {num_loops} loops...")
    
    # Obter a lista de bancos de dados excluindo "admin" e "config"
    bancos_dados = [db for db in conexao.list_database_names() if db not in ["admin", "config"]]

    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(num_loops):
            banco_dados = random.choice(bancos_dados)
            db = conexao[banco_dados]

            # Executar operações em paralelo
            executor.submit(operacao_insert, db, itens_supermercado)
            executor.submit(operacao_delete, db)
            executor.submit(operacao_update, db)

    print("Operações de estresse concluídas.")

# Solicitar ao usuário o número de loops desejado
try:
    num_loops = int(input("Digite o número de loops desejado: "))
    estresse_banco_dados(num_loops)
except ValueError:
    print("Por favor, digite um número válido para o número de loops.")