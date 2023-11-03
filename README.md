AccessCheck
Digital Accessibility refers to the practice of building inclusive technologies which are usable by users of diverse abilities. When building web applications, many of them go unchecked for how accessible they are and how well accessibility tools like screen-readers and keyboard navigation software may work with these applications. AccessCheck is a solution designed to make the digital world accessible to all by offering an efficient method to test and enhance the accessibility of any organization's web application
![alt text](https://github.com/RiyanaD/AccessCheck/blob/main/static/AC.home.png)

## Functionality

The user inputs the url link to the web application they would like to recieve a digital accessibility report for. 
![alt text](https://github.com/RiyanaD/AccessCheck/blob/main/static/petSmart.png)
The application sends the inputted url to the flask server with a POST request. The flaskServer retrieves the inputted urls html content and sends it to a python script to flag any violations of Web Content Accessibility Guidelines (WCAG) detected in the html script. The python script utilizes the Beautiful Soup library to parse specific html tags.

Above is the report generated when inputting the petSmart website. 

![alt text](https://github.com/RiyanaD/AccessCheck/blob/main/static/w3school.png)

## Usage instructions
```bash
git clone https://github.com/RiyanaD/AccessCheck.git
python app.py # start the flask server
```
