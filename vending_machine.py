# by Michael Horton, 2/9/2021

# I think the class should still work if you only change the parameters in the __init__ function, as long as all the appropriate
# fields are updated (e.g. if you add another item to the menu, you must increase menu_num_rows by 1).

import numpy as np

class VendingMachine:
    def __init__(self):
        # The first column is the type of coin, the second is the numerical value of that coin,
        # the third is how many of that coin are currently held, 
        # and the fourth is the amount of that coin after restock.
        self.change = [['$1', 100, 5, 5],
            ['50c', 50, 5, 5],
            ['20c', 20, 5, 5],
            ['10c', 10, 10, 10],
            ['5c', 5, 10, 10]]
        self.change_num_rows = 5

        self.starting_amount = 1000
        self.current_total = 1000
        self.inserted_amount = 0

        # The first 3 columns are printed when ShowMenu is called, 
        # the 4th is the numerical price value, the 5th is current stock of that item,
        # and the 6th is the amount of that item after restock.
        self.menu = [['Code', 'Item', 'Price'],
            ['1','Water', '$0.75', 75, 5, 5],
            ['2', 'Coke', '$1.20', 120, 5, 5],
            ['3', 'Diet Coke', '$1.20', 120, 5, 5],
            ['4', 'Iced Tea', '$1.00', 100, 5, 5],
            ['5', 'Swiss Chocolate', '$1.50', 150, 5, 5],
            ['6', 'Candy', '$0.95', 95, 5, 5],
            ['7', 'Chips', '$1.10', 110, 5, 5],
            ['8', 'Bubble Gum', '$0.50', 50, 5, 5],
            ['9', 'Turkish Delight', '$1.20', 120, 5, 5],
            ['10', 'End of Transaction']]
        self.menu_num_rows = 11

        self.restock_pin = '9999'
    
    # Print the menu
    def ShowMenu(self):
        for i in range(0,self.menu_num_rows-1):
            print(self.menu[i][0], self.menu[i][1], self.menu[i][2])
        print(self.menu[(self.menu_num_rows-1)][0], self.menu[(self.menu_num_rows-1)][1])
    
    # We assume that the coin is input as a string, e.g. for a 50 cent coint, the input will be '50c'.
    def InsertChange(self, coin):
        
        coin_rank = -1
        for i in range(0,self.change_num_rows):
            if (coin == self.change[i][0]):
                coin_rank = i
                break
        if (coin_rank == -1):
            self.DisplayErrorMessage()
        else:
            self.change[coin_rank][2] += 1
            self.current_total += self.change[coin_rank][1]
            self.inserted_amount += self.change[coin_rank][1]
            print('Current balance is $', end = '')
            balance = "{:.2f}".format(self.inserted_amount/100)
            print(balance)
        

    # We assume that the code is an integer input.
    def MakeSelection(self, code):

        if (code == 99):
            # We will assume the maintenance worker does not need a prompt for the pin,
            # but will print one dot to show the input went through.
            print('.')
            maintenance_code = input()
            if (maintenance_code == self.restock_pin):
                self.Restock()
            else:
                self.DisplayErrorMessage()
        # Filter out incorrect codes
        elif (code <= 0 or code >=self.menu_num_rows):
            self.DisplayErrorMessage()
        # Check for end of transaction
        elif (code == self.menu_num_rows-1):
            returning_change = self.ReturnChange(self.inserted_amount)
            print('Transaction complete! Returning change:')
            for i in range(self.change_num_rows):
                if (returning_change[i] > 0):
                    print(returning_change[i],'x', self.change[i][0])
                    self.change[i][2] += -returning_change[i]
            self.current_total += -self.inserted_amount
            self.inserted_amount = 0
        # Attempt to purchase the relevant item
        else:
            self.PurchaseItem(int(code))

    # We again assume the code is an integer
    def PurchaseItem(self, code):
        
        if (self.menu[code][4] == 0):
            print( self.menu[code][1], 'out of stock.')
        # We need to check if we can get correct change
        elif (self.inserted_amount < self.menu[code][3]):
            print('Balance not high enough, please insert more money.')
        else:
            returning_change = self.ReturnChange(self.inserted_amount - self.menu[code][3])
            if (returning_change[0] == -1):
                print('Error, cannot give correct change after purchase, purchase denied.')
            else:
                self.inserted_amount += -self.menu[code][3]
                self.menu[code][4] += -1
                print('Purchase complete, enjoy your', self.menu[code][1], end='')
                print('!')
                print('Current balance is $', end = '')
                balance = "{:.2f}".format(self.inserted_amount/100)
                print(balance)


    # Since we want to check if we can return the correct change after a purchase,
    # without actually returning change, we instead return an array with
    # the correct change to return.
    def ReturnChange(self, amount):
        outgoing_change = np.zeros(self.change_num_rows)
        remaining_balance = amount
        for i in range(0, self.change_num_rows):
            num_coins = int(remaining_balance/ self.change[i][1])
            if (num_coins <= self.change[i][2]):
                outgoing_change[i] = num_coins
            else: 
                outgoing_change[i] = self.change[i][2]
            remaining_balance += -(outgoing_change[i] * self.change[i][1])
        
        # If we are not able to find the correct change (there is still some
        # leftover balance), then set the first entry to -1 to notify the other functions.
        if (remaining_balance > 0):
            outgoing_change[0] = -1

        return outgoing_change

    def DisplayErrorMessage(self):
        print('Something went wrong! Please try again.')

    
    def Restock(self):
        print('Restocking!')
        current_balance = "{:.2f}".format(self.current_total/100)
        net_income = "{:.2f}".format((self.current_total - self.starting_amount)/100)
        print('Current balance: $', end = '')
        print(current_balance)
        print('Net income: $', end = '')
        print(net_income)
        for i in range(0,self.change_num_rows):
            self.change[i][2] = self.change[i][3]
        self.current_total = self.starting_amount
        
        for i in range(1,self.menu_num_rows-1):
            print('Sold', self.menu[i][5]-self.menu[i][4], 'many', self.menu[i][1], 'today.')
            self.menu[i][4] = self.menu[i][5]
        

