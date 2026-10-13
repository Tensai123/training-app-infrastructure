# Training App - Automatyzacja Wdrożenia z Ansible (Ubuntu 24.04)

Playbook Ansible do automatycznego wdrożenia mikrousług (`api`, `worker`, `frontend`, `redis`) na serwerze z systemem Ubuntu 24.04 LTS w architekturze kontenerowej (Docker Compose).

---

## Struktura katalogu

```
ansible/
├── ansible.cfg                      # Konfiguracja Ansible (SSH, inventory, callbacks)
├── deploy.yml                       # Główny playbook wdrożeniowy
├── inventory/
│   ├── hosts.ini                    # Plik inwentarza z adresem IP serwera docelowego
│   └── group_vars/
│       └── all.yml                  # Zmienne globalne (porty, tagi obrazów, ścieżki)
└── roles/
    ├── docker/                      # Rola instalująca Docker CE i Docker Compose Plugin
    │   └── tasks/main.yml
    └── app/                         # Rola wdrażająca aplikację
        ├── defaults/main.yml
        ├── tasks/main.yml
        └── templates/
            ├── docker-compose.yml.j2
            └── .env.j2
```

---

## Wymagania wstępne

1. Zainstalowany **Ansible** na maszynie lokalnej (`ansible --version`).
2. Dostęp SSH do serwera docelowego (np. klucz SSH w `~/.ssh/id_rsa` lub `~/.ssh/id_ed25519`).
3. Użytkownik z uprawnieniami `sudo` (np. domyślny `ubuntu`).

---

## Uruchomienie wdrożenia

### 1. Skonfiguruj adres IP serwera w inwentarzu:
Otwórz `ansible/inventory/hosts.ini` i podaj adres IP oraz użytkownika SSH:
```ini
[app_servers]
target-server ansible_host=TWOJ_ADRES_IP ansible_user=ubuntu
```

*(Opcjonalnie, jeśli używasz niestandardowego klucza SSH: dodaj `ansible_ssh_private_key_file=~/.ssh/twoj_klucz`)*.

### 2. Sprawdź łączność SSH:
```bash
cd ansible
ansible app_servers -m ping
```

### 3. Uruchom wdrożenie:
```bash
ansible-playbook deploy.yml
```

Playbook automatycznie:
1. Zainstaluje oficjalny Docker CE oraz Docker Compose na Ubuntu 24.04.
2. Przygotuje strukturę katalogów w `/opt/training-app`.
3. Wygeneruje sparametryzowane pliki `docker-compose.yml` oraz `.env`.
4. Pobierze najnowsze obrazy z Docker Hub (`tensai123/training-*`).
5. Uruchomi kontenery w tle.
6. Odczeka na status 200 z endpointu `/health`.
