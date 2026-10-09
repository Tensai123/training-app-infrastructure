# Standardy Tworzenia Commitów i Pull Requestów (SOC2 & PR Compliance)

Dokument opisuje wymagane zasady wersjonowania kodu, tworzenia commitów oraz zgłaszania Pull Requestów zgodne z wymaganiami audytowymi SOC2.

---

## 1. Standard Tworzenia Commitów

Każdy commit w repozytorium jest częścią ścieżki audytowej (*audit trail*). Musi być jednoznacznie powiązany z zadaniem w Jira oraz opisywać intencję zmiany.

### Struktura komunikatu commitu:
```text
type(scope): krótki zwięzły opis (PROJEKT-NNNN)
```

Gdzie:
- `type`: Typ zmiany wg standardu Conventional Commits (patrz tabela poniżej).
- `scope`: Zakres/komponent systemu (np. `api`, `worker`, `frontend`, `deps`, `docs`).
- `opis`: Zrozumiały opis w trybie rozkazującym lub czasu teraźniejszego (bez kropki na końcu).
- `(PROJEKT-NNNN)`: Obowiązkowy klucz zadania z Jira w nawiasie na końcu (np. `(DEVO-20450)`).

> [!IMPORTANT]
> **Zasada SOC2**: Klucz zadania Jira **musi** znajdować się w każdym commicie trafiającym do gałęzi głównej.

### Dopuszczalne typy commitów (`type`):
| Typ | Zastosowanie | Przykład |
| :--- | :--- | :--- |
| `feat` | Nowa funkcjonalność dla użytkownika lub systemu | `feat(api): add task cancellation endpoint (DEVO-12345)` |
| `fix` | Poprawka błędu / bugfix | `fix(worker): handle redis reconnection timeout (DEVO-12345)` |
| `docs` | Zmiany wyłącznie w dokumentacji lub szablonach | `docs(readme): add local setup instructions (DEVO-12345)` |
| `refactor`| Refaktoryzacja kodu (bez zmiany zachowania i API) | `refactor(database): extract session lifecycle (DEVO-12345)` |
| `chore` | Drobne prace porządkowe, aktualizacje zależności | `chore(deps): bump pydantic to 2.6.4 (DEVO-12345)` |
| `test` | Dodanie lub poprawa testów automatycznych | `test(api): add healthcheck integration tests (DEVO-12345)` |
| `ci` | Zmiany w pipeline'ach CI/CD lub workflow GitHub | `ci(github): add automated syntax linting (DEVO-12345)` |

### Dobre praktyki atomowości commitów:
1. **Jeden commit = jedna logiczna zmiana**: Nie łącz refaktoringu z dodawaniem nowych funkcji ani ze zmianami formatowania.
2. **Kompilowalny stan**: Każdy commit powinien zostawiać kod w stanie działającym (przechodzącym testy/kompilację).
3. **Użycie `git commit --amend`**: Jeśli przed wystawieniem PR chcesz poprawić komunikat ostatniego commitu lub dodać przeoczony plik:
   ```bash
   git commit --amend -m "feat(scope): poprawny opis z taskiem (DEVO-NNNN)"
   ```

---

## 2. Standard Nazewnictwa Gałęzi (Branch Naming)

Nowe gałęzie funkcyjne tworzymy według schematu:
```text
type/projekt-NNNN-krotki-opis
```
Przykłady:
- `feat/devo-12345-microservices-app`
- `fix/devo-12399-worker-reconnect`

---

## 3. Standard Pull Requestów (PR Compliance)

Każdy PR musi spełniać poniższy kontrakt:

1. **Tytuł PR**:
   Musi odpowiadać schematowi: `type(scope): opis (PROJEKT-NNNN)`
   Przykład: `feat(apps): add microservices application source code (DEVO-12345)`

2. **Ciało PR (Body)**:
   Musi wypełniać szablon `.github/pull_request_template.md` zawierający 4 sekcje:
   - `## Task`: **Pełny URL** do zadania Jira (np. `https://xplus-product-support.atlassian.net/browse/DEVO-12345`), a nie sam numer.
   - `## Problem / context`: 1–3 zdania wyjaśniające cel biznesowy lub problem techniczny.
   - `## Changes`: Wypunktowana lista kluczowych zmian w plikach i komponentach.
   - `## Verification`: Konkretne kroki i zaobserwowane wyniki weryfikacji (np. wynik testów, kod wyjścia `0`, zrzut logów).

3. **Checklista przed wystawieniem PR**:
   ```bash
   # Sprawdzenie czy task jest w treści:
   grep -cE '[A-Z][A-Z0-9]+-[0-9]+' pr-description.md
   
   # Sprawdzenie czy nie ma placeholderów:
   grep -nE '<!--|TODO|TBD|-NNNN|-XXXXX' pr-description.md
   
   # Sprawdzenie linku URL pod Task:
   grep -A2 '^## Task' pr-description.md | grep -c '^https://'
   ```
