import pandas as pd
import sys

#function to read a csv file into a pandas dataframe, then sort by timestamp
def readfile(filename):
    transactions = pd.read_csv(filename)
    transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
    transactions = transactions.sort_values(by='timestamp')
    return transactions

#function to spend points given timestamp sorted data frame and points to spend
def spend(df, points):
    
    #check if the user has enough points
    totalpoints = sum(df.points)
    if(points > totalpoints):
        print('Cannot use more than available points!')
        exit()

    #user has enough points so spend them in the correct way
    for i in df.index:
        #if remaining points to spend are more than this payers points
        if(points > df.points[i]):
            #use the points and set that index in the df to 0
            points -= df.points[i]
            df.at[i, 'points'] = 0

        #if remaining points are less than or equal to this payers points
        elif (points <= df.points[i]):
            #subtract how much we want to use then break since no remaining points to use
            df.at[i, 'points'] -= points
            points = 0
            break

    #setting up pointsleft dict
    pointsleft = {}
    names = df.payer.unique()
    for payer in names:
        pointsleft[payer] = 0

    #sum the remaining points we have for each payer in the dict
    for i in df.index:
        pointsleft[df.payer[i]] += df.points[i]

    return pointsleft


#DRIVER CODE

#if not enough arguments exit
if(len(sys.argv) != 3):
    print('Error: invalid arguments!')
    print('Usage: prompt> python3 fetch.py [points to spend] [csv filename]')
    exit()

#get filename and points to spend
file = sys.argv[2]
spend_points = int(sys.argv[1])
#readfile as a dataframe
data = readfile(file)

#prints the remaining points after using the specified points
print(spend(data, spend_points))