
# tex2pdf API

Este projeto é uma API em Flask que permite converter arquivos LaTeX (.tex) contidos em arquivos ZIP em PDFs. A API aceita um arquivo ZIP contendo um arquivo `.tex` e, opcionalmente, imagens associadas, e retorna o arquivo PDF gerado.

## Como funciona

1. O usuário envia um arquivo ZIP contendo um arquivo `.tex` (e imagens na pasta `fig`, caso haja).
2. O arquivo ZIP é extraído temporariamente.
3. O arquivo `.tex` é compilado para PDF utilizando o `pdflatex`.
4. Se o PDF for gerado com sucesso, ele é retornado ao usuário para download.
5. Arquivos temporários são removidos após a geração do PDF.

## Requisitos

- Python 3.x
- Flask
- pdflatex (disponível em sistemas com TeX Live ou MiKTeX)
- Docker (opcional, mas recomendado para facilitar a execução)

## Instalação

### Usando Docker

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. Construa e inicie o container Docker:

   ```bash
   docker-compose up -d --build
   ```

3. A API estará disponível em `http://latex.localhost`.

### Instalação manual

Caso não queira utilizar Docker, você pode rodar a aplicação diretamente no seu ambiente local:

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Certifique-se de que o `pdflatex` esteja instalado e disponível no PATH.
   
   - No Ubuntu, por exemplo, você pode instalar o TeX Live com o comando:
     
     ```bash
     sudo apt-get install texlive
     ```

3. Execute o aplicativo:

   ```bash
   python app.py
   ```

4. Acesse a API em `http://localhost:5000`.

## Endpoints

### `POST /generate-pdf`

Este endpoint permite enviar um arquivo ZIP contendo um arquivo `.tex` para ser compilado em um PDF.

#### Parâmetros

- **file** (required): O arquivo ZIP contendo um arquivo `.tex` e, opcionalmente, imagens na pasta `fig`.

#### Respostas

- **200 OK**: O PDF gerado será retornado como resposta para download.
- **400 Bad Request**: Caso o arquivo enviado não seja válido (não for um ZIP ou não contenha um arquivo `.tex`).
- **500 Internal Server Error**: Se ocorrer um erro durante a compilação do arquivo `.tex`.

#### Exemplo de Request

```bash
curl -X POST -F "file=@path/to/your/file.zip" http://localhost:5000/generate-pdf
```

#### Exemplo de Resposta

Se a compilação for bem-sucedida, o PDF será retornado para download:

```bash
Content-Type: application/pdf
Content-Disposition: attachment; filename=example.pdf
```

### Limpeza de arquivos temporários

Após a geração do PDF, os arquivos temporários (arquivo ZIP, arquivos extraídos e PDF gerado) são removidos automaticamente.

## Contribuindo

Sinta-se à vontade para fazer contribuições! Se você encontrar algum bug ou tiver sugestões de melhorias, abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
