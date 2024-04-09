$(document).ready(function () {
    $('#insert_modal').on('hidden.bs.modal', function () {
        $("#save").val("Save");
        $("#admin_form")[0].reset();
        $("#title").html("Add Admin")
        firstname_span.text("");
        lastname_span.text("");
        phone_span.text("")
        address_span.text("");
        username_span.text("");
        email_span.text("");
        role_span.text("")
        password_span.text("");
        $('#username').removeAttr("disabled");
        $("#email_noti").prop("checked", false);
        document.getElementById('hidediv').style.display="";
    });
});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function windowResizefn(){
	var Wi = jQuery(window).height();
	var HeaderHi = jQuery('.wrapper').innerHeight();
	var BtnHi = jQuery('.bottom-btn-wrapper').innerHeight();
	var innerHi1 = Wi - HeaderHi;
	var innerHi2 = innerHi1 - BtnHi;
	var innerHi3 = innerHi2 - 66;
	jQuery('.form_section').css('height', innerHi3 + 'px');
	console.log('innerHi3', innerHi3);
	
	setTimeout(function(){
		var Wi = jQuery(window).height();
		var HeaderHi = jQuery('.wrapper').innerHeight();
		var BtnHi = jQuery('.bottom-btn-wrapper').innerHeight();
		var innerHi1 = Wi - HeaderHi;
		var innerHi2 = innerHi1 - BtnHi;
		var innerHi3 = innerHi2 - 66;
		jQuery('.form_section').css('height', innerHi3 + 'px');
		console.log('innerHi3', innerHi3);
	},2000);
}
// changes darshan 31-08-2023 3
$('.modal').on('shown.bs.modal', function() {
    $(this).find('[autofocus]').focus();
  });
