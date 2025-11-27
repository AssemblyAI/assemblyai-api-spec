"""
Generate OpenAPI specification in JSON or YAML format.
"""
import json
import yaml
from main import app


def generate_openapi_spec(output_file: str = "openapi.yml"):
    """Generate OpenAPI spec and save to file."""
    # Get the OpenAPI spec
    openapi_spec = app.openapi()
    
    # Write to file based on extension
    with open(output_file, 'w') as f:
        if output_file.endswith('.json'):
            json.dump(openapi_spec, f, indent=2)
        else:
            # Default to YAML, use flow style false for better readability
            yaml.dump(openapi_spec, f, default_flow_style=False, sort_keys=False)
    
    print(f"OpenAPI spec generated: {output_file}")


if __name__ == "__main__":
    import sys
    
    # Allow specifying output file as command line argument
    output_file = sys.argv[1] if len(sys.argv) > 1 else "openapi.yml"
    generate_openapi_spec(output_file)