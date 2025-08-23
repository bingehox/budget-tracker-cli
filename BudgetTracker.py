import os
import csv
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.tree import Tree
from rich.columns import Columns
from rich.table import Table
from collections import defaultdict
from datetime import datetime, date
from time import sleep


#console = Console(force_terminal=True, no_color=True) #Initialize Console
console = Console()

#clear terminal
def clear_sys():
    os .system('cls' if os.name == 'nt' else 'clear')
    #console.clear()
    
#loading MAin Menu
def load_menu():
    with console.status("[bold green]Loading Main Menu") as status:
         sleep(1)
#handles float errors
#def isfloat(value:str) -> bool:
   # try:
      #  float(value)
      #  return True
   # except ValueError:
     #   return False



#Income Track Section
def add_income():
    clear_sys()

    filename = "income_track.csv"
    console.print(Panel("Income Track Section\n0. \\-->", style="green"))
    while True:
        try:
            #allowed income sources
            allowed_inc_src = {
                "Salary",
                "Business",
                "Investments",
                "Freelance",
                "Gifts",
                "Rental Income",
                "Dividends",
                "Interest",
                "Royalties",
                "Pension",
                "Side Hustle"
            }

            inc_src = str(Prompt.ask("[cyan]Enter income source eg.(Salary, Freelance or Gifts)\nor type 'help' to view Available list:\n>>>[/cyan]")).strip()#input income soucre
            #Return to Main Menu
            if inc_src == "0":
                clear_sys()
                return
            #Reject income input if a number is entered
            if inc_src.isdigit():
                raise ValueError("Income Source cannot be a number")
            #Reject if input empty
            if not inc_src:
                raise ValueError("Income Source cannot be empty")
            #Only allow letters and spaces
            if not all(x.isalpha() or x.isspace() for x in inc_src):
                raise ValueError("Income Source can only contain letters or spaces")
            #returns income list from with user can choose from 
            if inc_src == "help":
                console.print(Panel("\n".join(allowed_inc_src), title="Allowed Income Category",width=70))
                #raise ValueError("[green]choose from above list[/green]")
            #Only allow Income from the list
            if inc_src not in allowed_inc_src:
                console.print(Panel("\n".join(allowed_inc_src), title="Allowed Income Sources,Just For Now", width=70))
                raise ValueError("Please choose from the predefined options  Above for better experience.\nWe’re working on making the categories more flexible in the future! ")

            #handle Expense input exceptions
            income_input = (Prompt.ask("[cyan]Enter Expense Amount:\n>>>[/cyan]", default="0"))#input Amount
            if not income_input.replace(".", "", 1).isdigit():#allows decimals
                raise ValueError("Expense Amount can only contain numbers")
            inc_amt = float(income_input)
            break #breaks loop when both input are valid
        
        except ValueError as e:
            console.print(Panel(f"[bold red]{str(e)}[/bold red]\n"),style="bold red", width=70)
            #console.print(Panel("Invalid Value, Try Again"), style="bold red")
            continue

    #Date logic
    while True:

        try:
            date_str = Prompt.ask("[cyan]Enter date in (YY-MM-DD) format or none for default:\n>>>[/cyan]")# date string
            if date_str.strip() =="":
                date_obj = date.today()#Defaults to Current date if left blank
            else:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()#Converts date string to python date object

            break #exit loop if date is valid
        except ValueError:
            console.print(Panel("Invalid Date format! Please Try Again (example:2025-8-16)", style="bold red"))
            continue #repeats when user enters invalid date format


    fields = ['Source', 'Inc_Amount', 'Date']
    csv_income_data = {'Source':inc_src, 'Inc_Amount': inc_amt,'Date': date_obj}

    write_header = not os.path.exists(filename) or os.path.getsize(filename) == 0 #checks if the file name exists and is not empty

    #Saving Income data to a csv file  
    def save_income_info():
        with open(filename, 'a', newline='') as file:
            dict_writer = csv.DictWriter(file, fieldnames=fields)
            if write_header:#writes the header only once 
                dict_writer.writeheader()
            dict_writer.writerow(csv_income_data)
        with console.status("[bold green]Saving...") as status:
            sleep(1)
        console.log("[bold red]DONE!!")   
        console.print(Panel(f"Income data saved to {filename} Successfully", style="green"))

    save_income_info()

    input("\nPress Enter to continue to Main Menu:\n>>>")
    load_menu()
    clear_sys()


