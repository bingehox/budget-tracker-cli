# Budget Tracker CLI  

A command-line application for tracking personal income, expenses, and budgets.  
It’s built with Python and uses the [Rich] library for a better-looking terminal interface.  

---

## Overview  
This tool lets you manage personal finances directly from the terminal.  
You can record income, log expenses, set category budgets, and view summaries — all stored locally in CSV files.  

---

## Features  
- **Add Income**: record new income transactions  
- **Add Expenses**: log expenses by category (with optional budget limits)  
- **Update Budget**: change planned budget amounts for expense categories  
- **View Summary**: see totals for income, expenses, balance, savings %, and spending %  
- **Manage Transactions**:  
  - View all transactions  
  - Filter by income or expense  
  - Filter by category  
  - Filter by date or date range  

Data is saved automatically in CSV files so you can track finances over time.  

---

## Installation  

### Open terminal:

 - On windows use **Windows Terminal* or **Powershell* , **Terminal* on MacOs/Linux
   
 **Note** : Avoid using command prompt since it doesn't support some of [Rich] features.

- Navigate to a folder you would like to store the project, Example:
  ```
  cd Desktop
  ```

### Clone the repository:  
```bash
git clone https://github.com/bingehox/budget-tracker-cli.git
cd budget-tracker-cli
```
(Optional but recommended) Create and activate a virtual environment:
```
python -m venv venv
```

 #### On Windows
```
venv\Scripts\activate
```

#### On macOS/Linux
```
source venv/bin/activate
```

## Install dependencies:
```

pip install -r requirements.txt
```


---

## Usage

Run the app:
```

python BudgetTracker.py
```

You’ll see a menu with options to add income, add expenses, update budgets, view summaries, or manage transactions.


---

Data Storage

The app stores data in simple CSV files:

- income_track.csv → income entries

- expense_data.csv → expense entries

- budget_expense_amount.csv → budget limits per category



---

## Categories
These are the allowed Income and Expense Sources. Flexibility is deprived but this is so to allow better user experience, In the future we'll ensure flexibility is handled well.

- **Income sources**: Salary, Business, Freelance, Investments, Gifts, Rental Income, Dividends, Interest, Royalties, Pension, Side Hustle.

- **Expense categories**: Rent, Utilities, Food, Groceries, Transport, Personal use, Entertainment, Shopping, Healthcare, Education, Debt Repayments, Savings & Investments, Donations/Charity, Miscellaneous.


---

## Future Improvements

Some features/improvements I’d like to add later:

- Generate detailed reports (PDF/Excel)

- Visual charts (spending breakdown, trends)

- Intergrate TUI(text-based User Interface


- Cloud backup/sync

- Flexibility



---

License

MIT License
