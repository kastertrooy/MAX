┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           УРОВЕНЬ 1: ИНТЕРФЕЙСЫ ПОЛЬЗОВАТЕЛЯ                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────┐    ┌─────────────────────────────┐    ┌──────────────┐ │
│  │      TELEGRAM BOT           │    │        EMAIL MONITOR        │    │   LOCAL UI   │ │
│  │                             │    │                             │    │  (optional)  │ │
│  │  • Inline кнопки управления │    │  • IMAP каждые 10 мин       │    │  • CLI       │ │
│  │  • Уведомления о событиях   │    │  • Парсинг GitHub писем     │    │  • Web       │ │
│  │  • Приоритизация задач      │    │  • AI перевод на русский    │    │  • TUI       │ │
│  │  • Настройки параметров     │    │  • Callback кнопки в TG     │    │              │ │
│  └─────────────────────────────┘    └─────────────────────────────┘    └──────────────┘ │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         УРОВЕНЬ 2: ЯДРО ОРКЕСТРАЦИИ (CORE)                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         ORCHESTRATOR ENGINE                                      │   │
│  │                                                                                  │   │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │   │                    STATE MACHINE MANAGER                                   │   │   │
│  │   │                                                                              │   │   │
│   │   │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌────────┐│   │   │
│   │   │  │  IDLE   │───→│ FETCHING│───→│ANALYZING│───→│ CODING  │───→│TESTING ││   │   │
│   │   │  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └───┬────┘│   │   │
│   │   │                                                                  │      │   │   │
│   │   │  ┌─────────┐    ┌─────────┐                                    │      │   │   │
│   │   │  │COMPLETED│←───│CREATE_PR│←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←┘      │   │   │
│   │   │  └─────────┘    └─────────┘                                           │   │   │
│   │   │       ↑                                                                │   │   │
│   │   │       └←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←┘      │   │
│   │   │                    RETRY CONTROLLER (max 3 attempts)                     │   │   │
│   │   │                                                                              │   │   │
│   │   │  Ошибка на любом этапе → Возврат к CODING с контекстом ошибки → Повтор     │   │   │
│   │   │  После 3 попыток → BLACKLIST                                               │   │   │
│   │   └─────────────────────────────────────────────────────────────────────────────┘   │
│   │                                                                                      │
│   │   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │   │                    PRIORITY QUEUE MANAGER                                  │       │
│   │   │                                                                              │       │
│   │   │  СТРУКТУРА ОЧЕРЕДИ:                                                        │       │
│   │   │  • Heap-based (heapq) для O(log n) операций                                │       │
│   │   │  • Ключ сортировки: (-bounty_amount, created_at, issue_id)                │       │
│   │   │  • Persistence: Автосохранение в SQLite при каждом изменении               │       │
│   │   │  • Recovery: Полная загрузка из БД при старте                              │       │
│   │   │                                                                              │       │
│   │   │  ОПЕРАЦИИ:                                                                 │       │
│   │   │  • put(issue) → Добавление с приоритетом                                   │       │
│   │   │  • get() → Извлечение highest priority (thread-safe)                       │       │
│   │   │  • prioritize(issue_id, level) → Ручное повышение приоритета               │       │
│   │   │  • remove(issue_id) → Исключение из очереди                                │       │
│   │   └─────────────────────────────────────────────────────────────────────────┘       │
│   │                                                                                      │
│   │   ┌─────────────────────────────────────────────────────────────────────────┐       │
│   │   │                    RATE LIMIT CONTROLLER                                   │       │
│   │   │                                                                              │       │
│   │   │  GITHUB API:                                                                 │       │
│   │   │  • Limit: 5000 requests/hour                                               │       │
│   │   │  • Window: Sliding window tracking                                         │       │
│   │   │  • Action при <100: Пауза 60 сек → Повторная проверка                      │       │
│   │   │  • Action при <10: Критическая пауза → Уведомление TG → Ожидание          │       │
│   │   │                                                                              │       │
│   │   │  OPENAI API:                                                                 │       │
│   │   │  • Tier-based limits (RPM, TPM)                                            │       │
│   │   │  • Tracking: tokens/minute, requests/minute                                │       │
│   │   │  • Action при критическом: STOP PROGRAM → Уведомление TG                   │       │
│   │   │                                                                              │       │
│   │   │  DOCKER:                                                                     │       │
│   │   │  • Local resource limits (CPU, RAM)                                          │       │
│   │   │  • Concurrent container limit: 1 (последовательная обработка)               │       │
│   │   └─────────────────────────────────────────────────────────────────────────┘       │
│   │                                                                                      │
│   └─────────────────────────────────────────────────────────────────────────────────────┘
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      УРОВЕНЬ 3: МОДУЛИ ИНТЕГРАЦИИ (ADAPTERS)                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌──────────────┐ │
│  │      GITHUB MODULE          │  │        AI MODULE             │  │ DOCKER MODULE│ │
│  │                             │  │                               │  │              │ │
│  │  DUAL TOKEN ARCHITECTURE:   │  │  PROVIDER MANAGEMENT:         │  │  LIFECYCLE:  │ │
│  │  • READ_TOKEN (repo, org)   │  │  • Primary: GPT-4             │  │  • Ensure    │ │
│  │  • WRITE_TOKEN (workflow)   │  │  • Fallback: Claude-3         │  │    running   │ │
│  │                             │  │  • Switch: Manual (TG)        │  │  • Build     │ │
│  │  SUBMODULES:                │  │                               │  │  • Test      │ │
│  │  • Client (rate tracking)   │  │  COMPONENTS:                │  │  • Cleanup   │ │
│  │  • IssueAnalyzer (bounty)   │  │  • PromptEngineer             │  │              │ │
│  │  • ContentAPI (<100MB)      │  │  • CodeGenerator              │  │  SECURITY:   │ │
│  │  • GraphQLClient (linked)   │  │  • CommitMessageGenerator     │  │  • Pattern   │ │
│  │  • PRManager (create/commit)│  │  • OutputValidator            │  │    matching  │ │
│  │  • CommentManager           │  │                               │  │  • AST scan  │ │
│  │                             │  │  TOKEN TRACKING:              │  │  • Sandbox   │ │
│  │  OPERATIONS:                │  │  • Input/Output per request   │  │              │ │
│  │  • Search issues by labels  │  │  • Cost estimation            │  │  RESOURCES:  │ │
│  │  • Detect bounty via AI     │  │  • Monthly budget tracking    │  │  • Fixed:    │ │
│  │  • Download relevant files  │  │                               │  │    2-4-6 CPU │ │
│  │  • Parse linked issues A+B  │  │                               │  │  • RAM:      │ │
│  │  • Create branch ai/123/ts  │  │                               │  │    512+kb/10 │ │
│  │  • Commit with AI message   │  │                               │  │              │ │
│  │  • Create PR with body      │  │                               │  │  TIMEOUT:    │ │
│  │  • Comment on issue         │  │                               │  │    25 sec    │ │
│  └─────────────────────────────┘  └─────────────────────────────┘  └──────────────┘ │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         УРОВЕНЬ 4: ХРАНИЛИЩЕ ДАННЫХ (STORAGE)                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         SQLITE DATABASE SCHEMA                                     │   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  REPOSITORIES                                                                ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | owner | name | full_name | language | stars | last_checked | is_active  ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  ISSUES (central entity)                                                     ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | github_id | repo_id | number | title | body                           ││   │
│  │  │  has_bounty | bounty_amount | bounty_currency | detected_by                 ││   │
│  │  │  status (enum) | priority | queue_position                                   ││   │
│  │  │  linked_issue_ids [JSON] | linked_pr_numbers [JSON]                           ││   │
│  │  │  attempt_count | max_attempts | created_at | updated_at | started_at         ││   │
│  │  │  completed_at | is_blacklisted | blacklist_reason                             ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  ATTEMPTS (retry tracking)                                                   ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | issue_id | attempt_number | status (enum)                            ││   │
│  │  │  ai_model_used | prompt_tokens | completion_tokens | ai_response_raw        ││   │
│  │  │  generated_code [JSON] | files_modified [JSON]                              ││   │
│  │  │  docker_image | docker_cpu | docker_memory | test_duration                   ││   │
│  │  │  error_message | error_traceback | security_violations [JSON]               ││   │
│  │  │  created_at                                                                    ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  PULL_REQUESTS                                                               ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | issue_id | github_pr_number | branch_name | commit_sha                 ││   │
│  │  │  commit_message | pr_url | status | created_at | merged_at                  ││   │
│  │  │  initial_comment_posted | completion_comment_posted                         ││   │
│  │  │  email_notification_sent                                                     ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  BLACKLIST (permanent blocks)                                                ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | issue_id | reason | added_at | added_by | is_permanent (always TRUE)   ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  ANALYTICS (success metrics)                                                 ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | issue_id | estimated_bounty | actual_earned | currency                ││   │
│  │  │  time_to_solve | total_ai_tokens | github_api_calls | docker_runs           ││   │
│  │  │  success | failure_reason | language | recorded_at                          ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  RATE_LIMIT_LOGS (API monitoring)                                            ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | service | limit_remaining | limit_total | reset_at | warning_sent       ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐│   │
│  │  │  TELEGRAM_LOGS (notification history)                                          ││   │
│  │  │  ─────────────                                                               ││   │
│  │  │  id | message_type | chat_id | message_text | issue_id | sent_at | delivered  ││   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘│   │
│  │                                                                                  │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. ДЕТАЛЬНАЯ ЛОГИКА ПОТОКОВ (FLOW LOGIC)