//   changes darshan 31-08-2023 3 close


    var admin_form = $("#admin_form");
    var first_name = $("#first_name");
    var last_name = $("#last_name");
    var phone     = $("#phone");
    var address   = $("#address");
    var username   = $("#username");
    var email      = $("#email");
    var password  = $("#password");
    var role      =$("#role");

    var firstname_span =$("#firstname_span");
    var lastname_span = $("#lastname_span");
    var phone_span = $("#phone_span");
    var address_span = $("#address_span");
    var username_span  =$("#username_span");
    var email_span  = $("#email_span");
    var password_span =$("#password_span");
    var role_span   =$("#role_span");

    first_name.keyup(firstname_validate)
    email.keyup(email_validated)
    username.keyup(username_validate)



    function firstname_validate(){
        if($("#first_name").val().trim()== ''){
            firstname_span.text("First name required.");
            firstname_span.addClass("error");
            return false
        }else{
            firstname_span.text("");
            firstname_span.removeClass("error");
            return true
        }
    }
    function lastname_validate(){
        if($("#last_name").val().trim() == ''){
            lastname_span.text("Last name required.");
            lastname_span.addClass("error");
            return false
        }else{
            lastname_span.text("");
            lastname_span.removeClass("error");
            return true
        }
    }

    // changes darshan 31-08-2023 1
    // darshan changes bug sheet 3 4-09-2023
    function phone_validate() {
        var phoneInput = $("#phone").val().trim();
        var filter =/^[0-9]+$/
        if (phoneInput === '') {
            phone_span.text("Phone number required.");
            phone_span.addClass("error");
            return false;
        } else if (filter.test(phoneInput)) {
            phone_span.text("");
            phone_span.removeClass("error");
            return true;
        } else {
            phone_span.text("Enter valid Phone number.");
            phone_span.addClass("error");
            return false;
        }
    }
    // darshan changes bug sheet 3 4-09-2023 close
    // changes darshan 31-08-2023 1 close


    // function address_validated(){
    //     if($("#address").val().trim() == ''){
    //         address_span.text("Enter address");
    //         address_span.addClass("error");
    //         return false
    //     }else{
    //         address_span.text("");
    //         address_span.removeClass("error");
    //         return true
    //     }
    // }
    // darshan changes 31-08-2023 2
    function username_validate() {
        var usernameInput = $("#username").val().trim();
        var username_span = $("#username_span"); // Assuming this is where you display the error message

        if (usernameInput === '') {
            username_span.text("Username required.");
            username_span.addClass("error");
            return false;
        } else if (!/^[a-zA-Z]+$/.test(usernameInput)) {
            username_span.text("Only letters are allowed in the username.");
            username_span.addClass("error");
            return false;
        } else {
            username_span.text("");
            username_span.removeClass("error");
            return true;
        }
    }
     // darshan changes 31-08-2023 2 close

    function email_validated(){
        if($("#email").val().trim() == ''){
            email_span.text("Email address required.");
            email_span.addClass("error");
            return false;
        }else{
            var a = $("#email").val();
            var filter = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if(filter.test(a)){
                // console.log("okaaaaaay")
                email_span.text("");
                email_span.removeClass("error");
                return true
            }else{
                // console.log("errorr")
                email_span.text("Enter valid email.")
                email_span.addClass("error")
                return false
            }
        }
    }
    // darshan changes 31-08-2023 3
    // darshan chnages bug shhet 4-09-2023 2

    function password_validate() {
        var passwordInput = $("#password").val().trim();
        if (passwordInput.trim() === '') {
            password_span.text("Password required.");
            password_span.addClass("error");
            return false;
        } else if (passwordInput.length < 8) {
            password_span.text("The password must be at least 8 characters.The password format is invalid.");
            password_span.addClass("error");
            return false;
        } else {
            var strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
            if (strongRegex.test(passwordInput)) {
                // alert("hello")
                password_span.text("");
                password_span.removeClass("error");
                return true;
            } else {
                password_span.text("The password must be at least 8 characters.The password format is invalid.");
                password_span.addClass("error");
                return false;
            }
        }
    }
    // darshan chnages bug shhet 4-09-2023 2 close
    // darshan changes 31-08-2023 3 close
    function role_validate(){
        if($("#role").val().trim() == 0){
            role_span.text("Role required.")
            role_span.addClass("error")
            return false
        }else{
            role_span.text("")
            role_span.removeClass("error")
            return true
        }
    }

function savebtn(){
    var email = $("#email").val()
    var username = $("#username").val()
    var id = $("#id").val()

    if(id == 1){
        if (firstname_validate() & lastname_validate() & phone_validate() //  & // address_validated() &
        & username_validate() & email_validated() & role_validate() ){
            $.ajax({
                type: "post",
                url: WS_PATH+"admin_insert",
                data:$("#admin_form").serialize(),
                success: function (response) {
                    if(response == 0){
                        username_span.html("Username is already taken.").css('color', 'red')
                    }else if(response == 1){
                        email_span.html("Email is already taken.").css('color', 'red')
                    }else{
                        $('#inquiry_msg').show();
                    $("#inquiry_msg" ).html(response);
                    $("#insert_modal").scrollTop(0)
                    setTimeout(function(){ window.location.reload(); }, 2000);
                    }

                }
               });
        }
    }else{
        if (firstname_validate() & lastname_validate() & phone_validate() //  & // address_validated() &
        & username_validate() & email_validated() & password_validate() & role_validate()  ){
            $.ajax({
                type: "post",
                url: WS_PATH+"admin_insert",
                data:$("#admin_form").serialize(),
                success: function (response) {
                    if(response == 0){
                        username_span.html("Username is already taken.").css('color', 'red')
                    }else if(response == 1){
                        email_span.html("Email is already taken.").css('color', 'red')
                    }else{
                        $('#inquiry_msg').show();
                    $("#inquiry_msg" ).html(response);
                    $("#insert_modal").scrollTop(0)
                    setTimeout(function(){ window.location.reload(); }, 2000);
                    }

                }
               });

        }else{
        return false
        }
    }

}
function editbtn(id){
    document.getElementById('hidediv').style.display="none";
    $("#hidediv").addClass("display:none")
    $("#save").val("Update")
    $("#title").html("Update Admin")
    $("#username").attr("disabled", "disabled"); 
    $("#insert_modal").modal('show');
    $.ajax({
        type: "get",
        url: WS_PATH+"editdata/" + id,
        success: function (response) {
            // alert(response)
            $("#id").val(response[0][0]);
            $("#first_name").val(response[0][1])
            $("#last_name").val(response[0][2])
            $("#phone").val(response[0][3])
            $("#address").val(response[0][4])
            $("#username").val(response[0][5])
            $("#email").val(response[0][6])
            $("#password").val(response[0][7])
            $("#role").val(response[0][8])
            
            
            if(response[0][9]=='yes'){
                $('#email_id').show();
                $("#email_noti").prop("checked", true);
            }else{
                $('#email_id').show();
                $("#email_noti").prop("checked", false);
            }
            
        }
    });
    // alert(id)
}
function removebtn(id){
    var a = confirm("Are you sure want to delete this admin?")
    if(a){
       $.ajax({
        type: "Post",
        url: WS_PATH+"removedata/" + id,
        success: function (response) {
            $('#inquiry_msg1').show();
            $( "#inquiry_msg1" ).html(response);
            setTimeout(function(){ window.location.reload(); }, 1500);
        }
       });
    }else{
        return false
    }

}

