# Incluir nova versão ao Changelog

## ✅ Utilização

### 🔍 Checar a próxima versão:

```bash
poetry run cz bump --dry-run --check-consistency
```

---

### 🚀 Gerar changelog e subir versão:

```bash
poetry run cz bump
```

Este comando irá:
- Ler os commits desde a última tag
- Gerar ou atualizar o arquivo `CHANGELOG.md`
- Atualizar a versão no `pyproject.toml`
- Criar uma nova tag Git (`vX.Y.Z`)

---

## 🧪 Exemplo de Commit (Conventional Commit)

Para que a geração do changelog funcione, siga o padrão:

```bash
git commit -m "feat(api): adiciona autenticação via Keycloak"
git commit -m "fix(db): corrige conexão com PostgreSQL"
```

### Tipos comuns:

| Tipo     | Descrição                     |
|----------|-------------------------------|
| `feat`   | Adição de funcionalidade nova |
| `fix`    | Correção de bug               |
| `docs`   | Documentação                  |
| `chore`  | Tarefa técnica/misc           |
| `refactor` | Refatoração de código       |

---

## (Opcional) Automatizar com `taskipy`

1. Instale o `taskipy`:

```bash
poetry add --group dev taskipy
```

2. Configure o `pyproject.toml` com a task de release:

```toml
[tool.taskipy.tasks]
release = "cz bump"
```

3. Rode com:

```bash
poetry run task release
```

---

## 🔚 Resultado Final

Após a configuração, o processo de release fica automatizado com:

- **Changelog gerado automaticamente**
- **Versão atualizada no `pyproject.toml`**
- **Tag Git criada**
- **Tudo pronto para CI/CD ou deploy**

---

## 📁 Arquivos Criados

- `CHANGELOG.md` — com histórico gerado automaticamente
- Tag Git (ex: `v1.2.0`)
- Versão atualizada no `pyproject.toml`

---

## 📚 Referências

- [Commitizen](https://github.com/commitizen-tools/commitizen)
- [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/)
- [Poetry](https://python-poetry.org/)