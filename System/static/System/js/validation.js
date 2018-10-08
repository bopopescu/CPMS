
function validatePass()
    {
        var pass1= document.getElementById('password').value;
        var pass2= document.getElementById('pwd1').value;
        if(pass1!=pass2){
            alert("Password does not match");
        }

    }

    function validateName(name)
    {

        var x= document.getElementById(name).value;
        if(!/^[a-zA-Z]*$/g.test(x))
        {
            document.getElementById(name).value="";
        }
    }

    function validatePercentage(marks)
    {
        var x=document.getElementById(marks).value;

        if(/^[0-9.]*$/g.test(x) && x < 100)
        {

        }
        else
        {
             document.getElementById(marks).value="";
        }

    }


 function validateContact(num) {

    var x=document.getElementById(num).value;

    if(isNaN(x))
    {
        document.getElementById(num).value="";
    }

 }


  function validateBigFields(name)
    {

        var x= document.getElementById(name).value;
        if(!/^[a-zA-Z' ']*$/g.test(x))
        {
            document.getElementById(name).value="";
        }
    }