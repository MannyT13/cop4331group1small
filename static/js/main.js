$(document).ready(function(){    
    $('#add_contact_submit').on('click', function(event){
        $.ajax({
            url:"/add_contact",
            type: "POST",
            data: $('#add_contact_form').serialize(),
            success: function(data){
                console.log(data);
                var new_contact = '<tr><td>' + data.first_name + '</td><td>\
                ' + data.last_name + '</td><td>\
				' + data.phone + '</td><td>' + data.email + '</td><td><button type="button" class="btn btn-danger btn-sm remove-button" data-button="\
				' + data.id + '"><span class="glyphicon glyphicon-remove" href="#"></span> Delete Contact </button></td></tr>';
                $('tbody').append(new_contact);
            }
        });
    });

    $('.update-contact-submit').on('click', function(event){
        $.ajax({
            url:"/update_contact",
            type: "POST",
            data: $(this).parent().serialize(),
            success: function(data){
                console.log('successful update')
                // var new_contact = '<tr><td>' + ($('tbody').children().length) + '</td><td>' + data.first_name + '</td><td>\
                // ' + data.last_name + '</td><td>' + data.address1 + '</td><td>' + data.address2 + '</td><td>\
                // ' + data.email + '</td><td>' + data.phone + '</td><td>' + data.city + '</td><td>\
                // ' + data.zip + '</td><td><button class="remove-button" type="button" class="btn btn-default btn-sm" data-button="\
                // ' + data.id + '"><span class="glyphicon glyphicon-remove" href="#"></span> Remove </button></td></tr>';
                // $('tbody').append(new_contact);
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

    $('#searchContact').on('input', function(event){
        var input = $('#searchContact').val().toLowerCase()
        $('.my-data').each(function(){
            first = this.getAttribute('first').toLowerCase();
            last = this.getAttribute('last').toLowerCase();
            
            str = first + last;
            if(first.indexOf(input) == -1) $(this).hide()
            else $(this).show()

        });
    });

});
