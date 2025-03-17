# Insurance_data_visualization
## Description
This script visualizes insurance-related data, focusing on key aspects such as top tariffs, regional performance, and changes in tariffs over time. The raw data, consisting of numerous numeric and textual entries, can be difficult to interpret and analyze directly in a digital or textual format. By transforming this data into visualizations, the script makes it much easier to explore and understand complex relationships. It connects to an Oracle database to retrieve data about insurance products, regions, and various time periods. The program provides interactive graphs that allow users to explore trends, compare different insurance companies, and analyze the performance of specific tariffs. The primary goal is to enable users to easily track, visualize, and analyze insurance-related data to make informed business decisions.

## Functional Description
The program performs the following steps:
1. Connects to an Oracle database and retrieves insurance data.
2. Cleanses and processes the data to remove invalid or irrelevant entries.
3. Transforms the data into percentage-based values for easy visualization.
4. Generates several interactive scatter plots to visualize the relationship between different parameters such as tariffs, repeat business, and regions.
5. Offers interactive features such as dropdown menus and radio buttons for filtering and viewing data based on different regions and time intervals (dates, weeks, months).
6. Displays insights about the insurance market, including top 10 tariffs, regional performance, and tariff changes over time.

## How It Works
1. The program connects to an Oracle database using SQLAlchemy and retrieves data from relevant tables.
2. It filters out rows with invalid or irrelevant data, such as zero or missing values.
3. The data is processed to calculate percentages and averages for different metrics.
4. Interactive visualizations are generated using Plotly, displaying scatter plots of tariff performance across insurance companies and regions.
5. The app includes dropdown menus for selecting specific regions, and radio buttons for choosing time intervals (dates, weeks, or months).
6. The visualizations and data tables are updated dynamically based on user input, allowing for in-depth analysis.

## Input Structure
To run the program, the following parameters need to be provided:
1. Database credentials: Username, Password, Database DSN (Data Source Name).
2. The data tables to query for the insurance-related data: `al_babkina_dashbord_top10prol`, `al_babkina_dashbord_top10prol_2`, `al_babkina_dashbord_top10регион`, `al_babkina_dashbord_дата_расчета`.

## Technical Requirements
To run the program, the following are required:
1. Python 3.x
2. Installed libraries: sqlalchemy, pandas, plotly, dash, oracledb
3. Oracle Database with the following tables: `al_babkina_dashbord_top10prol`, `al_babkina_dashbord_top10prol_2`, `al_babkina_dashbord_top10регион`, `al_babkina_dashbord_дата_расчета`.

## Usage
1. Modify the username, password, and DSN values to connect to your Oracle database.
2. Ensure the necessary data tables are present in your database.
3. Run the script. It will generate a dashboard that displays the following:
   - Interactive visualizations of the top 10 tariffs.
   - Scatter plots showing performance by insurance company and region.
   - Tariff changes over time, grouped by dates, weeks, or months.
4. Use the dropdown menus and radio buttons to filter data by region and time interval.

## Example Output
- **Top 10 tariffs visualization**: Displays the top tariffs across insurance companies.
- **Regional performance visualization**: Shows the relationship between tariffs and repeat business for selected regions.
- **Tariff changes over time**: Visualizes changes in tariffs over different time intervals (days, weeks, months).

## Conclusion
This script provides an interactive dashboard that helps insurance companies visualize and analyze their data. It allows users to track trends, compare performance across different regions, and monitor changes in tariffs, helping to make data-driven business decisions.
