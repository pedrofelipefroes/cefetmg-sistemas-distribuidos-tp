###### CENTRO FEDERAL DE EDUCAÇÃO TECNOLÓGICA DE MINAS GERAIS <br> ENGENHARIA DE COMPUTAÇÃO <br> Sistemas Distribuídos <br> Prof. Anolan Barrientos <br> 2017-1

# <h1 style="margin-bottom:-20px;"> TRABALHO PRÁTICO </h1>

#### Pedro Felipe Froes <br> Saulo Antunes

Trabalho prático realizado para a disciplina de Sistemas Distribuídos do curso de Engenharia de Computação do CEFET-MG, lecionada pela Prof. Anolan Barrientos.

## Introdução

Um sistema distribuído será desenvolvido através de um jogo no sistema operacional Android, utilizando a IDE Android Studio para construir o código da aplicação. Inicialmente, será implementado uma aplicação simples que consiste em apenas mostrar a última localização conhecida do dispositivo, que geralmente é equivalente à localização atual do mesmo.

Para obter a última localização conhecida do dispositivo, utiliza-se a API do Google Play atrelada à localização, o _fused location provider_. Essa API é responsável por gerenciar os serviços relacionados à variável de localização, disponibilizando métodos para o programador escolher quais mais se adequam à sua aplicação.

## Desenvolvimento da aplicação

### _Setup_ inicial do projeto

Um novo projeto pode ser criado no Android Studio selecionando a opção _Empty project_ ao iniciá-lo. O projeto criado possui as pastas `manifest` e `java`, que contem arquivos de metadados e de código do projeto, respectivamente, e uma seção de _scripts_ do Gradle que auxiliam na compilação e criação do projeto.

Para acessar a _fused location provider_, é primeiro necessário importar a API do Google Play para o projeto, o que pode ser feito através do Android Studio na seção de `Tools/Android/SDK Manager`. Com a API importada, deve-se atualizar o script do Gradle para incluí-la na criação do projeto. Como será construída uma aplicação simples, importou-se apenas a API do Google Play relacionada à localização, incluindo `compile 'com.google.android.gms:play-services-location:10.2.1'` nas dependências do projeto no arquivo `build.gradle`.

//falar sobre permissões no manifest.xml

 a classe de atividades principais, a `MainActivity`, e um arquivo 

#### Descrição da abordagem utilizada

#### Forma de utilização

#### Conclusão

## Referências

https://developers.google.com/android/guides/setup

https://developer.android.com/training/location/retrieve-current.html

http://techlovejump.com/android-gps-location-manager-tutorial/