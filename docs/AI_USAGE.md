Here are the prompts I used for GenAI when developing this project. I've printed them here in chronological order:

"I'm looking to create a program in python that asks users for their input on what field of study, and a price cap (per year) using beautifulsoup or selenium to provide a top 10 list of universities for those parameters

https://www.appily.com/colleges/best-colleges/major/ let's see if this is a good site. at the bottom of this page, there is a list of links called "Best colleges by major" with a list of majors sorted A-Z, and clicking this takes you to https://www.appily.com/colleges/best-colleges/major/economics
for example. this is the list of top colleges ranked by popularity for the specific major (in this case economics) with tiles that show the net price and name of the school."
(Pictures of the website for structure context are included)

"Make the program super simple. like extremely simple, but effective. no fluff. try to make every piece of functionality really simple"

"As you can see by reading through the returned string, some type of list of schools is being returned, and it's even filtered by "math". interesting. tell me how i can help you fix this and have the query parse the data and go through as necessary"
(Picture of the data object randomly inputted in one part of the output, that had info to include in other parts of the output)

"As you can see here the, the code works. but but the first result shows the first bit of text on the page. we want to skip that."
(Picture included for context)

"I'm using your code now. what do you think is a good way to display and rank this data on the console? Give me an idea." ... "let's do option 3: the visul price bar combined with option 2 categorized by price range."

"Do you have any ideas on how to spice up the major entry and user input parts of the project? give me an idea or few"

"Can you separate the data validation part for the validation.py file and the data transformation part for the transformers.py file while keeping the majority of the implementation the same. for reference, i can provide you with my file structure:

├── src/
│   ├── scraper.py          # Main scraping logic
│   ├── validators.py       # Data validation rules
│   ├── transformers.py     # Data transformation pipeline"

"How much of the code in the transformers file you gave me is actually needed? condense it to make it as less code as possible to carry out the desired functionality"

"Here was the old validators.py file. given your overall context of the project, condense this code as much as possible to still carry out the desired functionality"


Most of the code in the project was AI-generated.