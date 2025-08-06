def export_quote(self):
    """Export current quote to Word document using unified quote generator"""
    print("=== EXPORT_QUOTE FUNCTION CALLED ===")
    print(f"Quote items: {self.quote_items}")
    
    if not self.quote_items:
        print("No quote items - showing warning")
        messagebox.showwarning("No Quote", "Please add items to the quote first.")
        return
    
    print("✓ Quote items validation passed")
    
    # Validate user is selected
    user_initials = self.get_user_initials()
    print(f"User initials retrieved: '{user_initials}'")
    
    if not user_initials:
        print("❌ No user selected - showing error")
        messagebox.showerror("User Required", 
            "You must select a user before exporting a quote.\n\n"
            "This is required for quote number generation and tracking.")
        return
    
    print(f"✓ Initials validation passed: '{user_initials}'")
    
    # Generate quote number if not already generated
    if not self.current_quote_number:
        print("Generating new quote number...")
        if not self.generate_new_quote_number():
            print("❌ Quote number generation failed")
            return  # Failed to generate quote number
    
    print(f"✓ Quote number available: {self.current_quote_number}")
    
    try:
        # Use quote number as default filename
        default_filename = f"{self.current_quote_number}.docx"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")],
            title="Export Quote",
            initialfile=default_filename
        )
        
        if filename:
            print(f"Export filename selected: {filename}")
            
            # Try to use unified quote generator for both single and multi-item export
            success = False
            main_items = [item for item in self.quote_items if item.get('type') == 'main']
            
            if main_items:
                # Get customer information
                customer_name = self.company_var.get() or "Customer Name"
                contact_name = self.contact_person_var.get() or "Contact Person"
                
                # Get employee information for template
                employee_name = ""
                employee_phone = ""
                employee_email = ""
                if hasattr(self, 'selected_employee_info') and self.selected_employee_info:
                    emp = self.selected_employee_info
                    employee_name = f"{emp['first_name']} {emp['last_name']}"
                    employee_phone = emp.get('work_phone', '')
                    employee_email = emp.get('work_email', '')
                    print(f"🔧 Using employee: {employee_name} ({employee_phone}, {employee_email})")
                else:
                    print("⚠ No employee selected, using default contact info")
                
                # Use the generated quote number (guaranteed to exist at this point)
                assert self.current_quote_number is not None
                quote_number = self.current_quote_number
                
                # Use unified quote generator for both single and multi-item quotes
                print(f"🚀 Unified quote export with {len(self.quote_items)} items")
                
                try:
                    from export.unified_quote_generator import generate_unified_quote
                    
                    # Prepare employee info
                    employee_info = {
                        'name': employee_name,
                        'phone': employee_phone,
                        'email': employee_email
                    }
                    
                    success = generate_unified_quote(
                        quote_items=self.quote_items,
                        customer_name=customer_name,
                        attention_name=contact_name,
                        quote_number=quote_number,
                        output_path=filename,
                        employee_info=employee_info,
                        lead_time=self.lead_time_var.get()
                    )
                    print(f"✅ Unified quote export success: {success}")
                    
                except Exception as e:
                    print(f"❌ Unified quote export failed: {e}")
                    import traceback
                    traceback.print_exc()
                    
                    # Fallback to old system if unified fails
                    is_multi_item = len(self.quote_items) > 1
                    if is_multi_item:
                        print("🔄 Falling back to composed multi-item export...")
                        try:
                            from export.word_template_processor import generate_composed_multi_item_quote
                            
                            employee_info = {
                                'name': employee_name,
                                'phone': employee_phone,
                                'email': employee_email
                            }
                            
                            success = generate_composed_multi_item_quote(
                                quote_items=self.quote_items,
                                customer_name=customer_name,
                                attention_name=contact_name,
                                quote_number=quote_number,
                                output_path=filename,
                                employee_info=employee_info,
                                lead_time=self.lead_time_var.get()
                            )
                            print(f"✅ Fallback multi-item export success: {success}")
                            
                        except Exception as fallback_e:
                            print(f"❌ Fallback multi-item export also failed: {fallback_e}")
                            success = False
                    else:
                        # For single items, try the old single-item export as fallback
                        print("🔄 Falling back to single-item export...")
                        try:
                            from export.word_template_processor import generate_word_quote
                            
                            main_item = main_items[0]
                            part_number = main_item.get('part_number', '')
                            quote_data = main_item.get('data', {})
                            
                            model = part_number.split('-')[0] if '-' in part_number else part_number[:6]
                            unit_price = quote_data.get('total_price', 0)
                            unit_price_str = f"{unit_price:.2f}" if unit_price > 0 else "Please Contact"
                            
                            success = generate_word_quote(
                                model=model,
                                customer_name=customer_name,
                                attention_name=contact_name,
                                quote_number=quote_number,
                                part_number=part_number,
                                unit_price=unit_price_str,
                                supply_voltage=quote_data.get('voltage', '115VAC'),
                                probe_length=str(quote_data.get('probe_length', 12)),
                                output_path=filename,
                                employee_name=employee_name,
                                employee_phone=employee_phone,
                                employee_email=employee_email,
                                lead_time=self.lead_time_var.get(),
                                **quote_data
                            )
                            print(f"✅ Fallback single-item export success: {success}")
                            
                        except Exception as fallback_e:
                            print(f"❌ Fallback single-item export also failed: {fallback_e}")
                            success = False
                
                if success:
                    # Save quote to database after successful export
                    try:
                        # Calculate total for database save
                        customer_name = self.company_var.get().strip() or "Customer Name"
                        if self.current_quote_number:
                            if self.db_manager.connect():
                                # At this point current_quote_number is guaranteed to be set
                                assert self.current_quote_number is not None
                                
                                # Calculate total correctly based on item type
                                total_quote_value = 0.0
                                for item in self.quote_items:
                                    if item.get('type') == 'main':
                                        unit_price = item.get('data', {}).get('total_price', 0)
                                    else:  # spare part
                                        unit_price = item.get('data', {}).get('pricing', {}).get('total_price', 0)
                                    quantity = item.get('quantity', 1)
                                    total_quote_value += unit_price * quantity
                                
                                # Save the quote to database
                                self.db_manager.save_quote(
                                    quote_number=self.current_quote_number,
                                    customer_name=customer_name,
                                    customer_email=self.contact_person_var.get().strip(),
                                    quote_items=self.quote_items,
                                    total_price=total_quote_value,
                                    user_initials=self.get_user_initials()
                                )
                                print(f"✅ Quote saved to database: {self.current_quote_number}")
                                self.db_manager.disconnect()
                        
                    except Exception as db_e:
                        print(f"⚠ Database save failed (export still successful): {db_e}")
                        # Don't fail the export if database save fails
                    
                    print("✅ Export completed successfully")
                    self.status_var.set(f"Quote exported successfully: {filename}")
                    messagebox.showinfo("Export Complete", f"Quote exported successfully to:\n{filename}")
                    
                    # Clear the quote after successful export and save
                    self.quote_items.clear()
                    self._refresh_quote_tree()
                    self.current_quote_number = None  # Reset for next quote
                    self.status_var.set("Quote exported and cleared - ready for new quote")
                    
                else:
                    print("❌ Export failed - all methods unsuccessful")
                    self.status_var.set("Export failed")
                    messagebox.showerror("Export Error", "Failed to export quote using all available methods.")
                
            else:
                print("❌ No main items found in quote")
                messagebox.showerror("Export Error", "No main items found in quote.")
                
    except Exception as e:
        print(f"❌ Exception in export_quote: {e}")
        import traceback
        traceback.print_exc()
        self.status_var.set("Export failed")
        messagebox.showerror("Export Error", f"Failed to export quote:\n{str(e)}")