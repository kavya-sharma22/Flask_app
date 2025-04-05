
# 🧑‍💻 Backend Developer Task Assignment

## 🌟 Objective

To architect, build, and maintain a high-performance backend using Flask that ensures data integrity, performance, security, and scalability.

## 🔏️ Task 1 – Project Setup

- Initialized a new Flask project using a modular architecture with **Blueprints**, **Services**, and **Repositories** to promote clean code and scalability.
- Configured **Docker** for containerized deployment and ensured support for multiple environments: development, staging, and production.







### ✅ Output

- Initialized a new Flask project using a modular architecture
- <img src="./Images/3.png" alt="Home Page" width="600"/>

- Flask project runs in a Docker container on `localhost:5000`

- <img src="./Images/1.png" alt="Home Page" width="600"/>

- Isolated environments via `.env.dev`
- Docker Compose manages app, database, Redis, Celery, and beat services
- Sample container setup output:

```bash
Creating flask_app ... done
Creating flask_postgres ... done
Creating flask_redis ... done
Creating flask_worker ... done
Creating flask_beat_scheduler ... done
```

Preview URL: `http://localhost:5000`




---

## 🔠️ Task 2 – Secure Database Connection

- Connected to **PostgreSQL** using **SQLAlchemy** with connection pooling for efficient resource usage.
- Added **retry mechanism** for failed DB connections during app startup.
- Managed all sensitive credentials using **environment variables** via `.env.dev`.
- Used **Alembic** for safe and consistent database migrations.

### ✅ Output

- `.env.dev` includes:
- - <img src="./Images/4.png" alt="Home Page" width="600"/>
  ```env
  DATABASE_URL=postgresql://postgres:kavy%40@localhost:5432/tasklist_db
  ```
- Sample Alembic migration:
  ```bash
  INFO  [alembic.runtime.migration] Running upgrade -> 123abc456, create taskmanager table
  ```
- Successfully connected to DB:
- - <img src="./Images/5.png" alt="Home Page" width="600"/>
  ```bash
  DB connection established successfully.

   
  ```
- Verified with `docker exec -it flask_postgres psql -U postgres` and listed tables in DB.

---

## 📊 Task 3 – Complex Model Definitions

- Defined three **SQLAlchemy models**: `TaskManager`, `TaskLogger`, and `User`.
- Implemented **Role-Based Access Control (RBAC)**: only users with proper roles can modify or delete tasks.
- Ensured **lazy loading**, **indexes** for optimized performance.
- Applied **cascading delete** rules for task removal.
- Created an **audit log** mechanism for tracking changes in task statuses.

### ✅ Output

- Models defined in `app/models/`:
  ```python
  class TaskManager(Base):
      __tablename__ = "task_manager"
      id = Column(Integer, primary_key=True)
      title = Column(String)
      status = Column(String)
      created_at = Column(DateTime, default=datetime.utcnow)
  ```
- Relationships implemented using `back_populates` and `lazy='dynamic'`
- Admins can view audit trail like:
  ```json
  {
    "task_id": 3,
    "previous_status": "in_progress",
    "new_status": "completed",
    "modified_by": "admin",
    "timestamp": "2025-04-05T17:32:00"
  }
  ```
- Deleting a task from `TaskManager` cascades and removes from `TaskLogger`
- User roles enforced:
  ```python
  if current_user.role != 'admin':
      raise Unauthorized("You are not allowed to modify tasks")
  ```

---

## 🌐 Task 4 – Scalable Daily Task Loader

- Implemented a distributed **Celery** task that runs daily to transfer only active tasks from `TaskManager` to `TaskLogger`
- Ensured the loader avoids duplicates by checking if an entry already exists for the same day.
- Used **Redis** as the message broker to support asynchronous and scalable task execution.

### ✅ Output

- Celery Beat logs:
- - <img src="./Images/2.png" alt="Home Page" width="600"/>
  ```bash
  [2025-04-05 19:05:29,743: INFO/MainProcess] beat: Starting...
  ```
- Celery Worker logs:
  ```bash
  [INFO] Running periodic task: sync_active_tasks_daily()
  Transferred 4 active tasks from TaskManager to TaskLogger
  ```
- Inside database, `TaskLogger` table shows updated entries:
  ```json
  {
    "id": 10,
    "title": "Fix bug #24",
    "transferred_on": "2025-04-05",
    "status": "active"
  }
  ```
- Redis queues being used confirm distributed message handling.

---

## 📂 Task 5 – API Development with Security & Performance

- Developed secure and optimized API endpoints:
  - `POST /upload-csv` → Upload and parse CSV into `TaskManager`
  - `GET /tasks` → Paginated list of all tasks from `TaskLogger`
  - `GET /tasks?date=<specific_date>` → Filtered by date with Redis caching
  - `GET /task/<task_logger_id>` → Get task details efficiently
  - `POST /task` → Create task, JWT protected
  - `PUT /task/<task_id>` → Update task, RBAC enforced
  - `DELETE /task/<task_id>` → Soft delete a task
- Implemented **rate limiting**, **input validation using Pydantic**, and **authentication using JWT**

### ✅ Output

- `POST /task` with valid JWT:
  ```json
  {
    "id": 12,
    "title": "Test task",
    "status": "active",
    "created_by": "admin"
  }
  ```
- `GET /tasks?date=2025-04-05`:
  ```json
  [
    {
      "id": 9,
      "title": "Deploy API",
      "status": "completed",
      "date": "2025-04-05"
    }
  ]
  ```
- `DELETE /task/5`:
  ```json
  {
    "message": "Task soft deleted successfully"
  }
  ```
- Validation error:
  ```json
  {
    "error": "Field 'title' is required"
  }
  ```
- Rate limit exceeded:
  ```json
  {
    "error": "Too many requests, please try again later."
  }
  ```
- Redis caching hit for date-based tasks retrieval confirmed in logs

---

## 🔍 Task 6 – Comprehensive Documentation & Testing

- Wrote detailed **docstrings** for all functions and services for better maintainability.
- Generated an **API reference guide** explaining usage of every endpoint.
- Conducted **unit and integration tests** using `pytest`.
- Verified token-protected routes, role access, data validation, and task scheduler behavior.

### ✅ Output

- Markdown API docs generated and accessible via `/docs`
- Sample docstring:
  ```python
  def create_task(data: TaskSchema) -> TaskManager:
      """
      Creates a new task in TaskManager table.
      Args:
          data (TaskSchema): Input task data
      Returns:
          TaskManager: Created task object
      """
  ```
- Sample test result:
  ```bash
  ================= test session starts =================
  collected 18 items
  test_task.py ..................                 [100%]
  ================== 18 passed in 2.67s ==================
  ```
- GitHub repo contains full documentation, setup instructions, and API usage examples.

---

The project is **well-structured**, **properly tested**, and **optimized**. Code is documented and adheres to **industry best practices**.

---

## 📖 Conclusion

This backend system for a Task Management app successfully incorporates modern best practices including secure authentication, scalable task scheduling, optimized APIs, and robust testing. It is containerized for portability and built with a modular design to support future scalability.

## 📄 Resources & References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Celery Docs](https://docs.celeryq.dev/)
- [Docker Docs](https://docs.docker.com/)
- [Redis Docs](https://redis.io/docs/)
- [Pytest Docs](https://docs.pytest.org/)

