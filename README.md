# Ansible Vault Extractor

A Python utility to extract and decrypt Ansible vault-encrypted values from YAML files. This tool provides a simple way to access vault-protected variables without needing to write a full Ansible playbook.

## Features

- Extract and decrypt Ansible vault-encrypted values from YAML files
- Multiple output formats: YAML, environment variables, or debug output
- Clean, filtered output (removes Ansible internal variables)
- Simple command-line interface
- Cross-platform compatibility

## Prerequisites

- Python 3.6 or higher
- Ansible installed and available in your PATH
- Access to the vault password file

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd ansible-extractor
```

2. Make the script executable (optional):
```bash
chmod +x extract_vault_values.py
```

## Usage

### Basic Usage

Extract vault-encrypted values and display as YAML:

```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file vault_password.txt
```

### Output Formats

**YAML format (default):**
```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file vault_password.txt
```

**Environment variables format:**
```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file vault_password.txt --env
```

**Debug output (raw Ansible output):**
```bash
python extract_vault_values.py --yaml-file secrets.yml --vault-password-file vault_password.txt --debug
```

### Command Line Options

- `--yaml-file`: Path to the YAML file with vault-encrypted values (required)
- `--vault-password-file`: Path to the vault password file (required)
- `--debug`: Show verbose ansible debug output
- `--env`: Output as exported environment variables with uppercase keys

## Examples

### Example 1: Basic Extraction
```bash
python extract_vault_values.py --yaml-file config/secrets.yml --vault-password-file .vault_pass
```

Output:
```
database_url: "postgresql://user:pass@localhost/db"
api_key: "sk-1234567890abcdef"
```

### Example 2: Environment Variables
```bash
python extract_vault_values.py --yaml-file config/secrets.yml --vault-password-file .vault_pass --env
```

Output:
```
export DATABASE_URL="postgresql://user:pass@localhost/db"
export API_KEY="sk-1234567890abcdef"
```

### Example 3: Source into Shell
```bash
source <(python extract_vault_values.py --yaml-file config/secrets.yml --vault-password-file .vault_pass --env)
```

## How It Works

The tool works by:

1. Creating a temporary Ansible inventory file
2. Running `ansible debug` with the provided YAML file and vault password
3. Parsing the Ansible output to extract variables
4. Filtering out Ansible internal variables
5. Outputting the results in the requested format

## Error Handling

The tool includes comprehensive error handling for:
- Missing input files
- Invalid vault passwords
- Ansible command failures
- JSON parsing errors
- General exceptions

## Security Notes

- The vault password file should be kept secure and not committed to version control
- Temporary files are automatically cleaned up after use
- The tool only extracts non-Ansible internal variables

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 