#Expense Track Section
def add_expenses():
    clear_sys()

    filename = "expense_data.csv"
    console.print(Panel("Expense Track Section\n0. \\-->", style="green", width=80))

    while True:
        try:

            #Allowed expense category
            allowed_expense_category = {
                "Rent": None,
                "Utilities": None,
                "Food": None,
                "Groceries": None,
                "Transport": None,
                "Personal use": None,
                "Entertainment": None,
                "Shopping": None,
                "Healthcare": None,
                "Education": None,
                "Debt Repayments": None,
                "Savings & Investments": None,
                "Donations/Charity": None,
                "Miscellaneous": None
            }
            
            #Track Planned budget for each Expense Category
            def plan_budget():
                
                filename = "budget_expense_amount.csv"
                if not os.path.exists(filename):#checks if file exists
                    qa_user = Prompt.ask("[cyan]Would you like to set your planned budget limit:(yes/no).\nNOTE: This is a one time process but you can make changes later to the budget\n>>>[/cyan]")
                    if qa_user == "yes":
                        console.print("Provide for each Below:")
                        
                        #loops through each category 
                        for key in allowed_expense_category.keys():
                            while True:
                                user_input = Prompt.ask(f"{key}:")
                                if user_input == "":
                                    allowed_expense_category[key] = None
                                    console.print(f"{key},[cyan]Saved as[/cyan] [yellow]None[/yellow]")
                                    break
                                else:
                                    try:
                                        allowed_expense_category[key] = float(user_input)
                                        break    
                                    except ValueError:
                                        console.print("Wrong Entry, should be numbers only", style="red")
                                        continue
                    #Save Budgets to none when user skips                
                    else:
                        for key in allowed_expense_category.keys():
                            allowed_expense_category[key] = None
                        console.print("[yellow]Budgets saved as None (you can update later)[/yellow]")

                    #save budget data to csv file
                    write_header = not os.path.exists(filename) or os.path.getsize(filename) == 0 #checks if the file name exists and is not empty
                    fields = ['Category', 'Budget']        
                    with open(filename, 'w', newline="") as file:
                        dict_w = csv.DictWriter(file, fieldnames=fields)
                        if write_header:
                            dict_w.writeheader()
                        for cat, amt in allowed_expense_category.items():
                            dict_w.writerow({"Category": cat, "Budget": amt}) 
                        with console.status("[bold green]Saving...") as status:
                            sleep(1)
                        console.log("[bold red]DONE!!")   
                        #console.print(Panel(f"Budget data saved", style="green"))  

                        input("\nPress Enter to continue:\n>>>")
                        clear_sys()
 

            plan_budget()





            #expense section
            category = str(Prompt.ask("[cyan]Enter Expense Category source eg.(Rent, Food or Transport, e.t.c)\n or type 'help' to view Options list:\n>>>[/cyan]")).strip()#input expese soucre
            #Return to Main Menu
            if category == "0":
                clear_sys()
                return 
            #Reject income input if a number is entered
            if category.isdigit():
                raise ValueError(" Expense Category  cannot be a number")
             #Reject if input empty
            if not category:
                raise ValueError("Expense category  cannot be empty")
            #Only allow letters and spaces
            if not all(x.isalpha() or x.isspace() for x in category):
                raise ValueError("Expense category can only contain letters or spaces")
            #returns expense list from with user can choose from 
            if category == "help":
                console.print(Panel("\n".join(allowed_expense_category), title="Allowed Expense Category", width=80))
                raise ValueError("[green]choose from above list[/green]")
            #Only allow expense category from this list
            if category not in allowed_expense_category:
                console.print(Panel("\n".join(allowed_expense_category), title="Allowed Expense Category", width=80))
               # raise ValueError("Please choose from the above predefined options for better user experince.\nWe’ll work on making the categories more flexible in the future!")
            
        

            #handle Expense input exceptions
            expense_input = (Prompt.ask("[cyan]Enter Expense Amount:\n>>>[/cyan]", default="0"))#input Amount
            if not expense_input.replace(".", "", 1).isdigit():#allows decimals
                raise ValueError("Expense Amount can only contain numbers")
            expense_amt = float(expense_input)
            break #breaks loop when both input are valid
        except ValueError as e: # for custom message
            console.print(Panel(f"[bold red]{str(e)}[/bold red]"), style="bold red", width=80)
            #console.print(Panel("Invalid Value, Try Again"), style="bold red")
            continue

    #Date logic
    while True:

        try:
            date_str = Prompt.ask("[cyan]Enter date in (YY-MM-DD) format or none for default:\n>>>[/cyan]")# date string
            if date_str.strip() =="":
                date_obj = date.today()#Defaults to Current date if left blank
            else:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()#Converts date string to python date object

            break #exit loop if date is valid
        except ValueError:
            console.print(Panel("Invalid Date format! Please Try Again (example:2025-8-16)", style="bold red"))
            continue #repeats when user enters invalid date format


    fields = ['Category', 'Expense_Amount', 'Date']
    csv_expense_data = {'Category':category, 'Expense_Amount': expense_amt,'Date': date_obj}

    write_header = not os.path.exists(filename) or os.path.getsize(filename) == 0 #checks if the file name exists and is not empty

    #Saving Expense data to a csv file  
    def save_expense_info():
        with open(filename, 'a', newline='') as file:
            dict_writer = csv.DictWriter(file, fieldnames=fields)
            if write_header:#writes the header only once 
                dict_writer.writeheader()
            dict_writer.writerow(csv_expense_data)
        with console.status("[bold green]Saving...") as status:
            sleep(1)
        console.log("[bold red]DONE!!")   
        console.print(Panel(f"Expense data saved to {filename} Successfully", style="green"))

    save_expense_info()
    
    input("\nPress Enter to continue Main Menu:\n>>>")
    clear_sys()
    load_menu()
