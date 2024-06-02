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

### Criando os Shards
Serão criados três grupos de shards, cada um contendo três servidores. Dessa forma, teremos um servidor primário e dois secundários em cada grupo. Essa configuração visa evitar inconsistências durante o processo de eleição para escolher o próximo servidor primário do grupo, caso haja indisponibilidade em alguns dos servidores de um dos grupos de shards. É importante garantir que o número de réplicas em um grupo de shards seja sempre ímpar, pois isso impede empates durante a eleição.




<a id="simulação_filiais"></a>
<a id="simulação_desempenho"></a>
