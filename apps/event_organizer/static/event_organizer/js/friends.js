$(document).ready(function(){
    console.log("running friends.js");

    //check first radio button
    $("input[value='first_name']").prop('checked',true)

    // replace placeholder text
    $("input[name=friend_search_type]").on('change',function(){
        input = $("input[name='friend_search']")
        val = $("input[name='friend_search_type']:radio:checked").val()
        if ( val == 'first_name' ) {
            $(input).attr('placeholder',"Friend's First Name");
        } else if (  val == 'last_name' ) {
            $(input).attr('placeholder',"Friend's Last Name");
        }  else {
            $(input).attr('placeholder',"Friend's Email");
        }
    })

    $("input[value='Find Friend']").on('click',function(){
        console.log("find friend clicked");
        val = $("input[name='friend_search_type']:radio:checked").val()
        input = $("input[name='friend_search']").val()
        console.log("input: ",input,"\nval:",val);


        if ( input == "" ) {
            console.log("empty input");
            flashMessage("Input is empty")
            return
        } else {
            console.log("let's do a search on this:", input);
        }
    })
})
