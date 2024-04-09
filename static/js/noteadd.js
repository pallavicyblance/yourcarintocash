$(document).ready(function(){
	getnotes();
});

function notesubmit() {
    $("#notesubmit_button").attr("disabled", true);
        if(validation_notes()){
            
             $("#loadingdieditvvehicle").show();
            $.ajax({
                type: "POST",
                url:WS_PATH+"notesadd",
                data:$("#createAccountForm").serialize(),
                success: function (response) {
                    var data = JSON.parse(response)
                    getnotes();
                    if(data.status){
                        $("#notefile").hide()
                        $("#createAccountForm")[0].reset()
                        $("#notes_add").show()
                        $("#file").val("");
                        $("#notes_add").html("Note added successfully.")
                        setTimeout(function(){
                        $("#notes_add").hide()
                        $("#notes_add").html("")
                        $("#notesubmit_button").attr("disabled", false);
                        },3000)
                    }else{

                    }
                     $("#loadingdieditvvehicle").hide();
                }
            });
        }else{
            $("#notesubmit_button").attr("disabled", false);
        }
}
function validation_notes(){
    if($('#notes').val().trim() == ''){
       $("#notes_error").text("This field is required.");
       $("#notes_error").addClass("error");
        return false;
    }else{
       $("#notes_error").text("");
       $("#notes_error").removeClass("error");
        return true;
    }
}


function getnotes(){
    var inquiry_id =  $("#inquiry_id").val()
    var user_id = $("#user_id").val()
    console.log("user id " +user_id)
    $.ajax({
        type: "GET",
        url:  WS_PATH+'get-notes/'+inquiry_id,
        success: function (response) {

            var data1 = response.data;
            var str ='';
            var role = $("#role_id").val()
            // console.log(data1)
            data1.forEach(file => {
                var divcall = ' odd';
                if(user_id == file[2]){
                    var divcall = ' even';
                }
                str += 	'<li class="col-lg-7'+divcall+'">';
                    str += 	'<div class="notes-content">';
                    str +=	'<b class="note_name">'+ file[6]+ '</b>'
                    str +=	'<span class="notes-detail-info w-100">'+formatDatetimechange(file[5]) + '</span>'
                    str +=	'<p><span id="file_name">'+file[3] + '</span>';
                        if(role == 'Super Admin'){
                            str += '<i class="fa fa-close" onclick="deletenote(' + file[0] + ')"></i>'
                        }
                        if(file[4] !=""){
                            if(getFileExtension(file[4]) == 'pdf' ){
                                str += '<div class="upload-images-box vehicle-img"><a href="/dev-carcash/static/images/icon/'+file[4]+'"  download><img class="" alt="" src="/dev-carcash/static/images/icon/pdf.png" width="100px"></a></div>'
                                //imag.append(str);
                            }else if(getFileExtension(file[4]) == 'txt'){
                                 str += '<div class="upload-images-box vehicle-img"><a href="/dev-carcash/static/images/icon/'+file[4]+'"  download><img class="" alt="" src="/dev-carcash/static/images/icon/txt.png" width="100px"></a></div>'
                                //imag.append(str);
                            }else if (getFileExtension(file[4]) == 'docx' || getFileExtension(file[4]) == 'doc'){
                                str += '<div class="upload-images-box vehicle-img"><a href="/dev-carcash/static/images/icon/'+file[4]+'"  download><img class="" alt="" src="/dev-carcash/static/images/icon/text-icon.png" width="100px"></a></div>'
                                //imag.append(str);
                            }else if(getFileExtension(file[4]) == 'wps' ){
                                str += '<div class="upload-images-box vehicle-img"><a href="/dev-carcash/static/images/icon/'+file[4]+'"  download><img class="" alt="" src="/dev-carcash/static/images/icon/wps.png" width="100px"></a></div>'
                                //imag.append(str);
                            }
                            else if(getFileExtension(file[4]) == 'png' || getFileExtension(file[4]) == 'jpg' || getFileExtension(file[4]) == 'jpeg' || getFileExtension(file[4]) == 'gif'){
                                str += '<div class="upload-images-box vehicle-img"><a rel="prettyPhoto[notegallery]" href="/dev-carcash/static/images/'+file[4]+'""><img rel="prettyPhoto[notegallery]" src="/dev-carcash/static/images/'+file[4]+'" width="100px"></div></a>'
                                //imag.append(str);
                            }else{
                                    str +='<a rel="prettyPhoto[notegallery]" href="/dev-carcash/static/images/'+ file[4]+'"><img src="/dev-carcash/static/images/'+ file[4]+'" id="notefile" alt="Your Image1" /></i></a>'
                                }
                        }
                    str +='</p>';
                    str +=	'</div>';
                str +=	'</li>';
                if(str ==''){
                       str += '<li class="col-lg-7">';
                          str += '<div class="notes-content">No Record</div>';
                       str += '</li>';
                    }
                $("#note_table").html(str);
            })
        }
    });
}

