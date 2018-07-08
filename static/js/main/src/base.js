$( document ).ready(function() {

    wordCloud();

    // init tab
    $('.pointing.menu .item').tab();

    // fixing right menu tab handling
    $('.right.menu .item').on('click', function() {
        $('.pointing.menu .item').removeClass('active');
        $(this).addClass('active');
    });

    $('.pointing.menu .item').on('click', function() {
        $('.pointing.menu .item').removeClass('active');
        $(this).addClass('active')
    });

    $('.pointing.menu .header.item').on('click', function() {
        $(this).removeClass('active')
    });

    $('div').on('click', '.messagebox', function() {
        // remove messagebox on click
        $.when($('.messagebox').fadeOut('slow'))
            .done(function() {
                // after fadeout remove html
                $('.messagebox').html('');
          });

    });

    /**

        This section describe the code for the SEARCH

    **/

    // async search api behaviour
    $('.ui.projectsearch.button')
        .api({
            action: 'search',
            on: 'click',
            method: 'POST',
            dataType: 'html',
            urlData: {
                query: getSearchPromptValue
            },
            onComplete: function(response) {
              // always called after XHR complete
              // nice
              $('.ui.image').transition({
                animation: 'tada',
                duration: '1s'
              });

              // append html to result class tag
              $.when($('.results').append(response))
                    .done(function() {
                    // append response to html
                    refreshResponse();
               });
            }
    });

    $('.ui.today.button')
        .api({
            action: 'today',
            on: 'click',
            method: 'POST',
            dataType: 'html',
            beforeSend: function() {
                // refresh search table
                $('.results').html('<br>');
                refreshResponse();
            },
            onComplete: function(response) {
              // append html to result class tag
              $.when($('.results').append(response))
                    .done(function() {
                    // append response to html
                    refreshResponse();
               });
            }
    });
    /**

        This section describe the code for the ADMIN Tab

    **/

    // admin tab ajax call
    $('#admin').tab({
        alwaysRefresh: true,
        cache: false,
        apiSettings: {
            action: 'admin',
            method: 'POST',
            dataType: 'html',
            beforeSend: function(settings) {
                // set segment on loading before send
                $('#admintab').addClass('loading');
                return settings;
            },
            onResponse: function(response) {
              // make some adjustments to response
              return response;
            },
            onComplete: function(response) {
                $.when($('#admintab').removeClass('loading'))
                    .done(function() {
                    // append response to html
                    $('').append(response);
               });
            }

        }

    });

    // delegate function for register buttons
    $(document).on('click', '.ui.button', function() {

        // AJAX API for accept
        $('.ui.accept.button').api({
            action: 'approval',
            method: 'POST',
            data: {
                access: true,
                dn: getDataId(this)
            },
            beforeSend: function(settings) {
            // set segment on loading before send
                return settings;
            },
            onComplete: function(response) {
                // fadeout after response
                $.when($(this).parent().closest('.card').fadeOut('slow'))
                    .done(function() {
                    // after fadeout remove html
                    $(this).parent().closest('.card').html('');
                });
            }
        });

        // AJAX API for deny
        $('.ui.deny.button').api({
            action: 'approval',
            method: 'POST',
            data: {
                access: false,
                dn: getDataId(this)
            },
            beforeSend: function(settings) {
                // set segment on loading before send
                return settings;
            },
            onComplete: function(response) {
                // fadeout after response
                $.when($(this).parent().closest('.card').fadeOut('slow'))
                    .done(function() {
                    // after fadeout remove html
                    $(this).parent().closest('.card').html('');
                });
            }
        });

    });


    // delegate tab menu in admin section
    $(document).on('mouseover mouseout', '.vertical.menu .item', function() {

        // init tab
        $('.vertical.menu .item').tab();

        // init dropdown
        $('.ui.dropdown').dropdown({
            transition: 'scale',
            action: 'activate',
            onChange: function(val, text, choice) {
                sendDropdownRole(val, text, choice);
            }
        });

    });

    $(document).on('mouseover mouseout', '.ui.ban.button', function() {

        $('.ui.ban.button').api({
            action: 'change ban',
            on: 'click',
            method: 'POST',
            data: {
                dn: getUserByElement(this),
                ban: true
            },
            beforeSend: function(settings) {
                return settings;
            },
            onComplete: function(response) {
                $(this).parent().closest('.card').fadeOut('slow');
                $('#admin').click();
            }
        });

    });

    $(document).on('mouseover mouseout', '.ui.activate.button', function() {

        $('.ui.activate.button').api({
            action: 'change ban',
            on: 'click',
            method: 'POST',
            data: {
                dn: getUserByElement(this),
                ban: false
            },
            beforeSend: function(settings) {
                return settings;
            },
            onComplete: function(response) {
                $(this).parent().closest('.card').fadeOut('slow');
                $('#admin').click();
            }
        });

    });

    /**

        This section describe the code for the COCKPIT Tab

    **/

    // admin tab ajax call
    $('#cockpit').tab({
        alwaysRefresh: true,
        cache: false,
        apiSettings: {
            action: 'cockpit',
            method: 'POST',
            dataType: 'html',
            beforeSend: function(settings) {
                // set segment on loading before send
                $('#cockpittab').addClass('loading');
                return settings;
            },
            onResponse: function(response) {
              return response;
            },
            onComplete: function(response) {
                $.when($('').append(response))
                    .done(function() {
                    // append response to html
                    setTimeout(function() {
                        // Re-Render Cockpit after AJAX Call
                        renderCockpit();
                    }, 1);

               });
            }
        }

    });

    // delegate function for cockpit buttons
    $(document).on('mouseover mouseout', '.plus.square.outline.icon', function() {

        // AJAX API for add
        $('.plus.square.outline.icon').api({
            action: 'cockpit-add',
            method: 'POST',
            on: 'click',
            data: {
                oid: getDataId(this)
            },
            beforeSend: function(settings) {
            // set segment on loading before send
                return settings;
            },
            onComplete: function(response) {
                // fadeout after response
                $.when($(this).removeClass('blue plus square outline'))
                    .done(function() {
                        $(this).addClass('green checkmark box');
                });
            }
        });

    });

    // delegate function for cockpit TAB
    $(document).on('mouseover', '#cockpit-secondary.menu .item', function() {

        // init sub-tab
        $('#cockpit-secondary.menu .item').tab();

    });


    /**

        This section describe the code for the USER Tab

    **/

    // delegate refresh button
    $(document).on('mouseover mouseout', '.refresh.profile', function() {

        $('div .refresh.profile').api({
            action: 'refresh profile',
            method: 'POST',
            beforeSend: function(settings) {
                // set segment on loading before send
                setTimeout(function() {
                    $('.refresh icon').addClass('loading');
                }, 500)

                return settings
            },
            onComplete: function(response) {
                // refresh user profile card
                $.when($('.refresh icon').removeClass('loading'))
                    .done(function() {
                        $('.messagebox').hide().append(response.html).fadeIn('slow');
                });
            }
        });

    });

});

