$( document ).ready(function() {
    // code for login page
    $('.ui.checkbox')
        .checkbox();

    $('.ui.input').on('focus click', 'input', function() {
        // fadeout messages html
         $.when($('.messages').fadeOut('slow'))
            .done(function() {
                // after fadeout remove html
                $('.messages').html('');
          });

    });

    // make login button clickable with ajax call
    $('form .submit.button')
        .api({
            action: 'login',
            method: 'POST',
            serializeForm: true,
            beforeSend: function(settings) {
                // set segment on loading before send
                $('.ui.form.segment').addClass('loading');
                return settings;
            },
            onComplete: function(response) {
                // always called after XHR complete
                $('.ui.form.segment').removeClass('loading');
            },
            onSuccess: function(response) {
                // call only on success
                $('.ui.dimmer').addClass('active');
                setTimeout(function() {
                    window.location.href = response.redirect;
                }, 250);
            },
            onFailure: function(response) {
                $.when($('.messages').html(''))
                    .done(function() {
                    // after fadeout remove html
                    $('.messages').hide().append(response.messages).fadeIn('slow');
                });

            }
        });

});

// hotkeys
$(document).keypress(function(e) {
    if(e.which == 13) {
    // simulate search button click on return
        loginButtonClickable();
    }
});

function loginButtonClickable() {



}