### ПОТОК 1: Первичное сканирование (Discovery Flow)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   STARTUP   │────→│  LOAD REPOS  │────→│  SCAN ISSUES│────→│  AI BOUNTY  │
│             │     │  from DB     │     │  by labels   │     │  DETECTION  │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                    │
    ┌───────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  CALCULATE  │────→│   INSERT    │────→│   NOTIFY    │
│  PRIORITY   │     │  into QUEUE │     │   (none)    │
│  (-bounty)  │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Логика:**
1. При старте загружаем список репозиториев из БД (или получаем через API)
2. Для каждого репозитория: GraphQL запрос на открытые issue с метками `[bounty, reward, $, paid, RTC]`
3. AI анализ текста issue (title + body) на наличие сумм (`$500`, `USD 100`, `reward: 50`)
4. Расчёт приоритета: `priority = -bounty_amount` (отрицательное для max-heap)
5. Вставка в PriorityQueue с сохранением в SQLite
6. **Нет уведомления** — только фоновое добавление в очередь

---

### ПОТОК 2: Обработка issue (Processing Flow)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  QUEUE GET  │────→│   FETCH     │────→│   ANALYZE   │────→│   GENERATE  │
│  (blocking) │     │   DATA      │     │   CONTEXT   │     │    CODE     │
└─────────────┘     └──────┬──────┘     └─────────────┘     └──────┬──────┘
                           │                                         │
                           │    ┌─────────────┐                      │
                           └───→│ CHECKPOINT  │←─────────────────────┘
                                │   SAVE      │
                                └─────────────┘
