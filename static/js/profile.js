
const quotes = ["Love is Commitment ",
                 "True Love is eternal, infinite and always like itself",
                 "Everything you can imagine is real",
                 "A life lived I love will never be dull",
                 "The best thing to hold onto in life is each other.",
                 "It's always better when we're together.",
                 "A life lived I love will never be dull",
                 "The best thing to hold onto in life is each other.",
                 "It's always better when we're together.",
                 "True Love is eternal, infinite and always like itself"

];
let x = Math.floor((Math.random()*10));
const change_quote= document.getElementById("quotes");
change_quote.innerHTML = quotes[x]; 