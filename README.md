# CyberSec_Web_Scrapper


Creating a Cyber Security Web Scrapper using a Raspberry Pi board. Raspberry Pi is acting as an server that is accessible via DDNS.

The Pi is running a script for scrapping information from reddit and other cyber security news website. It saves the results to OpenSearch and publishes everything to Grafana.

**Arhitecture**:
┌─────────────┐      ┌────────────┐       ┌──────────────┐
│ RSS Fetcher │ ──▶  │ Summarizer │ ────▶ │ Grafana Dash│
└─────────────┘      └────────────┘       └──────────────┘
       ▲                     │
       │                     ▼
[Feed List+ Reddit feeds]    HuggingFace(t5-small)

**Tech stack**
- Python: - packages: transformers, praw, feedparser, yaml, os, opensearchpy
- Docker: elasticSeach and Grafana services
- CronTab - job scheduler for automatic scrapping
- JSON - for Dashboard

**Results**

![image](https://github.com/user-attachments/assets/09cd184e-2eb1-43a7-a03d-6ffe6b6cc49e)
