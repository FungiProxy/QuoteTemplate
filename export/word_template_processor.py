"""
Word Template Processor for Professional Quote Generation

This module processes Word templates (.docx) with template variables like {{customer_name}}
and maintains the original professional formatting and layout.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING, List
from datetime import datetime
import logging

if TYPE_CHECKING:
    from docx import Document

try:
    from docx import Document
    from docx.shared import Inches
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

logger = logging.getLogger(__name__)

class WordTemplateProcessor:
    """
    Processes Word templates by replacing {{variable}} placeholders with actual values.
    Maintains original formatting and professional appearance.
    """
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the Word template processor.
        
        Args:
            templates_dir: Path to the templates directory
        """
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx is required. Install with: pip install python-docx")
            
        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.templates_dir = Path(templates_dir)
        
    def get_template_path(self, model: str) -> Optional[Path]:
        """
        Get the template file path for a given model.
        
        Args:
            model: Model name (e.g., 'LS2000H', 'FS10000S')
            
        Returns:
            Path to the template file, or None if not found
        """
        template_name = f"{model}_template.docx"
        template_path = self.templates_dir / template_name
        
        if template_path.exists():
            return template_path
        
        logger.warning(f"Template not found: {template_path}")
        return None
    
    def replace_variables_in_paragraph(self, paragraph, variables: Dict[str, str]) -> None:
        """
        Replace template variables in a paragraph while preserving formatting.
        
        Args:
            paragraph: docx paragraph object
            variables: Dictionary of variable name -> value mappings
        """
        # Get the full text of the paragraph
        full_text = paragraph.text
        
        # Find all template variables in the format {{variable_name}}
        variable_pattern = r'\{\{([^}]+)\}\}'
        matches = re.findall(variable_pattern, full_text)
        
        if not matches:
            return
        
        # Replace variables in the full text
        new_text = full_text
        for var_name in matches:
            placeholder = f"{{{{{var_name}}}}}"
            value = variables.get(var_name, f"{{{{MISSING: {var_name}}}}}")
            new_text = new_text.replace(placeholder, str(value))
        
        # Clear the paragraph and add the new text
        # This preserves the paragraph's formatting but not individual run formatting
        paragraph.clear()
        paragraph.add_run(new_text)

    def _process_conditional_content_document(self, doc, variables: Dict[str, str], model: Optional[str] = None) -> None:
        """
        Process conditional content at the document level to avoid breaking formatting.
        Handles {{if_option:option_code:content}} patterns by either showing or hiding content.
        Args:
            doc: Document object
            variables: Dictionary of variables including option information
            model: The template/model name (e.g., 'FS10000'), or None
        """
        import re
        try:
            option_codes = variables.get('option_codes', [])
            print(f"DEBUG: Raw option_codes from variables: {option_codes}")
            logger.info(f"Raw option_codes from variables: {option_codes}")
            print(f"DEBUG: Type of option_codes: {type(option_codes)}")
            logger.info(f"Type of option_codes: {type(option_codes)}")
            
            if isinstance(option_codes, str):
                # Handle string representation of a list (like "['XSP']")
                if option_codes.startswith('[') and option_codes.endswith(']'):
                    # It's a string representation of a list, try to evaluate it safely
                    try:
                        import ast
                        option_codes = ast.literal_eval(option_codes)
                        print(f"DEBUG: Parsed string list to: {option_codes}")
                        logger.info(f"Parsed string list to: {option_codes}")
                    except:
                        # Fallback: split by comma
                        option_codes = [opt.strip() for opt in option_codes.split(',') if opt.strip()]
                        print(f"DEBUG: Fallback split by comma: {option_codes}")
                        logger.info(f"Fallback split by comma: {option_codes}")
                else:
                    # Regular comma-separated string
                    option_codes = [opt.strip() for opt in option_codes.split(',') if opt.strip()]
                    print(f"DEBUG: Converted string option_codes to list: {option_codes}")
                    logger.info(f"Converted string option_codes to list: {option_codes}")
            elif isinstance(option_codes, list):
                print(f"DEBUG: Option_codes is already a list: {option_codes}")
                logger.info(f"Option_codes is already a list: {option_codes}")
            else:
                print(f"DEBUG: Unexpected option_codes type: {type(option_codes)}, value: {option_codes}")
                logger.warning(f"Unexpected option_codes type: {type(option_codes)}, value: {option_codes}")
                option_codes = []
            
            print(f"DEBUG: Final option_codes for processing: {option_codes}")
            logger.info(f"Final option_codes for processing: {option_codes}")
            
            # Process paragraphs for conditional content
            for paragraph in doc.paragraphs:
                try:
                    self._process_conditional_content_paragraph(paragraph, option_codes, model)
                except Exception as e:
                    logger.warning(f"Error processing conditional content in paragraph: {e}")
                    # Continue processing other paragraphs
            
            # Process tables for conditional content
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            try:
                                self._process_conditional_content_paragraph(paragraph, option_codes, model)
                            except Exception as e:
                                logger.warning(f"Error processing conditional content in table paragraph: {e}")
                                # Continue processing other paragraphs
            
            # Process headers and footers for conditional content
            for section in doc.sections:
                header = section.header
                for paragraph in header.paragraphs:
                    try:
                        self._process_conditional_content_paragraph(paragraph, option_codes, model)
                    except Exception as e:
                        logger.warning(f"Error processing conditional content in header: {e}")
                        # Continue processing other paragraphs
                
                footer = section.footer
                for paragraph in footer.paragraphs:
                    try:
                        self._process_conditional_content_paragraph(paragraph, option_codes, model)
                    except Exception as e:
                        logger.warning(f"Error processing conditional content in footer: {e}")
                        # Continue processing other paragraphs
                        
        except Exception as e:
            logger.error(f"Error in conditional content processing: {e}")
            # Don't let this break the entire template processing
            # Just log the error and continue

    def _process_conditional_content_paragraph(self, paragraph, option_codes: List[str], model: Optional[str] = None) -> None:
        """
        Process conditional content in a single paragraph.
        Args:
            paragraph: Paragraph object
            option_codes: List of option codes present in the part number
            model: The template/model name (e.g., 'FS10000'), or None
        """
        import re
        try:
            conditional_pattern = r'\{\{if_option:([^:]+):([^}]+)\}\}'
            full_text = paragraph.text
            matches = list(re.finditer(conditional_pattern, full_text))
            if not matches:
                return
            # Remove all conditional content blocks (do not insert any replacement text)
            for match in reversed(matches):
                start_pos = match.start()
                end_pos = match.end()
                paragraph.clear()
                new_text = full_text[:start_pos] + full_text[end_pos:]
                paragraph.add_run(new_text)
                full_text = new_text
        except Exception as e:
            logger.error(f"Error processing conditional content in paragraph: {e}")
            # Don't let this break the paragraph processing
            # Just log the error and continue
    
    def replace_variables_in_table(self, table, variables: Dict[str, str]) -> None:
        """
        Replace template variables in a table while preserving formatting.
        
        Args:
            table: docx table object
            variables: Dictionary of variable name -> value mappings
        """
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.replace_variables_in_paragraph(paragraph, variables)
    
    def process_template(self, model: str, variables: Dict[str, Any]) -> Optional[Any]:
        """
        Process a Word template by replacing all template variables.
        
        Args:
            model: Model name
            variables: Dictionary of template variables
            
        Returns:
            Processed Document object, or None if template not found
        """
        template_path = self.get_template_path(model)
        if not template_path:
            logger.error(f"Template not found for model: {model}")
            return None
        
        try:
            logger.info(f"Processing template: {template_path}")
            logger.info(f"Template variables: {list(variables.keys())}")
            
            # Load the template document
            doc = Document(str(template_path))
            logger.info(f"Template loaded successfully, {len(doc.paragraphs)} paragraphs")
            
            # Convert all values to strings
            str_variables = {k: str(v) if v is not None else "" for k, v in variables.items()}
            
            # Process conditional content first (before regular variable replacement)
            print("DEBUG: Processing conditional content...")
            logger.info("Processing conditional content...")
            print(f"DEBUG: Template variables keys: {list(str_variables.keys())}")
            logger.info(f"Template variables keys: {list(str_variables.keys())}")
            if 'option_codes' in str_variables:
                print(f"DEBUG: Option codes found in variables: {str_variables['option_codes']}")
                logger.info(f"Option codes found in variables: {str_variables['option_codes']}")
            else:
                print("DEBUG: No option_codes found in variables!")
                logger.warning("No option_codes found in variables!")
            
            self._process_conditional_content_document(doc, str_variables, model)
            print("DEBUG: Conditional content processing completed")
            logger.info("Conditional content processing completed")
            
            # Process all paragraphs
            logger.info("Processing regular template variables...")
            for paragraph in doc.paragraphs:
                self.replace_variables_in_paragraph(paragraph, str_variables)
            
            # Process all tables
            for table in doc.tables:
                self.replace_variables_in_table(table, str_variables)
            
            # Process headers and footers
            for section in doc.sections:
                header = section.header
                for paragraph in header.paragraphs:
                    self.replace_variables_in_paragraph(paragraph, str_variables)
                
                footer = section.footer
                for paragraph in footer.paragraphs:
                    self.replace_variables_in_paragraph(paragraph, str_variables)
            
            logger.info("Template processing completed successfully")
            return doc
            
        except Exception as e:
            logger.error(f"Error processing template {template_path}: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def save_document(self, doc: Any, output_path: str) -> bool:
        """
        Save a processed document to a file.
        
        Args:
            doc: Document object to save
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            doc.save(output_path)
            return True
        except Exception as e:
            logger.error(f"Error saving document to {output_path}: {e}")
            return False

def _format_fraction(size_str: str) -> str:
    """
    Convert regular fractions to Unicode fractions for better display.
    
    Args:
        size_str: Size string like "3/4"", "1/2"", "1""
        
    Returns:
        Formatted size string with Unicode fractions
    """
    if not size_str:
        return size_str
    
    # Remove quotes for processing
    clean_size = size_str.replace('"', '').replace("'", '')
    
    # Convert common fractions to Unicode
    fraction_map = {
        '1/2': '½',
        '1/4': '¼',
        '3/4': '¾',
        '1/8': '⅛',
        '3/8': '⅜',
        '5/8': '⅝',
        '7/8': '⅞',
        '1/3': '⅓',
        '2/3': '⅔',
        '1/5': '⅕',
        '2/5': '⅖',
        '3/5': '⅗',
        '4/5': '⅘',
        '1/6': '⅙',
        '5/6': '⅚'
    }
    
    # Check if it's a fraction we can convert
    if clean_size in fraction_map:
        return fraction_map[clean_size] + '"'
    
    # Return original with quotes restored
    return size_str

def _format_probe_length(probe_length: str) -> str:
    """
    Format probe length to not show decimals for whole numbers.
    
    Args:
        probe_length: Probe length as string (e.g., "10.0", "12", "22.5")
        
    Returns:
        Formatted probe length (e.g., "10", "12", "22.5")
    """
    try:
        length_float = float(probe_length)
        # If it's a whole number, return as integer string
        if length_float == int(length_float):
            return str(int(length_float))
        else:
            return str(length_float)
    except (ValueError, TypeError):
        return str(probe_length)

def _parse_insulator_for_template(kwargs: Dict[str, Any]) -> Dict[str, str]:
    """
    Parse insulator information into granular template variables.
    
    Args:
        kwargs: Dictionary containing insulator data
        
    Returns:
        Dictionary with parsed insulator variables for templates
    """
    import re
    
    # Check if there's a custom insulator specified in the part number
    insulator_display = kwargs.get('insulator', '')
    max_temp = kwargs.get('max_temperature', '450°F')
    
    # Parse material name and length from insulator display string
    # Format examples: "8.0\" Teflon", "4.0\" UHMWPE (Base: 4.0\")"
    material = 'UHMWPE'  # Default
    length_num = 4.0     # Default
    
    if insulator_display and '"' in insulator_display:
        # Extract length and material from strings like "8.0\" Teflon" or "4.0\" UHMWPE (Base: 4.0\")"
        
        # First, extract the length (number before the first quote)
        length_match = re.search(r'(\d+(?:\.\d+)?)"', insulator_display)
        if length_match:
            length_num = float(length_match.group(1))
        
        # Then extract the material name (text after the quote, before any parentheses)
        material_match = re.search(r'"\s*([^(]+?)(?:\s*\(|$)', insulator_display)
        if material_match:
            material = material_match.group(1).strip()
        else:
            # Fallback: try to extract material from the whole string
            parts = insulator_display.split('"')
            if len(parts) > 1:
                material_part = parts[1].strip()
                # Remove any base length information in parentheses
                if '(' in material_part:
                    material_part = material_part.split('(')[0].strip()
                material = material_part
    
    # If no custom insulator, use the default insulator_material and insulator_length
    if not insulator_display:
        insulator_material = kwargs.get('insulator_material', 'UHMWPE')
        insulator_length_raw = kwargs.get('insulator_length', '4"')
        
        # Parse material name (remove any extra formatting)
        material = insulator_material.strip()
        
        # Parse length (extract number from strings like "4\"" or "4 inches")
        length_match = re.search(r'(\d+(?:\.\d+)?)', str(insulator_length_raw))
        length_num = float(length_match.group(1)) if length_match else 4.0
    
    # Format length string
    length_str = str(int(length_num)) if length_num == int(length_num) else str(length_num)
    
    # Determine if "Long" should be included (4" or more)
    long_text = "Long" if length_num >= 4.0 else ""
    
    # Parse temperature rating (extract number from strings like "450°F" or "180 F")
    temp_match = re.search(r'(\d+)', str(max_temp))
    temp_rating = temp_match.group(1) if temp_match else "450"
    
    return {
        'material': material,
        'length': length_str + '"',
        'long_text': long_text,
        'temp_rating': temp_rating
    }

def generate_word_quote(
    model: str,
    customer_name: str,
    attention_name: str,
    quote_number: str,
    part_number: str,
    unit_price: str,
    supply_voltage: str,
    probe_length: str,
    output_path: str,
    **kwargs
) -> bool:
    """
    Generate a quote document using Word templates with template variables.
    
    Args:
        model: Model name
        customer_name: Customer company name
        attention_name: Contact person name
        quote_number: Quote number
        part_number: Full part number
        unit_price: Unit price
        supply_voltage: Supply voltage
        probe_length: Probe length in inches
        output_path: Output file path
        **kwargs: Additional template variables
        
    Returns:
        True if successful, False otherwise
    """
    if not DOCX_AVAILABLE:
        logger.error("python-docx not available")
        return False
    
    try:
        # Create template processor
        processor = WordTemplateProcessor()
        
        # Parse insulator information for granular template variables
        insulator_vars = _parse_insulator_for_template(kwargs)
        
        # Prepare template variables
        variables = {
            # Header information
            'date': datetime.now().strftime("%B %d, %Y"),
            'customer_name': customer_name,
            'company_name': customer_name,  # Alternative name
            'attention_name': attention_name,
            'contact_name': attention_name,  # Alternative name
            'quote_number': quote_number,
            
            # Product information
            'part_number': part_number,
            'quantity': kwargs.get('quantity', "1"),
            'unit_price': unit_price,
            'price': unit_price,  # Alternative name
            'supply_voltage': supply_voltage,
            'voltage': supply_voltage,  # Alternative name
            'probe_length': probe_length,
            'length': probe_length,  # Alternative name
            
            # Technical specifications
            'process_connection_size': kwargs.get('process_connection_size', '¾"'),
            'pc_type': kwargs.get('pc_type', 'NPT'),
            'pc_size': _format_fraction(kwargs.get('pc_size', '¾"')),
            'pc_matt': kwargs.get('pc_matt', 'SS'),
            'pc_rate': kwargs.get('pc_rate'),
            'insulator_material': kwargs.get('insulator_material', 'UHMPE'),
            'insulator_length': kwargs.get('insulator_length', '4"'),
            'probe_material': kwargs.get('probe_material', '316SS'),
            'probe_diameter': kwargs.get('probe_diameter', '½"'),
            'max_temperature': kwargs.get('max_temperature', '450°F'),
            'max_pressure': kwargs.get('max_pressure', '300 PSI'),
            
            # Length pricing information
            'length_adder': kwargs.get('length_adder', 0.0),
            'adder_per': kwargs.get('adder_per', 'none'),
            
            # Enhanced insulator template variables
            'ins_material': insulator_vars['material'],
            'ins_length': insulator_vars['length'], 
            'ins_long': insulator_vars['long_text'],
            'ins_temp': insulator_vars['temp_rating'],
            
            # Enhanced probe template variables  
            'probe_size': kwargs.get('probe_diameter', '½"').replace('"', '').replace("'", ''),
            'probe_material': kwargs.get('probe_material_name', kwargs.get('probe_material', '316SS')),
            'probe_length': _format_probe_length(probe_length),
            
            # Output specifications
            'output_type': kwargs.get('output_type', '10 Amp SPDT Relay'),
            
            # Company information (use employee info if provided, otherwise use defaults)
            'company_contact': kwargs.get('employee_name', 'John Nicholosi'),
            'company_phone': kwargs.get('employee_phone', '(713) 467-4438'),
            'company_email': kwargs.get('employee_email', 'John@babbitt.us'),
            'company_website': 'www.babbittinternational.com',
            
            # Employee information (for templates that use these specific variables)
            'employee_name': kwargs.get('employee_name', 'John Nicholosi'),
            'employee_phone': kwargs.get('employee_phone', '(713) 467-4438'),
            'employee_email': kwargs.get('employee_email', 'John@babbitt.us'),
            
            # Terms and conditions
            'delivery_terms': 'NET 30 W.A.C.',
            'fob_terms': 'FOB, Houston, TX',
            'quote_validity': '30 days'
        }
        
        # Add any additional variables from kwargs
        variables.update(kwargs)
        
        # Process the template
        doc = processor.process_template(model, variables)
        if not doc:
            logger.error(f"Failed to process template for model: {model}")
            return False
        
        # Save the document
        success = processor.save_document(doc, output_path)
        if success:
            logger.info(f"Quote generated successfully: {output_path}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error generating quote: {e}")
        return False

# Test function
def test_template_processing():
    """Test the Word template processing with sample data."""
    if not DOCX_AVAILABLE:
        print("❌ python-docx not available")
        return False
    
    test_success = generate_word_quote(
        model="LS2000S",
        customer_name="ACME Industrial Solutions",
        attention_name="John Smith, P.E.",
        quote_number="Q-2024-TEST-001",
        part_number="LS2000-115VAC-S-12",
        unit_price="1,250.00",
        supply_voltage="115VAC",
        probe_length="12",
        output_path="test_word_quote.docx",
        insulator_material="Teflon",
        probe_material="316SS",
        max_temperature="450°F"
    )
    
    if test_success:
        print("✓ Test quote generated successfully!")
        return True
    else:
        print("❌ Test quote generation failed")
        return False

if __name__ == "__main__":
    test_template_processing() 