# Arquitetura
Foram utilizados os serviços AWS para armazenamento, execução de ETL e análise de dados.
Dessa forma, pouco código foi desenvolvido, sendo necessárias apenas poucas conversões de tipos
nas células dos arquivos csv. As conversões foram implementadas em _python_ e deployadas no ambiente 
do AWS GLUE.

As análises foram feitas diretamente no AWS ATHENA que acessa os arquivos convertidos localizados no AWS S3.
Dessa forma, não foi necessário fazer importação dos dados em nenhum outro banco de dados, uma vez que o 
AWS ATHENA acessa diretamente os csv no S3, dando uma visão relacional (SQL) sobre esses dados.

**Serviços AWS:**
* **S3:** armazenamento dos arquivos csv originais e transformados.
* **Glue:** Contém as metainformações das tabelas e executa o ETL de transformação dos arquivos.
* **Athena:** console de análise SQL dos dados.

**Armazenamento dos Arquivos:** foi criado um diretório para os arquivos originais e um diretorio para cada tabela.

    < S3_BUCKET >/
        spec: todos os arqwuivos csv disponibilizados para analise.
        product: csv convertido da tabela Production.Product.
        customer: csv convertido da tabela Sales.Customer.
        person: csv convertido da tabela Person.Person.
        sales:
            order: csv convertido da tabela Sales.SalesOrderHeader.
            detail: csv convertido da tabela Sales.SalesOrderDetail.
            offer: csv convertido da tabela Sales.SpecialOfferProduct.
        script: código fonte do script de transformação dos dados. 
            Será refereciado na configuração do Job GLUE. 
        
> Essa estrutura de diretórios é importante pois as metatabelas GLUE apontam cada uma para um diretório.
> Assim, assume-se que os dados de Production.Product estão todos em um diretório, e assim por diante.
> Os nomes dos diretórios não precisam ser os mesmos, mas havendo mudança deve-se modificar o script rox.py.

**Transformações:** a transformação corresponde a conversão dos campos NULOS e DECIMAIS com VIRGULA para formato 
adequado ao Athena.

**Script de transformação:** o script de transformaão foi implementado em _python_ utilizando bibliotecas padrões.
Optou-se por não utilizar o pyspark devida a economia de tempo. 
O GLUE tem ambiente para execução de scripts  que fundamentalmente inicializa um container com ambiente python,
podendo-se, dessa forma, baixar os arquivos do S3, executar conversão e subir novamente os dados convertidos.

O script é configurado no AWS GLUE, descrito em seção posterior, e disparado manualmente.

**Modelo de Dados:** o modelo já foi apresentado no Teste. O schema dos dados (tipos dos campos) foi identificado
diretamente da análise dos arquivos e está descrito no diretório _schema_ do código no Github..

**Análise de Dados:** as análises foram executadas diretamente com SQL. 
Dado o poder da sintaxe do SQL Presto não foi necessário nenhum procedimento além da execução das queries
para alcançar os resultados. As queries se encontram no diretório _sql_ do código no Github.

> O Athena é a versão do AWS do banco de dados _Presto_.
> Dessa forma a sintaxe SQL é a utilizada pelo _Presto_.
> Em especial utilizou-se o comando não ANSI **WITH** que permite a criação de uma subquery
> utilizada na clausula **FROM** da principal.

## Design do ingestor de dados

O _ingestor_ converte os arquivos csv para um formato de campos legível pelo Athena. 
Tal conversão consiste apenas em percorrer todas as linhas através de um csv reader e converter
os campos necessários.

O detalhe a ser observado é que o método de conversão *ingestor.process()* recebe uma configuração
de quais transformações são executadas em cada campo. Tome o exemplo abaixo:

```python
ingest.process(localdir, 'Sales.Customer.csv',
               # Transformations of specific fields.
               transforms={"PersonID": [nullToZero], "StoreID":[nullToZero], "TerritoryID": [nullToZero]},
               # Transformations applied to all fields.
               alltransforms=[nulls, trim],
               writefile=True,
               # Callback to upload the converted file
               uploadS3=gen_s3_upload("customer"))
```
O parâmetro *transforms* corresponde a um dicionário que associa um atributo com uma lista de transformações.

Cada transformação é um método presente no diretório `ingest/transform`.

# Source Code
**Git hub:** *https://github.com/francara/rox.git* 
## Diretórios
    ./
        rox.py: script principal
        setup.py: montagem do projeto.
    ./ingest/
        filter/: eventuais filtros de linhas do arquivo.
            Não utilizado no projeto.
        transform/
            row.py: transformações de celulas do arquivo original.
    ./sql/
        *.sql: arquivos com as queries para executar as análises.
        *.png: imagens retiradas da execução das queries no console AWS Athena.
    ./schema/: json com schema exportado do GLUE.

# Setup
## AWS S3
Nenhuma configuração especial é necessário no AWS S3, apenas a criação de estrutura de diretórios semelhante a proposta.

Os dados originais devem ser copiados manualmente para um diretório (spec.)

## AWS Glue
É necessário a configuração manual das tabelas no AWS GLUE e a criação de um script de ingestão dos dados (Job).

### Tables
Deve ser criada uma tabela para cada uma do modelo conceitual disponibilizado.
O seguinte procedimento deve ser execuado manualmente a partir do console do AWS GLUE.
1. Adicionar tabela manualmente.
1. Nome da tabela coerente com os scripts SQL (product, person, customer, salesorder, salesdetail, specialoffer).
1. Amarrar com um banco de dados previamente criado no GLUE.
1. Tipo de fonte S3 e especificar um caminho exclusivo para os dados da tabela.
1. Tipo da tabela CSV com delimitador ";".
1. Criar cada coluna segundo salvo no diretório _schema_. 

### python
O script principal (*rox.py*) deve estar armazenado em um diretório do S3 (_script_) e referenciado no Job Glue. 
Além do script *rox.py* é necessário fazer o deploy da biblioteca wheel (whl) gerado pelo python.
Abaixo os comandos para geração da biblioteca.

`python3 -m venv venv`
 
`pip install wheel`

`pip install setuptools`

`pip install twine`

`python setup.py pytest`

### Job
Criar um trabalho/job executado manualmente.

1. Adicionar Trabalho/Job.
1. Função do IAM: role previamente criada que permite acesso do GLUE ao S3.
1. Type: python shell.
1. Nome do arquivo do script.
1. Localização no S3 do arquivo do script.

## AWS Athena

Uma vez criadas as metainformações no GLUE e ingerido os dados nenhuma configuração é necessária
para o ATHENA visualizar as tabelas e dados.

# Resultados

Os resultados das análises se encontram no diretório sql.
Foram colocadas, além das queries montadas, imagens do ambiente do ATHENA com a execução.
