
 jQuery(document).ready(function (e) {
   jQuery('#file-2').change(function(){
      inventoryuploadfile('file-2');
   });
});

jQuery(document).ready(function (e) {
   jQuery('#file-3').change(function(){
      inventoryuploadfile('file-3');
   });
});

jQuery(document).ready(function (e) {
   jQuery('#file-4').change(function(){
      inventoryuploadfile('file-4');
   });
});
jQuery(document).ready(function (e) {
   jQuery('#file-5').change(function(){
      inventoryuploadfile('file-5');
   });
});

 function inventoryuploadfile(id){
   var form_data = new FormData();
      if(id == 'file-2') {
         var errormsg = $('#d_file2_span');
         var ins = document.getElementById('file-2').files.length;
         var getphotinput = $("#hidden_file-2");
         var noi = 4;
       }else if(id == 'file-3'){
         var errormsg = $('#d_file3_span');
         var ins = document.getElementById('file-3').files.length;
         var getphotinput = $("#hidden_file-3"); 
         var noi = 1;
      }else if(id == 'file-4'){
         var errormsg = $('#d_file4_span');
         var ins = document.getElementById('file-4').files.length;
         var getphotinput = $("#hidden_file-4"); 
         var noi = 1;
      }else if(id == 'file-5'){
         var errormsg = $('#d_file5_span');
         var ins = document.getElementById('file-5').files.length;
         var getphotinput = $("#hidden_file-5");   
         var noi = 1;
      }else{
         //$("#loadingdieditvvehicle").show();
         var errormsg = $('#inventoryimageerrormsg');
         var ins = document.getElementById('file-3').files.length;
         var getphotinput = $("#hidden_file-3");
         var noi = 1;
      }
     
       if(id == 'file-2') {
         if (ins >= 5) {
            errormsg.html('<span style="color:red">Select only four images.</span>');
            return 
         }else{
            
            var aa = getphotinput.val();
            var arr = aa.split(",");
            var a1 = (arr.length - 1) + ins;
            if(a1>=5){
               errormsg.html('<span style="color:red">Select only four images.</span>');
               return 
            }
         }
      }

      if(ins == 0) {
         //errormsg.html('<span style="color:red">Select at least one file</span>');
         return;
      }

      for (var x = 0; x < ins; x++) {
         if(id == 'file-2') {
            form_data.append("files[]", document.getElementById('file-2').files[x]);
         }else if(id == 'file-3'){
            form_data.append("files[]", document.getElementById('file-3').files[x]);
         }else if(id == 'file-4'){
            form_data.append("files[]", document.getElementById('file-4').files[x]);
         }else if(id == 'file-5'){
            form_data.append("files[]", document.getElementById('file-5').files[x]);
         }
      }
       errormsg.html('');

      $("#loadingdieditvvehicle").show();
      var url = WS_PATH+'ajax-image-upload';
      
      if(id == 'file-2') {
         var getphot = getphotinput.val();
      }else{
         var getphot = '';   
      }
      $.ajax({
         url: url, // point to server-side URL
         dataType: 'json', // what to expect back from server
         cache: false,
         contentType: false,
         processData: false,
         data: form_data,
         type: 'post',
         success: function (response) {
         var phot ='';
            var  i = $('#editinventoryimage .vehicle-img').length;
            $.each(response, function (key, data) {
               if(data == '1') {
                     phot += key+','
                  i++;
               } else {
                  errormsg.append('<span class="text-danger mt-1 d-block message_error" > File type is not allowed <b>'+key+'</b></span>');
               }
            })
            //alert(phot);
            //alert(getphot+phot);
            getphotinput.val(getphot+phot);
             if(id == 'file-2') {
                 getimages(2)
               }else if(id == 'file-3'){
                  getimages(3)
               }else if(id == 'file-4'){
                  getimages(4)
               }else if(id == 'file-5'){
                   getimages(5)
               }

         },
         error: function (response) {
            errormsg.html(response.message); // display error response
         }
      });
 }


 function getimages(id){
  // console.log(id);
      if(id == '2') {
         var getphotinput = $("#hidden_file-2");
         var imageadd = $('#image-previews');
      }else if(id == '3'){
         var getphotinput = $("#hidden_file-3");
         var imageadd = $('#image-previews1');
      }else if(id == '4'){
         var getphotinput = $("#hidden_file-4");
         var imageadd = $('#image-previews2');
      }else if(id == '5'){
         var getphotinput = $("#hidden_file-5");
         var imageadd = $('#image-previews5');

      }
      
      var vehicle_photo = getphotinput.val();
      var vehiclephoto =vehicle_photo.split(",");
      var str = '<div id="image-previews" class="upload-image">';
      var i = 0;
      imageadd.html('');
      $.each(vehiclephoto, function (key, data) {
         if(data !=""){
            var ids = 'uploadimages_'+id+'_'+i;
            var str = '<div class="upload-images-box vehicle-img" id="uploadimages_'+id+'_'+i+'" ><img class="img-preview" alt="" src="https://yourcarintocash.com/dev-carcash/static/images/'+data+'" ><i fa-close="" class="fa fa-close vclose" onclick="delete_images('+ i +','+id+')"></i></div>';
            imageadd.append(str);
            i++;
         }
      });
      
      $("#loadingdieditvvehicle").hide();
 }

 function delete_images(imaid,id){
   var result = confirm("Are you sure! You want to delete this vehicle photo? ");
	if (result) {
      if(id == '2') {
         var getphotinput = $("#editvehicle_photo");
        // var imageadd = $('#editinventoryimage');
      }else{
         var getphotinput = $("#vehicle_photo");
        // var imageadd = $('#inventoryimage');
      }


      if(id == '2') {
         var getphotinput = $("#hidden_file-2");
         var imageadd = $('#image-previews');
      }else if(id == '3'){
         var getphotinput = $("#hidden_file-3");
         var imageadd = $('#image-previews1');
      }else if(id == '4'){
         var getphotinput = $("#hidden_file-4");
         var imageadd = $('#image-previews2');
      }else if(id == '5'){
         var getphotinput = $("#hidden_file-5");
         var imageadd = $('#image-previews5');
      }



      var vehicle_photo =getphotinput.val();
      var vehiclephoto =vehicle_photo.split(",");
      var photostr = '';
      $.each(vehiclephoto, function (key, data) {
         if(data !="" && key == imaid ){
            $("#uploadimages_"+key).remove();
         }else{
            if(data !=""){
               photostr += data +','
            }
         }
      });
         getphotinput.val(photostr);        
         getimages(id);
   }else{

   }
 }
