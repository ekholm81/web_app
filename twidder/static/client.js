window.onload=function(){
    var token=localStorage.getItem("token");
    console.log(token);
    if(localStorage.getItem("token")==""||localStorage.getItem("token")==null){
        var content=document.getElementById("welcomeview");
    }
	else{
        var content=document.getElementById("profileview");      
    } 
    var div=document.getElementById("maindiv");
	div.innerHTML=content.innerHTML;
    var pre=document.getElementById("pre");
    if(pre!=null){
        var res=serverstub.getUserDataByToken(token);
        pre.innerHTML=" Email:      "+res.data.email+"\n\n Firstname:  "+res.data.firstname+"\n Familyname: "+res.data.familyname+"\n\n Gender:     "+res.data.gender+"\n\n City:       "+res.data.city+"\n Country:    "+res.data.country;
    }
    var wall=document.getElementById("wallpre");
    if(wall!=null){
        var res=serverstub.getUserMessagesByToken(token);
        for(i=0;i<res.data.length;i++){
            wall.innerHTML+=" Post "+(i+1)+": "+res.data[res.data.length-1-i].content+"\n\n\n";
        }
    }
};

function validateEmail(email) {
    var regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return regex.test(email);
}

function btnfunc(){
    var e=document.getElementById("email").value;
    var p=document.getElementById("pass").value;
    if(e=="" ||p=="")alert("illegal input!");
    else if(!validateEmail(e))alert("illegal email!");
    else{
        var res=serverstub.signIn(e,p);
        if(res.success==false){
             alert(res.message);
            console.log("res.success=false");
            return;
        }
        else{
            console.log("res.success=true");
            localStorage.setItem('token',res.data);
            alert(res.message);
            console.log("token: "+res.data);
            window.location.reload();
        }
    }
}

function btnfunc2(){
    var d=[];
    d[d.length]=document.getElementById("fn").value;
    d[d.length]=document.getElementById("ln").value;
    d[d.length]=document.getElementById("s").value;
    d[d.length]=document.getElementById("city").value;
    d[d.length]=document.getElementById("country").value;
    d[d.length]=document.getElementById("semail").value;
    d[d.length]=document.getElementById("spass").value;
    d[d.length]=document.getElementById("srpass").value;
    for(i=0;i<d.length;i++){
        if(d[i]==""){
            alert("illegal input!");
            return;
        }
    }
    if(!validateEmail(d[5])){
        alert("invalid email!");
        return;
    }
    if(d[6]!=d[7] || d[6].length<6){
        alert("illegal password!");
        return;
    }
    var obj={email:d[5],
             password:d[6],
             firstname:d[0],
            familyname:d[1],
            gender:d[2],
            city:d[3],
            country:d[4]};
    var res=serverstub.signUp(obj);
    alert(res.message);   
}

function signout(){
    var res=serverstub.signOut(localStorage.getItem("token"));
    if(res.success==true){
        alert(res.message);
        localStorage.removeItem("token");
    }
    else{
        
        alert(res.message);
    }
    window.location.reload();
}

function changepwd(){
    var oldpwd=document.getElementById("oldpwd").value;
    var newpwd=document.getElementById("newpwd").value;
    var reppwd=document.getElementById("reppwd").value;
    if(newpwd!=reppwd){
        alert("Password repetition fail");
        return;
    }
    var res=serverstub.changePassword(localStorage.getItem("token"),oldpwd,newpwd);
    if(res.success==true){
        alert(res.message);
    }
    else{
        alert(res.message);
    }
}

function post(){
    var text=document.getElementById("pb").value;
    var res=serverstub.postMessage(localStorage.getItem("token"),text)
    alert(res.message);
    document.getElementById("pb").value="";
    window.location.reload();
}

function update(){
    window.location.reload();
}

function browse(){
    var email=document.getElementById("bemail").value;
    localStorage.setItem("bemail",email);
    var res=serverstub.getUserDataByEmail(localStorage.getItem("token"),email);
    if(res.success==true){
        var content=document.getElementById("browsehtml");
        document.getElementById("browsetab").innerHTML=content.innerHTML;
         var pre=document.getElementById("bpre");
        if(pre!=null){
            pre.innerHTML=" Email:      "+res.data.email+"\n\n Firstname:  "+res.data.firstname+"\n Familyname: "+res.data.familyname+"\n\n Gender:     "+res.data.gender+"\n\n City:       "+res.data.city+"\n Country:    "+res.data.country;
           
        }  
        var wall=document.getElementById("bwallpre");
        if(wall!=null){
            var res=serverstub.getUserMessagesByEmail(localStorage.getItem("token"),email);
            for(i=0;i<res.data.length;i++){
                wall.innerHTML+=" Post "+(i+1)+": "+res.data[res.data.length-1-i].content+"\n\n\n";
            }
        }   
    }
    else{
        alert(res.message)
    }
}

function bpost(){
    var text=document.getElementById("bpb").value;
    var res=serverstub.postMessage(localStorage.getItem("token"),text,localStorage.getItem("bemail"));
    alert(res.message);
    document.getElementById("bpb").value="";
}

function bupdate() {
    var wall=document.getElementById("bwallpre");
    var res=serverstub.getUserMessagesByEmail(localStorage.getItem("token"),localStorage.getItem("bemail"));
     wall.innerHTML="";
     for(i=0;i<res.data.length;i++){
                wall.innerHTML+=" Post "+(i+1)+": "+res.data[res.data.length-1-i].content+"\n\n\n";
            }
}

function breturn(){
    var content=document.getElementById("browseoriginalhtml");
    document.getElementById("browsetab").innerHTML=content.innerHTML;
}