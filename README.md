# Virtual Clerk ⚖️

Virtual Clerk is a legal-tech platform that automatically monitors court cases and alerts lawyers about **hearing dates, bench changes, and case updates**.

The goal is to build a scalable **court intelligence platform** capable of serving thousands of lawyers while performing safe, controlled scraping of court systems.

---

# Product Vision

Virtual Clerk continuously monitors court systems and provides:

- Hearing date alerts
- Cause list updates
- Bench and judge tracking
- Case monitoring for advocates
- Email / WhatsApp alerts
- Lawyer dashboard

Instead of each lawyer manually checking court portals, Virtual Clerk does it automatically.

---

# Core Principle

Scrape once → serve thousands of users.

Bad architecture:

10,000 lawyers → 10,000 scrapes → court blocks IP.

Correct architecture:

Central scraper → database → API → lawyers.

---

# System Architecture

Users (Lawyers)
        ↓
Frontend Dashboard
        ↓
API Server (FastAPI)
        ↓
PostgreSQL Database
        ↓
Redis Task Queue
        ↓
Scraper Workers (rate limited)
        ↓
Court Websites

---

# Repository Structure

virtual-clerk/

backend/
- FastAPI application
- API endpoints
- authentication
- lawyer dashboard APIs

scraper/
- court scraping modules
- Bombay HC
- other courts later

workers/
- background workers
- scraping tasks
- scheduled jobs

alerts/
- hearing change detection
- alert generation

database/
- database schema
- migrations

frontend/
- lawyer dashboard
- signup page
- alerts page

---

# Data Model

Lawyers

id  
name  
email  

Advocates

id  
name  

Cases

case_no  
advocate_name  
bench  
next_hearing  

Alerts

case_no  
old_hearing_date  
new_hearing_date  
created_at  

---

# Scraping Strategy

Scraping is centralized and rate-limited.

Example schedule:

8:00 AM scrape  
9:00 AM scrape  
10:00 AM scrape  

Each advocate is scraped at safe intervals.

Workers enforce delays:

3–7 seconds between requests.

This prevents court websites from blocking the system.

---

# Worker System

Scraping jobs are queued using Redis.

Example task:

scrape_advocate("DUSHYANT KUMAR")

Workers process tasks sequentially.

Advantages

- prevents request spikes
- avoids blocking
- allows horizontal scaling

---

# Alert Engine

When a hearing date changes:

Old: 4 March  
New: 12 April  

An alert is generated.

Example notification:

⚠ Hearing Date Changed

Case: WP/4805/2021  
Old Hearing: 4 March  
New Hearing: 12 April

Alerts are delivered through:

- Email
- WhatsApp
- Dashboard notifications

---

# Infrastructure (10k Lawyers)

Minimal infrastructure to support thousands of users.

API Server  
2GB VPS

Workers  
2GB VPS

Database  
PostgreSQL

Queue  
Redis

Monthly cost estimate:

$40 – $70

---

# Safety Controls

To prevent court blocking:

Random request delays  
User-agent rotation  
Retry logic  
Captcha detection  
Aggressive caching  

Maximum request rate:

~10 requests per minute

---

# Roadmap

Phase 1

Bombay High Court monitoring

Phase 2

Delhi High Court  
Karnataka High Court

Phase 3

Supreme Court

Phase 4

Legal analytics platform

- judge behavior analysis
- adjournment patterns
- case prediction models

---

# Why This Matters

Court data is extremely valuable.

Over time Virtual Clerk builds a structured dataset of:

- litigation timelines
- judge behavior
- case outcomes
- hearing patterns

This enables future products such as:

AI litigation prediction  
law firm intelligence tools  
legal research datasets  

---

# Running the Project

Start API server

uvicorn backend.app:app --reload

Start scraper worker

python3 workers/scraper_worker.py

Open API docs

http://127.0.0.1:8000/docs

---

# Vision

Virtual Clerk aims to become the operating system for litigation lawyers by turning fragmented court information into a reliable, real-time intelligence platform.

