import os
import nbformat
from pathlib import Path

def convert_notebook_to_mdx(notebook_path, output_path):
    """
    Convert a Jupyter notebook to MDX format.
    
    Args:
        notebook_path (str): Path to the input notebook file
        output_path (str): Path where the MDX file will be saved
    """
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Initialize MDX content with frontmatter
    mdx_content = [
        '---',
        f'title: "{Path(notebook_path).stem}"',
        '---\n',
    ]
    
    # Process each cell
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            # Add markdown content directly
            mdx_content.append(cell.source)
            mdx_content.append('\n')
        
        elif cell.cell_type == 'code':
            # Wrap code in markdown code fence
            mdx_content.append('```python')
            mdx_content.append(cell.source)
            mdx_content.append('```\n')
            
            # Add output if present
            if cell.outputs:
                mdx_content.append('<Output>\n')
                for output in cell.outputs:
                    if 'text' in output:
                        mdx_content.append('```')
                        mdx_content.append(output.text)
                        mdx_content.append('```')
                    elif 'data' in output:
                        if 'text/plain' in output.data:
                            mdx_content.append('```')
                            mdx_content.append(output.data['text/plain'])
                            mdx_content.append('```')
                        # Handle images if present
                        if 'image/png' in output.data:
                            mdx_content.append('![Output](data:image/png;base64,')
                            mdx_content.append(output.data['image/png'])
                            mdx_content.append(')\n')
                mdx_content.append('</Output>\n')
    
    # Write the MDX file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(mdx_content))

def process_directory(input_dir):
    """
    Recursively process all .ipynb files in a directory and its subdirectories.
    
    Args:
        input_dir (str): Path to the directory to process
    """
    # Convert input_dir to Path object
    input_path = Path(input_dir)
    
    # Create a directory for MDX files if it doesn't exist
    mdx_dir = input_path / 'mdx_output'
    mdx_dir.mkdir(exist_ok=True)
    
    # Find all .ipynb files
    for notebook_path in input_path.rglob('*.ipynb'):
        # Skip checkpoint files
        if '.ipynb_checkpoints' in str(notebook_path):
            continue
            
        # Create corresponding MDX path
        relative_path = notebook_path.relative_to(input_path)
        mdx_path = mdx_dir / relative_path.with_suffix('.mdx')
        
        # Create necessary subdirectories
        mdx_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f'Converting {notebook_path} to {mdx_path}')
        try:
            convert_notebook_to_mdx(str(notebook_path), str(mdx_path))
        except Exception as e:
            print(f'Error converting {notebook_path}: {str(e)}')

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print('Usage: python notebook_to_mdx.py <directory_path>')
        sys.exit(1)
    
    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f'Error: {directory_path} is not a valid directory')
        sys.exit(1)
    
    process_directory(directory_path)
    print('Conversion complete! Check the mdx_output directory for the converted files.')