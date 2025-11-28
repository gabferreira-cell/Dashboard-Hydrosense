# 🌱 Dashboard Interativo de Irrigação e Umidade do Solo para Cultivo de Tomate

Este projeto apresenta um dashboard interativo desenvolvido em **Python (Dash + Plotly)** para monitorar o uso de água e a umidade do solo ao longo das estações do ano no plantio de tomates. Com visual dinâmico, gráficos responsivos e troca automática de tema conforme a estação selecionada, o sistema permite uma análise clara e intuitiva, servindo como base para futuras integrações com sensores reais e soluções de automação agrícola.

---

## 🚀 Visão Geral do Projeto

Este projeto apresenta um dashboard interativo para monitoramento do uso de irrigação e da umidade do solo no cultivo de tomate. O sistema permite visualizar indicadores por estação do ano, alternando automaticamente o tema, as cores e os dados exibidos para facilitar a análise agrícola.

---

## 🧩 Principais Recursos

- Visualização da umidade média do solo (%) por estação.  
- Monitoramento do uso de água (m³) com destaque para a média geral.  
- Interface dinâmica com mudança automática de cores e temas.  
- Gráficos responsivos criados com Plotly (barras verticais e horizontais).  
- Seleção interativa das estações do ano (Primavera, Verão, Outono e Inverno).  

---

## 🧰 Tecnologias Utilizadas

- Python  
- Dash (Plotly)  
- Pandas  
- Bootstrap Components (DBC)  
- Visualizações com Plotly Express  

---

## 📌 Funcionamento do Sistema

- O dashboard carrega dados simulados sobre uso de água e umidade do solo.  
- Ao clicar em uma estação, o sistema filtra os dados daquela época do ano.  
- Todo o layout muda junto com a estação (cores, título, painéis e gráficos).  
- Um botão **“Limpar Filtros”** retorna os dados gerais de todo o cultivo.

---

## 📸 Estrutura Geral (Resumo)

- Botões interativos para cada estação.  
- Métricas automáticas (média de umidade e uso de água).  
- Gráfico de barra vertical para umidade.  
- Gráfico horizontal para uso de água com linha de referência da média.  
- Tema adaptativo baseado em cores e emojis de cada estação.

---

## 🧪 Testes Realizados

- Testes de navegação entre estações com animações fluídas.  
- Validação dos cálculos de média e atualização dinâmica.  
- Teste de responsividade em diferentes tamanhos de tela.  
- Teste de contraste e estética em cada paleta de cores.

---

## 📈 Resultados Obtidos

- Dashboard intuitivo e totalmente interativo.  
- Facilita a análise da irrigação por estação do ano.  
- Visual moderno, dinâmico e agradável ao usuário.  
- Base ideal para integração futura com sensores reais (ESP32, MQTT, APIs).

---

## 💡 Possíveis Melhorias Futuras

- Integrar o dashboard a dados reais de sensores via API ou MQTT.  
- Criar controle automatizado de irrigação via interface web.  
- Implementar histórico de dados e armazenamento em nuvem.  
- Adicionar previsão do tempo e recomendações inteligentes de irrigação.

---

## 👤 Autores

Projeto desenvolvido por **Lívia Araújo, Gabriel Ferreira, Emanuel Santana e Kayo Andrade**, como parte de um trabalho prático tópicos em bigdata com Python, para análise de dados aplicados à agricultura.
