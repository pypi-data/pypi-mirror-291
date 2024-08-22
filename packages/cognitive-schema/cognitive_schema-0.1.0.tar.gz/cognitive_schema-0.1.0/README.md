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

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cognitive_schema.git
   cd cognitive_schema
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -e .
   ```
4. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your_openai_api_key'  # On Windows use: set OPENAI_API_KEY='your_openai_api_key'
   ```

## Usage

### Download Database Schema

Run the following command to download your database schema:

```bash
cognitive_schema download --dbname <your_db_name> --user <your_username> --password <your_password> --host <your_host> --port <your_port>
```

_Expected Output:_

```
Schema fetched successfully! Sample data saved to `db/data/`.
```

### Generate Database Profiles

To generate profiles for the downloaded schema, use the following command:

```bash
cognitive_schema profile
```

_Expected Output:_

```
Profiles generated successfully! Profile saved to `db/profiles/`.
```

### Run All Operations

To run both downloading the schema and generating profiles in one command, use:

```bash
cognitive_schema run --dbname <your_db_name> --user <your_username> --password <your_password> --host <your_host> --port <your_port>
```

_Expected Output:_

```
Schema downloaded and profiles generated successfully!
```

## Sample Report

To illustrate the potential of **Cognitive Schema**, here’s an example profile for a table named `user_engagement_stats`:

#### Overview

The `user_engagement_stats` table captures key metrics related to user interactions within a digital platform. Each record provides insights into user behavior, including session duration, page views, and engagement rates over a specified timeframe. This data is essential for understanding user engagement patterns, optimizing content, and enhancing user experience.

#### Columns

| Name             | Description                                        | Type              | Sample Data                            |
| ---------------- | -------------------------------------------------- | ----------------- | -------------------------------------- |
| id               | Unique identifier for each record in the table.    | Number            | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10          |
| user_id          | Unique identifier for each user.                   | String            | user_001, user_002, user_003, user_004 |
| session_date     | Date of the user session.                          | Date              | 2023-01-01, 2023-01-02, 2023-01-03     |
| session_duration | Duration of the session in seconds.                | Number            | 300, 450, 1200, 600                    |
| page_views       | Total number of pages viewed during the session.   | Number            | 5, 8, 12, 3                            |
| engagement_rate  | Percentage of engaged users based on interactions. | Number (Nullable) | 75.0, 85.5, 60.0, NaN                  |
| created_at       | Timestamp of when the record was created.          | DateTime          | 2023-01-01 10:00:00                    |
| updated_at       | Timestamp of the last update to the record.        | DateTime          | 2023-01-02 12:00:00                    |

#### Insights

From the sample data observed in the `user_engagement_stats` table, several insights can be deduced:

1. **User Interaction Patterns**: The data reveals varying session durations, indicating different levels of user engagement. For instance, users with IDs `user_001` and `user_002` have significantly longer sessions (300 and 450 seconds) compared to others, suggesting they are more engaged with the content.
2. **Page Views Correlation**: There appears to be a correlation between session duration and the number of page views. Users who spent more time on the platform also viewed more pages, indicating that engaging content leads to longer sessions.
3. **Engagement Rate Variability**: The engagement rate shows variability, with some users exhibiting high engagement (e.g., 85.5%) while others have missing data (NaN). This suggests a need for further investigation into user behavior and potential barriers to engagement.
4. **Temporal Analysis**: The records span multiple days, allowing for trend analysis over time. Analyzing engagement metrics across different dates can help identify patterns, such as peak engagement times or the impact of new content releases.
5. **Data Completeness**: The presence of NaN values in the `engagement_rate` column highlights the importance of data completeness. Improving data collection methods could enhance the accuracy of engagement metrics.

Overall, the `user_engagement_stats` table serves as a vital resource for understanding user behavior, optimizing content strategies, and enhancing user experience on digital platforms. By leveraging the insights generated from this data, businesses can make informed decisions to drive user engagement and satisfaction.

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
