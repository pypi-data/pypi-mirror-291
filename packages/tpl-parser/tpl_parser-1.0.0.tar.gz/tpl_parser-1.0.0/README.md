# TPLParserPy

<p align="center">
  <img src="./assets/logo.png" alt="Logo" height="128px">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white"/>
</p>

# 🎨 TPLParserPy

Welcome to **TPLParserPy**! 🛠️ This Python package is designed to help you parse Photoshop TPL (Tool Preset) files and extract the data into a friendly JSON format. Perfect for anyone who wants to dive deep into TPL files and understand their inner workings! 💡

## ✨ Features

- 🔍 **Parse Photoshop TPL files** with ease.
- 🗂️ **Extract tool names, types, and properties** into JSON format.
- 💾 **Save the extracted data** for further use or analysis.

## 🚀 Installation

You can easily install TPLParserPy via pip:

```bash
pip install tpl-parser
```

## 🛠️ Usage

### Importing and Using the Library

Here's a quick example of how to use TPLParserPy in your Python project:

```python
from TPLParser import TPLReader

file_path = "path/to/yourfile.tpl"
reader = TPLReader(file_path)
tpl_data = reader.read_tpl()
reader.save_to_json("output.json")
```

### Command-Line Interface

TPLParserPy also includes a handy command-line interface for quick parsing:

```bash
tpl-parser path/to/yourfile.tpl -o output.json
```

## 🤝 Contributions

Contributions are welcome! 🎉 If you'd like to contribute to TPLParserPy, feel free to fork the repository and submit a pull request. If you have any questions or need guidance, don't hesitate to contact me at [devjonescodes@gmail.com](mailto:devjonescodes@gmail.com).

## 📄 License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. For more details, see the [LICENSE](./LICENSE) file. For commercial use, please contact [Dev Jones](mailto:devjonescodes@gmail.com).

## 📬 Contact

If you have any questions, suggestions, or just want to say hi, feel free to reach out via email: [devjonescodes@gmail.com](mailto:devjonescodes@gmail.com). We'd love to hear from you! 😊
