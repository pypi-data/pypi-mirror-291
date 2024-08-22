# Cognitive Schema

Unlock the power of your database with **Cognitive Schema**! This innovative command-line interface (CLI) tool not only downloads database schemas but also generates insightful profiles using cutting-edge AI technology. Say goodbye to tedious data analysis and hello to intelligent insights!

<img src="./logo.png" alt="Cognitive Schema Logo" width="200" height="200">

## Features

- **Effortlessly Download Schemas**: Quickly fetch database schemas from PostgreSQL with a single command.
- **Instant Sample Data**: Automatically retrieve and save sample data for each table, ready for analysis.
- **AI-Powered Insights**: Generate detailed profiles for each table, revealing hidden patterns and insights.
- **User-Friendly CLI**: Enjoy a seamless command-line experience designed for both beginners and experts.

## Requirements

- Python 3.6 or higher
- OpenAI API key (for generating profiles)

## Installation

1. Install the package using pip:
   ```bash
   pip install cognitive_schema
   ```
2. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your_openai_api_key'  # On Windows use: set OPENAI_API_KEY='your_openai_api_key'
   ```

## Usage

Refer to the [Northwind Example](./examples/northwind/README.md) to test **Cognitive Schema** with a sample PostgreSQL database.

## Directory Structure

```
cognitive_schema/
├── cognitive_schema/          # Main package directory
│   ├── cli.py                 # CLI tool implementation
│   ├── db/                    # Database-related modules
│   │   ├── download_schema.py  # Module for downloading the database schema
│   │   ├── generate_profiles.py # Module for generating database profiles
├── LICENSE                    # License file (MIT License)
├── README.md                  # Project documentation and instructions
├── requirements.txt           # Requirements file for dependencies
├── setup.py                   # Setup script for packaging the CLI tool
└── CHANGELOG.md               # Changelog for tracking updates and changes
```

## Troubleshooting

- **Error: Connection failed**: Ensure that your database credentials are correct and that the database server is running.
- **Error: OpenAI API key not set**: Make sure you have set your OpenAI API key as an environment variable.

## Contributing

We love contributions! Whether you have a bug fix, a new feature, or just a suggestion, your input is invaluable. Join our community and help us make **Cognitive Schema** even better!

1. Fork the repository.
2. Create a new branch.
3. Make your changes and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. The MIT License allows for reuse within proprietary software, as long as the license is distributed with that software.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the AI capabilities.

## Get Started Today!

Ready to unlock the potential of your database? Clone the repository, set up your environment, and start exploring the world of intelligent data analysis with **Cognitive Schema**!
