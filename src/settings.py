import os
from dotenv import load_dotenv


if __name__ == '__main__':
    project_folder = os.path.join(os.path.dirname(__file__), '../')
    load_dotenv(os.path.join(project_folder, '.env'))
