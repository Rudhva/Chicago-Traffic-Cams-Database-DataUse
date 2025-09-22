#
# Rudhva Patel
# UIN: 657512073
# This program is supposed to use the chicago-traffic-cameras.db 
# and display different facts, overview, and even plot the map/graph data!
#

import sqlite3
import matplotlib.pyplot as plt
import datetime


# Given a connection to the database, executes various
# SQL queries to retrieve and output basic stats.
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General Statistics:")
    
    # Number of Red Light Cameras
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    row = dbCursor.fetchone()
    print("  Number of Red Light Cameras:", f"{row[0]:,}")

    # Number of Speed Cameras
    dbCursor.execute("SELECT Count(*) FROM SpeedCameras")
    row = dbCursor.fetchone()
    print("  Number of Speed Cameras:", f"{row[0]:,}")

    # Number of Red Light Camera Violation Entries
    dbCursor.execute("SELECT Count(*) FROM RedViolations")
    row = dbCursor.fetchone()
    print("  Number of Red Light Camera Violation Entries:", f"{row[0]:,}")

    # Number of Speed Camera Violation Entries
    dbCursor.execute("SELECT Count(*) FROM SpeedViolations")
    row = dbCursor.fetchone()
    print("  Number of Speed Camera Violation Entries:", f"{row[0]:,}")

    # Range of Dates in the Database
    dbCursor.execute("SELECT MIN(Violation_Date) AS min_date, MAX(Violation_Date) AS max_date FROM RedViolations;")
    row = dbCursor.fetchone()
    print("  Range of Dates in the Database:", f"{row[0]} - {row[1]}")


    # Total Number of Red Light Camera Violations
    dbCursor.execute("SELECT Sum(Num_Violations) FROM RedViolations")
    row = dbCursor.fetchone()
    print("  Total Number of Red Light Camera Violations:", f"{row[0]:,}")


    # Total Number of Speed Camera Violations
    dbCursor.execute("SELECT Sum(Num_Violations) FROM SpeedViolations")
    row = dbCursor.fetchone()
    print("  Total Number of Speed Camera Violations:", f"{row[0]:,}", end='')
    print()

# Find an intersection by name
def option1(dbConn):
    dbCursor = dbConn.cursor()

    name = input("\nEnter the name of the intersection to find (wildcards _ and % allowed): ").upper()

    dbCursor.execute("""
        SELECT Intersection_ID, Intersection
        FROM Intersections
        WHERE Intersection LIKE ?
        GROUP BY Intersection_ID
        ORDER BY Intersection ASC
    """, (name,))

    rows = dbCursor.fetchall()

    if rows:
        for row in rows:
            print(f"{row[0]} : {row[1]}")
    else:
        print("No intersections matching that name were found.")


# Find an intersection by name
def option2(dbConn):
    dbCursor = dbConn.cursor()

    print()
    name = input("Enter the name of the intersection (no wildcards allowed): ")

    dbCursor.execute("""
        SELECT Camera_ID, Address
        FROM RedCameras
        JOIN Intersections ON Intersections.Intersection_ID = RedCameras.Intersection_ID
        WHERE Intersection LIKE ?
        GROUP BY Camera_ID
    """, (name,))

    rows = dbCursor.fetchall()

    if rows:
        print("\nRed Light Cameras:")
        for row in rows:
            print(f"   {row[0]} : {row[1]}")
    else:
        print("\nNo red light cameras found at that intersection.")

    dbCursor.execute("""
        SELECT Camera_ID, Address
        FROM SpeedCameras
        JOIN Intersections ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
        WHERE Intersection LIKE ?
        GROUP BY Camera_ID
    """, (name,))

    rows = dbCursor.fetchall()

    if rows:
        print("\nSpeed Cameras:")
        for row in rows:
            print(f"   {row[0]} : {row[1]}")
    else:
        print("\nNo speed cameras found at that intersection.")


