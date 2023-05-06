import threading
import random
import traceback
import time

#program deadlocks after first customer, need to fix

#what is pay's for restaurant that's not even grammar
#payment needed

def main():
    #seafood, steak, pasta
    tablea = Table('A')
    tableb = Table('B')
    tablec = Table('C')
    #kitchen init as shared resource
    kitchen = Kitchen()
    waiter0 = Waiter(0, kitchen)
    waiter1 = Waiter(1, kitchen)
    waiter2 = Waiter(2, kitchen)
    #
    tables = [tablea, tableb, tablec]
    waiters = [waiter0, waiter1, waiter2]
    #binds waiters to tables
    tables[0].bind(waiters[0])
    tables[1].bind(waiters[1])
    tables[2].bind(waiters[2])
    waiters[0].bind(tables[0])
    waiters[1].bind(tables[1])
    waiters[2].bind(tables[2])

    #list of 40 customers randomly generated
    customers = [Customer(i, tables) for i in range(40)]

    for c in customers:
        c.beginpurchase()

    for w in waiters:
        w.beginwaiting()

#two doors
def door(customer):
    doorsem = threading.Semaphore(2)
    try:
        doorsem.acquire()
        print(f'{customer} enters the restaurant')
        doorsem.release()
    except:
        traceback.print_exc()

class Kitchen:
    
    def __init__(self):
        self.semaphore = threading.Semaphore(1)

    def use(self, waiter):
        try:
            self.semaphore.acquire()
            print(f'{waiter} enters the kitchen to deliver an order')
            time.sleep(0.1 * random.randrange(0, 500) + 0.1)
            print(f'{waiter} exits the kitchen and waits')
            self.semaphore.release()
        except:
            traceback.print_exc()

class Customer:

    def __init__(self, cid, tables):
        self.customerid = cid
        self.tables = tables
        self.served = False
        self.semaphore = threading.Semaphore(0)

    def isserved(self):
        return self.served
    
    def setserved(self, ser):
        self.served = ser

    def signal(self):
        self.semaphore.release()

    def beginpurchase(self):
        try:
            #enter, and select preferred table
            door(self)
            prefertable = self.tables[random.randint(0,2)]
            print(f'{self} wants to eat at {prefertable}')

            #if line too long, choose backup
            #if backup too long, go back to first choice
            if prefertable.linelength() > 7:
                print(f'{self}\'s first choice has a long line')
                backuptable = self.tables[random.randint(0,2)]
                while backuptable == prefertable:
                    backuptable = self.tables[random.randint(0,2)]
                if backuptable.linelength() < 7:
                    prefertable = backuptable
                else:
                    print(f'{self}\'s backup choice has a long line')
            
            prefertable.seatcustomer(self)
            self.semaphore.acquire()

            #as per specifications
            print(f'{self} is eating')
            time.sleep(random.random() + 0.2)
            print(f'{self} is finished eating')
            prefertable.emptyseat(self)
            print(f'{self} leaves restaurant')
        except:
            traceback.print_exc()

    def __str__(self):
        return f'Customer {self.customerid}'
    
class Table:

    def __init__(self, name):
        self.name = name
        self.seats = []
        self.line = []
        self.semaphore = threading.Semaphore(1)
    
    def bind(self, waiter):
        self.waiter = waiter
    
    def linelength(self):
        return len(self.line)
    
    def getcustomer(self):
        try:
            for c in self.seats:
                if not c.isserved():
                    return c
        except:
            traceback.print_exc()

    def emptyseat(self, customer):
        try:
            self.semaphore.acquire()
            self.seats.remove(customer)
            print(f'{self} is done eating')

            if len(self.line) != 0:
                nextguy = self.line.pop()
                self.seats.append(nextguy)
                print(f'{nextguy} sits at {self}')
                self.waiter.flagdown()
            self.semaphore.release()
        except:
            traceback.print_exc()

    def seatcustomer(self, customer):
        try:
            self.semaphore.acquire()
            if len(self.seats) < 4:
                self.seats.append(customer)
                print(f'{customer} sits at {self}')
                self.waiter.flagdown()
            else:
                self.line.append(customer)
                print(f'{customer} stands in line for {self}')
            self.semaphore.release()
        except:
            traceback.print_exc()

    def __str__(self):
        return f'Table {self.name}'
    
class Waiter:
    
    def __init__(self, id, kitchen):
        self.id = id
        self.kitchen = kitchen
        self.semaphore = threading.Semaphore(0)

    def bind(self, table):
        self.table = table

    def flagdown(self):
        self.semaphore.release()
    
    def beginwaiting(self):
        try:
            while True:
                self.semaphore.acquire()
                customer = self.table.getcustomer()
                if customer is None:
                    break
                #follows specifications, but not sure how to 
                print(f'{self} is now serving {customer}')
                self.kitchen.use(self)
                print(f'{self} goes to the kitchen to deliver {customer}\'s order')
                time.sleep(random.random() + 0.3)
                print(f'{self} enters the kitchen to deliver {customer}\'s order')
                self.kitchen.use(self)
                customer.setServed(True)
                customer.signal()
            print(f'{self} cleans the table and leaves the restaurant')
        except:
            traceback.print_exc()
    
    def __str__(self):
        return f'Waiter {self.id}'
    
#begin running
if __name__ == "__main__":
    main()