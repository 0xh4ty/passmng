# PassMNG

This is a simple password manager application implemented in Python using the Tkinter library. It allows you to securely store and retrieve passwords for different websites and usernames.

## Prerequisites

- Python 3.x
- Tkinter library
- SQLite database
- cryptography library

## Getting Started

1. Clone the repository or download the source code.

2. Install the required dependencies.

3. Navigate to the `passmng` folder.

4. Open the `main.py` file in a text editor.

5. Locate the following variables in the code:

  ```python
  key_file_path = "key.txt"
  master_password = "Passw0rd!"
  ```

5. Change the key_file_path variable to the desired path where you want to store the encryption key file. Make sure to provide the full file path.

6. Update the master_password value with your preferred master password. This is the password that will be used to access the password manager features.

7. Save the changes to the main.py file.

## Usage

1. Run the main.py file using the following command:

 ```shell
 python main.py
 ```

2. You will be prompted to enter the master password. Enter the previously set master_password value.

3. Once logged in, you can use the password manager features to store, retrieve, and generate passwords for different websites and usernames.

## Security Considerations

1. Make sure to choose a strong master password that is unique and not easily guessable.

2. Safeguard the encryption key file (key.txt) by storing it in a secure location.

3. Consider using additional security measures like two-factor authentication and secure password storage mechanisms.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