function diclinebtn(){
    $("#loderscrren").show()

    if(d_name_validate() & d_email_validate() & d_phone_validate() & file2_validation() &file3_validation()  & file4_validation() & why_did_decline() & d_exceptprice_validate()){
        /*var form_data = new FormData();
        form_data.append('d_name',$('#d_name').val())
        form_data.append('d_email',$('#d_email').val())
        form_data.append('d_phone',$('#d_phone').val())
        form_data.append('why_did_decline',$('#why_did_decline').val())
        form_data.append('id',$('#d_id').val())

        var ins = document.getElementById('file-2').files.length;
        console.log(ins)
        var ins2 = document.getElementById('file-3').files.length;
        var ins3 = document.getElementById('file-4').files.length;
        var ins5 = document.getElementById('file-5').files.length;
        for (var x = 0; x < ins; x++) {
            form_data.append("file-2[]", document.getElementById('file-2').files[x]);
         }for (var x = 0; x < ins2; x++) {
            form_data.append("file-3[]", document.getElementById('file-3').files[x]);
         }
        for (var x = 0; x < ins3; x++) {
           form_data.append("file-4[]", document.getElementById('file-4').files[x]);
        }

        for (var x = 0; x < ins5; x++) {
            form_data.append("file-5[]", document.getElementById('file-5').files[x]);
         }*/

        $.ajax({
            type: "Post",
            url:  WS_PATH+"declineinsert",
           /*dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data:form_data,*/
            data: $('#dicline').serialize(),                    
            success: function (response) {
                if(response.status === 'success'){
                    $('#inquiry_msg_error').show();
                    var paramValue = getParameterByName('lang');

                    if(paramValue !== null){
                        if(paramValue == 'es'){
                            $( "#inquiry_msg_error").html("El tipo de archivo no está permitido");
                        }else{
                            $( "#inquiry_msg_error").html("File type is not allowed");
                        }
                    }else{
                        $( "#inquiry_msg_error").html("File type is not allowed");
                    }
                }else{
                    $("#loderscrren").hide()
                    $('#inquiry_msg').show();
                    if(paramValue !== null){
                        if(paramValue == 'es'){
                            $( "#inquiry_msg" ).html('Gracias por proporcionarnos la información. Agradecemos sus comentarios.');
                        }else{
                            $( "#inquiry_msg" ).html('Thank you for providing the information, We appreciate your feedback.');
                        }
                    }else{
                        $( "#inquiry_msg" ).html('Thank you for providing the information, We appreciate your feedback.'); 
                    }
                    $("#DeclineSteppopup").scrollTop(0)
                    setTimeout(function(){
                        $("#DeclineSteppopup").modal('hide')
                        $('#steps_12').hide();
                        $('#steps_18').show();
                        $('body').addClass('finish-step');
                        jQuery("#next-prev-id").hide();
                        windowResizefn();
                    }, 2000);

                    
                }

            }
        });
    }else{
        $("#loderscrren").hide()
        return false
    }

}
function d_name_validate(){
    if($("#d_name").val().trim() == ''){
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#d_name_span").text("Nombre requerido.")
            }else{
                $("#d_name_span").text("Name required.")
            }
        }else{
            $("#d_name_span").text("Name required.")
        }
        $("#d_name_span").addClass("error");
        return false
    }else{
        $("#d_name_span").text("")
        $("#d_name_span").removeClass("error");
        return true
    }
}
function d_email_validate(){
    if($("#d_email").val().trim() == ''){
        console.log("1 out")
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#d_email_span").text("Correo electronico requerido.")
            }else{
                $("#d_email_span").text("Email required.")
            }
        }else{
            $("#d_email_span").text("Email required.")
        }
        $("#d_email_span").addClass("error")
        return false
    }else{
        var a = $("#d_email").val()
        var filter =/^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if(filter.test(a)){
            console.log("1 in")
            $("#d_email_span").text("")
            $("#d_email_span").removeClass("error")
            return true;
        }else{
            console.log("1 getout")
            var paramValue = getParameterByName('lang');

            if(paramValue !== null){
                if(paramValue == 'es'){
                    $("#d_email_span").text("Ingrese un email valido.");
                }else{
                    $("#d_email_span").text("Enter valid Email.");
                }
            }else{
                $("#d_email_span").text("Enter valid Email.");
            }
            $("#d_email_span").addClass("error")
            return false;
        }
    }
}
function d_phone_validate(){
    if($("#d_phone").val().trim()==''){
        console.log("2 out")
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#d_phone_span").text("Se requiere teléfono.")
            }else{
                $("#d_phone_span").text("Phone required.")
            }
        }else{
            $("#d_phone_span").text("Phone required.")
        }
        $("#d_phone_span").addClass("error")
        return false
    }else{
        var a1 = $("#d_phone").val();
        var filter1 = /^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\./0-9]*$/g;
        if(filter1.test(a1)){
            console.log("2 in")

            if (a1.length >= 10) {
                $("#d_phone_span").text("");
                $("#d_phone_span").removeClass("error");
                return true;
            }else{
                var paramValue = getParameterByName('lang');

                if(paramValue !== null){
                    if(paramValue == 'es'){
                        $("#d_phone_span").text("Ingrese un mínimo de 10 dígitos del número de teléfono.");
                    }else{
                        $("#d_phone_span").text("Enter minimum 10 digit of Phone number.");
                    }
                }else{
                    $("#d_phone_span").text("Enter minimum 10 digit of Phone number.");
                }
                $("#d_phone_span").addClass("error");
                return false
            }
        }else{
            console.log("2 getout")
            var paramValue = getParameterByName('lang');

            if(paramValue !== null){
                if(paramValue == 'es'){
                    $("#d_phone_span").text("Ingrese un número de teléfono válido.");
                }else{
                    $("#d_phone_span").text("Enter valid Phone number.");
                }
            }else{
                $("#d_phone_span").text("Enter valid Phone number."); 
            }
            $("#d_phone_span").addClass("error");
            return false
        }
    }
}

