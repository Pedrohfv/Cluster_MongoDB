<p align="center">
  <a href="https://medium.com/@ManagedKube/deploy-a-mongodb-cluster-in-steps-9-using-docker-49205e231319"><img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*HWfG5YkyX5atHZjDFrHfaw.png"/></a>
</p>

<h1 align="center">Projeto Cluster MongoDB</h1>    

O objetivo deste trabalho é criar um sistema de banco de dados distribuído que seja escalável e eficiente para lidar com grandes volumes de dados. Isso requer o desenvolvimento de uma arquitetura que distribua e particione os dados de forma eficaz, garantindo alto desempenho e confiabilidade. Considerações importantes incluem balanceamento de carga, tolerância a falhas e otimização de consultas, essenciais para gerenciar grandes conjuntos de dados em ambientes distribuídos.

# Cenário do Projeto

Projetar um sistema de gerenciamento de estoque para uma cadeia de supermercados que possui filiais em diferentes cidades.

Principais requisitos:

* Cada filial possui um grande volume de produtos em seu estoque.
* O sistema precisa ser capaz de lidar com milhões de registros de produtos.
* A consulta de estoque e atualizações de inventário devem ser rápidas e eficientes.
* A escalabilidade do sistema é essencial, pois novas filiais podem ser adicionadas no futuro.

