import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper function to get environment variables with a default value
def get_env_variable(var_name, default=None):
    value = os.getenv(var_name)
    if value is None and default is None:
        raise ValueError(f"Missing required environment variable: {var_name}")
    return value if value is not None else default

# Load environment variables
PORT = get_env_variable('PORT')
DB_HOST = get_env_variable('DB_HOST')
DB_USER = get_env_variable('DB_USER')
DB_PASSWORD = get_env_variable('DB_PASSWORD')
DB_NAME = get_env_variable('DB_NAME')
DB_PORT = get_env_variable('DB_PORT')

SECRET_KEY = get_env_variable('SECRET_KEY')
ALGORITHM = get_env_variable('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_variable('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

# Optional: Print loaded configurations for debugging purposes
#print(f"Loaded configurations: PORT={PORT}, DB_HOST={DB_HOST}, ...")
