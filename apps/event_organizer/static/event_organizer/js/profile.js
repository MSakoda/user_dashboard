$(document).ready(function(){
    console.log("running profile.js");

    // add or remove 'required' if address field is empty or not
    $("#addressForm input").on('change',function(){
        console.log("something changed");

        // gather inputs
        address = {
            'street' : $("input[name=street]").val(),
            'street2' : $("input[name=street2]").val(),
            'city' : $("input[name=city]").val(),
            'state' : $("select[name=state]").val(),
            'zipcode' : $("input[name=zipcode]").val(),
        }

        // check if address form is empty
        addressIsEmpty = true;
        for ( key in address ) {
            console.log("key:",key,"\nval:",address[key]);
            if ( address[key] != '' ) {
                addressIsEmpty = false;
            }
        }

        // set fields to required if input happened or not if no input
        for ( key in address ) {
            if (key != 'street2'){
                $('input[name="'+key+'"]').prop('required', !addressIsEmpty)
            }
        }
            $("select[name='state']").prop('required', !addressIsEmpty)

    })

    // add remove 'required' if phone is empty or not
    $("input[name='phone']").on('change',function(){
        phone = $("input[name='phone']")
        console.log("phone has changed.\nvalue:",phone.val());
        if ( phone.val() != '' ) {
            console.log("phone has a value, make required");
            phone.attr('required',true)
        } else {
            console.log("phone has no value, not required");
            phone.attr('required',false)
        }
    })

    $("center").on('click',function(){
        console.log("clicked a center");
        $(this).slideUp('slow',function(){
            $(this).remove()
        })
    })

    // select user's state


})