#Percentage of violations for a specific date
def option3(dbConn):
    dbCursor = dbConn.cursor()
    date = input("\nEnter the date that you would like to look at (format should be YYYY-MM-DD): ")
    
    dbCursor.execute("""
        SELECT SUM(Num_Violations) 
        FROM RedViolations 
        WHERE Violation_Date LIKE ?""", (date,))
    redViolations = dbCursor.fetchone()[0]

    dbCursor.execute("""
        SELECT SUM(Num_Violations) 
        FROM SpeedViolations 
        WHERE Violation_Date LIKE ?""", (date,))
    
    speedViolations = dbCursor.fetchone()[0]

    redViolations = redViolations or 0
    speedViolations = speedViolations or 0
    total = redViolations + speedViolations
    
    if(total > 0):
        percentage = float(redViolations/total)
        print("Number of Red Light Violations:", f"{redViolations:,}", f"({percentage:.3%})")
        percentage = float(speedViolations/total)
        print("Number of Speed Violations:", f"{speedViolations:,}", f"({percentage:.3%})")
        print("Total Number of Violations:", f"{total:,}")
    else:
        print("No violations on record for that date.")
    

# Number of cameras at each intersection
def option4(dbConn):
    dbCursor = dbConn.cursor()

    # Red Cams
    dbCursor.execute("""
        SELECT Intersection as name, Intersections.Intersection_ID, count(RedCameras.Camera_ID) as totalCams
        FROM Intersections 
        JOIN RedCameras ON RedCameras.Intersection_ID = Intersections.Intersection_ID
        GROUP BY Intersections.Intersection
        ORDER BY totalCams DESC, Intersections.Intersection_ID DESC
""")
    rows = dbCursor.fetchall()

    # Total Red Cams
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    total = int(dbCursor.fetchone()[0] or 0)

    print("\nNumber of Red Light Cameras at Each Intersection")
    if rows:
        for row in rows:
            name = row[0]
            camID = row[1]
            cams_at_intersection = row[2]
            percentage = cams_at_intersection / total if total > 0 else 0
            print(f"  {name} ({camID:}) : {cams_at_intersection:,} ({percentage:.3%})")

        # Speed Cams
    dbCursor.execute("""
        SELECT Intersection as name, Intersections.Intersection_ID, count(SpeedCameras.Camera_ID) as totalCams
        FROM Intersections 
        JOIN SpeedCameras ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID
        GROUP BY Intersections.Intersection
        ORDER BY totalCams DESC, Intersections.Intersection_ID DESC
""")
    rows = dbCursor.fetchall()

    # Total Speed Cams
    dbCursor.execute("SELECT COUNT(*) FROM SpeedCameras;")
    total = int(dbCursor.fetchone()[0] or 0)

    print("\nNumber of Speed Cameras at Each Intersection")
    if rows:
        for row in rows:
            name = row[0]
            camID = row[1]
            cams_at_intersection = row[2]
            percentage = cams_at_intersection / total if total > 0 else 0
            print(f"  {name} ({camID:}) : {cams_at_intersection:,} ({percentage:.3%})")


