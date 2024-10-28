import csv
import os
import re

def generate_nav_html(directory, team):
   # Initialize an empty list to store HTML links
   links = []
   
   # Determine team path based on parameter
   team_path = f"../{team}/"
   
   # Iterate over the filenames in the directory
   for filename in os.listdir(directory):
      # Check if the file has an HTML extension
      if filename.endswith(".html"):
         # Remove the ID number and .html extension for the link text, leave just the athlete name
         athlete_name = re.sub(r"\d+\.html$", "", filename)
         # Create a hyperlink using the filename
         link = f'<li><a href="{team_path}{filename}">{athlete_name}</a></li>'
         # Add the hyperlink to the list
         links.append(link)
         
   # Join all links with a line break into a single string
   links_html = "\n".join(links)
   # Wrap the links in a <ul> tag
   nav_html = f"<ul>\n{links_html}\n</ul>"
   
   return nav_html


# Get the path to current directory
dir = os.getcwd()

# Generate nav links for men's team
nav_html_content_men = generate_nav_html(dir+"/mens_team", "mens_team")

# Generate nav links for women's team
nav_html_content_women = generate_nav_html(dir+"/womens_team", "womens_team")


def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile):
   # template 
   # Start building the HTML structure
   html_content = f'''<!DOCTYPE html>
   <html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <!-- Get your own FontAwesome ID -->
       <script src="https://kit.fontawesome.com/YOUR_ID.js" crossorigin="anonymous"></script>


      <link rel = "stylesheet" href = "../css/reset.css">
      <link rel = "stylesheet" href = "../css/style.css">
      <link rel="stylesheet"   href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap">

      <title>{data["name"]}</title>
   </head>
   <body>
   <div class="skip-to-main">
   <a href = "#main">Skip to Main Content</a>
   </div>
   <header class="header">
   <div class="logo"> 
      <img src="../images/skyline_logo.jpg" alt="Skyline High School eagle mascot logo">
   </div>
   <nav>
      <ul class="nav-bar">
        <li id="home-btn"><a href="../index.html">Home</a></li>
        
        <li>
         <details class="dropdown">
            <summary>Men's Team</summary>
            {nav_html_content_men}
         </details>
        </li>
        
        <li>
         <details class="dropdown">
            <summary>Women's Team</summary>
            {nav_html_content_women}
         </details>
        </li>     
      </ul>
   </nav>
   </header>
   <header class="profile">
      <!--Athlete would input headshot-->
       <h1>{data["name"]}</h1>
      <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200"> 
   </header>
   <main id = "main">
      <section id= "athlete-sr-table">
         <h2>Athlete's Seasonal Records (SR) By Year</h2>
            <table>
                  <thead>
                     <tr>
                        <th> Year </th>
                        <th> Season Record (SR)</th>
                     </tr>
                  </thead>
                  <tbody>
                  '''
   
   for sr in data["season_records"]:
      sr_row = f'''
                     <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                     </tr>                  
               '''
      html_content += sr_row

   html_content += '''                   
                </tbody>
                  </table>
                     </section>

                     <section id="athlete-result-table">
                        <h2>Race Results</h2>                        

                           <table id="athlete-table">
                              <thead>
                                 <tr>
                                    <th>Race</th>
                                    <th>Athlete Time</th>
                                    <th>Athlete Place</th>
                                    <th>Race Comments</th>
                                 </tr>
                              </thead>

                              <tbody>
                  '''

   # add each race as a row into the race table 
   for race in data["race_results"]:
      race_row = f'''
                                 <tr class="result-row">
                                    <td>
                                       <a href="{race["url"]}">{race["meet"]}</a>
                                    </td>
                                    <td>{race["time"]}</td>
                                    <td>{race["finish"]}</td>
                                     <td>{race["comments"]}</td>
                                 </tr>
      '''
      html_content += race_row

   html_content += '''
                              </tbody>

                        </table>
                     </section>
                     
                     </main>
                     <footer class="footer">
                     <p>
                     Skyline High School<br>
                     <address>
                     2552 North Maple Road<br>
                     Ann Arbor, MI 48103<br><br>

                     <a href = "https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                     Follow us on Instagram 
                     <a href = "https://www.instagram.com/a2skylinexc/" aria-label="Instagram">
                     <i class="fa-brands fa-instagram"></i>
                     </a> 


                     </footer>
               </body>
         </html>
   '''

   with open(outfile, 'w') as output:
      output.write(html_content)


def main():

   import os
   import glob

   # Define the folder path
   folder_path = 'mens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("mens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "mens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")


   # Define the folder path
   folder_path = 'womens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("womens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "womens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")

if __name__ == '__main__':
    main()
