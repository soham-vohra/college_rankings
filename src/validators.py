def validate_major_choice(choice, majors):
    """
    Validate user's major selection against available options.
    
    Args:
        choice (str): User input (should be a number 1-12)
        majors (dict): Available major options with keys '1'-'12'
        
    Returns:
        dict: Validation result with 'valid' boolean and 'message' string
    """
    # Simple validation: check if choice exists in majors dictionary
    return {'valid': choice in majors, 'message': 'Please enter a number between 1-12'} if choice not in majors else {'valid': True, 'message': 'Valid major selected'}

def validate_budget_input(budget_input):
    """
    Validate and sanitize user's budget input with comprehensive error checking.
    
    Handles common input formats like "$25,000", "25000", "25,000" and validates
    that the budget is reasonable for college costs.
    
    Args:
        budget_input (str): Raw user input for budget
        
    Returns:
        dict: Contains 'valid' boolean, 'budget' int (if valid), and 'message' string
    """
    # Remove common formatting characters that users might include
    cleaned = budget_input.replace(',', '').replace('$', '').strip()
    
    # Check for empty input after cleaning
    if not cleaned:
        return {'valid': False, 'budget': None, 'message': 'Please enter a budget amount'}
    
    try:
        # Attempt to convert cleaned string to integer
        budget = int(cleaned)
        
        # Validate budget is positive (negative budgets don't make sense)
        if budget <= 0:
            return {'valid': False, 'budget': None, 'message': 'Please enter a positive number'}
        
        # Enforce minimum budget to catch unrealistic low values
        if budget < 1000:
            return {'valid': False, 'budget': None, 'message': 'Budget too low. Enter at least $1,000'}
        
        # All validations passed
        return {'valid': True, 'budget': budget, 'message': 'Valid budget entered'}
        
    except ValueError:
        # Handle non-numeric input (letters, symbols, etc.)
        return {'valid': False, 'budget': None, 'message': 'Please enter a valid number (e.g., 25000)'}