
const selectors = document.getElementById("form-valg");
const hForm = document.getElementById("hovedform");
const smForm = document.getElementById("smallform");
const dagForm = document.getElementById("DagForm");
const forms = document.getElementsByClassName("formses");
const lists = document.getElementsByClassName("listes");


function ChangeForm(){
    for (let i = 0; i < forms.length; i++) {
        forms[i].style.display = "none";
        lists[i].style.display = "none";
    };

    switch(selectors.value){
        case "0":
            forms[0].style.display = "flex";
            lists[0].style.display = "grid";
            // console.log(lists[0])
        break;
        case "1":
            forms[1].style.display = "flex";
            lists[1].style.display = "grid";
            // console.log(lists[1])

        break;
        case "2":
            forms[2].style.display = "flex";
            lists[2].style.display = "grid";
            // console.log(lists[2])
        break;
    };
};

ChangeForm();

function imageSearch(){
    const nameInput = hForm.children
    console.log(nameInput)
    let query = nameInput.value;
    const queryURL = {{ url_for("Scrape", query=query)|tojson }} 

    fetch("{{ url_for('Scrape', query="+query+"}}")
};