#Update Budget Section 
def budget_update():
    clear_sys()
    console.print(Panel("UPDATE BUDGET\n0. \\-->", style="bold blue"))

    allowed_expense_category = {
        "Rent",
        "Utilities",
        "Food",
        "Groceries",
        "Transport",
        "Personal use",
        "Entertainment",
        "Shopping",
        "Healthcare",
        "Education",
        "Debt Repayments",
        "Savings & Investments",
        "Donations/Charity",
        "Miscellaneous"
    }

    while True:
        filename = "budget_expense_amount.csv"
        try:
            mod_budget = Prompt.ask("[cyan]Enter Category Name, (type 'help' for list)\n>>>[/cyan]")
            if mod_budget == "0":
                clear_sys()
                return
            if mod_budget == "help":
                budget_tree = Tree("[bold magenta]Category List[/bold magenta]")
                budget_tree.add("[yellow]Expense[/yellow]")
                for item in allowed_expense_category:
                    budget_tree.add(item)
                console.print(budget_tree, style="cyan")
                continue 

            if mod_budget not in allowed_expense_category:
                console.print(Panel("Enter Exact KeyWord, Type 'help to view list"), width=70, style="bold red") 
                continue  
               
            budget_amt = float(Prompt.ask("[cyan]Enter new Budget Amount\n>>>[/cyan]"))

            #read the budgets into a dictionary list
            data = []
            with open(filename, "r") as file:
                dict_r = csv.DictReader(file)
                for row in dict_r:
                    row["Budget"] = float(row["Budget"]) if row["Budget"] else None
                    #update the matching Category 
                    if row["Category"] == mod_budget:
                        row["Budget"] = budget_amt
                    data.append(row) #updates it in the list

            #Write back to the CSV file
            fields = data[0].keys() #gets header rows from the first dictionary 
            with open(filename, 'w', newline='') as file:
                dict_w = csv.DictWriter(file, fieldnames=fields)
                dict_w.writeheader()
                dict_w.writerows(data)

            console.print(Panel(f"[green]Updated {mod_budget} to {budget_amt} successfully![/green]"),style="green", width=70)
            break   

        except ValueError:
            console.print(Panel("wrong input", width=70, style="bold red"))
            continue  

    input("\nPress Enter to continue Main Menu:\n>>>")
    clear_sys()
    load_menu()
