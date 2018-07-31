$('#loginID, #password').bind('keyup', function() {
    if(allFilled())
        $('#user_login').removeAttr('disabled');
    else
        $('#user_login').prop("disabled", true);
});

function allFilled() {
    var filled = true;
    $('body input').each(function() {
        if($(this).val() == '') filled = false;
    });
    return filled;
}