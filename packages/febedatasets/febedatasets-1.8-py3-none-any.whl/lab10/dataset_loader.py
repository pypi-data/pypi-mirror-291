import os


def load_datasetpath(name):
    # Define the path to the datasets directory
    data_dir = os.path.join(os.path.dirname(__file__), "data")

    # Try to locate the dataset with various extensions
    possible_extensions = [".csv", ".txt"]
    dataset_path = None

    for ext in possible_extensions:
        potential_path = os.path.join(data_dir, f"{name}{ext}")
        if os.path.isfile(potential_path):
            dataset_path = potential_path
            break

    # If the dataset wasn't found, raise an error
    if not dataset_path:
        raise ValueError(f"Dataset {name} does not exist.")

    # Return the dataset path
    return dataset_path


# Example usage
# path = load_datasetpath('your_dataset_name')
