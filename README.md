# Memory Usage Monitoring

### Run Service

for running service there two option that depends on your requirements

first of all there is environment file, in .env file we got `LOCAL_EXECUTOR` which is `false` mainly.

`LOCAL_EXECUTOR` while changing to `true` that means service working with threading.timer







### Service Folder Tree

```bash
.
├── Dockerfile
├── README.md
├── celerybeat-schedule
├── docker-compose.yaml
├── entrypoint.sh
├── main.py
├── requirements.txt
├── sample.env
├── src
│   ├── db
│   │   ├── __init__.py
│   │   └── database.py
│   ├── model
│   │   ├── __init__.py
│   │   ├── repository
│   │   │   └── mem_service.py
│   │   └── system_ram_usage.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── memory_routers.py
│   ├── scheduler
│   │   ├── config.py
│   │   └── tasks.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── ram_schema.py
│   │   └── settings_schema.py
│   ├── settings
│   │   ├── __init__.py
│   │   └── middleware.py
│   ├── test
│   └── utils
│       ├── __init__.py
│       ├── decorators
│       │   ├── __init__.py
│       │   └── unit_convertor.py
│       └── get_ram_usage.py
└── storage
```

