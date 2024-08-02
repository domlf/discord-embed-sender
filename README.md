# Discord Embed Sender v1.0.0

![Screenshot](/screenshot.png)

A PyQt5 application for sending Discord embeds via webhook.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or higher. You can download Python from [python.org](https://www.python.org/downloads/).
- You have a Discord account and a webhook URL from a Discord server. You can create a webhook by following [this guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

## Installation

Follow these steps to install and set up the project on Windows:

1. **Clone the repository**:
    - Open Command Prompt.
    - Navigate to the directory where you want to clone the repository.
    - Run the following command:
      ```sh
      git clone https://github.com/suzuya0-0/discord-embed-sender.git
      cd discord-embed-sender
      ```

2. **Set up a virtual environment** (recommended):
    - Run the following commands in Command Prompt:
      ```sh
      python -m venv venv
      venv\Scripts\activate
      ```

3. **Install the dependencies**:
    - Ensure your virtual environment is activated.
    - Run the following command to install the required Python packages:
      ```sh
      pip install -r requirements.txt
      ```

## Usage

To run the application:

1. **Start the application**:
    - In Command Prompt, ensure you are in the project directory and your virtual environment is activated.
    - Run the following command:
      ```sh
      python discord_embed_sender.py
      ```

2. **Fill in the details in the GUI**:
    - Enter your Discord webhook URL.
    - Enter the embed title, description, and other details as needed.
    - Use the "Pick Color" button to select a color for the embed.
    - Add fields as necessary by clicking "Add Field".
    - Click "Send Embed" to send the embed to your Discord server.






## Troubleshooting

Here are some common issues and solutions:

1. **PyQt5 Installation Issues**:
    - Ensure you are using a Python version supported by PyQt5 (3.6 or higher).
    - If you encounter issues during installation, try updating `pip`:
      ```sh
      python -m pip install --upgrade pip
      ```

2. **Virtual Environment Activation Issues**:
    - Ensure you use the correct path to activate the virtual environment. For example, if your project is in `C:\Users\YourName\discord-embed-sender`, run:
      ```sh
      C:\Users\YourName\discord-embed-sender\venv\Scripts\activate
      ```

3. **Failed to Send Embed**:
    - Ensure the webhook URL is correct and starts with `https://discord.com/api/webhooks/`.
    - Check your internet connection.
    - Verify that the Discord server and channel where the webhook is set up have the correct permissions.

4. **GUI Issues**:
    - If the application window does not appear or crashes, ensure all dependencies are installed correctly.
    - Ensure your system meets the requirements to run PyQt5 applications.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Python](https://www.python.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Requests](https://pypi.org/project/requests/)
- [Discord Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- 

