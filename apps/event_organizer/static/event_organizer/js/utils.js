function flashMessage(message,type,duration) {
    console.log("duration:",duration);
    $("#flashMessage").html('')

    var time = 3000;
    if ( duration != undefined ) {
        time = duration;
    }

    var html = '';

    if ( typeof(message) == 'array' ) {
        for (var i = 0; i < message.length; i ++ ) {
            html += "<center class='alert alert-" + (type != undefined ? type : "error") + "'>" + message[i] + "</center>";
        }
    } else {
        html += "<center class='alert alert-" + (type != undefined ? type : "danger") + "'>" + message + "</center>";
    }
    $("#flashMessage").html(html);
    $("#flashMessage").slideDown('slow',function(){
        setTimeout(function(){
            $("#flashMessage").slideUp('slow')
        },time)
    })
}
