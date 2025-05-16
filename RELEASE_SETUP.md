# 📦 Automação de Versão e Changelog com Python, Poetry e Commitizen

Este documento descreve como configurar a automação de versionamento e geração de changelog para um projeto Python gerenciado com Poetry.

---

## 📌 Requisitos

- Python (>=3.7)
- [Poetry](https://python-poetry.org/)
- Git (com repositório inicializado)
- Commits seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/)

---

## ⚙️ Instalação das Ferramentas

1. **Adicione o Commitizen como dependência de desenvolvimento:**

```bash
poetry add --group dev commitizen
```

---

## 🛠️ Configuração

2. **Adicione as seguintes configurações ao seu `pyproject.toml`:**

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"  # versão inicial
version_files = ["pyproject.toml"]
tag_format = "v$version"
```

> Essa configuração define:
> - O padrão de commits usado (`cz_conventional_commits`)
> - O arquivo que terá sua versão atualizada automaticamente
> - O formato da tag usada no Git (ex: `v1.2.0`)

---