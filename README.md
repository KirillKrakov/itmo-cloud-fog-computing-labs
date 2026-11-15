# ☁️ Облачные и туманные вычисления — Портфолио лабораторных работ (ИТМО)

> **Студент:** Краков Кирилл Константинович, группа P3431
> **Факультет:** ФПИиКТ, Университет ИТМО
> **Направление:** 09.03.01 «Информатика и вычислительная техника»
> **Дисциплина:** Облачные и туманные вычисления

Набор из 3 лабораторных работ, выстроенных как **последовательная эволюция от локальной контейнеризации к cloud-native оркестрации и edge-вычислениям**. Каждая работа — законченный проект с полным исходным кодом в соответствующей подпапке (`lab1-swarm/`, `lab2-k8s/`, `lab3-fog/`), готовый к запуску через `docker-compose up` или `kubectl apply`.

Сценарий курса — двухуровневое приложение интернет-магазина (Flask + Redis), которое проходит путь от одиночного контейнера до отказоустойчивого кластера с 5 репликами, rolling update без простоя и edge-шлюза для IoT-датчиков.

---

## 🎯 Ключевые компетенции

- **Контейнеризация:** написание `Dockerfile`, multi-stage builds, `docker-compose.yml`, изоляция сервисов через bridge/overlay сети.
- **Docker Swarm:** инициализация кластера, `docker stack deploy`, декларативное управление сервисами, self-healing, горизонтальное масштабирование (`docker service scale`).
- **Kubernetes:** работа с Minikube, примитивы `Pod`, `Deployment`, `Service` (ClusterIP / NodePort), `readinessProbe`, `kubectl apply`, Rolling Update без простоя.
- **Service Discovery:** встроенный DNS Swarm и K8s, обращение к сервисам по имени (`redis`, `mosquitto`), overlay-сети.
- **Edge/Fog Computing:** архитектура Edge → Fog → Cloud, MQTT-брокер (Mosquitto), визуальная логика шлюза в Node-RED, фильтрация трафика на границе сети.
- **Отказоустойчивость:** политики рестарта (`restart: unless-stopped`, `restart_policy: condition: any`), автоматическое пересоздание упавших задач.
- **Observability:** работа с логами контейнеров, health-check через `readinessProbe`, диагностика через `docker service ps`, `kubectl get pods -o wide`.

---

## 📚 Обзор выполненных работ

| # | Работа | Тема | Ключевой результат | Директория |
|---|--------|------|---------------------|------------|
| 1 | **ЛР1** | От Docker к Swarm | Переход от `docker-compose` к оркестрации: self-healing, 5 реплик frontend, балансировка запросов между контейнерами | `lab1-swarm/` |
| 2 | **ЛР2** | Миграция в Kubernetes | Трансляция compose-логики в K8s-манифесты, Rolling Update (v1 → v2) без простоя, NodePort для внешнего доступа | `lab2-k8s/` |
| 3 | **ЛР3** | Edge/Fog шлюз «Умной фабрики» | Трёхуровневая архитектура: датчик (Python) → шлюз (Node-RED) → облако (Mosquitto), фильтрация критических событий на границе | `lab3-fog/` |

---

## 🛠 Инструменты и технологии

