import csv
from datetime import datetime

def format_college_data(colleges, budget):
    """
    Format and sort college data by price, filtering out colleges over budget.
    
    This function takes raw college data and prepares it for display by:
    1. Filtering out colleges without price data
    2. Removing colleges that exceed the user's budget
    3. Sorting remaining colleges by price (cheapest first)
    
    Args:
        colleges (list): List of college dictionaries with 'name' and 'price' keys
        budget (int): Maximum budget in dollars
        
    Returns:
        list: Sorted list of colleges within budget, ordered by price ascending
    """
    return sorted([c for c in colleges if c['price'] and c['price'] <= budget], key=lambda x: x['price'])

def categorize_by_price(colleges, budget):
    """
    Split colleges into three price tiers based on percentage of user's budget.
    
    Categories are designed to help students understand value:
    - Bargain: Under 50% of budget (great deals)
    - Affordable: 50-80% of budget (reasonable options)
    - Premium: 80%+ of budget (expensive but within reach)
    
    Args:
        colleges (list): List of college dictionaries with price data
        budget (int): User's maximum budget in dollars
        
    Returns:
        dict: Three lists of colleges categorized by price tier
    """
    return {
        'bargain': [c for c in colleges if c['price'] < budget * 0.5],      # Under 50% of budget
        'affordable': [c for c in colleges if budget * 0.5 <= c['price'] < budget * 0.8],  # 50-80% of budget
        'premium': [c for c in colleges if c['price'] >= budget * 0.8]      # 80%+ of budget
    }

def format_results_display(categories, major, budget, all_colleges):
    """
    Display categorized college results with visual progress bars and summary statistics.
    
    Creates a user-friendly console output that shows:
    - Header with major and budget information
    - Three categories of colleges with visual cost indicators
    - Progress bars showing cost relative to budget
    - Summary statistics for decision-making
    
    Args:
        categories (dict): Colleges organized by price category (bargain/affordable/premium)
        major (str): Selected academic major (used in header)
        budget (int): User's budget for display formatting
        all_colleges (list): Complete list of colleges for summary calculations
    """
    print(f"\n🏆 TOP {major.replace('-', ' ').upper()} COLLEGES UNDER ${budget:,}")
    print("═" * 70)
    
    # Early return if no colleges found within budget
    if not any(categories.values()):
        print("No colleges found within budget")
        return
    
    # Display each price category with visual indicators
    for key, (emoji, title) in [
        ('bargain', ('🔥', 'BARGAIN (Under 50% of budget)')),
        ('affordable', ('💚', 'AFFORDABLE (50-80% of budget)')),
        ('premium', ('💎', 'PREMIUM (80%+ of budget)'))
    ]:
        if categories[key]:  # Only show categories that have colleges
            print(f"\n{emoji} {title}")
            print("-" * 50)
            
            for i, college in enumerate(categories[key], 1):
                price = college['price']
                percentage = (price / budget) * 100
                
                # Create visual progress bar (20 characters total)
                bar_length = int((price / budget) * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                
                # Truncate long college names for consistent formatting
                name = college['name'][:35] + "..." if len(college['name']) > 35 else college['name']
                
                # Display: rank, name (38 chars), price (8 chars), progress bar, percentage
                print(f"{i:2d}. {name:<38} ${price:<8,} {bar} ({percentage:.0f}%)")
    
    # Display summary statistics to help with decision-making
    if all_colleges:
        avg_price = sum(c['price'] for c in all_colleges) / len(all_colleges)
        print(f"\n{'='*70}")
        print(f"📊 SUMMARY:")
        print(f"• {len(all_colleges)} colleges within ${budget:,} budget")
        print(f"• Average cost: ${avg_price:,.0f}")
        print(f"• Cheapest: {all_colleges[0]['name']} (${all_colleges[0]['price']:,})")
        print(f"• Most expensive: {all_colleges[-1]['name']} (${all_colleges[-1]['price']:,})")
        print("=" * 70)

def export_to_csv(colleges, major, budget, filename=None):
    """
    Export college search results to a CSV file for further analysis or sharing.
    
    Creates a comprehensive CSV file with all relevant data points:
    - College names and costs
    - Budget analysis (within budget, percentage of budget)
    - Category classification for easy filtering
    - Handles missing price data gracefully
    
    Args:
        colleges (list): List of college dictionaries to export
        major (str): Academic major (used in filename)
        budget (int): User's budget (used in filename and calculations)
        filename (str, optional): Custom filename. If None, auto-generates timestamped name
        
    Returns:
        str: Filename of created CSV file, or None if export failed
    """
    # Generate timestamped filename if none provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"college_search_{major}_{budget}_{timestamp}.csv"
    
    try:
        # Use UTF-8 encoding to handle special characters in college names
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define CSV column headers for clear data organization
            fieldnames = ['College Name', 'Annual Cost', 'Within Budget', 'Budget Percentage', 'Category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # Process each college and add calculated fields
            for college in colleges:
                price = college.get('price')
                
                # Calculate budget analysis fields, handling missing price data
                within_budget = price <= budget if price else 'Unknown'
                budget_percentage = f"{(price/budget)*100:.1f}%" if price else 'Unknown'
                
                # Classify college into category based on price tier
                if not price:
                    category = 'Unknown Price'
                elif price > budget:
                    category = 'Over Budget'  # Shouldn't happen due to filtering, but defensive programming
                elif price < budget * 0.5:
                    category = 'Bargain'
                elif price < budget * 0.8:
                    category = 'Affordable'
                else:
                    category = 'Premium'
                
                # Write row with formatted price for readability
                writer.writerow({
                    'College Name': college['name'],
                    'Annual Cost': f"${price:,}" if price else 'Unknown',
                    'Within Budget': within_budget,
                    'Budget Percentage': budget_percentage,
                    'Category': category
                })
        
        print(f"\n📊 Data exported to: {filename}")
        return filename
        
    except Exception as e:
        # Provide helpful error message for debugging
        print(f"Error exporting CSV: {e}")
        return None