```

**Детализация этапов:**

| Этап | Действия | Выход при ошибке |
|------|----------|------------------|
| **FETCH** | • Проверить Docker запущен (автозапуск)<br>• Content API: скачать файлы, связанные с issue<br>• GraphQL: получить linked issues (A+B)<br>• GraphQL: получить linked PR + их код<br>• Проверка размера каждого файла <100MB | `BLACKLIST` (file too large) → permanent |
| **ANALYZE** | • AI анализ: issue description + linked issues + PR код<br>• Формирование solution plan<br>• Определение файлов для модификации | Retry (max 3) → `BLACKLIST` |
| **CODE** | • AI генерация кода по plan<br>• Security scan: паттерны (rm -rf, System.exit, os.system)<br>• Commit message generation | `BLACKLIST` (security) → permanent |
| **TEST** | • Расчёт ресурсов: CPU ступени (2-4-6), RAM=512+kb/10<br>• Docker run с network=none, read-only volumes<br>• Таймаут 25 секунд<br>• Проверка exit code | Retry (max 3) → `BLACKLIST` |
| **PR** | • Создание ветки `ai/{issue_number}/{timestamp}`<br>• Commit с AI-generated message<br>• Push → Create PR → Comment in issue | Retry (max 3) → `BLACKLIST` |

---

### ПОТОК 3: Email обработка (Email Flow) — **ОБНОВЛЁННЫЙ**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  IMAP CHECK │────→│  PARSE NEW  │────→│  TRANSLATE  │────→│   SEND TG   │
│  (10 min)   │     │  "merged" PR│     │   to RU     │     │  with buttons│
└─────────────┘     └──────┬──────┘     └─────────────┘     └──────┬──────┘
                           │                                         │
                           │         ┌─────────────┐                  │
                           └────────→│  UPDATE DB  │←─────────────────┘
                                     │  status     │
                                     └─────────────┘
```

