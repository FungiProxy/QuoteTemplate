"""
RTF Template Processor and Word Document Exporter

This module handles the processing of RTF templates by replacing template variables
with actual data, and can convert the result to Word documents.
"""

import re
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Import the template fields from docs
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docs'))
from template_fileds import QuoteTemplateFields, TEMPLATE_PATTERNS

logger = logging.getLogger(__name__)

class RTFTemplateProcessor:
    """
    Processes RTF templates by replacing placeholders with actual values.
    """
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the RTF template processor.
        
        Args:
            templates_dir: Path to the templates directory
        """
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
        template_name = f"{model}_template.rtf"
        template_path = self.templates_dir / template_name
        
        if template_path.exists():
            return template_path
        
        logger.warning(f"Template not found: {template_path}")
        return None
    
    def load_template(self, model: str) -> Optional[str]:
        """
        Load RTF template content for a given model.
        
        Args:
            model: Model name
            
        Returns:
            RTF template content as string, or None if not found
        """
        template_path = self.get_template_path(model)
        if not template_path:
            return None
            
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading template {template_path}: {e}")
            return None
    
    def replace_basic_fields(self, rtf_content: str, fields: QuoteTemplateFields) -> str:
        """
        Replace basic header fields in RTF content.
        
        Args:
            rtf_content: RTF template content
            fields: Template fields data
            
        Returns:
            RTF content with basic fields replaced
        """
        field_dict = fields.to_dict()
        
        # Replace DATE
        rtf_content = re.sub(r'\bDATE\b', field_dict['DATE'], rtf_content)
        
        # Replace customer name variants
        for pattern in [r'\bCUSTOMER NAME\b', r'\bCUSTOMER\b', r'\bCOMPANY\b']:
            rtf_content = re.sub(pattern, field_dict['CUSTOMER'], rtf_content)
        
        # Replace ATTN field (preserve formatting)
        rtf_content = re.sub(r'(\bATTN:\s*)', f'\\1{field_dict["ATTN"]}', rtf_content)
        
        # Replace Quote number variants
        for pattern in [r'\bQuote #\s*', r'\bQuote#\s*']:
            rtf_content = re.sub(pattern, f'Quote # {field_dict["QUOTE_NUMBER"]}', rtf_content)
        
        return rtf_content
    
    def replace_part_number(self, rtf_content: str, part_number: str) -> str:
        """
        Replace part number patterns in RTF content.
        
        Args:
            rtf_content: RTF template content
            part_number: Actual part number
            
        Returns:
            RTF content with part numbers replaced
        """
        # Define part number patterns from different templates
        patterns = [
            r'FS10000-115VAC-S-xx',
            r'LS2000-XXXX-[HS]-XX"',
            r'LS2100-24VDC-[HS]-XX"',
            r'LS6000-XXXXX-[HS]-XX"',
            r'LS7000/2-XXXXXX-[HS]-XX"',
            r'LS7000-XXXXXX-[HS]-XX"',
            r'LS7500-XXXXXXXX-(?:FP|PR)-XX-150#-(?:FR|PR)',
            r'LS8000/2-(?:XXXXXX|xxx)-[HS]-(?:XX|xx)"',
            r'LS8000-(?:XXXXXX|xxx)-[HS]-(?:XX|xx)"',
            r'LS8500-XXXXXXXX-(?:FP|PR)-XX-150#',
            r'LT9000-XXXX-(?:H|TS)-XX"',
        ]
        
        for pattern in patterns:
            rtf_content = re.sub(pattern, f'{part_number}"', rtf_content, flags=re.IGNORECASE)
        
        return rtf_content
    
    def replace_supply_voltage(self, rtf_content: str, voltage: str) -> str:
        """
        Replace supply voltage patterns in RTF content.
        
        Args:
            rtf_content: RTF template content
            voltage: Supply voltage value
            
        Returns:
            RTF content with supply voltage replaced
        """
        # Pattern to match "Supply Voltage:" followed by blank or placeholder
        pattern = r'(Supply Voltage:\s*)(?:XXXX|xxx|\s*)'
        replacement = f'\\1{voltage}'
        
        return re.sub(pattern, replacement, rtf_content, flags=re.IGNORECASE)
    
    def replace_probe_length(self, rtf_content: str, length: str) -> str:
        """
        Replace probe length patterns in RTF content.
        
        Args:
            rtf_content: RTF template content
            length: Probe length in inches
            
        Returns:
            RTF content with probe lengths replaced
        """
        # Replace various XX" patterns
        patterns = [
            r'x XX"',
            r'xx"',
            r'XX"',
        ]
        
        for pattern in patterns:
            rtf_content = re.sub(pattern, f'{length}"', rtf_content, flags=re.IGNORECASE)
        
        return rtf_content
    
    def replace_price(self, rtf_content: str, price: str) -> str:
        """
        Replace price patterns in RTF content.
        
        Args:
            rtf_content: RTF template content
            price: Unit price
            
        Returns:
            RTF content with prices replaced
        """
        # Replace price patterns
        patterns = [
            r'\$\s+EACH',
            r'\$\s+xxx',
            r'\$\s*EACH',
        ]
        
        for pattern in patterns:
            rtf_content = re.sub(pattern, f'${price} EACH', rtf_content, flags=re.IGNORECASE)
        
        return rtf_content
    
    def process_template(self, model: str, fields: QuoteTemplateFields) -> Optional[str]:
        """
        Process a template by replacing all placeholders with actual values.
        
        Args:
            model: Model name
            fields: Template fields data
            
        Returns:
            Processed RTF content, or None if template not found
        """
        # Load template
        rtf_content = self.load_template(model)
        if not rtf_content:
            return None
        
        # Replace all fields
        rtf_content = self.replace_basic_fields(rtf_content, fields)
        rtf_content = self.replace_part_number(rtf_content, fields.part_number)
        rtf_content = self.replace_supply_voltage(rtf_content, fields.supply_voltage)
        rtf_content = self.replace_probe_length(rtf_content, fields.probe_length)
        rtf_content = self.replace_price(rtf_content, fields.unit_price)
        
        return rtf_content
    
    def save_processed_template(self, processed_content: str, output_path: str) -> bool:
        """
        Save processed RTF content to a file.
        
        Args:
            processed_content: Processed RTF content
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            return True
        except Exception as e:
            logger.error(f"Error saving processed template: {e}")
            return False