# Number of violations at each intersection, given a year
def option5(dbConn):
    dbCursor = dbConn.cursor()

    rawYear = input("\nEnter the year that you would like to analyze: ")
    year = "%" + rawYear + "%"

    # Red Violations
    dbCursor = dbConn.execute("""
    SELECT Intersections.Intersection as name, Intersections.Intersection_ID as ID, SUM(RedViolations.Num_Violations) as totalViolations
    FROM RedCameras
    JOIN Intersections ON Intersections.Intersection_ID = RedCameras.Intersection_ID
    JOIN RedViolations ON RedCameras.Camera_ID = RedViolations.Camera_ID
    WHERE Violation_Date LIKE ?
    GROUP BY Intersections.Intersection
    ORDER BY totalViolations DESC, ID DESC
                              """, (year,))
    rows = dbCursor.fetchall()
    dbCursor = dbConn.execute("SELECT SUM(Num_Violations) FROM RedViolations WHERE Violation_Date LIKE ?", (year,))
    vioTotal = dbCursor.fetchone()[0] or 0

    print("\nNumber of Red Light Violations at Each Intersection for", rawYear)
    if(vioTotal > 0):
        for row in rows:
            name = row[0]
            interID = row[1]
            vioCount = row[2] or 0
            percentage = float(vioCount/vioTotal)
            print(f"  {name} ({interID:}) : {vioCount:,} ({percentage:.3%})")
        print("Total Red Light Violations in", rawYear, ":", f"{vioTotal:,}")
    else :
        print("No red light violations on record for that year.")

    dbCursor = dbConn.execute("""
    SELECT Intersections.Intersection as name, Intersections.Intersection_ID as ID, SUM(SpeedViolations.Num_Violations) as totalViolations
    FROM SpeedCameras
    JOIN Intersections ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
    JOIN SpeedViolations ON SpeedCameras.Camera_ID = SpeedViolations.Camera_ID
    WHERE Violation_Date LIKE ?
    GROUP BY Intersections.Intersection
    ORDER BY totalViolations DESC, ID DESC
                              """, (year,))
    rows = dbCursor.fetchall()
    dbCursor = dbConn.execute("SELECT SUM(Num_Violations) FROM SpeedViolations WHERE Violation_Date LIKE ?", (year,))
    vioTotal = dbCursor.fetchone()[0] or 0
    

    print("\nNumber of Speed Violations at Each Intersection for", rawYear)
    if(vioTotal > 0):
        for row in rows:
            name = row[0]
            interID = row[1]
            vioCount = row[2] or 0
            percentage = float(vioCount/vioTotal)
            print(f"  {name} ({interID:}) : {vioCount:,} ({percentage:.3%})")
        print("Total Speed Violations in", rawYear, ":", f"{vioTotal:,}")
    else :
        print("No speed violations on record for that year.")

# Number of violations by year, given a camera ID
def option6(dbConn):
    dbCursor = dbConn.cursor()
    camera_id = input("\nEnter a camera ID: ")

    sqlRed = "SELECT SUBSTR(Violation_Date, 1, 4), SUM(Num_Violations) FROM RedViolations " \
    "WHERE Camera_ID = ? GROUP BY SUBSTR(Violation_Date, 1, 4);"
    sqlSpeed = "SELECT SUBSTR(Violation_Date, 1, 4), SUM(Num_Violations) FROM SpeedViolations " \
    "WHERE Camera_ID = ? GROUP BY SUBSTR(Violation_Date, 1, 4);"

    dbCursor.execute(sqlRed, (camera_id,))
    rowsRed = dbCursor.fetchall()
    dbCursor.execute(sqlSpeed, (camera_id,))
    rowsSpeed = dbCursor.fetchall()

    dictionary = {}
    for year, violations in rowsRed:
        dictionary[year] = dictionary.get(year, 0) + violations
    for year, violations in rowsSpeed:
        dictionary[year] = dictionary.get(year, 0) + violations

    rows = sorted(dictionary.items())

    if not rows:
        print("No cameras matching that ID were found in the database.")
    else:
        print("Yearly Violations for Camera", camera_id)

        for year, num in rows:
            print(f"{year} : {num:,}")
        
        print()
        shouldPlot = input("Plot? (y/n) ")
        if shouldPlot == "y":
            years = []
            violations = []
            for row in rows:
                print(row)
                years.append(row[0])
                violations.append(row[1])

            plt.plot(years, violations)
            plt.title("Yearly Violations for Camera "+camera_id)
            plt.xlabel("Year")
            plt.ylabel("Number of Violations")
            plt.show()


