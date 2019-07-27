# Battery_Monitor

## Requer

    Pyrebase

### python/batmonitorfirebase.py

    Monitora o estado da bateria, e informa quando deve ligar ou desligar o carregador.

### python/firebaseconfig.py

    Configuração dos dados de acesso ao Firebase.
    Configuração do caminho da variável a ser monitorado ou controlada.

### esp/batmonitorfirebase.ino

    Monitora o estado de uma variável no Firebase RealTime Database e controla um rele
    conforme este estado, ligando ou desligando o carregador do computador.

### service/batmonitor.service

    Deve ser instalado como serviço do sistema, para monitorar o estado da bateria.