#Summary sectio
def view_summary():
    clear_sys()
    console.print(Panel("Summary View", style= "green"))
    with console.status("[bold green] Fetching data...") as status:
        sleep(2)
    with console.status("[bold green] Getting Totals...") as status:
        sleep(2)

    console.log("[bold red]DONE!!")
    #find total income
    total_income = 0
    filename = "income_track.csv"
    try:
        with open(filename, 'r') as file:
            dict_r =csv.DictReader(file)
            for row in dict_r:
                amount = float(row['Inc_Amount'])
                total_income += amount

    except FileNotFoundError:
        console.print(Panel("No income to view, Try Adding Income"))

    #find total expense and for each category
    filename = "expense_data.csv"
    file_name ="budget_expense_amount.csv"
    total_expense = 0
    #exp_totals = {}
    exp_totals =defaultdict(float)# creates a dictionary to hold per category
    try:
        with open(filename, 'r') as file:
            dict_r =csv.DictReader(file)
            for row in dict_r:
                #total expense
                amount = float(row['Expense_Amount'])
                total_expense += amount
                #total expense for each category
                exp_category = row['Category']
                exp_amount = float(row["Expense_Amount"])
                exp_totals[exp_category] += exp_amount
                
        #read the budget into a dictionary
        dict_budget = {}
        with open(file_name, 'r') as file:
            dict_br = csv.DictReader(file)
            for row in dict_br:
                budget_cat = row["Category"]
                budget_amt = float(row["Budget"]) if row["Budget"] else 0.0
                dict_budget[budget_cat] = budget_amt






    except FileNotFoundError:
        console.print(Panel("No Expense to view, Try Adding Expenses"))


    #calculate balance, spending and savings and Budget status
    balance = total_income - total_expense
    spendings = (total_expense / total_income) * 100 if total_income else 0 #Prevents ZeroDivisionError
    savings = (balance / total_income) * 100 if total_income else 0 #Prevent crashing if income = 0
    #get budget status
    def budget_status(total,budget):
        if total > budget:
            return "[red]Over Limit[/red]"
        elif total == budget:
            return "[yellow]On limit[/yellow]"
        else:
            return "[green]Within Limit[/green]"    
    
    #savings and spending status
    def info_sp():
        if savings < spendings:
            return ("[bold red]Warning[/bold red]")
        else:
            return "✔" #prints empty to avoid printing None
        
    def info_sa():
        if savings > spendings:
            return ("[bold green]:)[/bold green]")
        else:
            return ":("#Prints empty to avoid returning None
        


    table = Table(title="Income and Expense Info", header_style="magenta", border_style="magenta")
    table.add_column("Type", justify="center", header_style="magenta", style="cyan", width=20)
    table.add_column("Amount", justify="center", header_style="magenta", style="cyan", width=20)
    table.add_row("Total Income", f"[bold green]{total_income:.2f}[/bold green]")
    table.add_row("Total Expense", f"[bold red]{total_expense:.2f}[/bold red]")
    table.add_row("Balance", f"[bold cyan]{balance:.2f}[/bold cyan]")

    #prints table for Income and expense Info
    console.print(table)

    #prints savings and spending panel
    panel_savings = (Panel(f"[bold green]{savings:.2f}%[/bold green] saved, {info_sa()}", title="Savings", border_style="magenta", width=40))#panel for savings
    panel_spendings = (Panel(f"[bold red]{spendings:.2f}%[/bold red] spent, {info_sp()}", title="spendings", border_style="magenta", width=40))#panel for spendings
    console.print("\n\nSavings and Spendigs")
    console.print("-" * 50)
    console.print(Columns([panel_savings, panel_spendings]))

    #with console.status("[bold green] Fetching data...") as status:
      #  sleep(2)
    #with console.status("[bold green]Getting Totals...") as status:
       # sleep(1)

    try:
        #loop through each category and sums
        console.print("\n\nExpense Amount Breakdown")
        console.print("-" * 80)
        console.print(f"{'Category':<20} {'Total':>5} {'Budget':>15} {'status':>15} {'%Usage':>15}", style="cyan")

        print("-" * 80)
        for category, total in exp_totals.items():
            budget = dict_budget.get(category, 0)#get the corresponding expense category(one-to-one lookup)
            usage_pct = (total / total_expense) * 100 if total else 0.0
            status = budget_status(total,budget)
            console.print(f"{category:<20} {total:>5.2f} {budget:>13} {status:>30} {usage_pct:>10.0f}%", style="cyan")
    except Exception as e:
        console.print(f"[red]Error while rendering breakdown: {e}[/red]")
         
    console.log("\n[bold red]DONE!!")
    
           
    input("\nPress Enter to continue Main Menu:\n>>>")
    clear_sys()
    load_menu()


