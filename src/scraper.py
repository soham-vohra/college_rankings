from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
from validators import validate_major_choice, validate_budget_input
from transformers import format_college_data, categorize_by_price, format_results_display, export_to_csv

def setup_driver():
    """Initialize Chrome WebDriver with headless options for background operation."""
    options = Options()
    options.add_argument('--headless')  # Run without opening browser window
    return webdriver.Chrome(options=options)

def get_majors():
    """Return mapping of user choices to major slugs and display names."""
    return {
        '1': ('economics', 'Economics'),
        '2': ('computer-science', 'Computer Science'),
        '3': ('business', 'Business'),
        '4': ('engineering', 'Engineering'),
        '5': ('biology-pre-med', 'Biology / Pre-Med'),
        '6': ('math', 'Mathematics'),
        '7': ('english-literature', 'English / Literature'),
        '8': ('political-science', 'Political Science'),
        '9': ('chemistry', 'Chemistry'),
        '10': ('physics', 'Physics'),
        '11': ('history', 'History'),
        '12': ('psychology', 'Psychology')
    }

def get_user_input():
    """Collect and validate user's major choice and budget with interactive prompts."""
    print("\n" + "=" * 60)
    print("🎓 COLLEGE SEARCH TOOL")
    print("=" * 60)
    
    majors = get_majors()
    
    # Display major selection menu
    print("\n📚 SELECT YOUR MAJOR:")
    print("-" * 30)
    
    for num, (slug, name) in majors.items():
        print(f"  {num:2s}. {name}")
    
    print("-" * 30)
    
    # Major selection loop with validation
    while True:
        choice = input("Enter major number (1-12): ").strip()
        validation_result = validate_major_choice(choice, majors)
        
        if validation_result['valid']:
            major_slug, major_name = majors[choice]
            print(f"✓ Selected: {major_name}")
            break
        else:
            print(f"❌ {validation_result['message']}")
    
    print("\n" + "-" * 60)
    
    # Display budget guidance with typical ranges
    print("💰 SET YOUR ANNUAL BUDGET:")
    print("-" * 30)
    print("  Common ranges:")
    print("  • $10,000 - $20,000  (In-state public)")
    print("  • $20,000 - $40,000  (Out-of-state public)")
    print("  • $40,000 - $80,000  (Private colleges)")
    print("-" * 30)
    
    # Budget input loop with validation
    while True:
        budget_input = input("Enter your max annual budget: $").strip()
        validation_result = validate_budget_input(budget_input)
        
        if validation_result['valid']:
            budget = validation_result['budget']
            print(f"✓ Budget set: ${budget:,}")
            break
        else:
            print(f"❌ {validation_result['message']}")
    
    print("\n" + "=" * 60)
    print(f"🔍 Searching for {major_name} programs under ${budget:,}...")
    print("=" * 60)
    
    return major_slug, budget

def scrape_colleges(major):
    """Scrape college data from Appily.com with fallback parsing methods."""
    driver = setup_driver()
    url = f"https://www.appily.com/colleges/best-colleges/major/{major}"
    
    try:
        driver.get(url)
        time.sleep(8)  # Respectful delay to avoid overwhelming servers
        
        colleges = []
        
        try:
            # Primary method: Find college card elements
            elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid*='college'], article, .card")
            
            for element in elements[:15]:  # Limit to 15 results
                try:
                    text = element.text
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    
                    college_name = None
                    price = None
                    
                    # Parse each line for college name and price
                    for line in lines:
                        # Look for university/college names
                        if any(word in line for word in ['University', 'College', 'Institute']) and len(line) > 10:
                            if not college_name:  # Take first match
                                college_name = line
                        
                        # Extract price using regex
                        price_match = re.search(r'\$([0-9,]+)', line)
                        if price_match:
                            try:
                                price = int(price_match.group(1).replace(',', ''))
                            except:
                                pass
                    
                    # Filter out spam/invalid entries
                    if college_name and not any(skip in college_name.lower() for skip in ['appily', 'best colleges', 'department', 'information']):
                        colleges.append({'name': college_name, 'price': price})
                
                except:
                    continue  # Skip problematic elements
        
        except:
            # Fallback method: Parse script tags for JSON data
            page_source = driver.page_source
            json_matches = re.findall(r'<script[^>]*>(.*?)</script>', page_source, re.DOTALL)
            
            for script_content in json_matches:
                try:
                    # Look for college names in JSON structure
                    college_matches = re.findall(r'"name":\s*"([^"]*(?:University|College|Institute)[^"]*)"', script_content)
                    
                    for name in college_matches[:10]:
                        if len(name) > 10:
                            colleges.append({'name': name, 'price': None})
                    
                    if colleges:
                        break
                except:
                    continue
        
        driver.quit()
        return colleges
    
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

def filter_colleges(colleges, budget):
    """Filter colleges to include only those within budget or with unknown pricing."""
    result = []
    for college in colleges:
        # Include colleges with no price data or within budget
        if college['price'] is None or college['price'] <= budget:
            result.append(college)
    return result

def show_results(colleges, major, budget):
    """Display formatted results and offer CSV export option."""
    if not colleges:
        print("No results found")
        return
    
    # Transform data for display
    formatted_colleges = format_college_data(colleges, budget)
    categories = categorize_by_price(formatted_colleges, budget)
    
    # Show categorized results
    format_results_display(categories, major, budget, formatted_colleges)
    
    # Optional CSV export
    export_choice = input("\n💾 Export results to CSV? (y/n): ").strip().lower()
    if export_choice in ['y', 'yes']:
        export_to_csv(colleges, major, budget)

def main():
    """Main program flow: get input, scrape data, filter results, display output."""
    major, budget = get_user_input()
    if not major:  # Exit if user input failed
        return
    
    print(f"\nSearching for {major.replace('-', ' ')}...")
    colleges = scrape_colleges(major)
    filtered = filter_colleges(colleges, budget)
    show_results(filtered, major, budget)

# Entry point
if __name__ == "__main__":
    main()