# Endpoints

## Autenticação
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
- Criar
- Retornar por ID
- Atualizar por ID
- Deletar  por ID
## Referências
- Listar
  - Paginação (Quantidade de itens retornados e iteração dos itens)
- Criar
- Retornar por ID
- Atualizar por ID
- Deletar  por ID

# TODO
- [X] Criar migration com atualização de tamanho da referência.
  - Migrations commitadas.
- [ ] Construir **raw text** para os campos de busca de palavra.
- [X] Incluir significados das palavras.
  - [Script](/database/importa_dados.sql) de inserção feito. 
- [ ] Vericar validações com novos tamanhos de campos.
- [X] Acordar se o fonema está associado à palavra ou significado.
  - Fonema ainda não padronizado;
  - Remover até versão final
- [ ] Checar se o significado pertence ao usuário e seu nível de autorização.
- [ ] Trocar [python-jose](https://pypi.org/project/python-jose/) para [pyjwt](https://pypi.org/project/PyJWT/) ou [PyJwt512](https://pypi.org/project/PyJwt512/).
- [ ] Ajustar significado e palavra.