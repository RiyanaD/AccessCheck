AccessCheck
Digital Accessibility refers to the practice of building inclusive technologies which are usable by users of diverse abilities. When building web applications, many of them go unchecked for how accessible they are and how well accessibility tools like screen-readers and keyboard navigation software may work with these applications. AccessCheck is a solution designed to make the digital world accessible to all by offering an efficient method to test and enhance the accessibility of any organization's web application
![alt text](https://github.com/RiyanaD/AccessCheck/blob/main/static/AC.home.png)

##Functionality
The user inputs the url link to the web application they would like to recieve a digital accessibility report for. 
![alt text](https://github.com/RiyanaD/AccessCheck/blob/main/static/petSmart.png)
The application sends the inputted url to the flask server with a POST request. The processUrl function in the flaskServer retrieves the urls html content and sends it to my python script to file to
