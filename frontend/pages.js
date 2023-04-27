// current page

//results = {{ results }}

var page = 0;

let sections_per_page = 10;

let length_results = 100; // {{ len(results) }}


function show_page() {
    var allResultsDiv = document.getElementById('all-results');
    
    for (i=0; i<sections_per_page; i++) {
        // Create a new section element
        var newSection = document.createElement('section');
        
        // Create and add the h1 and p elements inside the section element
        var bookHeader = document.createElement('h1');
        bookHeader.innerText = 'book';
        newSection.appendChild(bookHeader);
        
        var chapterHeader = document.createElement('h1');
        chapterHeader.innerText = 'chapter';
        newSection.appendChild(chapterHeader);
        
        var versePara = document.createElement('p');
        versePara.innerText = 'verse';
        newSection.appendChild(versePara);
        
        // Append the new section to the all-results div
        allResultsDiv.appendChild(newSection);
    }
}


function next_page() {
    if (length_results/10 > page) {
        page++;
    }
}

function back_page() {
    if (page > 0) {
        page--;
    }
}