**Логика кнопок в Telegram:**

```
┌─────────────────────────────────────────────────────────────┐
│  🎉 PR #123 успешно merged!                                │
│  Репозиторий: owner/repo                                   │
│  Сумма: $150                                               │
│                                                            │
│  Перевод письма:                                           │
│  "Ваш pull request #123 был успешно объединён..."          │
│                                                            │
│  [🔍 Анализировать]  [🗑 Удалить]                          │
│  [🚀 Статус] [⏸ Пауза] [⚙ Настройки]                      │
└─────────────────────────────────────────────────────────────┘
```

**Действия кнопок:**

| Кнопка | Действие |
|--------|----------|
| `🔍 Анализировать` | • Отправить код PR в AI<br>• Запросить анализ: "Что можно улучшить?"<br>• Предложить новые критерии<br>• Сохранить insights в БД |
| `🗑 Удалить` | • Архивировать запись<br>• Очистить логи<br>• Пометить как "обработано" |
| `🚀 Статус` | • Показать текущую очередь<br>• Rate limits<br>• Активные задачи |
| `⏸/▶` | • Переключить паузу<br>• Остановить/возобновить обработку |
| `⚙ Настройки` | • Модель (GPT-4/Claude)<br>• Таймаут Docker<br>• CPU ступени |

---

## 3. ЛОГИКА СОСТОЯНИЙ (State Logic)

### State Machine: Переходы и условия

```
┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
│  IDLE   │────────→│ FETCHING│────────→│ANALYZING│────────→│ CODING  │
│         │  start  │         │  success│         │  success│         │
└─────────┘         └────┬────┘         └────┬────┘         └────┬────┘
                           │                   │                   │
                      error│              error│              error│
                           ▼                   ▼                   ▼
                    ┌─────────┐         ┌─────────┐         ┌─────────┐
                    │  RETRY  │         │  RETRY  │         │  RETRY  │
                    │ counter+│         │ counter+│         │ counter+│
                    └────┬────┘         └────┬────┘         └────┬────┘
                         │                     │                     │
                    max 3?│                max 3?│                max 3?
                         │Yes                  │Yes                 │Yes
                         ▼                     ▼                     ▼
                    ┌─────────┐           ┌─────────┐           ┌─────────┐
                    │ BLACKLIST│          │ BLACKLIST│          │ BLACKLIST│
                    │ permanent│          │ permanent│          │ permanent│
                    └─────────┘           └─────────┘           └─────────┘

┌─────────┐         ┌─────────┐         ┌─────────┐
│ CODING  │────────→│ TESTING │────────→│CREATE_PR│
│         │  success│         │  success│         │
└─────────┘         └────┬────┘         └────┬────┘
                    error│                   error│
                         ▼                     ▼
                    ┌─────────┐           ┌─────────┐
                    │  RETRY  │           │  RETRY  │
                    │return to│           │return to│
                    │  CODING │           │  CODING │
                    │with error│          │with error│
                    │ context │           │ context │
                    └─────────┘           └─────────┘

┌─────────┐         ┌─────────┐
│CREATE_PR│────────→│COMPLETED│
│         │  success│         │
└─────────┘         └─────────┘
```

### Условия переходов:

| From | To | Condition | Action on fail |
|------|-----|-----------|----------------|
| IDLE | FETCHING | Queue not empty, Docker ready, Rate limits OK | Wait 5s, retry |
| FETCHING | ANALYZING | All files <100MB downloaded, Linked issues fetched | Blacklist (file too large) |
| ANALYZING | CODING | AI returned valid solution plan | Retry (3x) → Blacklist |
| CODING | TESTING | Security scan passed, Code generated | Blacklist (security) |
| TESTING | CREATE_PR | Docker exit code 0, within 25s | Retry (3x) → Blacklist |
| CREATE_PR | COMPLETED | PR created successfully, comment posted | Retry (3x) → Blacklist |

---

## 4. ЛОГИКА БЕЗОПАСНОСТИ (Security Logic)

