import os
import csv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from collections import defaultdict
from datetime import datetime, date
from time import sleep


console = Console() #Initialize Console

#clear terminal
def clear_sys():
     os .system('cls' if os.name == 'nt' else 'clear')

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
    console.print(Panel("Income Track Section", style="green"))
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

            inc_src = str(Prompt.ask("[cyan]Enter income source eg.(Salary, Freelance, Gifts or Investement)\nor type 'help' to view Available Income Category list:\n>>>[/cyan]")).strip()#input income soucre
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
                console.print(Panel("\n".join(allowed_inc_src), title="Allowed Income Category"))
                raise ValueError("[green]choose from above list[/green]")
            #Only allow Income from the list
            if inc_src not in allowed_inc_src:
                console.print(Panel("\n".join(allowed_inc_src), title="Allowed Income Sources,Just For Now"))
                raise ValueError("Please choose from the predefined options  Above for better experience.\nWe’re working on making the categories more flexible in the future! ")

            #handle Expense input exceptions
            income_input = (Prompt.ask("[cyan]Enter Expense Amount:\n>>>[/cyan]", default="0"))#input Amount
            if not income_input.replace(".", "", 1).isdigit():#allows decimals
                raise ValueError("Expense Amount can only contain numbers")
            inc_amt = float(income_input)
            break #breaks loop when both input are valid
        
        except ValueError as e:
            console.print(Panel(f"[bold red]{str(e)}[/bold red]\n"),style="bold red")
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
    console.print(Panel("Expense Track Section", style="green"))

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
            category = str(Prompt.ask("[cyan]Enter Expense Category source eg.(Rent, Food, Transport or Entertainment, e.t.c)\n or type 'help' to view Options list:\n>>>[/cyan]")).strip()#input income soucre
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
                console.print(Panel("\n".join(allowed_expense_category), title="Allowed Expense Category"))
                raise ValueError("[green]choose from above list[/green]")
            #Only allow expense category from this list
            if category not in allowed_expense_category:
                console.print(Panel("\n".join(allowed_expense_category), title="Allowed Expense Category"))
                raise ValueError("Please choose from the above predefined options for better user experince.\nWe’ll work on making the categories more flexible in the future!")
            
        

            #handle Expense input exceptions
            expense_input = (Prompt.ask("[cyan]Enter Expense Amount:\n>>>[/cyan]", default="0"))#input Amount
            if not expense_input.replace(".", "", 1).isdigit():#allows decimals
                raise ValueError("Expense Amount can only contain numbers")
            expense_amt = float(expense_input)
            break #breaks loop when both input are valid
        except ValueError as e: # for custom message
            console.print(Panel(f"[bold red]{str(e)}[/bold red]"), style="bold red")
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

#Summary section
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
            return ("[bold red]Warning 🔴")
        else:
            return "✔" #prints empty to avoid printing None
        
    def info_sa():
        if savings > spendings:
            return ("[bold green] :) 🟢")
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
            console.print(f"{category:<20} {total:>5.2f} {budget:>13.2f} {status:>30.0f} {usage_pct:>10.0f}%", style="cyan")
    except Exception as e:
        console.print(f"[red]Error while rendering breakdown: {e}[/red]")
         
    console.log("\n[bold red]DONE!!")
    
           
    input("\nPress Enter to continue Main Menu:\n>>>")
    clear_sys()
    load_menu()


def view_transaction():
    x =4

#main app
def Main_App():
    

    with console.status("[bold green]Starting Main App") as status:
        sleep(2)

    
    #App main menu
    table = Table.grid(padding = (1,2))
    table.add_row("[green]OPTIONS:")
    table.add_row("1.Add Income")
    table.add_row("2.Add Expenses")
    table.add_row("3.View Summary")
    table.add_row("4.View Transaction")
    table.add_row("5.Manage Transaction")
    table.add_row("6.Generate Report")
    table.add_row("0.Exit...?")

    
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

            #call view summary Section
            elif option == 3:
                view_summary()

            #call view Transaction Section
            elif option == 4:
                view_transaction()
            #Return when option not in 'option'
            elif option < 0 or option > 6:
                console.print(Panel("INVALID OPTION, TRY AGAIN", width=70, style="red"))
                clear_sys()
                load_menu()
                continue
            
        #return when unexpected value is entered
        except ValueError:
            console.print(Panel("INVALID VALUE,", width=70, style="red"))
            clear_sys()
            load_menu()
            continue



Main_App()    
