🚦 Chicago Traffic Camera Analysis

Author: Rudhva Patel

This project analyzes Chicago’s traffic camera database using Python and SQLite.
It provides statistics, insights, and visualizations about red-light and speed cameras across the city.
The program outputs both textual summaries and graphical plots, including camera locations on a real Chicago map.

✨ Features

  ✅ Database Statistics
  
    -> Number of cameras, violations, and coverage dates.
    -> Totals for red-light and speed violations.
  
  ✅ Search & Analysis Tools
  
    -> Find intersections by name.
    -> List cameras at a given intersection.
    -> Percentage breakdown of violations on a specific date.
    -> Violations by year, month, and camera ID.
    -> Compare red-light vs speed violations.
    -> List cameras by street with coordinates.
    
  ✅ Visualization
  
    📊 Line and bar graphs of violations.
    🗺️ Plotted camera locations on a real Chicago map overlay (chicago.png).
    🖼️ Example Outputs

  📂 Database
  
    -> The program uses chicago-traffic-cameras.db, which contains the following main tables:
    -> Intersections – Intersection names and IDs.
    -> RedCameras, SpeedCameras – Camera metadata, addresses, and coordinates.
    -> RedViolations, SpeedViolations – Daily violation counts per camera.

**The following shows an example of the graph outputted for 2023.**
<img width="577" height="444" alt="Screenshot 2025-09-22 at 3 30 08 PM" src="https://github.com/user-attachments/assets/ee7b756c-c09e-40cc-83fd-9a555d62a475" />


**The following is an example of the plotted Cameras on actual coordinates of Chicago streets (option 9):**
<img width="631" height="618" alt="Screenshot 2025-09-22 at 3 29 19 PM" src="https://github.com/user-attachments/assets/8cdd445d-917a-4470-8208-2d4a2168be9c" />
