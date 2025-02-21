"""
Database Operations and Data Visualization Script
Author: Shahrukh
Description: Connects to MySQL, creates database schema, processes CSV data, 
             and visualizes results using Bokeh.
"""

import mysql.connector
import numpy as np
import pandas as pd
import webbrowser
import os
from bokeh.plotting import figure, output_file, save
from typing import Tuple, List

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "python_assignment_shahrukh"
}

def initialize_database() -> None:
    """Create database and tables with required schema"""
    try:
        with mysql.connector.connect(**{**DB_CONFIG, "database": None}) as conn:
            with conn.cursor() as cursor:
                # Create database if not exists
                cursor.execute("CREATE DATABASE IF NOT EXISTS python_assignment_shahrukh")
                cursor.execute("USE python_assignment_shahrukh")
                
                # Table creation queries
                tables = [
                    """CREATE TABLE IF NOT EXISTS train (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        X FLOAT, y1 FLOAT, y2 FLOAT, y3 FLOAT, y4 FLOAT
                    )""",
                    """CREATE TABLE IF NOT EXISTS test (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        X FLOAT, Y FLOAT
                    )""",
                    """CREATE TABLE IF NOT EXISTS ideal (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        X FLOAT
                    )""",
                    """CREATE TABLE IF NOT EXISTS mapping (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        X FLOAT, Y FLOAT,
                        ideal_x FLOAT, ideal_y FLOAT,
                        deviation FLOAT
                    )"""
                ]
                
                for table_query in tables:
                    cursor.execute(table_query)
                
                # Add columns to ideal table if missing
                cursor.execute("SHOW COLUMNS FROM ideal")
                existing_columns = {col[0] for col in cursor.fetchall()}
                
                for col_num in range(1, 51):
                    col_name = f"y{col_num}"
                    if col_name not in existing_columns:
                        cursor.execute(f"ALTER TABLE ideal ADD COLUMN {col_name} FLOAT")
                
                conn.commit()
                print("Database initialization completed successfully.")
                
    except mysql.connector.Error as err:
        print(f"Database initialization failed: {err}")
        raise

def load_dataset(file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Load and process CSV data"""
    try:
        df = pd.read_csv(file_path)
        x_values = df['X'].values
        y_columns = [col for col in df.columns if col.startswith('y')]
        y_values = df[y_columns].values
        return x_values, y_values
    except (FileNotFoundError, pd.errors.EmptyDataError) as err:
        print(f"Data loading error: {err}")
        raise

def generate_visualization(train_data: Tuple[np.ndarray, np.ndarray],
                          test_data: Tuple[np.ndarray, np.ndarray],
                          mappings: List[Tuple]) -> None:
    """Create interactive visualization using Bokeh"""
    output_file("data_visualization.html")
    
    plot = figure(
        title="Dataset Comparison with Ideal Functions",
        x_axis_label='X-axis Values',
        y_axis_label='Y-axis Values',
        tools="pan,wheel_zoom,box_zoom,reset"
    )
    
    # Plot training data in green
    plot.scatter(train_data[0], train_data[1], 
                color='forestgreen', size=8, alpha=0.6,
                legend_label='Training Data')
    
    # Plot test data in blue
    plot.scatter(test_data[0], test_data[1], 
                color='navy', size=8, alpha=0.6,
                legend_label='Test Data')
    
    # Plot mapped points in red
    plot.scatter([m[0] for m in mappings], [m[1] for m in mappings],
                color='crimson', size=10, alpha=0.8,
                legend_label='Mapped Points')
    
    plot.legend.location = "top_left"
    save(plot)
    webbrowser.open(f"file://{os.path.abspath('data_visualization.html')}")

def main() -> None:
    """Main execution flow"""
    # Initialize database structure
    initialize_database()
    
    # Load datasets (update paths as needed)
    train_x, train_y = load_dataset("path/to/train.csv")
    test_x, test_y = load_dataset("path/to/test.csv")
    
    # Generate sample ideal functions (replace with actual data)
    ideal_functions = np.random.rand(50, 2)
    
    # Create sample mappings (simplified example)
    data_mappings = [
        (x, y, *ideal_functions[np.random.randint(50)])
        for x, y in zip(test_x, test_y)
    ]
    
    # Generate and display visualization
    generate_visualization(
        (train_x, train_y[:, 0]),  # Using first y column from training
        (test_x, test_y),
        data_mappings
    )

if __name__ == "__main__":
    main()