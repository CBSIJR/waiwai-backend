# Endpoints

## Autenticação e Autorização
- Registro
- Acesso
## Palavras
- Listar
  - Paginação (Quantidade de itens retornados e iteração dos itens)
- Criar
- Retornar por ID
- Atualizar por ID
- Deletar  por ID
## Significados das palavras
- Criar
- Atualizar
## Significados
- Retornar por ID
- Atualizar por ID
- Deletar por ID
## Categorias
- Listar
  - Paginação (Quantidade de itens retornados e iteração dos itens)
  - Busca textual
- Criar
- Retornar por ID
- Atualizar por ID
- Deletar  por ID
## Referências
- Listar
  - Paginação (Quantidade de itens retornados e iteração dos itens)
  - Busca textual
- Criar
- Retornar por ID
- Atualizar por ID
- Deletar  por ID

# TODO
- [X] Criar migration com atualização de tamanho da referência.
  - Migrations commitadas.
- [ ] Construir **raw text** para os campos de busca de palavra.
- [X] Script para incluir significados das palavras.
- [ ] Vericar validações com novos tamanhos de campos.
- [X] Acordar se o fonema está associado à palavra ou significado.
  - Fonema ainda não padronizado;
  - Remover até versão final
- [ ] Checar se o significado pertence ao usuário e seu nível de autorização.
- [ ] Trocar [python-jose](https://pypi.org/project/python-jose/) para [pyjwt](https://pypi.org/project/PyJWT/) ou [PyJwt512](https://pypi.org/project/PyJwt512/).
- [ ] Ajustar significado e palavra.
- [X] Relacionar anexos com o usuário.
- [ ] Checar em modelos validação para texto vazio e com espaços fora do corpo.
- [X] Criar associação de upload
- [X] Fazer rota de upload.
- [ ] Melhorar tratamento para tipos seguros de arquivos na rota upload.
- [ ] Para upload, deve-se criar arquivo temporário para escrevê-lo posteriormente na pasta pública.
- [ ] Corrigir performance exportação de tabelas. URGENTE!
- [ ] Incluir container NGINX para proxy e cacheamento das rotas de exportação. 
- [ ] Configuração de cacheamento para rotas de exportação. [Aqui](https://www.uvicorn.org/deployment/#running-with-https). 
- [ ] Ajuste no deploy para proxy NGINX. [Aqui](https://www.youtube.com/watch?v=ltwt2WcH_S8).