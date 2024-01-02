const loginElement = document.querySelector('#login-form');
const contentElement = document.querySelector("#content-sign-in");
const userDetailsElement = document.querySelector('#user-details');
const authBarElement = document.querySelector("#authentication-bar");

// Elements for sensor readings
const tempElement = document.getElementById("temp");
const humElement = document.getElementById("hum");
const motElement = document.getElementById("mot");

// Storage element




// MANAGE LOGIN/LOGOUT UI
const setupUI = (user) => {
  if (user) {
    //toggle UI elements
    loginElement.style.display = 'none';
    contentElement.style.display = 'block';
    authBarElement.style.display ='block';
    userDetailsElement.style.display ='block';
    userDetailsElement.innerHTML = user.email;

    // get user UID to get data from database
    var uid = user.uid;
    console.log(uid);


    // Database references
    var dbRefTemp = firebase.database().ref('Temperature');
    var dbRefHum = firebase.database().ref('Humidity');
    var dbRefMot = firebase.database().ref('time');

    // Update page with new readings
    dbRefTemp.on('value', snap => {
      tempElement.innerText = snap.val().toFixed(2);
    });

    dbRefHum.on('value', snap => {
      humElement.innerText = snap.val().toFixed(2);
    });

    dbRefMot.on('value', snap => {
      motElement.innerText = snap.val().toFixed(2);
    });

    //one
    $('#List').find('tbody').html('');
      var i = 0;
      storageRef.listAll().then(function(result){
        result.items.forEach(function(imageRef){
          i++;
          displayImage(i, imageRef)
        });
      });

      function displayImage(row, images){
        images.getDownloadURL().then(function(url){
          console.log(url);
          let new_html='';
          new_html+='<tr>';
          new_html+='<td>';
          new_html+=row;
          new_html+='</td>';
          new_html+='<td>';
          new_html+='<img src="'+url+'" width="100px" style="float:right">';
          new_html+='</td>';
          new_html+='</tr>';
          $('#List').find('tbody').append(new_html);
        });
      }
      //one



  // if user is logged out
  } else{
    // toggle UI elements
    loginElement.style.display = 'block';
    authBarElement.style.display ='none';
    userDetailsElement.style.display ='none';
    contentElement.style.display = 'none';
  }
}