![Docker](https://img.shields.io/badge/Docker-Compose%20%7C%20Swarm-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube%20%7C%20kubectl-326CE5?logo=kubernetes)
![Python](https://img.shields.io/badge/Python-Flask%20%7C%20paho--mqtt-3776AB?logo=python)
![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-green)
![Node-RED](https://img.shields.io/badge/Node--RED-Flow--based-orange)
![Redis](https://img.shields.io/badge/Redis-7--alpine-DC382D?logo=redis)
![SRE](https://img.shields.io/badge/Practices-Self--healing%20%7C%20Rolling%20Update-lightgrey)
![ITMO](https://img.shields.io/badge/University-ITMO-blue)

---

## 🔍 Краткое содержание работ

### ЛР1 — От Docker к Swarm (оркестрация)
**Сценарий:** интернет-магазин готовится к «Чёрной пятнице» — нужно выдержать наплыв трафика.

**Архитектура:**
- **Frontend:** Flask-приложение, отображающее счётчик посещений.
- **Backend:** Redis для хранения количества хитов.

**Этапы:**
1. Написан `Dockerfile` и `docker-compose.yml` для локального запуска — проверена связность App ↔ Redis.
2. Кластер инициализирован через `docker swarm init` (single-node: manager + worker).
3. Compose-файл конвертирован в `docker-stack.yml` с секцией `deploy:` (реплики, политики рестарта, overlay-сеть).
4. **Тест на отказ (self-healing):** `docker kill <container_id>` → Swarm автоматически пересоздаёт задачу.
5. **Масштабирование:** `docker service scale shop_frontend=5` → запросы распределяются между 5 репликами (проверено по меняющемуся hostname контейнера на странице).

**Ключевой вывод:** Docker Compose удобен для локальной разработки, но только Swarm/K8s дают декларативное управление состоянием, автоматическое восстановление и горизонтальное масштабирование.

---

### ЛР2 — Миграция в Kubernetes (Cloud-Native)
**Сценарий:** перенос приложения из Swarm в Kubernetes с использованием декларативных манифестов.

**Архитектура (K8s-примитивы):**
- `redis-deployment.yaml` + `redis-service.yaml` (ClusterIP) — внутренний сервис.
- `frontend-deployment.yaml` (2 реплики, `readinessProbe`) + `frontend-service.yaml` (NodePort).

**Этапы:**
1. Запущен локальный кластер через `minikube start`.
2. Образ `shop_frontend:v1` собран и загружен в Minikube через `minikube image load`.
3. Манифесты применены через `kubectl apply -f k8s/`.
4. Доступ получен через `minikube service frontend --url` (проксирование NodePort → localhost).
5. **Rolling Update:** код обновлён (новая вёрстка), собран образ `v2`, манифест изменён → `kubectl apply` плавно заменяет старые поды новыми **без простоя сервиса**.

**Ключевой вывод:** Kubernetes добавляет слой абстракции над контейнерами — декларативное описание желаемого состояния, автоматический жизненный цикл подов, встроенный service discovery (DNS-имя `redis` доступно всем подам frontend).

---

### ЛР3 — Edge/Fog шлюз «Умной фабрики»
**Сценарий:** на заводе установлены датчики температуры. Нужен «туманный узел», который фильтрует нормальные показания локально и оповещает облако только о критических событиях.

**Трёхуровневая архитектура:**
- **Edge (датчик):** Python-скрипт, генерирующий случайную температуру и публикующий её в MQTT-топик `factory/sensor/1` каждую секунду.
- **Fog (шлюз):** Node-RED с визуальной логикой: `MQTT In → JSON → Switch (>80?) → MQTT Out (factory/cloud/alerts)`.
- **Cloud (центр):** Python-подписчик, получающий только критические алерты.

**Инфраструктура (всё в Docker):**
- `mosquitto` — MQTT-брокер с persistence.
- `node-red` — визуальный flow-редактор (настраивается через `localhost:1880`).
- `sensor`, `cloud` — кастомные образы с `paho-mqtt`.
- Единая bridge-сеть `factory-net` для service discovery по DNS.

**Ключевой результат:** облако получает лишь малую часть трафика — только сообщения с `temp > 80`. Это демонстрирует **экономию пропускной способности (bandwidth savings)** — главный принцип fog computing.

---

## 💡 Применимость в SRE-практиках

| Навык из курса | Применение в SRE |
|----------------|------------------|
| Docker + Docker Compose | Базовая упаковка сервисов, воспроизводимость окружений, локальная отладка инцидентов |
| Docker Swarm (self-healing, scale) | Понимание принципов оркестрации, которые напрямую переносятся на K8s/ECS |
| Kubernetes (Deployment, Service, readinessProbe) | **Прямой production-навык** — развёртывание, обновление и мониторинг сервисов в кластере |
| Rolling Update без простоя | Zero-downtime deployments — ключевое требование к SRE при релизах |
| Service Discovery (DNS в overlay-сетях) | Понимание, как сервисы находят друг друга в микросервисной архитектуре |
| Edge/Fog + MQTT | Проектирование IoT-инфраструктуры, edge-обработка, снижение нагрузки на центр |
| Node-RED flow-логика | Быстрое прототипирование правил маршрутизации и фильтрации событий |
| Health-check (readinessProbe) | Понимание разницы между liveness/readiness — критично для корректного вывода подов из балансировки |
| Declarative infrastructure (YAML-манифесты) | GitOps-подход, Infrastructure as Code — основа современной SRE-практики |
| Observability (логи, `kubectl get pods`, `docker service ps`) | Диагностика состояния кластера, troubleshooting упавших подов и сервисов |

---

## 📂 Структура репозитория

```
.
├── README.md                          ← этот файл
├── reports/                           ← отчёты и вспомогательные материалы
│   ├── ЛР №1 по ОТВ Краков Кирилл.pdf
│   ├── ЛР №2 по ОТВ Краков Кирилл.pdf
│   ├── ЛР №3 по ОТВ Краков Кирилл.pdf
│   └── список последовательных команд для запуска ЛР.txt
├── lab1-swarm/                        ← ЛР1: Docker → Swarm
│   ├── frontend/
│   │   ├── app.py                     # Flask-приложение со счётчиком
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── docker-compose.yml             # локальный запуск
│   └── docker-stack.yml               # деплой в Swarm
├── lab2-k8s/                          ← ЛР2: Kubernetes (Minikube)
│   ├── frontend/                      # (образ v1/v2)
│   └── k8s/
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml      # NodePort
│       ├── redis-deployment.yaml
│       └── redis-service.yaml         # ClusterIP
└── lab3-fog/                          ← ЛР3: Edge/Fog шлюз
    ├── sensor/                        # Edge: датчик температуры
    ├── cloud/                         # Cloud: подписчик на алерты
    ├── node-red/                      # Fog: визуальный шлюз
    ├── mosquitto/config/              # MQTT-брокер
    └── docker-compose.yml
```

### Быстрый старт

```bash
# ЛР1 — Swarm
cd lab1-swarm && docker-compose up --build
docker swarm init
docker stack deploy -c docker-stack.yml shop
docker service scale shop_frontend=5

# ЛР2 — Kubernetes
cd lab2-k8s && minikube start
docker build -t shop_frontend:v1 ./frontend
minikube image load shop_frontend:v1
kubectl apply -f k8s/
minikube service frontend --url

# ЛР3 — Edge/Fog
cd lab3-fog && docker-compose up --build
# открыть http://localhost:1880 (Node-RED UI)
```
