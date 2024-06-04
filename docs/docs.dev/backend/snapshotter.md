# Snapshotter

## Overview
Snapshotter is a Python script designed to facilitate the creation and loading of database snapshots in SQLAlchemy-based applications. It simplifies the process of dumping the current database state to a file and loading a database state from a file.

## Technologies used
- Python
- SQLAlchemy

## Description
Snapshotter provides functionality to dump the current state of a database into a JSON file and load a database state from a JSON file. It ensures that foreign key constraints are handled properly during the loading process, allowing users to easily create snapshots of their database and load them back in without encountering foreign key constraint errors.

### Dumping Database State
When dumping the database state, Snapshotter retrieves data from all tables in the database and writes it to a JSON file. It ensures that the data is properly formatted and ready for loading into another database.

### Loading Database State
When loading the database state, Snapshotter reads data from a JSON file and inserts it into the corresponding tables in the database. It handles foreign key constraints by ensuring that tables are inserted in the correct order to satisfy dependencies, thereby preventing foreign key constraint errors.

## Command-line Arguments
Snapshotter can be invoked from the command line with the following arguments:

- `action`: Specifies the action to perform. Supported actions are `dump` and `load`.
- `file_path`: Specifies the path to the JSON file for dumping or loading the database state.