function deletenote(id){
    a = confirm("Are you sure want to delete note?")
    if(a){
        $.ajax({
            type: "POST",
            url: WS_PATH+'notes-delete/'+id,
            success: function (response) {
                var data = JSON.parse(response)
                    getnotes();
                if(data.status){
                    // getnotes()
                    $("#notes_add").show()
                    $("#notes_add").html("Note deleted successfully.")
                    setTimeout(function(){
                        window.location.reload()
                    $("#notes_add").hide()
                    $("#notes_add").html("")
                    },3000)
                }else{

                }
            }
        });
    }
}

function statuses_update(data){
    var id = $("#inquiry_id").val()
    $.ajax({
        type: "POST",
        url: WS_PATH+'update_status/',
        data: {data : data , id:id},
        success: function (response) {
            var data = JSON.parse(response)
                if(data.status){
                    $("#notes_add1").show()
                    $("#notes_add1").html("Status Updated successfully.")
                    setTimeout(function(){
                    $("#notes_add1").hide()
                    $("#notes_add1").html("")
                    },3000)
                }
        }
    });
  }

jQuery(document).ready(function (e) {
    jQuery('#filenote').change(function(){
    
       note_file_upload();
    });
 });

 function note_file_upload(){

    var form_data = new FormData();

          var errormsg = $('#fileerrormsg');
          var ins = document.getElementById('filenote').files.length;
        console.log(ins)
          var getphotinput = $("#file");
          var imageadd = $('#uploadfile');
          var imag = $('#notefile');
          var imag1= $('#notefile1')

    if(ins == 0) {
       // errormsg.html('<span style="color:red">Select at least one file</span>');
       return;
    }
    for (var x = 0; x < ins; x++) {
        form_data.append("files[]", document.getElementById('filenote').files[x]);
    }

    var url = WS_PATH +'file-upload'; //local working

    var getphot = getphotinput.val();
    $("#loadingdieditvvehicle").show();
    $.ajax({
       url: url, // point to server-side URL
       dataType: 'json', // what to expect back from server
       cache: false,
       contentType: false,
       processData: false,
       data: form_data,
       type: 'post',
       success: function (response) {
          // console.log("darshan + " + response)
       var phot ='';
          var  i = $('#uploadfile .file').length;
             $.each(response, function (key, data) {
                console.log("darshan  " +  key)
                if(data == '1') {
                   phot += key+''
                   if(getFileExtension(key) == 'pdf'){
                     imag.attr('src','/dev-carcash/static/images/icon/pdf.png');
                     imag.show();
                   }else if (getFileExtension(key) == 'txt'){
                      imag.attr('src','/dev-carcash/static/images/icon/txt.png');
                      imag.show();
                   }else if (getFileExtension(key) == 'docx' || getFileExtension(key) == 'doc'){

                      imag.attr('src','/dev-carcash/static/images/icon/text-icon.png');
                      imag.show();
                   }else if (getFileExtension(key) == 'wps'){

                      imag.attr('src','/dev-carcash/static/images/icon/wps.png');
                      imag.show();
                   }
                   else{
                      imag.attr("src", "/dev-carcash/static/images/" +key); //local working
                      i++;
                      imag.show();
                   }
                    $("#loadingdieditvvehicle").hide();

                } else {
                   errormsg.append('<span class="text-danger mt-1 d-block message_error" > File type (<b>'+key+'</b>) is not allowed </span>');

                   setTimeout(function(){ errormsg.html(''), $("#loadingdieditvvehicle").hide(); }, 4000);
                }
             })

          // getphotinput.val(getphot+phot);

          getphotinput.val(phot);
       },
       error: function (response) {
          errormsg.html(response.message); // display error response
       }
    });
}


function getFileExtension(filename)
{
  var ext = /^.+\.([^.]+)$/.exec(filename);
  return ext == null ? "" : ext[1];
}


function formatDatetimechange(dbDateFormat) {
    // const dbDateFormat = "2023-08-24 16:28:00";
    const dateObject = new Date(dbDateFormat);   
    const formattedDate = new Intl.DateTimeFormat('en-US', {
        timeZone: 'US/Central',
        weekday: 'long', month: 'short', day: 'numeric', year: 'numeric',
        hour: 'numeric', minute: 'numeric', hour12: true
    }).format(dateObject);
    return formattedDate;
    console.log(" " + formattedDate);
}

// console.log("darshan "  + formatDatetimechange("2023-11-07 04:27:11"))