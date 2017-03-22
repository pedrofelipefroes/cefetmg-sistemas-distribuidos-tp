###### CENTRO FEDERAL DE EDUCAÇÃO TECNOLÓGICA DE MINAS GERAIS <br> ENGENHARIA DE COMPUTAÇÃO <br> Sistemas Distribuídos <br> Prof. Anolan Barrientos <br> 2017-1

# TRABALHO PRÁTICO

#### Pedro Felipe Froes <br> Saulo Antunes

Trabalho prático realizado para a disciplina de Sistemas Distribuídos do curso de Engenharia de Computação do CEFET-MG, lecionada pela Prof. Anolan Barrientos.

## Introdução

Um sistema distribuído será desenvolvido através de um jogo no sistema operacional Android, utilizando a IDE Android Studio para construir o código da aplicação. Inicialmente, será implementado uma aplicação simples que consiste em apenas mostrar a última localização conhecida do dispositivo, que geralmente é equivalente à localização atual do mesmo.

Para obter a última localização conhecida do dispositivo, utiliza-se a API do Google Play atrelada à localização, o _fused location provider_. Essa API é responsável por gerenciar os serviços relacionados à variável de localização, disponibilizando métodos para o programador escolher quais mais se adequam à sua aplicação.

## Desenvolvimento da aplicação

### _Setup_ inicial do projeto

Um novo projeto pode ser criado no Android Studio selecionando a opção _Empty project_ ao iniciá-lo. O projeto criado possui as pastas `manifest` e `java`, que contem arquivos de metadados e de código do projeto, respectivamente, e uma seção de _scripts_ do Gradle que auxiliam na compilação e criação do projeto.

Para acessar a _fused location provider_, é primeiro necessário importar a API do Google Play para o projeto, o que pode ser feito através do Android Studio na seção de `Tools/Android/SDK Manager`. Com a API importada, deve-se atualizar o script do Gradle para incluí-la na criação do projeto. Como será construída uma aplicação simples, importou-se apenas a API do Google Play relacionada à localização, incluindo `compile 'com.google.android.gms:play-services-location:10.2.1'` nas dependências do projeto no arquivo `build.gradle`.

Posteriormente, é necessário atualizar as permissões da aplicação para acessar a localização do dispositivo. Para acessar a localização via GPS, é necessário alterar o arquivo `Android.manifest.xml` para incluir as permissões à `ACCESS_FINE_LOCATION` e `INTERNET`. Com as devidas permissões e API importadas, pode-se começar a trabalhar na classe de atividades principais da aplicação, a `MainActivity`. 

#### Descrição da abordagem utilizada

Para retornar a localização do dispositivo, é necessário implementar os métodos da interface `LocationListener` na classe principal. É necessário inicializar uma variável do tipo `LocationManager`, que será responsável por chamar os métodos `getSystemService` e `requestLocationUpdates`. Esse último método possui quatro parâmetros principais:

* `provider`, que recebe o provedor da localização do dispositivo – nesse caso, o GPS do mesmo;
* `minTime`, o intervalo mínimo entre a atualização da localização;
* `minDistance`, a distância mínima entre a atualização da localização;
* `listener`, o método que implementa a interface `LocationListener` – nesse caso, a classe `MainActivity`da aplicação.

Para exibir a localização para o usuário, é necessário utilizar os _getters_ `getLatitute` e `getLongitude` para imprimir a latitude e longitude na interface, respectivamente.

Finalmente, é uma boa prática atentar para casos onde o GPS não está habilitado – nesses casos, deve-se redirecionar o usuário para as configurações de GPS do seu dispositivo. Usa-se uma variável do tipo `Intent` para fazer o redirecionamento, passando o caminho `Settings.ACTION_LOCATION_SOURCE_SETTINGS` que corresponde às configurações relacionadas à localização no dispositivo.

#### Forma de utilização

Pode-se utilizar a aplicação através de um emulador de Android ou no próprio dispositivo. Utilizando em um emulador, deve-se atentar às permissões de acesso à localização da máquina do usuário. Para utilizar em um dispositivo, basta abrir a aplicação e caminhar – a localização deverá ser atualizada de acordo com o tempo e distância que usuário passar com a aplicação aberta. Por exemplo, a lozalização pode ser atualizada a cada 2 segundos e/ou a cada 200 metros caso os parâmetros `minTime` e `minDistance` sejam equivalentes a esses valores, respectivamente.

SCREENSHOTS DE UTILIZAÇÃO

## Referências

**Google API for Android**: Set Up Google Play Services. Disponível em: <https://developers.google.com/android/guides/setup>. Acesso em: 20, Mar, 2017.

**Android Developers**: Getting the Last Known Location. Disponível em: <https://developer.android.com/training/location/retrieve-current.html>. Acesso em: 20, Mar, 2017.

**TechLoveJump**: Android Tutorials. Android GPS – Location Manager Tutorial. Disponível em: <http://techlovejump.com/android-gps-location-manager-tutorial/>. Acesso em: 20, Mar, 2017.