var objPeople = [ 
    {
        username: "sam",
        password: "1234"
    },
    {
        username: "balls",
        password: "4321"
    },
    {
        username: "daniel",
        password: "69420"
    },
]

function getInfo() {
    var username = document.getElementById("username").value
    var password = document.getElementById("password").value
    
    for(i = 0; i < objPeople.length; i++){
        if(username == objPeople[i].username && password == objPeople[i].password){
            console.log(username + " is logged in")
        }
    }
}