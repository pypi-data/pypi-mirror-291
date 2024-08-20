class examples:

    def __init__(self):
        """Explain what the 'examples' class does."""
        print("The 'examples' class provides code examples for popular libraries in various fields.")
        print("Use methods like 'examples.ai()' or 'examples.web()' to get examples for specific fields.")
    
    @staticmethod
    def ai():
        print("Example of using TensorFlow:")
        print("""
import tensorflow as tf

# Build a simple model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

# Compile the model
model.compile(optimizer='adam', 
              loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=5)
        """)

    @staticmethod
    def computer_vision():
        print("Example of using OpenCV for image processing:")
        print("""
import cv2

# Read an image
image = cv2.imread('image.jpg')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the image
cv2.imshow('Gray Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    @staticmethod
    def nlp():
        print("Example of using SpaCy for Named Entity Recognition:")
        print("""
import spacy

# Load the pre-trained model
nlp = spacy.load("en_core_web_sm")

# Process some text
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# Print named entities
for entity in doc.ents:
    print(entity.text, entity.label_)
        """)

    @staticmethod
    def web():
        print("Example of using Flask to create a simple web app:")
        print("""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
        """)

    @staticmethod
    def data():
        print("Example of using Pandas for data manipulation:")
        print("""
import pandas as pd

# Create a DataFrame
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 24, 35, 32]}
df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# Perform basic operations
print(df['Age'].mean())  # Average age
        """)

    @staticmethod
    def embedded():
        print("Example of controlling a GPIO pin on a Raspberry Pi using RPi.GPIO:")
        print("""
import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Blink an LED connected to the pin
for i in range(10):
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(18, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
        """)

    @staticmethod
    def os():
        print("Example of using the `os` module to list files in a directory:")
        print("""
import os

# List all files in the current directory
files = os.listdir('.')
for file in files:
    print(file)
        """)

    @staticmethod
    def math():
        print("Example of using SymPy for symbolic mathematics:")
        print("""
from sympy import symbols, diff

# Define a symbol
x = symbols('x')

# Differentiate an expression
expr = x**2 + 3*x + 2
derivative = diff(expr, x)

# Print the derivative
print(derivative)
        """)

    @staticmethod
    def robotics():
        print("Example of using PyBullet for robotics simulation:")
        print("""
import pybullet as p
import time

# Connect to physics server
p.connect(p.GUI)

# Load a plane and a robot
plane = p.loadURDF("plane.urdf")
robot = p.loadURDF("r2d2.urdf")

# Run simulation
for i in range(10000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
        """)

    @staticmethod
    def networking():
        print("Example of using the `socket` module for a simple TCP client:")
        print("""
import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a server
client_socket.connect(('localhost', 8080))

# Send data
client_socket.sendall(b'Hello, server')

# Receive data
response = client_socket.recv(1024)
print('Received', repr(response))

# Close the connection
client_socket.close()
        """)

    @staticmethod
    def database():
        print("Example of using SQLAlchemy to interact with a database:")
        print("""
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database engine
engine = create_engine('sqlite:///:memory:')
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))

# Create the table
Base.metadata.create_all(engine)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Create a new user
new_user = User(name='John Doe')
session.add(new_user)
session.commit()

# Query the database
for user in session.query(User).all():
    print(user.name)
        """)

    @staticmethod
    def security():
        print("Example of using the `cryptography` library for encryption:")
        print("""
from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt some data
cipher_text = cipher_suite.encrypt(b"Secret message")
print("Encrypted:", cipher_text)

# Decrypt the data
plain_text = cipher_suite.decrypt(cipher_text)
print("Decrypted:", plain_text.decode())
        """)