vendor = VendingMachine()

print('Welcome to my vending machine program! You may type "help" to see what commands are available, or type "quit" to end the program.')

quit = False

while (quit == False):
    
    command = input()

    if (command == 'quit'):
        print('Ending program, have a nice day!')
        break
    
    elif (command == 'help'):
        print('help - prints this message again')
        print('quit - ends the program')
        print('insert - starts inserting coins')
        print('menu - prints the vending machine menu')
        print('select - inputs the next message as a code to the vending machine')
    
    elif (command == 'insert'):
        print('To insert coins, they must be typed in the following format:')
        print('$1, 50c, 20c, 10c, 5c')
        print('This program will keep inserting coins until you type "stop"')

        while(quit == False):
            coin = input()
            if (coin == 'stop'):
                print('Returning to main input mode')
                break
            if (coin == 'quit'):
                print('Ending program, have a nice day!')
                quit = True
                break
            vendor.InsertChange(coin)


    elif (command == 'menu'):
        vendor.ShowMenu()

    elif (command == 'select'):
        print('Please input your selection code: ', end = '')
        code = input()
        if (code == 'quit'):
            print('Ending program, have a nice day!')
            break
        elif (str.isnumeric(code) == False or int(code) != float(code)):
            print('Only integer codes please.')
        else: 
            vendor.MakeSelection(int(code))
    
    # Debug functions
    #elif(command == 'print change'):
    #    print(vendor.change)
    #elif(command == 'print amount'):
    #    print(vendor.inserted_amount)
    #elif(command == 'print total'):
    #    print(vendor.current_total)
    #elif(command == 'money'):
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])
    #    vendor.InsertChange(vendor.change[0][0])


    else:
        print('Unrecognized command, type "help" for more info.')