function d_exceptprice_validate(){
    if($("#except_price").val().trim()==''){
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#d_except_price_span").text("Precio esperado requerido.")
            }else{
                $("#d_except_price_span").text("Expected price required.")
            }
        }else{
            $("#d_except_price_span").text("Expected price required.")
        }
        $("#d_except_price_span").addClass("error")
        return false
    }else{
        var a1 = $("#except_price").val();
        var filter1 = /^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s\./0-9]*$/g;
        if(!filter1.test(a1)){
            
            var paramValue = getParameterByName('lang');

            if(paramValue !== null){
                if(paramValue == 'es'){
                    $("#d_except_price_span").text("Introduzca sólo el valor numérico.");
                }else{
                    $("#d_except_price_span").text("Enter only number value.");
                }
            }else{
                $("#d_except_price_span").text("Enter only number value.");
            }
            $("#d_except_price_span").addClass("error");
            return false
        }else{

            $("#d_except_price_span").text("");
            $("#d_except_price_span").removeClass("error");
            return true;
        }
    }
}

function file2_validation(){
        var selectedFiles = $("#file-2")[0].files;
        console.log(selectedFiles)
        if (selectedFiles.length >= 5) {
            var paramValue = getParameterByName('lang');

            if(paramValue !== null){
                if(paramValue == 'es'){
                    $("#d_file2_span").text("Seleccione solo cuatro imágenes.");
                }else{
                    $("#d_file2_span").text("Select only four images.");
                }
            }else{
                $("#d_file2_span").text("Select only four images.");
            }
            $("#d_file2_span").addClass("error");
            return false;
        }else{
            $("#d_file2_span").text("");
            $("#d_file2_span").removeClass("error");
            return true;
        }

}

