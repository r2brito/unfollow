# Automação para Deixar de Seguir no Instagram

Este projeto automatiza o processo de deixar de seguir perfis no Instagram utilizando Selenium WebDriver. Ele é projetado para lidar com operações em grande escala, com pausas estratégicas para evitar que os mecanismos anti-bot do Instagram sejam acionados.

## Funcionalidades

- Faz login na sua conta do Instagram.
- Navega até a lista de perfis que você segue.
- Deixa de seguir perfis automaticamente em lotes.
- Adiciona pausas configuráveis entre as sessões para simular o comportamento humano.

## Requisitos

- Python 3.7+
- Google Chrome
- ChromeDriver (compatível com a sua versão do Chrome)

## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:r2brito/unfollow-bot.git
   cd unfollow-bot
   ```

2. Instale as bibliotecas necessárias do Python:

   ```bash
   pip install selenium python-dotenv
   ```

3. Baixe o ChromeDriver:

   - Encontre a versão correspondente ao seu navegador Chrome em [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).
   - Coloque o executável `chromedriver` no PATH do sistema ou na pasta do projeto.

4. Crie o arquivo `.env` a partir do exemplo disponível:
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` e preencha com suas credenciais do Instagram:
   ```
   USERNAME=seu_usuario
   PASSWORD=sua_senha
   ```

## Configuração

Edite o script para configurar suas preferências de sessão:

- **MAX_UNFOLLOWS**: Número total de perfis para deixar de seguir.
- **SESSION_LIMIT**: Número de perfis para deixar de seguir por sessão.
- **PAUSE_DURATION**: Duração da pausa (em minutos) entre as sessões.

Exemplo de configuração no script:

```python
MAX_UNFOLLOWS = 3000
SESSION_LIMIT = 100
PAUSE_DURATION = 10
```

## Uso

1. Execute o script:

   ```bash
   python unfollow_instagram.py
   ```

2. O script irá:
   - Fazer login no Instagram.
   - Navegar até sua lista de "Seguindo".
   - Deixar de seguir perfis em lotes, com pausas entre as sessões.

## Notas

- Use este script de forma responsável para evitar violar os termos de serviço do Instagram.
- Evite executar o script continuamente por longos períodos.
- Certifique-se de que as versões do Chrome e do ChromeDriver sejam compatíveis.

## Solução de Problemas

- **Erro de elemento não encontrado**:

  - Inspecione a estrutura HTML do Instagram para garantir que os seletores XPath no script estejam atualizados.

- **Conta bloqueada ou banida**:
  - Reduza o valor de `SESSION_LIMIT` e aumente o de `PAUSE_DURATION` para simular melhor o comportamento humano.

## Contribuição

Sinta-se à vontade para enviar issues ou pull requests para melhorar este projeto.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---

**Aviso Legal:**
Este script é apenas para fins educacionais. Use por sua conta e risco e esteja ciente dos termos de serviço do Instagram.
