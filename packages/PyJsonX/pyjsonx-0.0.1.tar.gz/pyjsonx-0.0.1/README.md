# PyjsonX

### Overview

`PyJsonX` is a Python library that allows embedding Python code within JSON files. This feature enables dynamic and programmable JSON content generation.

### Installation

You can install `PyJsonX` using pip:

```bash
pip install PyJsonX
```

### Usage

#### Embedding Python in JSON

You can embed Python code within JSON using `<?py ... ?>` tags. Here’s an example:

```json
{
    "static_field": "value",  // Static field
    <?py
        result = ""
        // Generate dynamic fields with values from 0 to 4
        for i in range(5):
            result += f'"dynamic_{i}": "{i * 2}", \n'
        return result
    ?>
    "another_static_field": "another_value"  // Another static field
}
```

#### Executing Embedded Python

1. **From JSON String:**

    ```python
    import PyJsonX

    json_str = '''
    {
        "static_field": "value",
        <?py
            result = ""
            // Generate dynamic fields with values from 0 to 4
            for i in range(5):
                result += f'"dynamic_{i}": "{i * 2}", \n'
            return result
        ?>
        "another_static_field": "another_value"
    }
    '''

    # Process the JSON string and execute the embedded Python code
    processed_str = PyJsonX.execute(json_str)
    print(processed_str)  # Output the processed JSON
    ```

2. **From JSON Files:**

    ```python
    import PyJsonX

    input_json_path = 'input.json'  // Path to the input JSON file
    output_json_path = 'output.json'  // Path to the output JSON file

    # Process the JSON file and execute the embedded Python code
    PyJsonX.execute_file(input_json_path, output_json_path)
    ```

### Features

- **Dynamic Content Generation:** Embed and execute Python code directly within JSON to generate dynamic content.
- **Flexible Data Creation:** Generate complex JSON structures dynamically based on programmatic logic.

### Documentation

For more detailed information, visit the [PyJsonX Documentation](https://github.com/nnnnnnn0090/PyJsonX).

### Contributing

Contributions are welcome! Please submit a pull request or open an issue on our [GitHub repository](https://github.com/nnnnnnn0090/PyJsonX).

### License

`PyJsonX` is licensed under the MIT License. See [LICENSE](https://github.com/nnnnnnn0090/PyJsonX/blob/main/LICENSE) for details.