/**

    This section describe the custom functions

**/


function sendDropdownRole(val, text, choice) {
    /**

        AJAX Call for change_role on Dropdown change

    **/
    $.ajax({
        url: '/change_role',
        type: 'POST',
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: 'json',
        data: {
            role: val,
            user: getUserByElement(choice)
        }
    })

}

function sendDropdownCockpitAction(val, text, choice) {
    /**

        AJAX Call for change_role on Dropdown change

    **/
    $.ajax({
        url: 'cockpit/action',
        type: 'POST',
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: 'json',
        data: {
            action: val,
            oid: getProjectByElement(choice)
        }
    })

}

function sendDropdownCockpitUser(val, text, choice) {
    /**

        AJAX Call for change_role on Dropdown change

    **/

    $.ajax({
        url: 'cockpit/change_user',
        type: 'POST',
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: 'json',
        data: {
            user: text,
            oid: getProjectByElement(choice)
        }
    })

}

function saveNotice(oid) {
    // AJAX Call for save notice
    var element = "#input-" + oid;

    $("#i-" + oid).addClass('loading');

    $.ajax({
        url: 'cockpit/update',
        type: 'POST',
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType: 'json',
        data: {
            value: $(element).val(),
            oid: oid
        },
        complete: function() {
            // fadeout after response
            setTimeout(function() {
                $("#i-" + oid).removeClass('loading');
            }, 500);

        }
    })

}

function getUserByElement(element) {
    var dn = $(element).parent().closest('.card').attr('data-id');
    return dn;
}

function getProjectByElement(element) {
    var oid = $(element).parent().closest('.content').attr('data-id');
    return oid;
}

function stickyContext() {
    // sticky menu
    $('.ui.sticky').sticky({
        context: '#basecontent'
    });
}

function tableAccordion(){
    $('.accordion').accordion();
}

function tableSortFunction(){
    $('table').tablesort();
}


// get data-id attribute from button
function getDataId(element) {
    return $(element).attr('data-id');
}

function getValue(element) {
    var value = $(element).attr('value');
    return value;
}

// function for search input value
function getSearchPromptValue() {
    var result = $('.search.prompt').val();
//    $('.search.prompt').val('');
    $('.results').html('<br>');
    return result;
}

function refreshResponse() {
    stickyContext();
    tableAccordion();
    tableSortFunction();
    flask_moment_render_all();
}

function renderCockpit() {
    tableAccordion();
    tableSortFunction();
    flask_moment_render_all();

    // init dropdown
    $('.ui.dropdown.action').dropdown({
        transition: 'scale',
        onChange: function(val, text, choice) {
            sendDropdownCockpitAction(val, text, choice);

            // change dropdown color
            if (text == 'OPEN') {
                $(this).removeClass('grey green yellow orange');
                $(this).addClass('green');
            } else if (text == 'WIP') {
                $(this).removeClass('grey green yellow orange');
                $(this).addClass('yellow');
            } else if (text == 'ASSIGNED') {
                $(this).removeClass('grey green yellow orange');
                $(this).addClass('orange');
            } else if (text == 'CLOSED') {
                $(this).removeClass('grey green yellow orange');
                $(this).addClass('grey');
            }

        }
    });

    // init dropdown
    $('.ui.dropdown.user').dropdown({
        transition: 'scale',
        onChange: function(val, text, choice) {
            sendDropdownCockpitUser(val, text, choice);

        }
    });

    $('#cockpit-secondary.menu .item.active').on('click', function() {
        $('#cockpit').trigger('click');
    });

    $('#cockpittab').removeClass('loading')
    console.log('Rerendering Cockpit after AJAX Call');
}

// hotkeys
$(document).keypress(function(e) {
    if(e.which == 13) {
    // simulate search button click on return
        $('.ui.projectsearch.button').click();
    }
})