function file3_validation(){
    var selectedFiles1 = $("#file-3")[0].files;
    if (selectedFiles1.length >= 2) {
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#d_file3_span").text("Seleccione solo una imagen.");
            }else{
                $("#d_file3_span").text("Select only one image.");
            }
        }else{
            $("#d_file3_span").text("Select only one image.");
        }
        $("#d_file3_span").addClass("error");
        return false;
    }else{
        $("#d_file3_span").text("");
        $("#d_file3_span").removeClass("error");
        return true;
    }
}
function file4_validation(){
    var selectedFiles2 = $("#file-4")[0].files;
    if (selectedFiles2.length >= 2) {
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#d_file4_span").text("Seleccione solo una imagen.");
            }else{
                $("#d_file4_span").text("Select only one image.");
            }
        }else{
            $("#d_file4_span").text("Select only one image.");
        }
        $("#d_file4_span").addClass("error");
        return false;
    }else{
        $("#d_file4_span").text("");
        $("#d_file4_span").removeClass("error");
        return true;
    }
}

function decline_getdata(){
    var record_id = $('#record_id').val();
    $.ajax({
        type: "get",
        url: WS_PATH+"decline_data/" + record_id,
        success: function (response) {
            // alert(response[0][1])
            $("#d_name").val(response[0][22])
            $("#d_phone").val(response[0][24])

        }
    });
}

function why_did_decline(){
    if($("#why_did_decline").val() == ''){
        var paramValue = getParameterByName('lang');

        if(paramValue !== null){
            if(paramValue == 'es'){
                $("#why_did_decline_error").text("Indique el motivo para rechazar esta oferta.")
            }else{
                $("#why_did_decline_error").text("Please provide reason for declining this offer.")
            }
        }else{
            $("#why_did_decline_error").text("Please provide reason for declining this offer.")
        }
        $("#why_did_decline_error").addClass("error");
        return false
    }else{
        $("#why_did_decline_error").text("")
        $("#why_did_decline_error").removeClass("error");
        return true
    }

}


function ragiser_button() {
    $("#raister_popup").modal("show");
}
function ragister_form_save(){
    if(first_name_ragister_validate() & last_name_ragister_validate() & phone_ragister_validate() & username_span_ragister() & email_span_ragister() & password_ragister_validate()){
        $.ajax({
            type: "POST",
            url: WS_PATH+"admin_insert",
            data:$("#ragister_form").serialize(),
            success: function (response) {
                if(response == 0){
                    $('#ragister_success_error').show();
                    $("#ragister_success_error").html("Username is already taken.")
                }else if(response == 1){
                    $('#ragister_success_error').show();
                    $("#ragister_success_error").html("Email is already taken.")
                }else{
                    user_email_send()
                    /*$('#ragister_form')[0].reset();
                     $('#ragister_success').show();
                     $("#ragister_success" ).html("Ragister Successfully");
                     setTimeout(function(){ window.location.reload(); }, 2000);*/
                }

            }
        });
        return true;
    }else{
        return false;
    }
};

