# Tmsa7/core/helper.py

class help:
    def __init__(self):
        """Automatically print a description of the help class when an instance is created."""
        print("The 'help' class provides access to various fields of Python libraries.")
        print("You can explore libraries for fields like AI, Computer Vision, NLP, Web Development, Data Processing, Embedded Systems, Operating Systems, Math, Robotics, Networking, Database, and Security.")
        print("Use the 'python()' method to list all available fields and how to access them.")
        print("For example, use 'help.ai()' to list AI-related libraries.")

    @staticmethod
    def python():
        """List the available fields and how to access them."""
        fields = {
            'ai': 'Use help.ai() to list AI-related libraries.',
            'computer_vision': 'Use help.computer_vision() to list Computer Vision libraries.',
            'nlp': 'Use help.nlp() to list NLP-related libraries.',
            'web': 'Use help.web() to list Web Development libraries.',
            'data': 'Use help.data() to list Data Processing and Analysis libraries.',
            'embedded': 'Use help.embedded() to list Embedded Systems libraries.',
            'os': 'Use help.os() to list Operating System-related libraries.',
            'math': 'Use help.math() to list Mathematical and Scientific Computing libraries.',
            'robotics': 'Use help.robotics() to list Robotics libraries.',
            'networking': 'Use help.networking() to list Networking libraries.',
            'database': 'Use help.database() to list Database libraries.',
            'security': 'Use help.security() to list Security libraries.',
        }
        for field, usage in fields.items():
            print(f'{field}: {usage}')

    @staticmethod
    def ai():
        """List AI-related libraries."""
        packages = {
            'tensorflow': 'Used for deep learning and building neural networks. (pip install tensorflow)',
            'pytorch': 'A deep learning framework that provides flexibility with dynamic computation graphs. (pip install torch)',
            'keras': 'A high-level neural networks API, running on top of TensorFlow. (pip install keras)',
            'scikit-learn': 'Used for machine learning, including classification, regression, and clustering. (pip install scikit-learn)',
            'mxnet': 'A deep learning framework designed for both efficiency and flexibility. (pip install mxnet)',
            'xgboost': 'Optimized gradient boosting library designed for speed and performance. (pip install xgboost)',
            'lightgbm': 'A fast, distributed, high-performance gradient boosting framework. (pip install lightgbm)',
            'catboost': 'A gradient boosting library designed to handle categorical features. (pip install catboost)',
            'cntk': 'Microsoft’s Cognitive Toolkit for deep learning. (pip install cntk)',
            'dlib': 'A toolkit for making real-world machine learning and computer vision applications. (pip install dlib)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def computer_vision():
        """List Computer Vision libraries."""
        packages = {
            'opencv': 'Used for computer vision tasks such as image processing, video capture, and object detection. (pip install opencv-python)',
            'tensorflow': 'Used for deep learning and building neural networks, including computer vision tasks. (pip install tensorflow)',
            'torchvision': 'Provides datasets, model architectures, and image transformations for computer vision tasks. (pip install torchvision)',
            'mediapipe': 'A cross-platform library for building custom computer vision and machine learning solutions. (pip install mediapipe)',
            'dlib': 'A toolkit for building machine learning applications, with a strong focus on facial recognition. (pip install dlib)',
            'detectron2': 'A PyTorch-based library for object detection and segmentation. (pip install detectron2)',
            'imageai': 'Enables the use of AI in computer vision tasks such as object detection and video analysis. (pip install imageai)',
            'albumentations': 'A fast image augmentation library designed for deep learning. (pip install albumentations)',
            'simplecv': 'An open-source framework for building computer vision applications. (pip install simplecv)',
            'mmcv': 'OpenMMLab computer vision library with useful tools for training models. (pip install mmcv)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def nlp():
        """List NLP (Natural Language Processing) libraries."""
        packages = {
            'nltk': 'Natural Language Toolkit, used for working with human language data. (pip install nltk)',
            'spacy': 'Used for advanced NLP tasks, such as named entity recognition and part-of-speech tagging. (pip install spacy)',
            'transformers': 'Transformers library by HuggingFace for NLP tasks. (pip install transformers)',
            'gensim': 'Used for topic modeling and document similarity analysis in NLP. (pip install gensim)',
            'flair': 'A simple framework for state-of-the-art NLP. (pip install flair)',
            'fasttext': 'Library for efficient learning of word representations and text classification. (pip install fasttext)',
            'stanfordnlp': 'Stanford NLP suite for text analysis. (pip install stanfordnlp)',
            'polyglot': 'A multilingual NLP pipeline with tokenization, language detection, and more. (pip install polyglot)',
            'pytorch-nlp': 'Natural language processing toolkit built on top of PyTorch. (pip install pytorch-nlp)',
            'textblob': 'Simplified text processing library for common NLP tasks. (pip install textblob)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def web():
        """List web development libraries."""
        packages = {
            'django': 'A high-level web framework for building complex web applications. (pip install django)',
            'flask': 'A lightweight web framework for building web applications and APIs. (pip install flask)',
            'fastapi': 'A modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. (pip install fastapi)',
            'requests': 'Used for making HTTP requests to interact with web services and APIs. (pip install requests)',
            'bottle': 'A fast, simple, and lightweight WSGI micro web framework. (pip install bottle)',
            'tornado': 'A scalable web server and web application framework. (pip install tornado)',
            'pyramid': 'A lightweight and flexible Python web framework. (pip install pyramid)',
            'aiohttp': 'Asynchronous HTTP client/server framework for asyncio and Python. (pip install aiohttp)',
            'dash': 'A framework for building web applications with Python, especially focused on data visualization. (pip install dash)',
            'sanic': 'A Python web framework that’s built to go fast. (pip install sanic)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def data():
        """List data processing and analysis libraries."""
        packages = {
            'pandas': 'Used for data manipulation and analysis, particularly for working with tabular data. (pip install pandas)',
            'numpy': 'Used for numerical computations, particularly with arrays and matrices. (pip install numpy)',
            'matplotlib': 'Used for data visualization and plotting graphs. (pip install matplotlib)',
            'seaborn': 'A Python data visualization library based on matplotlib. (pip install seaborn)',
            'plotly': 'Used for creating interactive graphs and visualizations. (pip install plotly)',
            'dask': 'Parallel computing and processing large datasets. (pip install dask)',
            'pyarrow': 'Handles large datasets and facilitates data interchange between different tools. (pip install pyarrow)',
            'polars': 'A fast DataFrame library for data manipulation. (pip install polars)',
            'h5py': 'A Python interface to the HDF5 binary data format. (pip install h5py)',
            'vaex': 'Out-of-core DataFrames for processing large datasets that don’t fit in memory. (pip install vaex)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def embedded():
        """List libraries for embedded systems development."""
        packages = {
            'micropython': 'A lean and efficient implementation of Python for microcontrollers. (pip install micropython)',
            'circuitpython': 'A fork of MicroPython designed to simplify experimentation on low-cost microcontrollers. (pip install adafruit-circuitpython)',
            'RPi.GPIO': 'A module to control the Raspberry Pi GPIO channels. (pip install RPi.GPIO)',
            'pyserial': 'A module encapsulating access to serial ports for embedded systems. (pip install pyserial)',
            'mraa': 'A C/C++ library with bindings to Python for low-level sensor and I/O control. (pip install mraa)',
            'upm': 'High-level sensor and actuator library for IoT devices. (pip install upm)',
            'pyb': 'Python module for MicroPython on the pyboard. (pip install pyb)',
            'picamera': 'A pure Python interface to the Raspberry Pi camera module. (pip install picamera)',
            'gpiozero': 'A simple interface to GPIO devices on the Raspberry Pi. (pip install gpiozero)',
            'microbit': 'Python library for programming the BBC micro:bit. (pip install microbit)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def os():
        """List libraries for interacting with the operating system."""
        packages = {
            'os': 'Provides a way of using operating system-dependent functionality. (Built-in)',
            'psutil': 'A cross-platform library for retrieving information on running processes and system utilization. (pip install psutil)',
            'subprocess': 'Allows for spawning new processes, connecting to input/output/error pipes, and obtaining return codes. (Built-in)',
            'pathlib': 'Offers classes for working with filesystem paths. (Built-in)',
            'shutil': 'Offers high-level operations on files and collections of files. (Built-in)',
            'click': 'A Python package for creating command-line interfaces. (pip install click)',
            'watchdog': 'A Python library that monitors the filesystem for changes. (pip install watchdog)',
            'pexpect': 'A Python module for spawning child applications and controlling them automatically. (pip install pexpect)',
            'pyautogui': 'Cross-platform GUI automation for automating keyboard and mouse actions. (pip install pyautogui)',
            'path': 'Object-oriented file system paths (pip install path)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def math():
        """List libraries for mathematical and scientific computing."""
        packages = {
            'math': 'Provides mathematical functions like trigonometry, logarithms, and more. (Built-in)',
            'sympy': 'A Python library for symbolic mathematics and algebraic manipulation. (pip install sympy)',
            'scipy': 'Used for scientific and technical computing. (pip install scipy)',
            'statistics': 'Provides functions for mathematical statistics. (Built-in)',
            'random': 'Used for generating random numbers and performing randomization. (Built-in)',
            'mpmath': 'A Python library for arbitrary-precision floating-point arithmetic. (pip install mpmath)',
            'numexpr': 'Used for fast numerical computation with NumPy arrays. (pip install numexpr)',
            'pymc3': 'A probabilistic programming library for Bayesian statistics. (pip install pymc3)',
            'cvxpy': 'A Python-embedded modeling language for convex optimization problems. (pip install cvxpy)',
            'networkx': 'Used for the creation, manipulation, and study of the structure of complex networks. (pip install networkx)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def robotics():
        """List Robotics libraries."""
        packages = {
            'ros': 'Robot Operating System - a framework for writing robot software. (pip install rospkg)',
            'pyrobot': 'A Python library for working with robots. (pip install pyrobot)',
            'pybullet': 'A Python module for physics simulation, robotics, and machine learning. (pip install pybullet)',
            'urx': 'A Python library to control the Universal Robots arms. (pip install urx)',
            'robotframework': 'A generic test automation framework for robotic process automation. (pip install robotframework)',
            'robosuite': 'A framework for robot learning and simulation. (pip install robosuite)',
            'gym': 'OpenAI Gym - a toolkit for developing and comparing reinforcement learning algorithms. (pip install gym)',
            'moveit': 'A ROS-based library for mobile manipulation and motion planning. (pip install moveit)',
            'webots': 'A robot simulator for modern mobile robotics. (pip install webots)',
            'vpython': 'A Python library for 3D programming and simulations. (pip install vpython)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def networking():
        """List Networking libraries."""
        packages = {
            'socket': 'Low-level networking interface for socket programming. (Built-in)',
            'paramiko': 'Python implementation of SSHv2 for network connections. (pip install paramiko)',
            'scapy': 'A powerful packet manipulation tool for network traffic analysis. (pip install scapy)',
            'requests': 'Simplified HTTP requests for interacting with web services and APIs. (pip install requests)',
            'asyncio': 'A Python library to write concurrent code using async/await. (Built-in)',
            'twisted': 'An event-driven networking engine for building network applications. (pip install twisted)',
            'pyshark': 'A Python wrapper for TShark, for packet parsing. (pip install pyshark)',
            'ftplib': 'A built-in library for handling FTP connections. (Built-in)',
            'dnspython': 'A DNS toolkit for Python. (pip install dnspython)',
            'socketio': 'A networking library for WebSocket and socket.io support. (pip install python-socketio)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def database():
        """List Database libraries."""
        packages = {
            'sqlalchemy': 'A Python SQL toolkit and Object Relational Mapper (ORM). (pip install sqlalchemy)',
            'pymongo': 'A Python driver for MongoDB. (pip install pymongo)',
            'redis-py': 'The Python client for Redis, a powerful in-memory data structure store. (pip install redis)',
            'psycopg2': 'A PostgreSQL adapter for Python. (pip install psycopg2)',
            'sqlite3': 'A DB-API 2.0-compliant SQLite database interface. (Built-in)',
            'mysql-connector-python': 'A MySQL client library for Python. (pip install mysql-connector-python)',
            'peewee': 'A small, expressive ORM for Python. (pip install peewee)',
            'pony': 'An ORM that lets you write database queries using Python syntax. (pip install pony)',
            'dataset': 'A database abstraction layer for Python. (pip install dataset)',
            'elasticsearch-py': 'A Python client for Elasticsearch. (pip install elasticsearch)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')

    @staticmethod
    def security():
        """List Security libraries."""
        packages = {
            'cryptography': 'A package designed to expose cryptographic recipes and primitives. (pip install cryptography)',
            'paramiko': 'An implementation of SSHv2 protocol, providing both client and server functionality. (pip install paramiko)',
            'pyopenssl': 'A wrapper around a subset of the OpenSSL library. (pip install pyopenssl)',
            'hashlib': 'A built-in library providing secure hash algorithms like SHA256. (Built-in)',
            'nmap': 'A Python library for network exploration and security auditing. (pip install python-nmap)',
            'requests-ntlm': 'A library for HTTP NTLM authentication. (pip install requests-ntlm)',
            'passlib': 'A comprehensive password hashing library for Python. (pip install passlib)',
            'pycryptodome': 'A self-contained Python package of low-level cryptographic primitives. (pip install pycryptodome)',
            'pylibnacl': 'Python binding to the Networking and Cryptography library (NaCl). (pip install libnacl)',
            'jwt': 'A Python library for JSON Web Tokens (JWT). (pip install PyJWT)',
        }
        for package, description in packages.items():
            print(f'{package}: {description}')