def format_college_data(colleges, budget):
    """Format and sort college data."""
    valid = [c for c in colleges if c['price'] and c['price'] <= budget]
    return sorted(valid, key=lambda x: x['price'])

def categorize_by_price(colleges, budget):
    """Split colleges into price categories."""
    return {
        'bargain': [c for c in colleges if c['price'] < budget * 0.5],
        'affordable': [c for c in colleges if budget * 0.5 <= c['price'] < budget * 0.8],
        'premium': [c for c in colleges if c['price'] >= budget * 0.8]
    }

def format_results_display(categories, major, budget, all_colleges):
    """Display categorized results."""
    print(f"\n🏆 TOP {major.replace('-', ' ').upper()} COLLEGES UNDER ${budget:,}")
    print("═" * 70)
    
    if not any(categories.values()):
        print("No colleges found within budget")
        return
    
    # Show each category
    for key, (emoji, title) in [
        ('bargain', ('🔥', 'BARGAIN (Under 50% of budget)')),
        ('affordable', ('💚', 'AFFORDABLE (50-80% of budget)')),
        ('premium', ('💎', 'PREMIUM (80%+ of budget)'))
    ]:
        if categories[key]:
            print(f"\n{emoji} {title}")
            print("-" * 50)
            
            for i, college in enumerate(categories[key], 1):
                price = college['price']
                percentage = (price / budget) * 100
                bar_length = int((price / budget) * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                name = college['name'][:35] + "..." if len(college['name']) > 35 else college['name']
                
                print(f"{i:2d}. {name:<38} ${price:<8,} {bar} ({percentage:.0f}%)")
    
    # Summary
    avg_price = sum(c['price'] for c in all_colleges) / len(all_colleges)
    print(f"\n{'='*70}")
    print(f"📊 SUMMARY:")
    print(f"• {len(all_colleges)} colleges within ${budget:,} budget")
    print(f"• Average cost: ${avg_price:,.0f}")
    print(f"• Cheapest: {all_colleges[0]['name']} (${all_colleges[0]['price']:,})")
    print(f"• Most expensive: {all_colleges[-1]['name']} (${all_colleges[-1]['price']:,})")
    print("═" * 70)