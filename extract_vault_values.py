#!/usr/bin/env python3
"""
Simple vault extractor - Python version
Extracts and decrypts Ansible vault-encrypted values from YAML files.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import yaml
from pathlib import Path


def run_ansible_debug(yaml_file, vault_password_file):
    """Run ansible debug command and return the output."""
    # Create temp inventory
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_inv:
        temp_inv.write("localhost ansible_connection=local\n")
        temp_inv_path = temp_inv.name
    
    try:
        # Run ansible command
        cmd = [
            'ansible', 'localhost',
            '-i', temp_inv_path,
            '--vault-password-file', vault_password_file,
            '-e', f'@{yaml_file}',
            '-m', 'debug',
            '-a', 'var=hostvars[inventory_hostname]'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout
    finally:
        # Clean up temp file
        Path(temp_inv_path).unlink(missing_ok=True)


def extract_variables_from_ansible_output(output):
    """Extract variables from ansible debug output."""
    # Find the JSON data in the ansible output
    match = re.search(r'localhost.*SUCCESS.*?({.*})', output, re.DOTALL)
    if not match:
        raise ValueError("No valid output found in ansible response")
    
    # Parse the JSON
    data = json.loads(match.group(1))
    
    # Extract variables from hostvars[inventory_hostname]
    variables = data.get('hostvars[inventory_hostname]', {})
    
    # Filter out Ansible internal variables (those starting with 'ansible_')
    filtered_variables = {}
    for key, value in variables.items():
        if not key.startswith('ansible_') and key not in ['group_names', 'groups', 'inventory_dir', 'inventory_file', 'inventory_hostname', 'inventory_hostname_short', 'omit', 'playbook_dir']:
            filtered_variables[key] = value
    
    return filtered_variables


def show_yaml_output(variables):
    """Show variables as clean YAML."""
    # Clean up the variables by stripping whitespace and newlines
    cleaned_variables = {}
    for key, value in variables.items():
        if isinstance(value, str):
            # Strip whitespace and newlines from string values
            cleaned_variables[key] = value.strip()
        else:
            # Keep non-string values as-is
            cleaned_variables[key] = value
    
    # Output with double quotes only for values, not keys
    for key, value in cleaned_variables.items():
        if isinstance(value, str):
            print(f'{key}: "{value}"')
        else:
            print(f'{key}: {value}')


def show_env_output(variables):
    """Show variables as exported environment variables with uppercase keys."""
    # Clean up the variables by stripping whitespace and newlines
    cleaned_variables = {}
    for key, value in variables.items():
        if isinstance(value, str):
            # Strip whitespace and newlines from string values
            cleaned_variables[key] = value.strip()
        else:
            # Keep non-string values as-is
            cleaned_variables[key] = value
    
    # Output as exported environment variables with uppercase keys
    for key, value in cleaned_variables.items():
        # Convert key to uppercase and replace hyphens/periods with underscores
        env_key = key.upper().replace('-', '_').replace('.', '_')
        if isinstance(value, str):
            print(f'export {env_key}="{value}"')
        else:
            print(f'export {env_key}={value}')


def show_debug_output(output):
    """Show the raw ansible debug output."""
    print(output)


def main():
    parser = argparse.ArgumentParser(
        description='Extract and decrypt Ansible vault-encrypted values from YAML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --yaml-file secrets.yml --vault-password-file vault_password.txt
  %(prog)s --yaml-file secrets.yml --vault-password-file vault_password.txt --debug
  %(prog)s --yaml-file secrets.yml --vault-password-file vault_password.txt --env
        """
    )
    
    parser.add_argument(
        '--yaml-file', 
        required=True,
        help='Path to the YAML file with vault-encrypted values'
    )
    parser.add_argument(
        '--vault-password-file', 
        required=True,
        help='Path to the vault password file'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true', 
        help='Show verbose ansible debug output'
    )
    parser.add_argument(
        '--env', 
        action='store_true', 
        help='Output as exported environment variables with uppercase keys'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not Path(args.yaml_file).exists():
        print(f"Error: YAML file '{args.yaml_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not Path(args.vault_password_file).exists():
        print(f"Error: Vault password file '{args.vault_password_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Run ansible to decrypt the vault
        output = run_ansible_debug(args.yaml_file, args.vault_password_file)
        
        if args.debug:
            show_debug_output(output)
        elif args.env:
            # Output as environment variables
            variables = extract_variables_from_ansible_output(output)
            show_env_output(variables)
        else:
            # Default: show clean YAML
            variables = extract_variables_from_ansible_output(output)
            show_yaml_output(variables)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running ansible command: {e}", file=sys.stderr)
        if e.stderr:
            print(f"Ansible error output: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing output: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main() 