# Number of violations by month, given a camera ID and year
def option7(dbConn):
    dbCursor = dbConn.cursor()

    camID = input("\nEnter a camera ID: ")

    # Check if camera exists in either table
    dbCursor.execute("SELECT 1 FROM RedCameras WHERE Camera_ID = ?", (camID,))
    exists = dbCursor.fetchone()
    if not exists:
        dbCursor.execute("SELECT 1 FROM SpeedCameras WHERE Camera_ID = ?", (camID,))
        exists = dbCursor.fetchone()

    if not exists:
        print("No cameras matching that ID were found in the database.")
        return

    year = input("Enter a year: ")

    # Query violations by month (check both tables)
    dbCursor = dbConn.execute("""
        SELECT substr(Violation_Date, 1, 7) as month, SUM(Num_Violations)
        FROM RedViolations
        WHERE Camera_ID = ? AND Violation_Date LIKE ?
        GROUP BY month
        ORDER BY month ASC
        """, (camID, year + "%"))
    rows = dbCursor.fetchall()

    dbCursor = dbConn.execute("""
        SELECT substr(Violation_Date, 1, 7) as month, SUM(Num_Violations)
        FROM SpeedViolations
        WHERE Camera_ID = ? AND Violation_Date LIKE ?
        GROUP BY month
        ORDER BY month ASC
        """, (camID, year + "%"))
    rows += dbCursor.fetchall()

    # Combine results (if same month appears in both)
    monthly_totals = {}
    for row in rows:
        month = row[0]  # YYYY-MM
        count = row[1] or 0
        monthly_totals[month] = monthly_totals.get(month, 0) + count

    print(f"Monthly Violations for Camera {camID} in {year}")
    if monthly_totals:
        for month in sorted(monthly_totals.keys()):
            yyyy, mm = month.split("-")
            print(f"{mm}/{yyyy} : {monthly_totals[month]:,}")

    shouldPlot = input("\nPlot? (y/n) ").lower()
    if shouldPlot == 'y' and monthly_totals:
        months = sorted(monthly_totals.keys())
        totals = [monthly_totals[m] for m in months]
        # convert months to MM/YYYY for plot labels
        month_labels = [m.split("-")[1] + "/" + m.split("-")[0] for m in months]
        plt.figure(figsize=(8,5))
        plt.plot(month_labels, totals, color="skyblue")
        plt.xlabel("Month")
        plt.ylabel("Number of Violations")
        plt.title(f"Monthly Violations for Camera {camID} in {year}")
        plt.show()

