Architecture Overview
Design Philosophy
We built this project with simplicity and maintainability as core principles. The architecture separates concerns into three focused modules while keeping the overall codebase minimal and easy to understand.

Module Structure
src/
├── scraper.py      # Main application logic and web scraping
├── validators.py   # Input validation and data cleaning  
├── transformers.py # Data formatting and display logic
scraper.py - Core Logic
Contains the main application flow and Selenium-based web scraping. We chose Selenium over lighter alternatives because the target website loads college data dynamically with JavaScript. The scraper handles both element-based extraction and fallback regex parsing when the primary method fails.

Key decisions:

8-second wait time balances data reliability with respectful server usage
Headless Chrome for performance and deployment flexibility
Multiple extraction strategies since college ranking sites frequently change their HTML structure
validators.py - Input Handling
Handles user input validation with minimal but essential checks. We kept this lightweight since over-validation would hurt user experience.

Design choices:

Basic range checking (minimum $1,000 budget) to catch obvious input errors
String cleaning for common input variations ($, commas)
Simple error messages that guide users without being patronizing
transformers.py - Display Logic
Manages data categorization and visual output formatting. The visual progress bars and price categorization make cost comparison intuitive without requiring complex charting libraries.

Technical approach:

Price categorization based on budget percentages (50%, 80% thresholds)
ASCII progress bars for universal terminal compatibility
Compact summary statistics that highlight key decision factors
Technology Choices
Selenium WebDriver: Necessary for JavaScript-heavy college ranking sites. The overhead is worth it for reliable data extraction.

Minimal Dependencies: Only selenium and built-in Python libraries. Keeps installation simple and reduces security surface area.

No Database: College data changes frequently enough that caching wouldn't provide significant value. Fresh scraping ensures current information.

Performance and Error Handling
The 8-second delay between requests is intentionally conservative. We tested faster intervals but found them unreliable for consistent data extraction. The trade-off favors reliability over speed since users typically run this tool once per search session.

We implemented graceful degradation rather than strict error handling. If the primary extraction method fails, the tool attempts regex-based fallback parsing. This acknowledges that web scraping is inherently fragile - better to give users some results than to fail completely when websites change their structure.

Future Considerations
The modular structure makes it straightforward to add new data sources or modify the display format. The biggest architectural risk is dependency on external website structure, which we've mitigated with multiple extraction methods.