def transactions():
    clear_sys()  

    #Transaction menu
    def transaction_menu():
        table_tm = Table.grid(padding=(1, 2))
        table_tm.add_row("[green]OPTIONS[/green]")
        table_tm.add_row("1. View all transactions")
        table_tm.add_row("2. View only Income")
        table_tm.add_row("3. View only Expenses")
        table_tm.add_row("4. View by Category")
        table_tm.add_row("5. View by Date Range")
        table_tm.add_row(" 0. \\->...?")

        console.print(Panel(table_tm, title="TRANSACTION MENU", border_style="magenta", style="cyan", width=70))



        #view all transaction
        def view_all_transactions():
            clear_sys()

            table_t = Table(title="All TRANSACTION", width=70, style="cyan", show_lines=True, box=box.ROUNDED, show_header=True)
            table_t.add_column("Type",header_style="magenta",style="cyan")
            table_t.add_column("Category",header_style="magenta",style="cyan")
            table_t.add_column("Amount", header_style="magenta", style="cyan")
            table_t.add_column("Date", header_style="magenta", style="cyan")
            try:

                filename = "expense_data.csv"
                file_name = "income_track.csv"

                with  open(file_name, 'r') as file:
                    dict_ri = csv.DictReader(file)
                    
                    for row in dict_ri:
                        table_t.add_row("Income", row['Source'], f"[green]{row['Inc_Amount']}[/green]", row['Date'])

                with  open(filename, 'r') as f:
                    dict_re = csv.DictReader(f)                    
                    for row in dict_re:
                        table_t.add_row("Expense", row['Category'], f"[red]{row['Expense_Amount']}[/red]", row['Date'])
                
                console.print(table_t)
            except FileNotFoundError:
                console.print(Panel("No Transactions Found"))

            input("Enter to continue\n>>>")
            clear_sys()
            sleep(0.3)
            console.print(Panel(table_tm, title="TRANSACTION MENU", border_style="magenta", style="cyan", width=70))

            

        #view only income transactions
        def view_only_income():
            clear_sys()

            v_table_i = Table(title="INCOME TRANSACTION", width=70, style="cyan", show_lines=True, show_header=True)
            v_table_i.add_column("Category",header_style="magenta",style="cyan")
            v_table_i.add_column("Amount", header_style="magenta", style="cyan")
            v_table_i.add_column("Date", header_style="magenta", style="cyan")
            try:

                file_name = "income_track.csv"

                with  open(file_name, 'r') as file:
                    dict_ri = csv.DictReader(file)
                    
                    for row in dict_ri:
                        v_table_i.add_row(row['Source'], f"[green]{row['Inc_Amount']}[/green]", row['Date'])

                    console.print(v_table_i)

            except FileNotFoundError:
                console.print(Panel("No Transactions Found"))
            
            input("Enter to continue\n>>>")
            clear_sys()
            sleep(0.3)
            console.print(Panel(table_tm, title="TRANSACTION MENU", border_style="magenta", style="cyan", width=70))
            

        #view only expense transactios
        def view_only_expense():
            clear_sys()

            table_e = Table(title="EXPENSE TRANSACTIONS", width=70, style="cyan", show_lines=True, box=box.ROUNDED, show_header=True)
            table_e.add_column("Category",header_style="magenta",style="cyan")
            table_e.add_column("Amount", header_style="magenta", style="cyan")
            table_e.add_column("Date", header_style="magenta", style="cyan")
            try:

                filename = "expense_data.csv"

                with  open(filename, 'r') as file:
                    dict_ri = csv.DictReader(file)
                    
                    for row in dict_ri:
                        table_e.add_row(row['Category'], f"[red]{row['Expense_Amount']}[/red]", row['Date'])

                console.print(table_e)

            except FileNotFoundError:
                console.print(Panel("No Transactions Found"))


            input("Enter to continue\n>>>")
            
            clear_sys()
            sleep(0.4)
            console.print(Panel(table_tm, title="TRANSACTION MENU", border_style="magenta", style="cyan", width=70))

        

        #view transactions(expense and income) by specific category
        def view_by_category():
            clear_sys()

            allowed_inc_src = {
                "Salary",
                "Business",
                "Investments",
                "Freelance",
                "Gifts",
                "Rental Income",
                "Dividends",
                "Interest",
                "Royalties",
                "Pension",
                "Side Hustle"
            }

            #Allowed expense category
            allowed_expense_category = {
                "Rent",
                "Utilities",
                "Food",
                "Groceries",
                "Transport",
                "Personal use",
                "Entertainment",
                "Shopping",
                "Healthcare",
                "Education",
                "Debt Repayments",
                "Savings & Investments",
                "Donations/Charity",
                "Miscellaneous"
            }

            #console.print(Panel("Filter By Category"))

            tree = Tree("[bold magenta]Transaction Structure[/bold magenta]", guide_style="bright_cyan",)
            income_tree = tree.add("[bold green]Income[/bold green]")
            for income in allowed_inc_src:
                income_tree.add(income)
            expense_tree = tree.add("[bold red]Expense[/bold red]")
            for expense in allowed_expense_category:
                expense_tree.add(expense)

            console.print(tree)

            while True:
                q_user = Prompt.ask("Provide a category key-word you would like to lookup 🔎:\n>>>")

                #check income list for the specified category
                if q_user in allowed_inc_src:
                    table_cat = Table(title=f"{q_user} Category")
                    t_totals_i = Table(show_header=False, box=None)
                    table_cat.add_column("Category")
                    table_cat.add_column("Amount")
                    table_cat.add_column("Date")

                    try:
                        total_i = defaultdict(float)
                        with open("income_track.csv",'r') as file:
                            dict_r = csv.DictReader(file)
                            for row in dict_r:
                                if row['Source'] == q_user:
                                    source = row["Source"]
                                    amount_i = float(row["Inc_Amount"])
                                    total_i[source] += amount_i #Accumulate totals for the category
                                    table_cat.add_row(row['Source'], row['Inc_Amount'], row['Date'])


                        for x, y in total_i.items():
                            #table_cat.add_row("TOTALS:", f"{y:.1f}")
                            t_totals_i.add_row("TOTALS:", f"{y:.1f}")
                            
                        console.print(table_cat)
                        console.print(t_totals_i)
                        break

                    except FileNotFoundError:
                        console.print("No Transactions found")
                        break

                #checks expense list for the specified category
                elif q_user  in allowed_expense_category:

                    table_cat_e = Table(title=f"{q_user} Category")
                    t_totals = Table(show_header=False, box=None)
                    table_cat_e.add_column("Category")
                    table_cat_e.add_column("Amount")
                    table_cat_e.add_column("Date")

                    try:
                        total_e = defaultdict(float)
                        with open("expense_data.csv",'r') as file:
                            dict_r = csv.DictReader(file)
                            for row in dict_r:
                                if row['Category'] == q_user:
                                    #exp_category = row['Category']
                                    #exp_amount = float(row["Expense_Amount"])
                                    #exp_totals[exp_category] += exp_amount
                                    category = row["Category"]
                                    amount = float(row['Expense_Amount'])
                                    total_e[category] += amount #accumulate totals for each category
                                    table_cat_e.add_row(row['Category'], row['Expense_Amount'], row["Date"])
                        
                        for x, y in total_e.items():
                            t_totals.add_row("TOTALS:", f"{y:.2f}")
                        
                    

                        console.print(table_cat_e)
                        console.print(t_totals)
                        break


                    except FileNotFoundError:
                        console.print("No Transactions found")
                        break
                        
                else:
                    console.print("[red]Invalid key-word[/red]")
                    continue




            input("\nEnter to continue\n>>>")
            clear_sys()
            sleep(0.3)
            console.print(Panel(table_tm, title="TRANSACTION MENU", border_style="magenta", style="cyan", width=70))

            

        #view by date range()
        def view_by_date():
            clear_sys()

            console.print(Panel("View by Date/Date Range"), width=70, style="magenta")
            console.print("[magenta]1.View by Single Date[/magenta]", style="magenta")
            console.print("[magenta]2.View by Date Range[/magenta]", style="magenta")

            option_d = int(Prompt.ask("[cyan]Choose an Option[/cyan]:\n>>>"))

            #view by singe Date
            if option_d == 1:
                while True:
                    try:
                        date_e = Prompt.ask("[cyan]Enter date in (YY-MM-DD) format or none for default:\n>>>[/cyan]")# date string
                        if date_e.strip() =="":
                            date_obj = date.today()#Defaults to Current date if left blank
                        else:
                            date_obj = datetime.strptime(date_e, "%Y-%m-%d").date()#Converts date string to python date object

                        break #exit loop if date is valid
                    except ValueError:
                        console.print(Panel("Invalid Date format! Please Try Again (example:2025-8-16)"), style="bold red")
                        continue #repeats when user enters invalid date format

                try:
                    table_d_e = Table(title="Date Category", border_style="cyan")
                    table_d_e.add_column("Category", style="cyan", header_style="magenta")
                    table_d_e.add_column("Amount", style="red", header_style="magenta")
                    table_d_e.add_column("Date", style="cyan", header_style="magenta")
                    with open("expense_data.csv", 'r') as file:
                        dict_r = csv.DictReader(file)
                        for row in dict_r:
                            date_row = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                            if date_obj == date_row:
                                table_d_e.add_row(row['Category'], row['Expense_Amount'], row['Date'])

                    console.print(table_d_e)

                        

                except FileNotFoundError:
                    console.print("No data Found, Try adding New Ones")

            #view by Date Range
            elif option_d == 2:
                while True:
                    try:
                        console.print("Use YYYY-mm-dd format", style = "magenta")
                        date1 = Prompt.ask("[cyan]Enter Start date:[/cyan]")
                        date2 = Prompt.ask("[cyan]Enter End date:[/cyan]")
                        
                        if not date1:
                            date_obj1 = date.today()
                        else:
                            date_obj1 = datetime.strptime(date1, "%Y-%m-%d").date()

                        if not date2:
                            date_obj2 = date.today()
                        else:
                            date_obj2 = datetime.strptime(date2, "%Y-%m-%d").date()
                            
                            
                        break #exit loop if date is valid
                    except ValueError:
                        console.print(Panel("Invalid Date format! Please Try Again (example:2025-8-16)"), style="bold red")
                        continue #repeats when user enters invalid date format

                    

                try:
                    table_date_range = Table(title="Date Category")
                    table_date_range.add_column("Category", style="cyan", header_style="magenta")
                    table_date_range.add_column("Amount", style="red", header_style="magenta")
                    table_date_range.add_column("Date", style="cyan", header_style="magenta")
                    with open("expense_data.csv", 'r') as file:
                        dict_r = csv.DictReader(file)
                        for row in dict_r:
                            date_row = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                            if date_obj1 <= date_row <= date_obj2:
                                table_date_range.add_row(row['Category'], row['Expense_Amount'], row['Date'])
                            
                            

                    console.print(table_date_range)

                        

                except FileNotFoundError:
                    console.print("No data Found, Try adding New Ones")

                

            input("\nEnter to continue\n>>>")
            clear_sys()
            sleep(0.3)
            console.print(Panel(table_tm, title="TRANSACTION MENU", border_style="magenta", style="cyan", width=70))


        def exit():
            clear_sys()
            load_menu()


        #logic flow section

        while True:

            try:
                option = int(Prompt.ask("[cyan]Choose an Option[/cyan]"))

                #return to main menu
                if option == 0:
                    #with console.status("[green]loading...[/green]") as status:
                        #sleep(2)
                    exit()#exit to mainmenu
                    break
                #view all transaction
                elif option == 1:
                    view_all_transactions()

                #view Income only
                elif option == 2:
                    view_only_income()

                #view only expense
                elif option == 3:
                    view_only_expense()
                
                #view by category
                elif option == 4:
                    view_by_category()

                #view by Date
                elif option == 5:
                    view_by_date()

                elif option < 0 or option > 5:
                    console.print(Panel("INVALID OPTION, TRY AGAIN", width=70, style="red"))
                    sleep(0.3)
                    continue    


            
            #return when unexpected value is entered
            except ValueError:
                console.print(Panel("INVALID VALUE,", width=70, style="red"))
                sleep(0.3)
                
                continue

            
        

   

    transaction_menu()

    











    #input("\nPress Enter to continue Main Menu:\n>>>")
    #clear_sys()
    #load_menu()


