$(document).ready(function(){
    $("input[name='date']").val(moment().add(1,'day').format("YYYY-MM-DD"))
    $("input[name='date']").attr('min',moment().add(1,'day').format("YYYY-MM-DD"))


})

function validateForm(){
    console.log("running validateForm");
    start_time = $("input[name='start_time']").val()
    end_time = $("input[name='end_time']").val()

    console.log("start time:", start_time, ", end time:", end_time);

    start_split = start_time.split(":")
    end_split = end_time.split(":")

    start_hour = parseInt(start_split[0])
    end_hour = parseInt(end_split[0])

    diff = end_hour - start_hour
    console.log("diff:",diff);
    if ( diff < 0 ) {
        console.log("end time is before start time.. why?");
        console.log("lets add 24 to end time to see the diff now");
        diff2 = end_hour + 24 - start_hour
        console.log("diff2:",diff2);
        if ( diff2 > 8) {
            flashMessage("Event must be a minimum of 2 hours in length",'danger',6000);
            return false
        }
    }

    // if ( start_time > end_time ) {
    //     flashMessage("start time must be after end time",'danger',6000);
    //     return false
    // }

    if ( ( end_hour - start_hour ) < 2 ) {
        flashMessage("Event must be a minimum of 2 hours in length",'danger',6000);
        return false
    }

    // return true;
    return false;
}
