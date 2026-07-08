print("======Part 1======")

cinema_name = "CineMax Cinema"
base_price = 12.5
seats_available = 120
is_weekend = True
screen_number = int(input("Enter screen number: "))
print (type(cinema_name))
print (type(base_price))
print (type(seats_available))
print (type(is_weekend))
print (f"cinema name = {cinema_name}, base price = {base_price}, seats available = {seats_available}, is weekend = {is_weekend}, screen number = {screen_number}")

print("======Part 2======")

adult_tickets = 3
child_tickets = 2
senior_tickets = 1
base_price = 12.5
child_price = base_price * 0.6
print( "child price is ", child_price )
senior_price = base_price - (base_price // 4)
print( "senior price is ", senior_price)
adult_price = base_price
print( "adult price is ", adult_price)
subtotal = ((child_price * child_tickets) + (senior_price * senior_tickets) + (adult_price * adult_tickets)) 
print ( "The subtotal is ", subtotal)
service_fee = subtotal % 5
print ( "The service fee is ", service_fee)
tax = subtotal * 0.0825
print ( "The tax is ", tax)
total = subtotal + tax + service_fee
print ( "The total is ", total)
average_ticket_price = total / (adult_tickets + child_tickets + senior_tickets)
print ( "The average ticket price is ", average_ticket_price)

print("======Part 3======")
Membership= input("What is your membership?")
Ticket_count= int(input("What is your ticket count?"))
if Membership == "Gold":
    discount_rate = 0.2
elif Membership == "Silver" and Ticket_count >= 5 :
    discount_rate = 0.15
elif Membership == "Silver" and Ticket_count < 5:
    discount_rate = 0.08
elif Membership == "Bronze" or Ticket_count>= 10:
    discount_rate = 0.05
else:
    discount_rate = 0.00
print ("The discount_rate is", discount_rate)

print("======Part 4======")
time_slot = input("Time slot")
if is_weekend:
    if time_slot == "evening":
        if Membership == "Gold":
            final_price = base_price * 1.10
        elif Membership == "silver" or Membership == "bronze":
            final_price = base_price * 1.20
        else:
            final_price = base_price * 1.30
    else:
        if Membership == "Gold":
            final_price = base_price
        else:
            final_price = base_price * 1.10
else:
    if time_slot == "evening":
        if Membership == "Gold" or Membership == "Silver":
            final_price = base_price - (base_price * 0.05)
        else:
            final_price = base_price
    else:
        final_price = base_price - (base_price * 0.25)
print ("The final price is ",  final_price)

print("======Part 5a======")


running_total = 0
mismatch_found = 0
for i in range(8):
    age = int(input("Enter age: "))
    ticket_type = input("Enter ticket type (child/adult/senior)")
    if ticket_type == "child":
        expected_age = age <12
        running_total = running_total + child_price 
    elif ticket_type == "adult":
        expected_age = 12 <= age < 65
        running_total = running_total + adult_price
    else:
        expected_age = age >= 65
        running_total = running_total + senior_price
    if expected_age == True:
        print (running_total)
    else:
        print ("mismatch")
        mismatch_found = mismatch_found + 1
print (mismatch_found)
print (running_total)

print("======Part 5b======")

seats_available = 5
tickets_booked = 0
total_revenue = 0

while True:
    booking_tickets = input("Enter option (book/exit): ")
    if booking_tickets == "book":
        if seats_available == 0:
            print("Sold out!")
        else:
            print("You have sucessfully booked a ticket")
            seats_available = seats_available - 1
            tickets_booked = tickets_booked + 1
            total_revenue = total_revenue + 12.5
    elif booking_tickets == "exit":
        print("The total number tickets booked is ", tickets_booked)
        print("The total number of seats available is ", seats_available)
        print("The total revenue is ", total_revenue)
        break
    else:
        print("Invalid option")