function first_name_ragister_validate(){
    if($("#first_name_ragister").val().trim() == ''){
       $("#firstname_span_ragister").text("This field is required.")
       $("#firstname_span_ragister").addClass("error")
        return false;
    }else{
       $("#firstname_span_ragister").text("")
       $("#firstname_span_ragister").removeClass("error")
        return true;
    }
};

function last_name_ragister_validate() {
    if($("#last_name_ragister").val().trim() == ''){
        $("#lastname_span_ragister").text("This field is required.")
        $("#lastname_span_ragister").addClass("error")
         return false;
     }else{
        $("#lastname_span_ragister").text("")
        $("#lastname_span_ragister").removeClass("error")
        return true;
    }
}

function phone_ragister_validate() {
    if($("#phone_ragister").val().trim() == ''){
        $("#phone_span_ragister").text("This field is required.")
        $("#phone_span_ragister").addClass("error")
         return false;
     }else{
        var a = $("#phone_ragister").val();
        var filter = /^[0-9-+]+$/;
        if (filter.test(a)) {
            if (a.length >= 10) {
                $("#phone_span_ragister").text("");
                return true;
            } else {
                $("#phone_span_ragister").text("Enter valid phone number.");
                $("#phone_span_ragister").addClass("error")
                return false;
            }
        }else{
            $("#phone_span_ragister").text("Enter valid phone number.");
            $("#phone_span_ragister").addClass("error")
            return false;
        }
    }
}
function username_span_ragister(){
    if($("#username_ragister").val().trim() == ''){
        $("#username_span_ragister").text("This field is required.")
        $("#username_span_ragister").addClass("error")
        return false;
     }else{
        $("#username_span_ragister").text("")
        $("#username_span_ragister").removeClass("error")
        return true;
    }
}

function email_span_ragister(){
    if($("#email_ragister").val().trim() == ''){
        $("#email_span_ragister").text("This field is required.")
        $("#email_span_ragister").addClass("error")
        return false
    }else{
        var a = $("#email_ragister").val();
        var filter = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if(filter.test(a)){
            $("#email_span_ragister").text("");
            $("#email_span_ragister").removeClass("error");
            return true
        }else{
            
            $("#email_span_ragister").text("Enter valid email.")
            $("#email_span_ragister").addClass("error")
            return false
        }
    }
}

function password_ragister_validate() {
    var passwordInput = $("#password_ragister").val().trim();
    if (passwordInput.trim() === '') {
         $("#password_span_ragister").text("This field is required.");
         $("#password_span_ragister").addClass("error");
        return false;
    } else if (passwordInput.length < 8) {
         $("#password_span_ragister").text("The password must be at least 8 characters.The password format is invalid.");
         $("#password_span_ragister").addClass("error");
        return false;
    } else {
        var strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        if (strongRegex.test(passwordInput)) {
        
             $("#password_span_ragister").text("");
             $("#password_span_ragister").removeClass("error");
            return true;
        } else {
             $("#password_span_ragister").text("The password must be at least 8 characters.The password format is invalid.");
             $("#password_span_ragister").addClass("error");
            return false;
        }
    }
 }

 function user_email_send(){
    console.log('hello mail sent soce');

    var url = WS_maillib+'/twincities-email.php';
    $.ajax({
        url:url,
        data: $('#ragister_form').serialize(),
        type: 'POST',
        success: function (response) {
           /*console.log(response)
             $("#transport_succemsg").show();
             $("#transport_succemsg").html('Mail successfully sent');*/
        }
    });
    return false;
    }