class WordDocumentExporter:
    """
    Exports RTF files to Word documents using system tools.
    """
    
    def __init__(self):
        self.rtf_processor = RTFTemplateProcessor()
    
    def convert_rtf_to_docx(self, rtf_path: str, docx_path: str) -> bool:
        """
        Convert RTF file to DOCX using system tools.
        
        Args:
            rtf_path: Path to RTF file
            docx_path: Output DOCX path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Try using LibreOffice if available
            result = subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'docx',
                '--outdir', os.path.dirname(docx_path), rtf_path
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # LibreOffice creates file with same name but .docx extension
                generated_file = os.path.splitext(rtf_path)[0] + '.docx'
                if os.path.exists(generated_file) and generated_file != docx_path:
                    os.rename(generated_file, docx_path)
                return True
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("LibreOffice not available or conversion failed")
        
        try:
            # Try using pandoc if available
            result = subprocess.run([
                'pandoc', rtf_path, '-o', docx_path
            ], capture_output=True, text=True, timeout=30)
            
            return result.returncode == 0
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("Pandoc not available")
        
        logger.error("No RTF to DOCX converter available")
        return False
    
    def generate_quote_document(
        self, 
        model: str, 
        fields: QuoteTemplateFields, 
        output_path: str,
        format: str = 'rtf'
    ) -> bool:
        """
        Generate a complete quote document.
        
        Args:
            model: Model name
            fields: Template fields data
            output_path: Output file path
            format: Output format ('rtf' or 'docx')
            
        Returns:
            True if successful, False otherwise
        """
        # Process the template
        processed_content = self.rtf_processor.process_template(model, fields)
        if not processed_content:
            logger.error(f"Failed to process template for model: {model}")
            return False
        
        if format.lower() == 'rtf':
            # Save as RTF
            return self.rtf_processor.save_processed_template(processed_content, output_path)
        
        elif format.lower() == 'docx':
            # Save as RTF first, then convert to DOCX
            rtf_path = output_path.replace('.docx', '.rtf')
            if not self.rtf_processor.save_processed_template(processed_content, rtf_path):
                return False
            
            success = self.convert_rtf_to_docx(rtf_path, output_path)
            
            # Clean up temporary RTF file
            try:
                os.remove(rtf_path)
            except:
                pass
            
            return success
        
        else:
            logger.error(f"Unsupported output format: {format}")
            return False

# Convenience function for easy usage
def generate_quote(
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
    Generate a quote document with the provided information.
    
    Args:
        model: Model name
        customer_name: Customer company name
        attention_name: Contact person name
        quote_number: Quote number
        part_number: Full part number
        unit_price: Unit price
        supply_voltage: Supply voltage
        probe_length: Probe length
        output_path: Output file path
        **kwargs: Additional template fields
        
    Returns:
        True if successful, False otherwise
    """
    # Create template fields
    fields = QuoteTemplateFields(
        date=datetime.now().strftime("%B %d, %Y"),
        customer_name=customer_name,
        attention_name=attention_name,
        quote_number=quote_number,
        part_number=part_number,
        quantity="1",
        unit_price=unit_price,
        supply_voltage=supply_voltage,
        probe_length=probe_length,
        process_connection_size=kwargs.get('process_connection_size', '¾'),
        insulator_material=kwargs.get('insulator_material', 'Teflon'),
        insulator_length=kwargs.get('insulator_length', '4'),
        probe_material=kwargs.get('probe_material', '316SS'),
        probe_diameter=kwargs.get('probe_diameter', '½'),
        max_temperature=kwargs.get('max_temperature', '450 F'),
        max_pressure=kwargs.get('max_pressure', '300 PSI'),
        **{k: v for k, v in kwargs.items() if k not in [
            'process_connection_size', 'insulator_material', 'insulator_length',
            'probe_material', 'probe_diameter', 'max_temperature', 'max_pressure'
        ]}
    )
    
    # Determine output format from file extension
    format = 'docx' if output_path.lower().endswith('.docx') else 'rtf'
    
    # Generate document
    exporter = WordDocumentExporter()
    return exporter.generate_quote_document(model, fields, output_path, format)