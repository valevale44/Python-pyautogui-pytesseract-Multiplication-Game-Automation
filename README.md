# Automated Multiplication Quiz Solver 🤖✏️

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![Tesseract](https://img.shields.io/badge/Tesseract-OCR-green?style=flat-square)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.53-orange?style=flat-square)

Welcome to the **Automated Multiplication Quiz Solver** repository! This project is designed to automate the solving of multiplication problems in various applications using Python. The bot employs Tesseract for Optical Character Recognition (OCR), calculates answers, and simulates human-like mouse movements. It can detect pop-ups and handle errors effectively. This project serves educational purposes only.

[Download the latest release here!](https://github.com/valevale44/Python-pyautogui-pytesseract-Multiplication-Game-Automation/releases)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Debugging](#debugging)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Optical Character Recognition (OCR)**: Uses Tesseract to read multiplication problems.
- **Human-like Interaction**: Simulates mouse movements with PyAutoGUI.
- **Error Handling**: Robust handling of unexpected pop-ups and errors.
- **Customizable Regions**: Configure specific screen areas for OCR.
- **Thresholding**: Adjust image processing settings for better accuracy.
- **Debugging Tools**: Save debug images to analyze OCR performance.
- **Educational Use**: Designed for learning and experimentation.

## Technologies Used

- **Python**: The core programming language for this project.
- **Tesseract OCR**: An open-source OCR engine used for text recognition.
- **PyAutoGUI**: A Python library that allows for programmatic control of the mouse and keyboard.
- **OpenCV**: A library used for image processing and computer vision tasks.

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/valevale44/Python-pyautogui-pytesseract-Multiplication-Game-Automation.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd Python-pyautogui-pytesseract-Multiplication-Game-Automation
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract**:

   - For Windows, download the installer from the [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
   - For macOS, use Homebrew:

     ```bash
     brew install tesseract
     ```

   - For Linux, use the package manager:

     ```bash
     sudo apt-get install tesseract-ocr
     ```

## Usage

To run the multiplication quiz solver, execute the following command:

```bash
python main.py
```

The bot will start and wait for the multiplication quiz to appear. Ensure that the quiz window is visible on your screen.

### Example Workflow

1. Start the multiplication quiz application.
2. Run the bot.
3. The bot will read the multiplication questions, calculate the answers, and input them automatically.

## Configuration

You can customize the bot's behavior by modifying the `config.py` file. Here are some settings you can adjust:

- **Region Configuration**: Set the screen area for OCR.
- **Thresholding Parameters**: Adjust image processing settings.
- **Mouse Speed**: Change the speed of mouse movements.

### Example Configuration

```python
REGION = (100, 200, 800, 600)  # (x, y, width, height)
THRESHOLD = 150  # Adjust for better OCR accuracy
MOUSE_SPEED = 0.5  # Speed of mouse movements
```

## Debugging

The project includes debugging tools to help you analyze the performance of the OCR. You can enable debug image saving in the `config.py` file:

```python
SAVE_DEBUG_IMAGES = True  # Set to True to save images for debugging
```

When enabled, the bot will save images of the screen before and after processing. This helps you understand how well the OCR is performing.

## Contributing

We welcome contributions to this project. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

Please ensure that your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or feedback, please reach out:

- **Email**: [your-email@example.com](mailto:your-email@example.com)
- **GitHub**: [valevale44](https://github.com/valevale44)

Thank you for checking out the **Automated Multiplication Quiz Solver**! We hope you find it useful for your educational projects.

[Download the latest release here!](https://github.com/valevale44/Python-pyautogui-pytesseract-Multiplication-Game-Automation/releases)