// JavaScript page for the login form 

/*  Form page 

    Math Placement Test Project

    Designed by: 
        Bruce Keener
        Matteo Filippi
        Mille Berg
*/

function logIn()
{
    var email = document.getElementById("email").value.trim();
    var password = document.getElementById("password").value.trim();

    if (email == "blodgett" && password == "b1") 
    {
        window.open("./pages/mpt_professorView.html");
    } 

    if(email == "bruce" && password == "b2")
        window.open("./pages/mpt_studentView.html", "_blank");

}