# Compare the number of red light and speed violations, given a year
def option8(dbConn):
    dbCursor = dbConn.cursor()

    year = input("\nEnter a year: ")

    # Query red light violations
    dbCursor.execute("""
        SELECT Violation_Date, SUM(Num_Violations)
        FROM RedViolations
        WHERE Violation_Date LIKE ?
        GROUP BY Violation_Date
        ORDER BY Violation_Date ASC
    """, (year + "%",))
    red_rows = dbCursor.fetchall()

    # Query speed violations
    dbCursor.execute("""
        SELECT Violation_Date, SUM(Num_Violations)
        FROM SpeedViolations
        WHERE Violation_Date LIKE ?
        GROUP BY Violation_Date
        ORDER BY Violation_Date ASC
    """, (year + "%",))
    speed_rows = dbCursor.fetchall()

    # Build dictionaries for fast lookup
    red_dict = {row[0]: row[1] for row in red_rows}
    speed_dict = {row[0]: row[1] for row in speed_rows}

    # Combine all dates from both tables
    all_dates = sorted(set(red_dict.keys()) | set(speed_dict.keys()))

    if not all_dates:
        print("Red Light Violations:")
        print("Speed Violations:")
        shouldPlot = input("\nPlot? (y/n) ").lower()
        if shouldPlot == 'y':
            plt.figure(figsize=(12,5))
            plt.xlabel("Day of the Year")
            plt.ylabel("Number of Violations")
            plt.title(f"Violations Each Day of {year}")
            plt.legend(["Red Light", "Speed"])
            plt.show()
        return

    # Display first 5 and last 5 days
    first5 = all_dates[:5]
    last5 = all_dates[-5:]
    display_dates = first5 + last5 if len(all_dates) > 10 else all_dates

    print("Red Light Violations:")
    for date in display_dates:
        print(f"{date} {red_dict.get(date,0)}")

    print("Speed Violations:")
    for date in display_dates:
        print(f"{date} {speed_dict.get(date,0)}")

    shouldPlot = input("\nPlot? (y/n) ").lower()
    if shouldPlot == 'y':
        # Determine day-of-year values
        start_date = datetime.datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
        # Determine the last day of the year
        end_date = datetime.datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
        num_days = (end_date - start_date).days + 1
        day_numbers = list(range(1, num_days + 1))
        date_list = [(start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]

        red_values = [red_dict.get(d, 0) for d in date_list]
        speed_values = [speed_dict.get(d, 0) for d in date_list]

        plt.figure(figsize=(12,5))
        plt.plot(day_numbers, red_values, color="red", label="Red Light")
        plt.plot(day_numbers, speed_values, color="orange", label="Speed")
        plt.xlabel("Day of the Year")
        plt.ylabel("Number of Violations")
        plt.title(f"Violations Each Day of {year}")
        plt.legend()
        plt.tight_layout()
        plt.show()

# Find cameras located on a street
def option9(dbConn):
    dbCursor = dbConn.cursor()

    street = input("\nEnter a street name: ")

    sqlRed = "SELECT Camera_ID, Address, Latitude, Longitude FROM RedCameras " \
    "WHERE Address LIKE ? ORDER BY Camera_ID;"
    sqlSpeed = "SELECT Camera_ID, Address, Latitude, Longitude FROM SpeedCameras " \
    "WHERE Address LIKE ? ORDER BY Camera_ID;"

    dbCursor.execute(sqlRed, ("%"+street+"%",))
    rowsRed = dbCursor.fetchall()
    dbCursor.execute(sqlSpeed, ("%"+street+"%",))
    rowsSpeed = dbCursor.fetchall()

    if not rowsRed and not rowsSpeed:
        print("There are no cameras located on that street.")
    else:
        print()
        print("List of Cameras Located on Street:", street)
        print("  Red Light Cameras:")
        for id, addr, lat, lon in rowsRed:
            print(f"     {id} : {addr} ({lat}, {lon})")
        
        print("  Speed Cameras:")
        for id, addr, lat, lon in rowsSpeed:
            print(f"     {id} : {addr} ({lat}, {lon})")
        print()

        p = input("Plot? (y/n) ")
        if p == "y":
            x = []
            y = []

            for _, _, lat, lon in rowsRed:
                x.append(lon)
                y.append(lat)
            
            for _, _, lat, lon in rowsSpeed:
                x.append(lon)
                y.append(lat)

            image = plt.imread("chicago.png")
            xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map
            plt.imshow(image, extent=xydims)

            plt.plot(x, y, 'ro-')
            plt.title("Cameras on Street: "+street)
            for id, _, lat, lon in rowsRed:
                plt.annotate(id, (lon, lat))
            for id, _, lat, lon in rowsSpeed:
                plt.annotate(id, (lon, lat))
            plt.xlim([-87.9277, -87.5569])
            plt.ylim([41.7012, 42.0868])
            plt.show()
    print()

def printMenuOptions():
    print()
    print("Select a menu option: ")
    print("  1. Find an intersection by name")
    print("  2. Find all cameras at an intersection")
    print("  3. Percentage of violations for a specific date")
    print("  4. Number of cameras at each intersection")
    print("  5. Number of violations at each intersection, given a year")
    print("  6. Number of violations by year, given a camera ID")
    print("  7. Number of violations by month, given a camera ID and year")
    print("  8. Compare the number of red light and speed violations, given a year")
    print("  9. Find cameras located on a street")
    print("or x to exit the program.")

def displayInitialMessage():
    print("Project 1: Chicago Traffic Camera Analysis")
    print("CS 341, Fall 2025")
    print()
    print("This application allows you to analyze various")
    print("aspects of the Chicago traffic camera database.")
    print()
    print_stats(dbConn)
    printMenuOptions()





dbConn = sqlite3.connect('chicago-traffic-cameras.db')

displayInitialMessage()

user_input = input("Your choice --> ")

while user_input != "x":
    if(user_input == "1"):
        option1(dbConn)
        printMenuOptions()
    elif(user_input == "2"):
        option2(dbConn)
        printMenuOptions()
    elif(user_input == "3"):
        option3(dbConn)
        printMenuOptions()
    elif(user_input == "4"):
        option4(dbConn)
        printMenuOptions()
    elif(user_input == "5"):
        option5(dbConn)
        printMenuOptions()
    elif(user_input == "6"):
        option6(dbConn)
        printMenuOptions()
    elif(user_input == "7"):
        option7(dbConn)
        printMenuOptions()
    elif(user_input == "8"):
        option8(dbConn)
        printMenuOptions()
    elif(user_input == "9"):
        option9(dbConn)
        printMenuOptions()
    else:
        print("Error, unknown command, try again...")
        printMenuOptions()    
    user_input = input("Your choice --> ")

print("Exiting program.")