#main app
def Main_App():
    

    with console.status("[bold green]Starting Main App") as status:
        sleep(2)

    
    #App main menu
    table = Table.grid(padding = (1,2))
    table.add_row("[green]OPTIONS:")
    table.add_row("1.Add Income")
    table.add_row("2.Add Expenses")
    table.add_row("3.Update Budget")
    table.add_row("4.View Summary")
    table.add_row("5.Manage Transactions")
    table.add_row("6.Generate Report")
    table.add_row("0. \\-->...?")

    
    while True:

        console.print(Panel("Burget Tracker App", width=70,  style="green"))

        #load_menu()
        console.print(Panel(table,  title="MAIN MENU", subtitle="<<>>", width=70, style="cyan", border_style="magenta"))


        try:
            option = int(Prompt.ask("[magenta]Enter an Option:\n>>>[/magenta]"))
            
            #terminate MAinApp
            if option == 0:
                with console.status("[bold green]Closing Main App") as status:
                    sleep(2)
                console.print(Panel("GoodBye", width=70, style="green"))
                break


            #Calling the income Track Section
            elif option == 1:
                add_income()

            #calling the expense Track Section
            elif option == 2:
                add_expenses()
            #Update existing budgets
            elif option == 3:
                budget_update()

            #call view summary Section
            elif option == 4:
                view_summary()

            #call view Transaction Section
            elif option == 5:
                transactions()
            #Return when option not in 'option'
            elif option < 0 or option > 6:
                console.print(Panel("INVALID OPTION, TRY AGAIN", width=70, style="red"))
                sleep(0.4)
                clear_sys()
                load_menu()
                continue
            
        #return when unexpected value is entered
        except ValueError:
            console.print(Panel("INVALID VALUE,", width=70, style="red"))
            sleep(0.4)
            clear_sys()
            load_menu()
            continue



Main_App() 

