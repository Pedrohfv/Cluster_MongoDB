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
* Passo 2: [Simulação de dados no banco de dados das filiais](#simulação_filiais).
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
Para realizar a configuração dos ConfigServers em um replicaset será necessário acessar o shell do  mongo de um dos containers dos ConfigServes (mongo-config-1,  mongo-config-2,  mongo-config-3)
```shell
$ docker exec -it mongo-config-1 mongosh
```
# Vincular os ConfigServers em um replicaset com o seguinte comando:
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
Serão criados três grupos de shards, cada um contendo três servidores. Dessa forma, teremos um servidor primário e dois secundários em cada grupo. Essa configuração visa evitar inconsistências durante o processo de eleição para escolher o próximo servidor primário do grupo, caso haja indisponibilidade em alguns dos servidores de um dos grupos de shards. É importante garantir que o número de réplicas em um grupo de shards seja sempre ímpar, pois isso impede empates durante a eleição.

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
Para realizar a configuração dos 3 grupos de Shards em um replicaset será necessário acessar o shell de um dos containers dos Shards individualmente.
* Grupo 1(Shards-1):mongo-shard-1-a, mongo-shard-1-b e mongo-shard-1-c.
* Grupo 2(Shards-2):mongo-shard-2-a, mongo-shard-2-b e mongo-shard-2-c.
* Grupo 3(Shards-3):mongo-shard-3-a, mongo-shard-3-b e mongo-shard-3-c.

# Grupo 1
```shell
$ docker exec -it mongo-shard-1-a mongosh
```
# Vincular os Shards em um replicaset com o seguinte comando:
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





<a id="simulação_filiais"></a>
<a id="simulação_desempenho"></a>
