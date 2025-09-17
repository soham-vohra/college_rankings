def validate_major_choice(choice, majors):
    """Validate user's major selection choice."""
    return {'valid': choice in majors, 'message': 'Please enter a number between 1-12'} if choice not in majors else {'valid': True, 'message': 'Valid major selected'}

def validate_budget_input(budget_input):
    """Validate and clean user's budget input."""
    cleaned = budget_input.replace(',', '').replace('$', '').strip()
    
    if not cleaned:
        return {'valid': False, 'budget': None, 'message': 'Please enter a budget amount'}
    
    try:
        budget = int(cleaned)
        if budget <= 0:
            return {'valid': False, 'budget': None, 'message': 'Please enter a positive number'}
        if budget < 1000:
            return {'valid': False, 'budget': None, 'message': 'Budget too low. Enter at least $1,000'}
        return {'valid': True, 'budget': budget, 'message': 'Valid budget entered'}
    except ValueError:
        return {'valid': False, 'budget': None, 'message': 'Please enter a valid number (e.g., 25000)'}