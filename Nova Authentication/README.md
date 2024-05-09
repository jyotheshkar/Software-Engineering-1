# Face and Hand Authentication System

This project provides two Python modules for secure multifactor authentication: face recognition and hand recognition.

## Prerequisites

- Python 3.8+
- Pip package manager

## Installation

1. Clone the repository to your local system:
    ```bash
    git clone https://github.com/your-username/face-hand-auth.git
    ```
2. Navigate to the project directory:
    ```bash
    cd face-hand-auth
    ```
3. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Face Recognition Authentication

The `face_auth.py` file provides face recognition functionality. Here's how to use it:

1. Import the relevant functions and classes from `face_auth.py`.
2. Adjust any configuration values as needed.
3. Run the face authentication script:
    ```bash
    python face_auth.py
    ```
4. The script will use a webcam or specified video source to detect and authenticate the user's face.

### Hand Recognition Authentication

The `Auth.py` file includes the code for hand-based authentication. To use it:

1. Import the necessary classes and functions from `Auth.py`.
2. Adjust the configurations if needed.
3. Run the hand authentication script:
    ```bash
    python Auth.py
    ```
4. The script will use a camera or video source to authenticate the user through hand recognition.

### Test Script

The `test.py` file provides testing functionality for both face and hand authentication. To run the test:

1. Import or adjust the testing methods as needed.
2. Execute the test script to verify the authentication modules:
    ```bash
    python test.py
    ```

## Contributing

To contribute to this authentication system:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

