
let accessViolationsData = {};

document.getElementById("urlForm").addEventListener("submit", function(event) {
    event.preventDefault(); 
    const url = document.getElementById("url").value; // get entered URL
    console.log('URL:', url); 
    fetch('/process_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'url=' + encodeURIComponent(url),
    })
    .then(response => response.text())
    .then(data => {
    const parsedData = JSON.parse(data);
    accessViolationsData = parsedData;
    // check if there are imageAlt issues
    if (parsedData["Image without alt attribute"]) {
        // show the accessibility div
        const imageAltDiv = document.getElementById("imageAltDiv");
        imageAltDiv.style.display = "block";

    } else {
        // hide the accessibility div if there are no issues
        const imageAltDiv = document.getElementById("imageAltDiv");
        imageAltDiv.style.display = "none";
    }

    if (parsedData["lang attribute present in the HTML document."] == false) {
        // show the languageDiv
        const languageDiv = document.getElementById("languageDiv");
        languageDiv.style.display = "block";
        languageDiv.innerHTML = "<h2>Language Issue</h2>";
        languageDiv.innerHTML += "<p>" + "lang attribute not present in the HTML document." + "</p>";
    } else {
        // Hide the languageDiv if there are no issues
        const languageDiv = document.getElementById("languageDiv");
        languageDiv.style.display = "none";
    }

    if (parsedData["Form element without corresponding label"]) {
        // Show the languageDiv
        const formLabelsDiv = document.getElementById("formLabelsDiv");
        formLabelsDiv.style.display = "block";
        // formLabelsDiv.innerHTML = "<h2>Language Issue</h2>";
        // languageDiv.innerHTML += "<p>" + "lang attribute not present in the HTML document." + "</p>";
    } else {
        // hide languageDiv if there are no issues
        const formLabelsDiv = document.getElementById("languageDiv");
        formLabelsDiv.style.display = "none";
    }

    if (parsedData["Non-descriptive links"]){
        const linkDescriptionDiv = document.getElementById("linkDescriptionDiv");
        linkDescriptionDiv.style.display = "block";
    } else {
        // Hide the languageDiv if there are no issues
        const linkDescriptionDiv = document.getElementById("linkDescriptionDiv");
        linkDescriptionDiv.style.display = "none";
    }

    })
    .catch(error => {
        console.error('Error:', error);
    });
});

let currentModalTarget = null; // Track the current target button
const moreInfoButtons = document.getElementsByClassName("more-info-button");
for (const button of moreInfoButtons) {
    button.addEventListener("click", function(event) {
        // Get the title from the "data-title" attribute of the button
        const title = this.getAttribute("data-title");
        // Call the showMoreInfo function with the event and title as arguments
        showMoreInfo(event, title);
    });
}

// Function to show the modal with more info
function showMoreInfo(event, title) {
    console.log("HII");
    const modal = document.getElementById("moreInfoModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalList = document.getElementById("modalList");

    // Set the modal title
    modalTitle.innerText = title;

    // Get the list of violations for the selected issue
    const violations = accessViolationsData[title];
    let listItems = '';
    for (const violation of violations) {
        listItems += "<li>" + violation.tag + " (Line " + violation.line_number + ")</li>";
    }
    modalList.innerHTML = listItems;
    console.log(listItems);
    // Show the modal
    modal.style.display = "block";

    const button = event.target;
    if(button){
        const dataTitle = button.getAttribute("data-title");
        console.log(dataTitle);
    }
    const accessibilityDiv = button.parentElement;
    console.log(accessibilityDiv); 

    const accessibilityDivRect = accessibilityDiv.getBoundingClientRect();

    console.log("Top:", accessibilityDivRect.top);
    console.log("Right:", accessibilityDivRect.right);
    modal.style.top = accessibilityDivRect.top + 'px';
    modal.style.left = accessibilityDivRect.right + 10 + 'px';

    // store the current target button in the global variable
    currentModalTarget = button;
}

function closeModal() {
    const modal = document.getElementById("moreInfoModal");
    modal.style.display = "none";
}

// event listener to close  modal when clicking outside of it
document.addEventListener("click", function(event) {
    if (event.target !== currentModalTarget) {
        closeModal();
    }
});