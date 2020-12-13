$("form[name=signup_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

$("form[name=login_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

$("form[name=google-signin]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/loginGoogle",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

$("form[name=mood_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/makemoodchanges",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

$("form[name=genre_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/makegenrechanges",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

$("form[name=google_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/loginGoogle",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});