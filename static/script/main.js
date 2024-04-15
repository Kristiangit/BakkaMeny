
const d = new Date();
let day = d.getDay();

let Focus_Day = day -1;
if (Focus_Day > 4){         // I helgen så viser den retten for Mandag
    Focus_Day = 0;
};
console.log(Focus_Day)
let Left_Day = Focus_Day - 1;
let Right_Day = Focus_Day + 1;
let gone = false;

const main = document.getElementById("main");
const prev = document.getElementById("dag1");
const next = document.getElementById("dag3");

const LeftPlan = prev.getElementsByClassName("left");
const RightPlan = next.getElementsByClassName("next");
const FocusedPlan = main.getElementsByClassName("focus");

let WeekPlan =[
    Mon_Plan =[
        day = "Mandag",
        dish = "Pasta",
        price = "kr 40,-",
    ],
    Tue_Plan =[
        day = "Tirsdag",
        dish = "Lasagne",
        price = "kr 40,-",
    ],
    Wed_Plan =[
        day = "Onsdag",
        dish = "Hamburger",
        price = "kr 45,-",
    ],
    Thu_Plan =[
        day = "Torsdag",
        dish = "Lasagne",
        price = "kr 45,-",
    ],
    Fri_Plan =[
        day = "Fredag",
        dish = "Pastasalat",
        price = "kr 45,-",
    ],
];
console.log(WeekPlan)
WeekPlan = DagPlan

CheckSide();
ChangeDays();

prev.addEventListener("click", function() {
    console.log(Focus_Day, "lll")
    if (Focus_Day == 4 && gone == true) {
        next.style.display = "flex";
        gone = false;
        Right_Day = 5;
    };
    if (Focus_Day > 0) {
        Focus_Day -= 1;
        Right_Day -= 1;
        Left_Day -= 1;
    };

    CheckSide();
    ChangeDays();
});

next.addEventListener("click", function() {
    console.log(Focus_Day, "rrr")
    if (Focus_Day == 0 && gone) {
        prev.style.display = "flex";
        gone = false;
        Left_Day = -1;
    };
    if (Focus_Day < 4) {
        Focus_Day += 1;
        Left_Day += 1;
        Right_Day += 1;
    };
    CheckSide();
    ChangeDays();
});

function ChangeDays() {
    if (gone == false){
        for (let i = 0; i < 3; i++) {
            FocusedPlan[i].textContent = WeekPlan[Focus_Day][i];
            // if (i != 3) {
                LeftPlan[i].textContent = WeekPlan[Left_Day][i];
                RightPlan[i].textContent = WeekPlan[Right_Day][i];
            // }
        }
    } else if (gone && Focus_Day == 4) {
        for (let i = 0; i < 3; i++) {
            FocusedPlan[i].textContent = WeekPlan[Focus_Day][i];
            // if (i != 3) {
                LeftPlan[i].textContent = WeekPlan[Left_Day][i];
            // }
        }
    } else if (gone && Focus_Day == 0) {
        console.log(FocusedPlan, Focus_Day)
        for (let i = 0; i < 3; i++) {
            console.log("focus, ", i)
            FocusedPlan[i].textContent = WeekPlan[Focus_Day][i];
            // if (i != 3) {
                RightPlan[i].textContent = WeekPlan[Right_Day][i];
            // }
        }
    }
};

function CheckSide(){
    if (Right_Day > 4 && gone == false) {
        next.style.display = "none";
        gone = true;
    };
    if (Left_Day < 0 && gone == false) {
        prev.style.display = "none";
        gone = true;
    };
};