### Security Scan: Уровни угроз

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY SCAN LAYERS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LAYER 1: PATTERN MATCHING (regex)                          │
│  ├─ CRITICAL: rm -rf /, System.exit(), Runtime.exec()       │
│  ├─ CRITICAL: os.system(), subprocess(shell=True)            │
│  ├─ CRITICAL: eval(), exec(), __import__()                   │
│  ├─ WARNING:  socket, urllib, http requests                  │
│  └─ WARNING:  absolute path access (/etc, C:\\Windows)        │
│                                                             │
│  LAYER 2: AST ANALYSIS (abstract syntax tree)                │
│  ├─ Проверка импортов на неожиданные модули                 │
│  ├─ Проверка вызовов функций высокого риска                 │
│  └─ Проверка доступа к файловой системе                     │
│                                                             │
│  LAYER 3: DOCKER ISOLATION                                  │
│  ├─ Network: none (полная изоляция)                       │
│  ├─ Filesystem: read-only volumes                           │
│  ├─ Resources: CPU/RAM limits                               │
│  ├─ No privilege escalation                                   │
│  └─ Auto-kill after 25s timeout                             │
│                                                             │
│  LAYER 4: BLACKLIST ENFORCEMENT                              │
│  ├─ Permanent ban for security violations                   │
│  ├─ Permanent ban for 3 failed attempts                     │
│  └─ Permanent ban for files >100MB                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Реакция на угрозы:

| Уровень | Обнаружение | Реакция | Blacklist |
|---------|-------------|---------|-----------|
| CRITICAL | Запрещённый паттерн в коде | Немедленная остановка, уведомление TG | **PERMANENT** |
| WARNING | Подозрительный импорт | Логирование, продолжение с повышенным мониторингом | Нет |
| DOCKER FAIL | Выход за пределы контейнера | Убийство контейнера, анализ логов | По результатам |
| TIMEOUT | >25s выполнения | Прерывание, retry с оптимизацией | После 3 попыток |

---

## 5. ЛОГИКА РЕСУРСОВ (Resource Logic)

### Docker Resource Calculation: Фиксированные ступени

```
┌─────────────────────────────────────────────────────────────┐
│              CPU ALLOCATION (фиксированные ступени)          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Размер кода (строк)    │  CPU   │  Пример проекта          │
│  ───────────────────────┼────────┼───────────────────────── │
│  < 1,000                │   2    │  Простой скрипт          │
│  1,000 - 5,000          │   4    │  Средний модуль          │
│  > 5,000                │   6    │  Большой сервис          │
│                                                             │
│  RAM = 512MB + (file_size_kb / 10)                         │
│  Пример: файл 1024KB → 512 + 102.4 = ~614MB                │
│                                                             │
│  HARD LIMITS:                                               │
│  • CPU: max 6 (не более 6 физических ядер)                │
│  • RAM: max 4096MB (4GB)                                   │
│  • Swap: disabled (memswap = memory)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Rate Limit Management:

```
┌─────────────────────────────────────────────────────────────┐
│                    RATE LIMIT STATES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GITHUB API:                                                │
│  ├─ GREEN (>1000): Нормальная работа                        │
│  ├─ YELLOW (100-1000): Предупреждение в логах               │
│  ├─ ORANGE (10-100): Уведомление TG, пауза 60s              │
│  └─ RED (<10): Критическая пауза, ожидание reset            │
│                                                             │
│  OPENAI API:                                                │
│  ├─ GREEN: Нормальная работа                                │
│  ├─ YELLOW: Переключение на Claude (если доступен)          │
│  └─ RED: STOP PROGRAM, уведомление TG                       │
│                                                             │
│  DOCKER:                                                    │
│  ├─ GREEN: Контейнер запущен, ресурсы доступны              │
│  ├─ YELLOW: Высокая нагрузка CPU/RAM                        │
│  └─ RED: Невозможно запустить контейнер → остановка         │
│                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. ЛОГИКА ВОССТАНОВЛЕНИЯ (Recovery Logic)

### Checkpoint System:

```
┌─────────────────────────────────────────────────────────────┐
│                    CHECKPOINT STRATEGY                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  СОХРАНЯЕМ в SQLite после каждого успешного шага:           │
│  • FETCHING → files_downloaded, linked_issues               │
│  • ANALYZING → solution_plan, context                       │
│  • CODING → generated_code, commit_message                  │
│  • TESTING → test_results, docker_logs                      │
│  • CREATE_PR → pr_number, branch_name, commit_sha           │
│                                                             │
│  ПРИ СБОЕ (crash/restart):                                   │
│  1. Загрузить все issue со status ≠ completed/failed         │
│  2. Для каждого: определить последний successful checkpoint  │
│  3. Восстановить state machine с этого шага                  │
│  4. Продолжить обработку                                     │
│                                                             │
│  ПРИ ОШИБКЕ (error in step):                                 │
│  1. Сохранить error_details в attempts таблицу               │
│  2. Increment attempt_counter                                │
│  3. If attempt < 3 → return to CODING with error context    │
│  4. If attempt >= 3 → BLACKLIST permanent                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. ИНТЕГРАЦИОННАЯ СХЕМА (Integration Map)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES MAP                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   GITHUB.COM                    OPENAI API                    DOCKER DESKTOP │
│   ───────────                   ───────────                   ────────────── │
│   • REST API v3                 • GPT-4 (primary)               • Local daemon│
│   • GraphQL API v4              • Claude-3 (manual fallback)    • Windows exe│
│   • Dual tokens (read/write)    • Token counting                • Images:     │
│   • Webhooks (optional)         • Rate limit tracking             python:3.11 │
│                                   • Cost tracking                 openjdk:17 │
│                                                                             │
│   TELEGRAM API                  GMAIL IMAP                    LOCAL SYSTEM   │
│   ───────────                   ───────────                   ────────────── │
│   • Bot API (aiogram 3)         • imap.gmail.com:993          • SQLite DB   │
│   • Inline keyboards            • App Password                • File system │
│   • Callback queries            • 10-min polling              • Logs (JSON) │
│   • Chat notifications          • HTML/Plain text parsing                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. ЖИЗНЕННЫЙ ЦИКЛ ЗАДАЧИ (Issue Lifecycle)

```
CREATED (вручную или сканером)
    │
    ▼
┌─────────┐
│ PENDING │◄────────────────────────────────────────┐
│         │                                         │
└────┬────┘                                         │
     │                                               │
     │ queue.get()                                   │
     ▼                                               │
┌─────────┐     ┌─────────┐     ┌─────────┐         │
│FETCHING │────→│ANALYZING│────→│ CODING  │         │
│         │     │         │     │         │         │
└────┬────┘     └────┬────┘     └────┬────┘         │
     │               │               │              │
     │error          │error          │error         │
     │               │               │              │
     ▼               ▼               ▼              │
┌─────────┐     ┌─────────┐     ┌─────────┐         │
│ BLACKLIST│    │ RETRY   │     │ RETRY   │         │
│ permanent│    │ (1/3)   │     │ (2/3)   │         │
└─────────┘     └────┬────┘     └────┬────┘         │
                     │               │               │
                     └───────────────┘               │
                                     │               │
                                     ▼               │
                              ┌─────────┐            │
                              │ RETRY   │────────────┘
                              │ (3/3)   │   return to CODING
                              └────┬────┘   with error context
                                   │
                              error│
                                   ▼
                            ┌─────────┐
                            │ BLACKLIST│
                            │ permanent│
                            └─────────┘

SUCCESS PATH:
CODING ──→ TESTING ──→ CREATE_PR ──→ COMPLETED
            │            │
            │            ▼
            │       ┌─────────┐
            │       │  NOTIFY │
            │       │  TG: PR │
            │       │  created│
            │       └────┬────┘
            │            │
            ▼            ▼
       ┌─────────┐   ┌─────────┐
       │  EMAIL  │   │  EMAIL  │
       │  wait   │◄──│  merged │
       │  10 min │   │  check  │
       └────┬────┘   └────┬────┘
            │            │
            ▼            ▼
       ┌─────────┐   ┌─────────┐
       │  NOTIFY │   │  NOTIFY │
       │  TG:    │   │  TG:    │
       │ success │   │ merged  │
       │ $ earned│   │ +buttons│
       └─────────┘   └─────────┘

Это полная глубокая архитектура без кода. Все компоненты, потоки данных, состояния и логика взаимодействия описаны для реализации.
