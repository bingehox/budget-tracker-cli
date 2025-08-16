import os
import csv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
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



#Income Track Section
def add_income():
    clear_sys()

    filename = "income_track.csv"
    console.print(Panel("Income Track Section", style="green"))
    while True:
        try:
            inc_src = str(input("Enter income source eg.(Salary, Freelance, Gifts or Investement):\n>>>"))#input income soucre
            #Reject income input if a number is entered
            if inc_src.isdigit():
                raise ValueError("Income Source cannot be Integers")
            
            inc_amt = float(input("Enter Amount:\n>>>"))#input Amount
            break #breaks loop when both input are valid
        except ValueError:
            console.print(Panel("Invalid Value, Try Again"), style="bold red")
            continue

    #Date logic
    while True:

        try:
            date_str = input("Enter date in (YY-MM-DD) format or none for default:\n>>>")# date string
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
        with console.status(f"(Saving...)") as status:
            sleep(1)
        console.log("[bold red]DONE!!")   
        console.print(Panel(f"Income data saved to {filename} Successfully", style="green"))

    save_income_info()

    input("\nPress Enter to continue:\n>>>")
    load_menu()
    clear_sys()



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
            option = int(input("Enter an Option:\n>>>"))
            
            #terminate MAinApp
            if option == 0:
                with console.status("[bold green]Closing Main App") as status:
                    sleep(2)
                console.print(Panel("GoodBye", width=70, style="green"))
                break


            #Calling the income Track Section
            elif option == 1:
                add_income()

            #Return when option not in 'option'
            elif option < 0 or option > 6:
                console.print(Panel("INVALID OPTION, TRY AGAIN", width=70, style="red"))
                load_menu()
                clear_sys()
                continue
            
        #return when unexpected value is entered
        except ValueError:
            console.print(Panel("INVALID VALUE,", width=70, style="red"))
            load_menu()
            clear_sys()
            continue



Main_App()    
