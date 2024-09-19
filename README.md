Create Alembic Configuration
:~ alembic init alembic

Create a Migration Script
:~ alembic revision --autogenerate -m "Initial migration"

Apply the Migration
:~ alembic upgrade head

