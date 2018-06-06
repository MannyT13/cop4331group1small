$(document).ready(function(){    
    //for the login error: if user has incorrect username of password
    $('#loginForm').on('submit', function(event){
        
        //when user has a login error we will send the loginError.html  as a json and put in a div using ajax using
        //return jsonify({'resp': render_template('loginError.html', loginError=True)})
        //if the user logged in successfully
        //return jsonify({'resp': 'loggedIn'})
        //must 
        $.ajax({
            url:"/test",
            type: "POST",
            success: function(resp){
                if(resp.resp != "loggedIn")
                 $('div#alertDiv').html(resp.resp);
            }
        });
    });


    //for the registration error: if user has a already taken username and/or two different passwords
    $('#registrationForm').on('submit', function(event){
        
        //when user has a registration error we will send the registrationError.html as a json and put in a div using ajax using
        //return jsonify({'resp': render_template('registrationError.html', usernameTaken=True, passwordMatch=True)})
        //make sure to put the right boolean values
        //if the user registered  successfully
        //return jsonify({'resp': 'registered'})

        $.ajax({
            url:"/test",
            type: "POST",
            success: function(resp){
                if(resp.resp != "registered")
                 $('div#alertDiv').html(resp.resp);
            }
        });
    });


    $('#add_contact_submit').on('click', function(event){
        $.ajax({
            url:"/add_contact",
            type: "POST",
            data: $('#add_contact_form').serialize(),
            success: function(data){
                console.log(data);
                var new_contact = '<tr><td>' + ($('tbody').children().length + 1) + '</td><td>' + data.first_name + '</td><td>\
                ' + data.last_name + '</td><td>' + data.address1 + '</td><td>' + data.address2 + '</td><td>\
                ' + data.email + '</td><td>' + data.phone + '</td><td>' + data.city + '</td></td>' + data.zip + '</td></tr>\
                ' + data.id + '</td></td>';
                $('tbody').append(new_contact);
            }
        });
    });

    $('.remove-button').on('click', function(event){
        var obj = $(this);
        $.ajax({
            url:"/delete_contact",
            type: "POST",
            contentType: 'application/json',
            dataType : 'json',
            data: JSON.stringify($(this).attr('data-button')),
            success: function(data){
                $(obj).closest("tr").remove();
            }
        });
    });
    $('#search').keyup(function() {
function myFunction(){
    var input, filter, table, tr, td, i;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      } 
    }
}
    });








});