# Projeção dos passos a serem seguidos
* Passo 1: [Criação do Cluster Mongodb](#Criando_o_Cluster_Mongodb).
* Passo 2: [Implementação Simulada de Dados](#Implementação_Simulada_de_Dados).
* Passo 3: [Simluação de desempesnho do cluster](#simulação_desempenho).

# Criando o Cluster Mongodb
<a id="Criando_o_Cluster_Mongodb"></a>

### Introdução e Conceitos básicos dos recursos
O cluster MongoDB será criado com o auxílio do Docker e utilizará recursos do MongoDB, como particionamento e replicação, para garantir um banco de dados com alta disponibilidade e consistência.
Com o intuido de melhorar o entendimento da elaboração do cluster precisamos entender alguns servições do Mongo, são eles:

* Roteadores: Servidores reponsáveis pelas requisições de escrita e leitura redirecionado para as partições corretas(Shards).

* Config Servers: Reponsáveis por armazenar os metadados das partições(shards).

* Shards: Responsáveis pelo armazenamento dos dados. Cada shard fica responsável por um subconjunto dos dados do banco.

### Procedimento incial 
Como se trata de um projeto estudantil e não para fins de produção, vamos criar uma rede para comunicação entre os contêineres em nossa própria máquina. Em prol da segurança e boas praticas nossa rede sejá insolada dos demais, impedindo que outros contêineres não tenham acesso a rede. Podemos gerar essa rede executando o seguinte comando:
```shell
$ docker network create mongo-cluster
```

### Criandos os ConfigServers
Ter três Config Servers é fundamental para garantir a alta disponibilidade e a tolerância a falhas no ambiente de sharding. Se um Config Server falhar, os outros dois ainda podem manter a integridade do sistema e permitir que as operações de sharding continuem sem interrupções.
```shell
$ docker run --name mongo-config-1 --net mongo-shard -d mongo mongod --configsvr --replSet config-servers --port 27017
$ docker run --name mongo-config-2 --net mongo-shard -d mongo mongod --configsvr --replSet config-servers --port 27017
$ docker run --name mongo-config-3 --net mongo-shard -d mongo mongod --configsvr --replSet config-servers --port 27017
```
### Configurando os ConfigServers
Para realizar a configuração dos ConfigServers em um replicaset, será necessário acessar o shell do Mongo de um dos containers dos ConfigServes (mongo-config-1,  mongo-config-2,  mongo-config-3)
```shell
$ docker exec -it mongo-config-1 mongosh
```
### Vincular os ConfigServers em um replicaset com o seguinte comando:
```shell
rs.initiate(
   {
      _id: "config-servers",
      configsvr: true,
      version: 1,
      members: [
         { _id: 0, host : "mongo-config-1:27017" },
         { _id: 1, host : "mongo-config-2:27017" },
         { _id: 2, host : "mongo-config-3:27017" }
      ]
   }
)
```

### Criando os Shards
Serão criados três grupos de shards, cada um contendo três servidores. Dessa forma, teremos um servidor primário e dois secundários em cada grupo. Essa configuração visa evitar desastres e inconsistências durante o processo de eleição para escolher o próximo servidor primário do grupo, caso haja indisponibilidade em alguns dos servidores de um dos grupos de shards. É importante garantir que o número de réplicas em um grupo de shards seja sempre ímpar, pois isso impede empates durante a eleição, lembrando que a mesma regra também pode ser replicada para os ConfigServers.

### Comandos para o grupo 1 dos Shards
```shell
$ docker run --name mongo-shard-1-a --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-1 --port 27017
$ docker run --name mongo-shard-1-b --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-1 --port 27017
$ docker run --name mongo-shard-1-c --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-1 --port 27017
```
### Comandos para o grupo 2 dos Shards
```shell
$ docker run --name mongo-shard-2-a --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-2 --port 27017
$ docker run --name mongo-shard-2-b --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-2 --port 27017
$ docker run --name mongo-shard-2-c --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-2 --port 27017
```
### Comandos para o grupo 3 dos Shards
```shell
$ docker run --name mongo-shard-3-a --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-3 --port 27017
$ docker run --name mongo-shard-3-b --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-3 --port 27017
$ docker run --name mongo-shard-3-c --net mongo-cluster -d mongo mongod --shardsvr --replSet shards-3 --port 27017
```
### Configurando os Shards 1, 2 e 3
Para configurar os 3 grupos de shards em um replicaset, é necessário acessar o shell do Mongo em pelo menos um dos containers de cada em cada grupo de shards.
* Grupo 1(Shards-1):mongo-shard-1-a, mongo-shard-1-b e mongo-shard-1-c.
* Grupo 2(Shards-2):mongo-shard-2-a, mongo-shard-2-b e mongo-shard-2-c.
* Grupo 3(Shards-3):mongo-shard-3-a, mongo-shard-3-b e mongo-shard-3-c.

### Grupo 1
```shell
$ docker exec -it mongo-shard-1-a mongosh
```
### Vincular os Shards em um replicaset com o seguinte comando:
```shell
rs.initiate(
   {
      _id: "shards-1",
      version: 1,
      members: [
         { _id: 0, host : "mongo-shard-1-a:27017" },
         { _id: 1, host : "mongo-shard-1-b:27017" },
         { _id: 2, host : "mongo-shard-1-c:27017" },
      ]
   }
)
```
### Grupo 2
```shell
$ docker exec -it mongo-shard-2-a mongosh
```
### Vincular os Shards em um replicaset com o seguinte comando:
```shell
rs.initiate(
   {
      _id: "shards-2",
      version: 1,
      members: [
         { _id: 0, host : "mongo-shard-2-a:27017" },
         { _id: 1, host : "mongo-shard-2-b:27017" },
         { _id: 2, host : "mongo-shard-2-c:27017" },
      ]
   }
)
```
### Grupo 3
```shell
$ docker exec -it mongo-shard-3-a mongosh
```
### Vincular os Shards em um replicaset com o seguinte comando:
```shell
rs.initiate(
   {
      _id: "shards-3",
      version: 1,
      members: [
         { _id: 0, host : "mongo-shard-3-a:27017" },
         { _id: 1, host : "mongo-shard-3-b:27017" },
         { _id: 2, host : "mongo-shard-3-c:27017" },
      ]
   }
)
```
### Criando o Roteador
Como o objetivo do roteador é realizar consultas no banco de dados e não armazenar dados, podemos optar por ter pelo menos 1 roteador, visando custo para o cenário do projeto. Mesmo com sua falha, os dados do cluster não seriam perdidos, pois há redundância nos shards e nos servidores de configuração que são responsáveis pela armazenagem dos dados.
```shell
$ docker run -p 27017:27017 --name mongo-router --net mongo-cluster -d mongo mongos --port 27017 --configdb config-servers/mongo-config-1:27017,mongo-config-2:27017,mongo-config-3:27017 --bind_ip_all
```

### Associação do roteador aos Shards
Para associar o roteador aos grupos de shards, é necessário acessar o shell do Mongo ao container do roteador.
```shell
$ docker exec -it mongo-router mongosh
```
### Associar os shards com os comandos
```shell
sh.addShard("shards-1/mongo-shard-1-a:27017")
sh.addShard("shards-1/mongo-shard-1-b:27017")
sh.addShard("shards-1/mongo-shard-1-c:27017")
sh.addShard("shards-2/mongo-shard-2-a:27017")
sh.addShard("shards-2/mongo-shard-2-b:27017")
sh.addShard("shards-2/mongo-shard-2-c:27017")
sh.addShard("shards-3/mongo-shard-3-a:27017")
sh.addShard("shards-3/mongo-shard-3-b:27017")
sh.addShard("shards-3/mongo-shard-3-c:27017")
```
### Fragmentação dos dados

Após a criação do cluster, iremos definir como será a fragmentação dos dados nas shards. Isso será concretizado a partir do momento em que criarmos o banco de dados da filial e sua collection. Cada collection possuirá um índice chamado id_produto(campo do documento), que será definido como hashed. Após a definição do índice hashed, será implementada a distribuição da collection. Isso permitirá que os dados sejam bem distribuídos e não sobrecarreguem nenhum dos shards. Cada dado inserido na collection será armazenado em um shard, e a definição do shard será feita com a ajuda do balancer, que moverá os chunks (faixas de dados). Isso permitirá que o cluster tenha uma escala horizontal, distribuindo dados e carga de trabalho entre múltiplos servidores de forma eficiente.

* Shard: Um servidor ou conjunto de servidores que armazena uma parte dos dados de um banco de dados sharded.
* Chunk: Uma faixa de dados dentro de um shard, que é distribuída com base na chave de shard.
* Balancer: Processo que move chunks entre shards para garantir um balanceamento de carga.

A fragmentação será essencial para o objetivo do projeto devido ao grande número de filiais, o que gerará um volume significativo de inserções, exclusões, atualizações e consultas nos bancos de dados.

Códigos para o processo de fragmentação da sua colletion. Executados no shell do Mongo ou diretamento no seu código caso exista.

```shell
<banco>.<collection>.createIndex({"id_produto": "hashed"}))
```
```shell
use <banco>
```
```shell
sh.shardCollection("<banco>.<collection>",{"id_produto":"hashed"})
```
### Resultado da destribuição:
Imagens ilustrativas da distribuição prevista
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Fragmenta%C3%A7%C3%A3o.png"/>
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Fragmenta%C3%A7%C3%A3o2.png"/>

### Cluster MongoDB finalizado

Contêineres em execução no Docker:

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Docker.png"/>

MongoDBCompass:

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Cluster_funcionamento.png"/>

# Implementação Simulada de Dados
<a id="Implementação_Simulada_de_Dados"></a>

Após a implementação do Cluster foi criado os bancos de dados para cada filial, gerado a inserção de dados para cada collention.
O processo de Simulação de dados foi gerados atráves de um arquivo programado em Python (), desenvolvido para este projeto. Incialmente foram gerados 5 bancos para cada filial(varejo_filial_x) e cada filial possuirá 1 collection(estoque_produtos_filial_x).

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Simula%C3%A7%C3%A3o_dados.png"/>

Foram injetados 100mil documentos para cada filial e o processo de destribuição dos dados foram feitos conforme idealizados. Importante salientar que o processo de configuração para o roteador realizar a fragmentação dos dados ocorreu no momento de gerar a coleção. 

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Conf_fragmenta%C3%A7%C3%A3o.png"/>

### Imagens da destribuição dos documentos para os grupos de shards 1, 2 e 3 de cada coleção:
* estoque_produtos_filial_1
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Filial_1.png"/>

* estoque_produtos_filial_2
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Filial_2.png"/>

* estoque_produtos_filial_3
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Filial_3.png"/>

* estoque_produtos_filial_4
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Filial_4.png"/>

* estoque_produtos_filial_5
<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Filial_5.png"/>

### Consulta e Atualização de dados

Através do programa() também existe a possibilidade de realizar consultas dos produtos por lote ou nome e alterações de preço e quantidades.

### Simulação de consulta:

Realizando a simulação de uma consulta de um produto pelo lote. 

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Consulta_banco.png"/>

### Simulação de Alteraçao:

Realizando a simulação de atualização de um produto pelo ID. 

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Atualiza_banco.png"/>

# Simluação de desempesnho do cluster
<a id="simulação_desempenho"></a>

Como forma de realizar um teste de desempenho no cluster, foi desenvolvido outro programa em Python para realizar requisições no banco de dados, tais como inserções, exclusões e atualizações.

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Atualiza_banco.png"/>

### Leitura dos parametros de performace do banco.

Foram realizados testes de estresse nos bancos de dados e o monitoramento ocorreu pelo MongoCompass.

O desempenho do banco de dados apresenta um comportamento estável em termos de operações realizadas. A rede mostra uma atividade consistente, com 99 KB de dados enviados e 9 KB recebidos. A memória utilizada permanece eficiente, com 2.57 GB de memória virtual e 80 MB de memória residente. As operações mais lentas foram as consultas "GETMORE" na coleção estoque_produtos_filial_3, com tempos em torno de 39 ms, indicando uma performance aceitável para as operações de leitura no banco de dados.

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Parametros_banco.png"/>

<img src="https://github.com/Pedrohfv/Cluster_MongoDB/blob/main/Prints/Teste_estresse_2.png"/>

# Relatório Final

A abordagem adotada para o projeto do Cluster MongoDB buscou criar uma infraestrutura distribuída capaz de atender aos requisitos de escalabilidade e eficiência para o gerenciamento de grandes volumes de dados de uma cadeia de supermercados. A arquitetura do sistema foi projetada com base nos princípios de balanceamento de carga, tolerância a falhas e otimização de consultas.

Após a criação do cluster MongoDB utilizando contêineres Docker, foram configurados os componentes essenciais, como Config Servers, Shards e o Roteador. A distribuição dos dados foi planejada de forma a garantir a redundância e a alta disponibilidade do sistema, com a criação de réplicas dos shards e config servers.

A simulação de dados foi realizada através de um programa em Python, que gerou e inseriu um grande volume de registros em cada filial da cadeia de supermercados. A fragmentação dos dados foi implementada conforme planejado, garantindo uma distribuição eficiente e equilibrada nos grupos de shards.

Durante os testes de desempenho do cluster, foram realizadas operações de consulta, atualização e inserção, com monitoramento constante através do MongoDB Compass. Os resultados dos testes demonstraram uma performance estável e eficiente do banco de dados, com tempos de resposta aceitáveis para as operações realizadas.






