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

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
$(function(){
    
    
    $('#mileage').keyup(function(){

		$('#utv').prop('checked', false);
		$('#mileage_label').removeClass('greyed-out');
	});

	$('#utv').change(function(){
		if ($(this).is(":checked")) {
			console.log("Checkbox is checked");
			$('#mileage').val('');
			$('#mileage_label').addClass('greyed-out');
		}else{
			$('#mileage_label').removeClass('greyed-out');
		}
	});
	
	$("#year_drop").change(function () {

	    var no_load= $('#no_load').val();

		if(no_load!='yes'){
		    //$("#loadingdiv").show();
		}
		$('#make_drop').val('').trigger('change');
		$('#model_drop').val('').trigger('change');
		var year = this.value;
		if (year) {
			get_model(1,year);
		}
	});
	windowResizefn();

	$(window).resize(function () {
		windowResizefn();
	});
	$("#make_drop").change(function () {
		var make = this.value;
		var no_load= $('#no_load').val();
		if (make) {
			var year = $("#year_drop").val();
			var make = $(this).find(':selected').data("id");
			var make_code = $(this).find(':selected').data("code");
			console.log('make_code', make_code);
			$("#make_id").val(make);
			$("#make_code").val(make_code);
			if(no_load!='yes'){
			//$("#loadingdiv").show();
			}
			get_make(1,year, make)

		}
	});


	$("#model_drop").change(function () {
		var model = this.value;
		if (model) {
			var model = $(this).find(':selected').data("id");
			$("#model_id").val(model);
			//setTimeout(function(){
			var aaa = $('#currenttab').val();
			if(aaa=='1'){
				$('#next').trigger('click');
                $('body').removeClass('offer_amount_step');
                windowResizefn();
                $('#newvinset').html('');
			}
			//},1000);
		}
	});

	$("#prev").click(function(){
		var id = $("#currenttab").val();
		jQuery("body").removeClass('thankyou-laststep-body');
		prevsteps(id);
	});

	$("#next").click(function(){
	    jQuery("body").removeClass('thankyou-laststep-body');
		var tabid = $("#currenttab").val();
		var paramValue = getParameterByName('lang');
		//alert(tabid);
		if($("#currenttab").val() == 1){
				if($("#year_drop").val() == '' || $("#make_drop").val() == '' || $("#model_drop").val() == ''){
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_1").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_1").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_1").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_1").addClass("alert alert-danger");
				}else{
					$("#prev").removeAttr("disabled");
					$(".circletab_2").addClass("active");
					jQuery(".steps").hide();
					jQuery("#steps_2").show();
					$("#currenttab").val(2)	;
					$("#steps_error_1").text("");
					$("#steps_error_1").removeClass("alert alert-danger");
	                    $(".circletab_1").addClass("complete");
	                    var make_name = $("#make_drop").find(":selected").text();
	                    var model_name = $("#model_drop").find(":selected").text();
	                    var my_year = $("#year_drop").find(":selected").text();

	                    $('.make_name').html(make_name);
	                    $('.my_model').html(model_name);
	                    $('.my_year').html(my_year);
	                    $('.model_name').html(model_name);
						var title =  $(".circletab_2").html();
						$("#progressive-text").html(title);

	                    autoinquirybid(1);
					}
		}else if ($("#currenttab").val() == 2) {
			var l = $("#v_zip_code").val();
			if($("#v_zip_code").val() == ''){
					console.log('1122');
					//$("#steps_error_2").text("Please enter a valid input");
					var ab = $('#no_load').val();
					if(ab!='yes'){
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_2").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_2").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_2").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_2").addClass("alert alert-danger");
					}
				}else{
					if(l.length!=5){
						if(paramValue !== null){
							if(paramValue == 'es'){
								$("#steps_error_2").text("Ingrese un código postal válido de 5 dígitos.");
							}else{
								$("#steps_error_2").text("Please enter a valid 5-digit zip code.");
							}
						}else{
							$("#steps_error_2").text("Please enter a valid 5-digit zip code.");
						}
						$("#steps_error_2").addClass("alert alert-danger");
					}else{
						//$('.car-tires-areas').hide();
						var zip_value = $("#v_zip_code").val();
						var record_id = $("#record_id").val();
						$.ajax({
							type: 'POST',
							url: WS_PATH + "get_location_using_zip",
							data: { v_zip: zip_value, record_id: record_id },
							success: function (responses) {
								var response = JSON.parse(responses);
								if(response.status){
									console.log(response['data'])
									console.log('in')
									var cityname = capitalizeFLetter(response['data'][2]);
									var statename = capitalizeFLetter(response['data'][3]);
									$('#pdamagediv').show();
									$('#d_title').show();
				          			$('#d_title1').hide();
									$("#v_zip_code").val(response['data'][1])
									$("#v_zip1").val(response['data'][1])
									$("#cityinput").val(cityname)
									$('#states_drop').val(response['data'][3]).trigger('change');
									$("#user_city").val(cityname)
									$("#user_state").val(statename)
									insert_location_using_zip()
									$('#d_subtitle').show();
	          						$('#d_subtitle1').hide();
									nextsteps(tabid);
								}else{
									//$("#v_zip_code").val('')
									if(paramValue !== null){
										if(paramValue == 'es'){
											$("#steps_error_2").text("Ingrese un código postal de EE. UU. válido (5 dígitos).");
										}else{
											$("#steps_error_2").text("Please enter a valid (5-digit) USA ZIP code.");
										}
									}else{
										$("#steps_error_2").text("Please enter a valid (5-digit) USA ZIP code.");
									}
									$("#steps_error_2").addClass("alert alert-danger");
								}
							}
						});
					}
				}
		}else if ($("#currenttab").val() == 3) {
			console.log('1122');
			 if ($('input[name="utv"]:checked').length == 0 && $("#mileage").val()=='' ) {
					console.log('in');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_3").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_3").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_3").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_3").addClass("alert alert-danger");
				}else{
					//nextsteps(tabid);
					if($("#mileage").val()=='0' || $("#mileage").val()=='00' || $("#mileage").val()=='000'){
						if(paramValue !== null){
							if(paramValue == 'es'){
								$("#steps_error_3").text("Por favor ingrese un número positivo válido.");
							}else{
								$("#steps_error_3").text("Please enter valid positive number.");
							}
						}else{
							$("#steps_error_3").text("Please enter valid positive number.");
						}
						$("#steps_error_3").addClass("alert alert-danger");
					}else{
						nextsteps(tabid);
					}
				}
		}else if ($("#currenttab").val() == 4) {
		 	if ($('input[name="damage"]:checked').length == 0) {
				console.log('1122');
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_4").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
					}else{
						$("#steps_error_4").text("The field cannot be left blank. Please enter the required information.");
					}
				}else{
					$("#steps_error_4").text("The field cannot be left blank. Please enter the required information.");
				}
				$("#steps_error_4").addClass("alert alert-danger");
			}else{
				var radioValue = $("input[name='damage']:checked").val();
				console.log(radioValue);
				if(radioValue=='Yes'){
					nextsteps(4,'Yes')
				}else{
					nextsteps(4,'no')
				}
			}
		}else if ($("#currenttab").val() == 5) {

			var radioValue = $("input[name='damage']:checked").val();
			//alert(radioValue)
			if(radioValue=='Yes'){
			 	if ($('input[name="damageimg[]"]:checked').length == 0) {
					console.log('1122');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_5").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_5").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_5").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_5").addClass("alert alert-danger");
				}else{

					nextsteps(tabid);
				}
			}else{
				nextsteps(tabid+1);
			}
		}else if ($("#currenttab").val() == 6) {

			if ($('input[name="airbag"]:checked').length == 0 ) {
				console.log('in');
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_6").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
					}else{
						$("#steps_error_6").text("The field cannot be left blank. Please enter the required information.");
					}
				}else{
					$("#steps_error_6").text("The field cannot be left blank. Please enter the required information.");
				}
				$("#steps_error_6").addClass("alert alert-danger");
			}else{
				console.log('form_signin_add');
				nextsteps(tabid);
			}
		}else if ($("#currenttab").val() == 7) {
			console.log('1122');
			 if ($('input[name="drive"]:checked').length == 0) {
					console.log('in');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_7").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_7").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_7").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_7").addClass("alert alert-danger");
				}else{
					nextsteps(tabid);
				}
		}else if ($("#currenttab").val() == 8) {
			 if ($('input[name="sdamage"]:checked').length == 0) {
					console.log('1122');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_8").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_8").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_8").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_8").addClass("alert alert-danger");
				}else{
					nextsteps(tabid);
				}
		}else if ($("#currenttab").val() == 9) {
			 if ($('input[name="key"]:checked').length == 0) {
					console.log('1122');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_9").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_9").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_9").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_9").addClass("alert alert-danger");
				}else{
					nextsteps(tabid);
				}
		}else if ($("#currenttab").val() == 10) {
			 if ($('input[name="title"]:checked').length == 0) {
					console.log('1122');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_10").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_10").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_10").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_10").addClass("alert alert-danger");
				}else{
					nextsteps(tabid);

				}
		}else if ($("#currenttab").val() == 11) {
			console.log('1122');
			 if ($('input[name="fire_damage"]:checked').length == 0 ) {
					console.log('in');
					if(paramValue !== null){
						if(paramValue == 'es'){
							$("#steps_error_11").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
						}else{
							$("#steps_error_11").text("The field cannot be left blank. Please enter the required information.");
						}
					}else{
						$("#steps_error_11").text("The field cannot be left blank. Please enter the required information.");
					}
					$("#steps_error_11").addClass("alert alert-danger");
				}else{
					nextsteps(tabid);
					autoinquirybid(2);
					windowResizefn();
					get_offer_id();
				}
		}else if ($("#currenttab").val() == 12) {
			console.log('form_signin_add 1212');
			nextsteps(tabid);

		} else if ($("#currenttab").val() == 13) {
			if ($("#locationNameinput").val() == ''  || $("#cityinput").val() == '' || $("#states_drop").val() == '') {
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_13").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
					}else{
						$("#steps_error_13").text("The field cannot be left blank. Please enter the required information.");
					}
				}else{
					$("#steps_error_13").text("The field cannot be left blank. Please enter the required information.");
				}
				$("#steps_error_13").addClass("alert alert-danger");
			} else {
				nextsteps(tabid);
				autoinquirybid(2);
				windowResizefn();
				$("#prev").show()
				$("#prev").removeAttr("disabled");
			}
		} else if ($("#currenttab").val() == 14) {
			var numbers = /^[0-9]+$/;
			var p = $("#phoneinput").val();
			var p1 = $("#alternatePhoneinput").val();
			var email = $('#emailinput').val();
			if ($("#fnameinput").val() == '' || $("#phoneinput").val() == '' || $("#emailinput").val() == '') {
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_14").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
					}else{
						$("#steps_error_14").text("The field cannot be left blank. Please enter the required information.");
					}
				}else{
					$("#steps_error_14").text("The field cannot be left blank. Please enter the required information.");
				}
				$("#steps_error_14").addClass("alert alert-danger");
			}else if(!p.match(numbers)){
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_14").text("Por favor ingrese únicamente el valor numérico.");
					}else{
						$("#steps_error_14").text("Please input numeric value only.");
					}
				}else{
					$("#steps_error_14").text("Please input numeric value only.");
				}
				$("#steps_error_14").addClass("alert alert-danger");
			}else if (!isValidEmail(email)) {
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_14").text("Por favor ingrese un formato de correo electrónico válido.");
					} else {
						$("#steps_error_14").text("Please enter a valid email format.");
					}
				} else {
					$("#steps_error_14").text("Please enter a valid email format.");
				}
				$("#steps_error_14").addClass("alert alert-danger");
			} else {
				nextsteps(tabid);
				autoinquirybid(2);
			}
			function isValidEmail(email) {
				var emailPattern = /^[_a-z_A-Z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/;
				return emailPattern.test(email);
			}
		} else if ($("#currenttab").val() == 15) {
			if ($("#ownerFnameinput").val() == '') {
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_15").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
					}else{
						$("#steps_error_15").text("The field cannot be left blank. Please enter the required information.");
					}
				}else{
					$("#steps_error_15").text("The field cannot be left blank. Please enter the required information.");
				}
				$("#steps_error_15").addClass("alert alert-danger");
			} else {
				$('#svg_t').hide();
				var paramValue = getParameterByName('lang');
				if(paramValue !== null){
					if(paramValue == 'es'){
						$('#d_next_btn').text('Entregar');
					}else{
						$('#d_next_btn').text('Submit');
					}
				}else{
					$('#d_next_btn').text('Submit');
				}
				nextsteps(tabid);
				//autoinquirybid(2);

			}
		} else if ($("#currenttab").val() == 16) {
			if ($("#payeeFnameinput").val() == '' ) {
				if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_16").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
					}else{
						$("#steps_error_16").text("The field cannot be left blank. Please enter the required information.");
					}
				}else{
					$("#steps_error_16").text("The field cannot be left blank. Please enter the required information.");
				}
				$("#steps_error_16").addClass("alert alert-danger");
			} else {
				$("#next").attr("disabled", true);
				$("body").addClass('offer_amount_step');
				nextsteps(tabid);
				get_offer_id();
				autoinquirybid(111);
			}
		}
	});

	$('#modelSelectPopup').on('hidden.bs.modal', function () {

	    $("#model_select_msg_error").hide();
		$("#model_select_msg_error").text("");

		var str = '';
		var paramValue = getParameterByName('lang');
		if(paramValue !== null){
			if(paramValue == 'es'){
				str += '<option value="" >Modelo</option>';
			}else{
				str += '<option value="" >Model</option>';
			}
		}else{
			str += '<option value="" >Model</option>';
		}
		$('#model_select_drop').html(str);
	});
});

function hideShow(){

	$('#sdamage_div').show();
}

$("#vip_input").keyup(function() {
  	 var vip = $("#vip_input").val();
     if(vip.length === 17){
     	$('#vin_back_btn').attr("disabled",true);
     	getvipinfo();
     }else{
     	$("#autofill_id").attr("disabled",true);
     	$("body").addClass('offer_amount_step');
     }

    if(vip !="" ){
    	$('#vin_back_btn').attr("disabled",true);
    }
});

	function get_make(id,year, make){
		var model_id ='';
		if(id == 2){
			var model_id = $("#model_id").val();
		}
		var myKeyVals = { year: year, make: make, models: 'models' }
		console.log(myKeyVals);
		$.ajax({
				url: WS_PATH+'getmodel',
				//url: '/getmodel',
				data: myKeyVals,
				type: 'POST',
				success: function (response) {
					var data = JSON.parse(response);
					var data1 = data.model;
					console.log(data1);
					var str = '';
					var paramValue = getParameterByName('lang');
					if(paramValue !== null){
						if(paramValue == 'es'){
							str += '<option value="" >Modelo</option>';
						}else{
							str += '<option value="" >Model</option>';
						}
					}else{
						str += '<option value="" >Model</option>';
					}
					data1.forEach(product => {
						if(model_id == product[3]){
							str += '<option  data-id="'+ product[3] +'" value="' + product[2] + '" selected > ' + product[2] + '</option>';
						}else{
							str += '<option  data-id="'+ product[3] +'" value="' + product[2] + '">' + product[2] + '</option>';
						}

					})
					$('#model_drop').html(str);
					var aaa = $('#no_load').val();
					if(aaa=='no'){
					    $("#model_drop").select2( "open" );
					}
					$("#loadingdiv").hide();


				},
				error: function (error) {
					console.log(error);
				}
			});
	}

	function get_make_new(id,year, make){
		var model_id ='';
		var myKeyVals = { year: year, make: make, models: 'models' }
		console.log(myKeyVals);
		$.ajax({
				url: WS_PATH+'getmodel',
				data: myKeyVals,
				type: 'POST',
				success: function (response) {
					var data = JSON.parse(response);
					var data1 = data.model;
					console.log(data1);
					var str = '';
					var paramValue = getParameterByName('lang');
					if(paramValue !== null){
						if(paramValue == 'es'){
							str += '<option value="" >Modelo</option>';
						}else{
							str += '<option value="" >Model</option>';
						}
					}else{
						str += '<option value="" >Model</option>';
					}
					data1.forEach(product => {
						if(model_id == product[3]){
							str += '<option  data-id="'+ product[3] +'" value="' + product[2] + '" selected > ' + product[2] + '</option>';
						}else{
							str += '<option  data-id="'+ product[3] +'" value="' + product[2] + '">' + product[2] + '</option>';
						}

					})
					$('#model_select_drop').html(str);
				},
				error: function (error) {
					console.log(error);
				}
			});
	}

	function get_model(id,year){
		var myKeyVals = { year: year, makes: 'makes' }
		var make_id ='';
		if(id == 2){
			var make_id =$("#make_id").val();
		}
		$.ajax({
				url: WS_PATH+'getmakes',
				// url: '/getmakes',
				data: myKeyVals,
				type: 'POST',
				success: function (response) {
					var data = JSON.parse(response);
					var data1 = data.makes;
					var str = '';
					var paramValue = getParameterByName('lang');

					if(paramValue !== null){
						if(paramValue == 'es'){
							str += '<option value="" >Hacer</option>';
						}else{
							str += '<option value="" >Make</option>';
						}
					}else{
						str += '<option value="" >Make</option>';
					}
					data1.forEach(product => {
						if(make_id == product[0]){
							str += '<option data-id="'+ product[0] +'" data-code="'+ product[2] +'" value="' + product[1] + '" selected >' + product[1] + '</option>';
						}else{
							str += '<option data-id="'+ product[0] +'" data-code="'+ product[2] +'" value="' + product[1] + '">' + product[1] + '</option>';
						}

					})
					$('#make_drop').html(str);
					var aaa = $('#no_load').val();

					if(aaa=='no'){
					$("#make_drop").select2( "open" );
					}
					$("#loadingdiv").hide();
				},
				error: function (error) {
					console.log(error);
				}
			});
	}

function getvipinfo(){
	$('#vin_back_btn').attr("disabled",true);
	var vip = $("#vip_input").val();
	var settings = {
	  "url": "https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesextended/"+vip+"?format=json",
	  "method": "GET",
	  "timeout": 0,
	  "Content-Type": 'application/json',
	};
	$.ajax(settings).done(function (response) {
	    if(response.Results){
    	    //console.log(response.Results[0]+' nigam1');
    	   	const {Make, Model, ModelYear} = response.Results[0]
    	   	$('#no_load').val('yes');
    	   	if(Make !="" && Model !="" && ModelYear !=""){
    	   		$("#vinmake").html(convert(Make));
    	   		$("#vinmodel").html(convert(Model));
    	   		$("#vinyear").html(ModelYear);
    	   		$("#autofill_id").attr("disabled",false);

    	        //$('#newvinset').html(ModelYear+' '+Make+' '+Model);
    	   		$('#year_drop').val(ModelYear).trigger('change');
    	   $.ajax({
    				url: WS_PATH+'vehicleinfocheck',
    				data: { make : Make, model: Model, modelyear: ModelYear, vehicle: 'vehicleinfo'  },
    				type: 'POST',
    				success: function(responses){
    					//$("#loadingdivaddvehicle").hide();
    					$("#vinmake").html(convert(Make));
    	   		        $("#vinmodel").html(convert(Model));
    			   		$("#vinyear").html(ModelYear);
    			        //$('#newvinset').html(ModelYear+' '+Make+' '+Model);
    			   		$('#year_drop').val(ModelYear).trigger('change');

    			   		 setTimeout(function(){
    			   		    selectMake(Make)

    			            setTimeout(function(){
    				   		     setTimeout( selectModel(Model), 1500);
    				   		     $('#loadingdiv').hide();
    				   		     $("#autofill_id").attr("disabled",true);
    				   		     $('#vin_back_btn').attr("disabled",false);
    				   		 },1100);
    			   		 },1000);
    				},
    				error: function(error){
    					console.log(error);
    				}
    			});
    	   		//selectMakeModel(Make,Model);
    	   		$("#carInfo").show();
    	   		$("#steps_error_01").text("");
    			$("#steps_error_01").removeClass("alert alert-danger");
    			console.log('nigam111');
    	   	}else{
    	   	    console.log('nigam11');
    	   		var paramValue = getParameterByName('lang');
    	   		if(paramValue !== null){
					if(paramValue == 'es'){
						$("#steps_error_01").text("Por favor ingrese un VIN válido");
					}else{
						$("#steps_error_01").text("Please enter a valid VIN");
					}
				}else{
					$("#steps_error_01").text("Please enter a valid VIN");
				}
    			$("#steps_error_01").addClass("alert alert-danger");
    			$("#autofill_id").attr("disabled",true);
    			$('#vin_back_btn').attr("disabled",false);
    			$("body").addClass('offer_amount_step');
    	   	}
	    }else{
	        console.log('nigam1');
	        var paramValue = getParameterByName('lang');
	        if(paramValue !== null){
				if(paramValue == 'es'){
					$("#steps_error_01").text("Por favor ingrese un VIN válido");
				}else{
					$("#steps_error_01").text("Please enter a valid VIN");
				}
			}else{
				$("#steps_error_01").text("Please enter a valid VIN");
			}
    		$("#steps_error_01").addClass("alert alert-danger");
    		$("#autofill_id").attr("disabled",true);
    		$('#vin_back_btn').attr("disabled",false);
    		$("body").addClass('offer_amount_step');
	    }
	});
}

function convert(str)
{

    let ch = str.split("");
    for (let i = 0; i < str.length; i++) {

        // If first character of a word is found
        if (i == 0 && ch[i] != ' ' ||
            ch[i] != ' ' && ch[i - 1] == ' ') {

            // If it is in lower-case
            if (ch[i] >= 'a' && ch[i] <= 'z') {

                // Convert into Upper-case
                ch[i] = String.fromCharCode(ch[i].charCodeAt(0) - 'a'.charCodeAt(0) + 'A'.charCodeAt(0));
            }
        }

        // If apart from first character
        // Any one is in Upper-case
        else if (ch[i] >= 'A' && ch[i] <= 'Z')

            // Convert into Lower-Case
            ch[i] = String.fromCharCode(ch[i].charCodeAt(0) + 'a'.charCodeAt(0) - 'A'.charCodeAt(0));
    }

    // Convert the char array to equivalent String
    let st = (ch).join("");
    return st;
}

function selectMake(Make){

    $.ajax({
		url: WS_PATH+'setvinmake',
		//url: '/setvinmake',
		data: {Make:Make},
		type: 'POST',
		success: function (response) {

			var data = JSON.parse(response);
			var data1 = data.data;
			$('#make_drop').val(data1[1]).trigger('change')
		}
    });
}

function selectModel(Model){

    $.ajax({
		url: WS_PATH+'setvinmodel',
		//url: '/setvinmodel',
		data: {Model:Model},
		type: 'POST',
		success: function (response) {

			var data = JSON.parse(response);
			var data1 = data.data;
			$('#model_drop').val(data1[1]).trigger('change')
		}
    });
}


function selectMakeModel(Make,Model){

//     $.ajax({
// 		url: '/Offer/setvinmake',
// 		//url: '/getqoute',
// 		data: {Make:Make,Model:Model},
// 		type: 'POST',
// 		success: function (response) {

// 		}
//     });
}


function keyDisable(result){

    var radioValue = result
    if(radioValue=='N'){
        //$("#drive1,#drive2").attr("disabled",true);
    }else{
        //$("#drive1,#drive2").attr("disabled",false);
    }
}

function nextsteps(id,s=null) {
	var nextTabid = id;
    
	$('body').removeClass('finish-step');
	//alert(id);

	console.log('next tabid', nextTabid);
	windowResizefn();

	if(id==3){
		if ($('input[name="utv"]:checked').length == 0 && $("#mileage").val()=='' ) {
			console.log('in');
			var paramValue = getParameterByName('lang');
			if(paramValue !== null){
				if(paramValue == 'es'){
					$("#steps_error_3").text("El campo no se puede dejar en blanco. Por favor ingrese la información requerida.");
				}else{
					$("#steps_error_3").text("The field cannot be left blank. Please enter the required information.");
				}
			}else{
				$("#steps_error_3").text("The field cannot be left blank. Please enter the required information.");
			}
			//$("#steps_error_3").text("The field cannot be left blank. Please enter the required information.");
			$("#steps_error_3").addClass("alert alert-danger");
		return false;
		}
	}

	if(id == 11 ){

	    var selectedOption = $('#make_drop').find('option:selected');
		var dataIdValue = selectedOption.data('id');


		var make_selected = $('#make_drop').data('id');
		var model_selected = $('#model_drop').val();
		var year_selected = $('#year_drop').val();

		//get parameter value code start
		var urlParams = new URLSearchParams(window.location.search);
        var paramValue = urlParams.get('model');

        if ((paramValue !== null && paramValue !== '' && paramValue != undefined & paramValue != 'undefined') || (model_selected!='' && model_selected!=null)) {

    	    $('#loading-cal-gif').show();
    		get_offer_id();
    		var make_name = $("#make_drop").find(":selected").text();
	                    var model_name = $("#model_drop").find(":selected").text();
	                    var my_year = $("#year_drop").find(":selected").text();

	                    $('.make_name').html(make_name);
	                    $('.my_model').html(model_name);
	                    $('.my_year').html(my_year);
	                    $('.model_name').html(model_name);
    		$.ajax({
    			url: WS_PATH+'getqoute',
    			//url: '/getqoute',
    			data: $('#formproquotes').serialize(),
    			type: 'POST',
    			success: function (response) {
    				var data = JSON.parse(response);
    				var data1 = data.data;
    				var data2 = data.proquotesget1;
    				//console.log(data2[0][1])
    				const {claimNumber, quoteId, highQuote, lowQuote, proQuote} = data1
    				console.log("proQuote ",proQuote);
    				var proQuoteo = proQuote;
    				$("body").addClass('offer_amount_step');
                    $("body").addClass('offer_amount_step_1');

                    var minPrice = '';
                    var maxPrice = '';
                    var perPrice = '';
    		         if(proQuote <= data2[0][3]){
    		         	var p1 = data2[0][1];
    		            proqoute = parseFloat((proQuote*p1)/100);
    		            minPrice = '0';
    		            maxPrice = data2[0][3];
    		            perPrice = p1;
    		        }else if(proQuote >= data2[0][5] && proQuote <= data2[0][6]){
    		        	var p2 = data2[0][4];
    		            proqoute = parseFloat((proQuote*p2)/100);
    		            minPrice = data2[0][5];
    		            maxPrice = data2[0][6];
    		            perPrice = p2;
    		        }else if(proQuote >= data2[0][8] && proQuote <= data2[0][9]){
    		        	var p3 = data2[0][7];
    		            proqoute = parseFloat((proQuote*p3)/100);
    		            minPrice = data2[0][8];
    		            maxPrice = data2[0][9];
    		            perPrice = p3;
    		        }else if(proQuote >= data2[0][11] && proQuote <= data2[0][12]){
    		        	var p3 = data2[0][10];
    		            proqoute = parseFloat((proQuote*p3)/100);
    		            minPrice = data2[0][11];
    		            maxPrice = data2[0][12];
    		            perPrice = p3;
    		        }else if(proQuote >= data2[0][14] && proQuote <= data2[0][15]){
    		        	var p3 = data2[0][13];
    		            proqoute = parseFloat((proQuote*p3)/100);
    		            minPrice = data2[0][14];
    		            maxPrice = data2[0][15];
    		            perPrice = p3;
    		        }else{
    		        	var p4 = data2[0][16];
    		            proqoute = parseFloat((proQuote*p4)/100);
    		            minPrice = data2[0][17];
    		            maxPrice = 'Above';
    		            perPrice = p4;
    		        }

    		        record_id = $('#record_id').val();
    		        $.ajax({
                		url: WS_PATH + 'updateofferid',
                		data: { id: record_id,minPrice:minPrice,maxPrice:maxPrice,perPrice:perPrice },
                		type: 'POST',
                		success: function (response) {
                		}
                	});

    		        $.ajax({
    					url: WS_PATH+'getqoute-conditional',
    					data: $('#formproquotes').serialize(),
    					type: 'POST',
    					success: function (response) {

    						var data5 = JSON.parse(response);
    						var data3 = data5.conditionalLogic;
    						console.log(data3+'111111111111111')

    						var con_amt = '';
    						var con_type = '';
    						var con_plus = '';
    						var con_per = '';
    						var con_per_amt = '';
    						var not_to_exceed = '';
    						var fetch_type1 = 'copart';
    						var fet_confition_id1 = '';
    						var condition_title1 = '';

    						record_id = $('#record_id').val();

    						var myArray = [];
    						myArray.push({
						        'con_amt': proqoute,
						        'con_type': con_type,
						        'con_plus': con_plus,
						        'con_per': con_per,
						        'con_per_amt': con_per_amt,
						        'not_to_exceed': not_to_exceed,
						        'record_id': record_id,
						        'proqoute': proqoute,
						        'fetch_type1' : fetch_type1,
						        'fet_confition_id1': fet_confition_id1,
						        'condition_title1': condition_title1,
						    });

    						if(data3!=undefined && data3!=false && data3!='false' && data3!=null && data3!='null'){

    							$.each(data3, function(index, value){

    								fetch_type1 = 'condition report';
    								fet_confition_id1 = value[0]
    								condition_title1 = value[1]
						        	if(value[19]=="Fixed Amount"){

					        			proqoute = parseFloat(value[24]);
					        			con_type = 'Fixed Amount';
					        			con_amt = value[24];
					        			not_to_exceed = value[23];
	    				        		record_id = $('#record_id').val();
	    				        	}else{

	    				        	    con_type = 'Proquote Estimate';
	    				        		if(value[20]=='minus'){
	    				        		    con_plus = '-';
	    				        			if(value[21]=='percentage'){
	                                            con_per = '%';
	    				        				var per1 = parseFloat((proQuote*value[22])/100);
	    				        				var total1 = parseFloat(proQuote) - per1;

	    				        				if(value[23]>total1){
	    				        					proqoute = total1;
	    				        				}else{
	    				        					proqoute = parseFloat(value[23]);
	    				        				}
	    				        				con_per_amt = value[22];
	    				        			}else{
	                                            con_per = '$';
	    				        			 var per1 = value[22];
	    				        				var total1 = parseFloat(proQuote) - parseFloat(per1);
	    				        				if(value[23]>total1){
	    				        					proqoute = total1;
	    				        				}else{
	    				        					proqoute = parseFloat(value[23]);
	    				        				}
	    				        				con_per_amt = per1;
	    				        			}
	    				        		}else{
	                                        con_plus = '+';
	    				        			if(value[21]=='percentage'){
	                                            con_per = '%';
	    				        				var per1 = parseFloat((proQuote*value[22])/100);
	    				        				var total1 = parseFloat(proQuote) + per1;

	    				        				if(value[23]>total1){
	    				        					proqoute = total1;
	    				        				}else{
	    				        					proqoute = parseFloat(value[23]);
	    				        				}
	    				        				con_per_amt = value[22];
	    				        			}else{
	                                            con_per = '$';
	    				        				var per1 = value[22];
	    				        				var total1 = parseFloat(proQuote) + parseFloat(per1);
	    				        				if(value[23]>total1){
	    				        					proqoute = total1;
	    				        				}else{
	    				        					proqoute = parseFloat(value[23]);
	    				        				}
	    				        				con_per_amt = per1;
	    				        			}
	    				        		}

	    				        		con_amt = proqoute;
	    				        		not_to_exceed = value[23];
	    				        		record_id = $('#record_id').val();

	    				        		console.log(con_amt+'nig' + value[23]);

	    				        	}

	    				        	myArray.push({
	    				        		'con_amt': con_amt,
	    				        		'con_type': con_type,
	    				        		'con_plus': con_plus,
	    				        		'con_per': con_per,
	    				        		'con_per_amt': con_per_amt,
	    				        		'not_to_exceed': not_to_exceed,
	    				        		'record_id': record_id,
	    				        		'proqoute': proqoute,
	    				        		'fetch_type1' : fetch_type1,
						        		'fet_confition_id1': fet_confition_id1,
						        		'condition_title1': condition_title1,
	    				        	});

						    	});
						    }

						    myArray.sort(function(a, b) {
							  return b.con_amt - a.con_amt;
							});
						    console.log(myArray);

						    con_amt = myArray[0]['con_amt'];
						    con_type = myArray[0]['con_type'];
						    con_plus = myArray[0]['con_plus'];
						    con_per = myArray[0]['con_per'];
						    con_per_amt = myArray[0]['con_per_amt'];
						    not_to_exceed = myArray[0]['not_to_exceed'];
						    record_id = myArray[0]['record_id'];
						    proqoute = myArray[0]['proqoute'];

						    fetch_type1 = myArray[0]['fetch_type1'];
						    fet_confition_id1 = myArray[0]['fet_confition_id1'];
						    condition_title1 = myArray[0]['condition_title1'];

						    $.ajax({
                        		url: WS_PATH + 'updateofferidcondition',
                        		data: { id: record_id,con_amt:con_amt,con_type:con_type,con_plus:con_plus,con_per:con_per,con_per_amt:con_per_amt,not_to_exceed:not_to_exceed,fetch_type1:fetch_type1,fet_confition_id1:fet_confition_id1,condition_title1:condition_title1 },
                        		type: 'POST',
                        		success: function (response) {
                        		}
                        	});

    				// 		var con_amt = '';
    				// 		var con_type = '';
    				// 		var con_plus = '';
    				// 		var con_per = '';
    				// 		var con_per_amt = '';
    				// 		if(data3!=undefined && data3!=false && data3!='false' && data3!=null && data3!='null'){

    				//         	if(data3[19]=="Fixed Amount"){

				    //     			proqoute = parseFloat(data3[24]);
				    //     			con_amt = data3[24];
				    //     			con_type = 'Fixed Amount';
    				//         	}else{
    				//         	    con_type = 'Proquote Estimate';
    				//         		if(data3[20]=='minus'){
    				//         		    con_plus = '-';
    				//         			if(data3[21]=='percentage'){
        //                                     con_per = '%';
    				//         				var per1 = parseFloat((proQuote*data3[22])/100);
    				//         				var total1 = parseFloat(proQuote) - per1;

    				//         				if(data3[23]>total1){
    				//         					proqoute = total1;
    				//         				}else{
    				//         					proqoute = parseFloat(data3[23]);
    				//         				}
    				//         				con_per_amt = data3[22];
    				//         			}else{
        //                                     con_per = '$';
    				//         			 var per1 = data3[22];
    				//         				var total1 = parseFloat(proQuote) - parseFloat(per1);
    				//         				if(data3[23]>total1){
    				//         					proqoute = total1;
    				//         				}else{
    				//         					proqoute = parseFloat(data3[23]);
    				//         				}
    				//         				con_per_amt = per1;
    				//         			}
    				//         		}else{
        //                                 con_plus = '+';
    				//         			if(data3[21]=='percentage'){
        //                                     con_per = '%';
    				//         				var per1 = parseFloat((proQuote*data3[22])/100);
    				//         				var total1 = parseFloat(proQuote) + per1;

    				//         				if(data3[23]>total1){
    				//         					proqoute = total1;
    				//         				}else{
    				//         					proqoute = parseFloat(data3[23]);
    				//         				}
    				//         				con_per_amt = data3[22];
    				//         			}else{
        //                                     con_per = '$';
    				//         				var per1 = data3[22];
    				//         				var total1 = parseFloat(proQuote) + parseFloat(per1);
    				//         				if(data3[23]>total1){
    				//         					proqoute = total1;
    				//         				}else{
    				//         					proqoute = parseFloat(data3[23]);
    				//         				}
    				//         				con_per_amt = per1;
    				//         			}
    				//         		}

    				//         		con_amt = proqoute;

    				//         		record_id = $('#record_id').val();
        //             		        $.ajax({
        //                         		url: WS_PATH + 'updateofferidcondition',
        //                         		data: { id: record_id,con_amt:con_amt,con_type:con_type,con_plus:con_plus,con_per:con_per,con_per_amt:con_per_amt },
        //                         		type: 'POST',
        //                         		success: function (response) {
        //                         		}
        //                         	});
    				//         	}
    				// 		}else{
    				// 		    console.log('innnnnnnnnnnnnnnnnnnn')
    				// 		}

    						jQuery("#proQuote_span_offer_original").hide();
    						//jQuery("#proQuote_span_offer").html( proqoute.toFixed(2));
    						jQuery("#proQuote_span_offer").html( proqoute.toFixed(2));
    						jQuery("#proQuote_span_offer_a").html( proqoute.toFixed(2));
    						jQuery("#proQuote_span_offer_original").html("Original price $" + proQuoteo);

    						jQuery("#original_price").val(proQuoteo);
    						jQuery("#revised_price").val(proqoute.toFixed(2));
    						//jQuery("#revised_price").val(proqoute);

    						jQuery("#proQuotespanoffer").html( proqoute.toFixed(2));
    						//jQuery("#proQuotespanoffer").html( proqoute);
    						var nid = parseInt(id) + 1;
    						$("#steps_error_" + id).text("");
    						$("#steps_error_" + id).removeClass("alert alert-danger");
    						$(".circletab_" + id).addClass("active");
    						jQuery(".steps").hide();
    						jQuery("#steps_" + nid).show();
    						$("#currenttab").val(nid)

    						var title =  $(".circletab_"+id).html();
    						$("#progressive-text").html(title);

    						var id1 = parseInt(id) - 1;
    						$(".circletab_"+ id1).addClass("complete");
    						autoinquirybid(2);
    						$('#loading-cal-gif').hide();

    					},
    					error: function (error) {
    					    $('#loading-cal-gif').hide();
    						console.log(error);
    					}
    				});
    			},
    			error: function (error) {
    			    $('#loading-cal-gif').hide();
    				console.log(error);
    			}
    		});
        }else{

            get_make_new('11',year_selected,dataIdValue);
        	var myModal = new bootstrap.Modal(document.getElementById('modelSelectPopup'));
            myModal.show();
        }
	}else{
	    if(id == 17){
			autoinquirybid(2);
			console.log('hiihiihiihiihihi');
		}

		if(id==4){
			//alert(id);
			var radioValue = $("input[name='damage']:checked").val();
			if(s=='Yes'){
				$("input[type=radio][name=airbag]").prop('checked', false);
				$('.circletab_5').show();
				var nid = parseInt(id) + 1;
				var nid1 = parseInt(id) - 2;
				var id1 = parseInt(id)-1;
			}else{
				var nid = parseInt(id) + 2;
				var nid1 = parseInt(id) + 2;
				var id1 = id;
				id = parseInt(id) + 1;
				nid = nid + 1;
				$("input[name=airbag][value='N']").prop("checked",true);
				$('#steps_6').hide();
				$('.circletab_5').hide();
				var title =  $(".circletab_"+nid1).html();
				$("#progressive-text").html(title);
			}
			$("#steps_error_" + id).text("");
			$("#steps_error_" + id).removeClass("alert alert-danger");
			$(".circletab_" + nid1).addClass("active");




			jQuery(".steps").hide();
			jQuery("#steps_" + nid).show();
			$("#currenttab").val(nid)
			$(".circletab_"+ id1).addClass("complete");
			if(id == 12 ){
				$("body").removeClass('offer_amount_step');
	            $("body").removeClass('offer_amount_step_1');
				$(".progress_part_2").show();
				$(".progress_part_1").hide();
				console.log('fffffff');
			}
		}else{


			if(id>=5){
				var radioValue = $("input[name='damage']:checked").val();
				if(radioValue=='Yes'){
					var nid1 = id;
					var id1 = parseInt(id) - 1;
				}else{
					var nid1 = id;
					var id1 = parseInt(id) - 1;
				}

			}else{
				var nid1 = parseInt(id) + 1;
				var id1 = id;
			}

			var drive = $("input[name='drive']:checked").val();
			if(id==7){
				if(drive=='D'){
					$("input[type=radio][name=sdamage]").prop('checked', false);
					var nid = parseInt(id) + 1;
					$('.circletab_'+id).show();
					$('.circletab_'+nid).hide();
				}else{

					if(drive=='S'){
						var nid = parseInt(id) + 3;
						nid1 = parseInt(id) + 2;
						var aa1 = parseInt(id) + 1;
						$('.circletab_'+nid1).show();
						$('.circletab_'+id).hide();
						$('.circletab_'+aa1).hide();
						$("input[name=key][value='Y']").prop("checked",true);
						$("input[name=sdamage][value='Yes, major engine issues']").prop("checked",true);
					}else{
						var nid = parseInt(id) + 2;
						nid1 = parseInt(id) + 1;
						$('.circletab_'+nid1).show();
						$('.circletab_'+id).hide();
						$("input[name=sdamage][value='Yes, major engine issues']").prop("checked",true);
						$("input[type=radio][name=key]").prop('checked', false);
					}
				}
			}else{

				if(id==8){
					var drive = $("input[name='drive']:checked").val();
					if(drive=='D'){
						var nid = parseInt(id) + 2;
						$('.circletab_'+id).hide();
						var nid1 = parseInt(id) + 1;
						$("input[name=key][value='Y']").prop("checked",true);
					}else{
						$("input[type=key][name=sdamage]").prop('checked', false);
						$("input[type=radio][name=key]").prop('checked', false);
						$('.circletab_'+id).show();
						var nid = parseInt(id) + 1;
					}
				}else{
					$('.circletab_'+id).show();
					var nid = parseInt(id) + 1;
				}
			}
			$("#steps_error_" + id).text("");
			$("#steps_error_" + id).removeClass("alert alert-danger");
			$(".circletab_" + nid1).addClass("active");


			var title =  $(".circletab_"+nid1).html();
			$("#progressive-text").html(title);

			jQuery(".steps").hide();

			//alert(id);
			if(id==16){
				var title =  "Completed";
				$("#progressive-text").html(title);
				jQuery("body").addClass('thankyou-laststep-body');
				jQuery("#steps_18").show();
				jQuery("#next-prev-id").hide();
			}else{
			    jQuery("body").removeClass('thankyou-laststep-body');
				jQuery("#steps_" + nid).show();
			}

			$("#currenttab").val(nid)
			$(".circletab_"+ id1).addClass("complete");
			if(id == 12 ){
				$("body").removeClass('offer_amount_step');
	            $("body").removeClass('offer_amount_step_1');
				$(".progress_part_2").show();
				$(".progress_part_1").hide();
				console.log('fffffff');
			}
		}
	}
}

function setModelID(){

	var selectedOption = $('#model_select_drop').val();

	if(selectedOption==''){
		var paramValue = getParameterByName('lang');
		$("#model_select_msg_error").show();
   		if(paramValue !== null){
			if(paramValue == 'es'){
				$("#model_select_msg_error").text("Por favor seleccione el campo modelo.");
			}else{
				$("#model_select_msg_error").text("Please select the model field.");
			}
		}else{
			$("#model_select_msg_error").text("Please select the model field.");
		}
	}else{


		$('#model_drop').val(selectedOption).trigger('change');
		var myModalnew = document.getElementById('modelSelectPopup');
		var modalnew = bootstrap.Modal.getOrCreateInstance(myModalnew)
		modalnew.hide();

        $("#model_select_msg_error").hide();
        $("#model_select_msg_error").text("");

        var str = '';
		var paramValue = getParameterByName('lang');
		if(paramValue !== null){
			if(paramValue == 'es'){
				str += '<option value="" >Modelo</option>';
			}else{
				str += '<option value="" >Model</option>';
			}
		}else{
			str += '<option value="" >Model</option>';
		}
		$('#model_select_drop').html(str);
	}
}

function prevsteps(id) {

	$('body').removeClass('finish-step');
	//alert(id);
	$('#svg_t').show();
	var paramValue = getParameterByName('lang');
	if(paramValue !== null){
		if(paramValue == 'es'){
			$('#d_next_btn').text('Próxima');
		}else{
			$('#d_next_btn').text('Next');
		}
	}else{
		$('#d_next_btn').text('Next');
	}
	var prevTabid = id;
	console.log('prev tabid', prevTabid);
	//var title =  $(".circletab_"+prevTabid).prev('.circle').html();
	//$("#progressive-text").html(title);

	windowResizefn();



	if (id == 1 ) {
		$("#prev").attr("disabled", true);
		//$(".circletab_1").removeClass("active");
		jQuery(".steps").hide();
		jQuery("#steps_1").show();
		$("#currenttab").val(1);
		$("#steps_error_1").text("");
		$("#steps_error_1").removeClass("alert alert-danger");
		$("body").removeClass('offer_amount_step');
        $("body").removeClass('offer_amount_step_1');
		for (let i = 1; i < 11; i++) {
 			$(".circletab_"+i).removeClass("complete");
 			$(".circletab_"+i).removeClass("active");
		}
		$(".circletab_1").addClass("active");
		var title =  $(".circletab_"+1).html();
		$("#progressive-text").html(title);
	}else if(id == 6){

		var radioValue = $("input[name='damage']:checked").val();

		if(radioValue=='Yes'){

			var id1 = parseInt(id) - 1;
			$(".circletab_" + id1).removeClass("active");
			var pid = id - 1;
			var pid1 = id - 2;

			jQuery(".steps").hide();
			jQuery("#steps_" + pid).show();
			$("#currenttab").val(pid);
			$("#steps_error_" + id).text("");
			$("#steps_error_" + id).removeClass("alert alert-danger");
			$(".circletab_"+ pid1).removeClass("complete");
		}else{
			var id1 = parseInt(id) - 1;
			$(".circletab_" + id1).removeClass("active");
			var pid = id - 3;

			jQuery(".steps").hide();
			jQuery("#steps_" + pid).show();
			$("#currenttab").val(pid);
			$("#steps_error_" + id).text("");
			$("#steps_error_" + id).removeClass("alert alert-danger");
			$(".circletab_"+ pid).removeClass("complete");

			$('#steps_6').hide();
			$('.circletab_5').hide();
		}

		var title =  $(".circletab_"+pid1).html();
		$("#progressive-text").html(title);
	} else {

		if(id== 14){
			if($("#sharing_genrate_id").val() != ''){
				$("#prev").hide()
			}
		}
		if (id == 2 ) {
			$("#prev").attr("disabled", true);
		}
		if (id == 13 ) {
			$(".progress_part_2").hide();
			$(".progress_part_1").show();
			$("body").addClass('offer_amount_step');
            $("body").addClass('offer_amount_step_1');
		}
		if(id == 12 || id == 17){
			$("#next").removeAttr("disabled");
			$("body").removeClass('offer_amount_step');
            $("body").removeClass('offer_amount_step_1');
		}


		if(id>=7){
			var radioValue = $("input[name='damage']:checked").val();
			if(radioValue=='Yes'){
				var id1 = parseInt(id) - 1 ;
				var pid1 = parseInt(id) - 2;
			}else{
				if(id==7){
					var id1 = parseInt(id) - 1;
					var pid1 = parseInt(id) - 3;

					id = parseInt(id) - 2;
					pid = parseInt(id) - 1;
				}else{
					var id1 = parseInt(id) - 1;
					var pid1 = parseInt(id) - 2;
				}
			}
		}else{
			var id1 = id;
			var pid1 = parseInt(id) - 1
		}


		$(".circletab_" + id1).removeClass("active");

		if(id==9){
			var drive = $("input[name='drive']:checked").val();
			if(drive!='D'){
				var pid = id - 2;
				pid1 = parseInt(id) - 3;
			}else{
				var pid = id - 1;
			}
		}else{
			var pid = id - 1;
		}

		if(id==10){
			var drive = $("input[name='drive']:checked").val();
			if(drive=='D'){
				var pid = id - 2;
				pid1 = parseInt(id) - 3;
			}else{
				if(drive=='S'){
					var pid = id - 3;
					pid1 = parseInt(id) - 4;
				}else{
					var pid = id - 1;
				}
			}
		}else{

			if(id==9){
				var pid = id - 2;
			}else{
				var pid = id - 1;
			}
		}

		jQuery(".steps").hide();
		jQuery("#steps_" + pid).show();
		$("#currenttab").val(pid);
		$("#steps_error_" + id).text("");
		$("#steps_error_" + id).removeClass("alert alert-danger");
		$(".circletab_"+ pid1).removeClass("complete");

		var title =  $(".circletab_"+pid1).html();
		$("#progressive-text").html(title);
	}
}

function usemyname(id){
	var fname = $("#fnameinput").val();
	//var lname = $("#lnameinput").val();
	if(id == 1){
		$("#ownerFnameinput").val(fname);
		//$("#ownerLnameinput").val(lname);
	}else{
		$("#payeeFnameinput").val(fname);
		//$("#payeeLnameinput").val(lname);
	}
}

function vip_autofill(id){
	$("#carInfo").hide();
	if(id == 1){
	    $('#no_load').val('yes');
	    $('#vip_input').val('');
		$("#autofill_year").hide();
		$("#divautofill_vin").show();
		$("body").addClass('offer_amount_step');
	}else if(id==222){

		var vip = $("#vip_input").val();
         if(vip.length == ''){
         	$("#autofill_id").attr("disabled",true);
         	$("body").addClass('offer_amount_step');
         }

		autoinquirybid(1);
		$('#next').trigger('click');
		$("body").removeClass('offer_amount_step');
        $("body").removeClass('offer_amount_step_1');
		$("#divautofill_vin").hide();
		$("#autofill_year").show();
		//$('#currenttab').val('2');
		$("#prev").removeAttr("disabled");
		$(".circletab_2").addClass("active");
		jQuery(".steps").hide();
		jQuery("#steps_2").show();
		$("#currenttab").val(2)	;
		$("#steps_error_1").text("");
		$("#steps_error_1").removeClass("alert alert-danger");
        $(".circletab_1").addClass("complete");
        var make_name = $("#make_drop").find(":selected").text();
        var model_name = $("#model_drop").find(":selected").text();
        var my_year = $("#year_drop").find(":selected").text();
        $('.make_name').html(make_name);
    	$('.my_model').html(model_name);
	        $('.my_year').html(my_year);
        $('.model_name').html(model_name);
        $('#no_load').val('yes');
        $('#newvinset').html('');
	}else{
	    $('#no_load').val('no');
		$("body").removeClass('offer_amount_step');
        $("body").removeClass('offer_amount_step_1');
		$("#divautofill_vin").hide();
		$("#autofill_year").show();
	}
    windowResizefn();
}

function useracceptbid(){
	$.ajax({
		url: WS_PATH+'useracceptbid',
		//url: '/useracceptbid',
		data: $('#formproquotes').serialize(),
		type: 'POST',
		success: function (response) {
			$('body').addClass('finish-step');
			$('#steps_16').hide();
			$('#steps_18').show();
		},
		error: function (error) {
			console.log(error);
		}
	});
}

function autoinquirybid(id){


	if ($("#sharing_id").val()){
		var a = $("#sharing_id").val()
		url = WS_PATH+'sharing_genrate_id?amt=' + a
		$("#sharing_genrate_id").val('sharing_genrate_id')
	}else{
		url = WS_PATH+'inquiryautoupdate';
		url1 = WS_PATH+'adminmail.php';
		url333 = WS_PATH+'image-curl-dynamic.php';
		url2 = WS_PATH+'testmail.php';
		url3 = WS_PATH+'test1.php';
		
	}

	//url = '/autoinquirysave'

	$.ajax({
		url: url,
		data: $('#formproquotes').serialize(),
		type: 'POST',
		success: function (response) {
			var data = JSON.parse(response);
			var data1 = data.data;
			
			if($('#record_id').val()==''){
				$('#record_id').val(data1);
				$("#sharing_id").val('')
				var paramValue = getParameterByName('lang');
				if(paramValue !== null){
					if(paramValue == 'es'){
						$('.comman_get_offer_id').html('<b>ID de oferta</b>: ' + data1);
						$('.new_offer').text('YC'+data1);
					}else{
						$('.comman_get_offer_id').html('<b>Offer ID</b>: ' + data1);
						$('.new_offer').text('YC'+data1);
					}
				}else{
					$('.comman_get_offer_id').html('<b>Offer ID</b>: ' + data1);
					$('.new_offer').text('YC'+data1);
				}
			}

			if(id==111){
				
				$('body').addClass('finish-step');
				$('#steps_17').hide();
				$('#steps_18').show();
				//getOffers()
				user_send_mail();
				$.ajax({
            		url: url1,
            		data: $('#formproquotes').serialize(),
            		type: 'POST',
            		success: function (response) {

            		},
            		error: function (error) {
            			console.log(error);
            		}
            	});

            // 	$.ajax({
            // 		url: url2,
            // 		data: $('#formproquotes').serialize(),
            // 		type: 'POST',
            // 		success: function (response) {

            // 		},
            // 		error: function (error) {
            // 			console.log(error);
            // 		}
            // 	});

            // 	$.ajax({
            // 		url: url3,
            // 		data: $('#formproquotes').serialize(),
            // 		type: 'POST',
            // 		success: function (response) {

            // 		},
            // 		error: function (error) {
            // 			console.log(error);
            // 		}
            // 	});
            	
            	$.ajax({
					url: url333,
					data: $('#formproquotes').serialize(),
					type: 'POST',
					success: function (response) {
						
					},
					error: function (error) {
						console.log(error);
					}
				});
			}

		},
		error: function (error) {
			console.log(error);
		}
	});
}
//getOffers();
function getOffers(){

    $.ajax({
    	url: WS_PATH+'get-offer',
    	//url: '/get-offer',
    	data: $('#formproquotes').serialize(),
    	type: 'POST',
    	success: function (response) {

            console.log('response')
            console.log(response)
    	},
    	error: function (error) {
    	    console.log('response1')
    		console.log(error);
    	}
    });
}

function goToDashboard(){

	//window.location.reload();
	window.location.href = 'https://yourcarintocash.com/dev-carcash/'
}

function resetForm(){
    //formproquotes
    window.location.reload();
}

function get_offer_id() {
	var record_id = $('#record_id').val();
	$.ajax({
		url: WS_PATH + 'getofferid',
		data: { id: record_id },
		type: 'POST',
		success: function (response) {
			var data = JSON.parse(response);
			var data2 = data.data;
			console.log(data2)
			var paramValue = getParameterByName('lang');
			if(paramValue !== null){
				if(paramValue == 'es'){
					$('.comman_get_offer_id').html('<b>ID de oferta</b>: ' + data2);
					$('.new_offer').text('YC'+data2);
				}else{
					$('.comman_get_offer_id').html('<b>Offer ID</b>: ' + data2);
					$('.new_offer').text('YC'+data2);
				}
			}else{
				$('.comman_get_offer_id').html('<b>Offer ID</b>: ' + data2);
				$('.new_offer').text('YC'+data2);
			}
			$("#d_id").val(data2);

			var aaabc = $('#record_id').val();
			if(paramValue !== null){
				if(paramValue == 'es'){
					$('.comman_get_offer_id').html('<b>ID de oferta</b>: ' + aaabc);
					$('.new_offer').text('YC'+aaabc);
				}else{
					$('.comman_get_offer_id').html('<b>Offer ID</b>: ' + aaabc);
					$('.new_offer').text('YC'+aaabc);
				}
			}else{
				$('.comman_get_offer_id').html('<b>Offer ID</b>: ' + aaabc);
				$('.new_offer').text('YC'+aaabc);
			}
			//$('#your_offer_id_1').html('<b>Offer ID</b>: ' + data2);


		}
	});
}



function capitalizeFLetter(string) {
	console.log(string)
	var stringone = ''
   if(string !=""){
   		var strings = string.toLowerCase();
   		stringone =  strings.replace(/^./, strings[0].toUpperCase())
   		console.log(strings.replace(/^./, strings[0].toUpperCase()));
   }
   return stringone;

}

function insert_location_using_zip() {
	var record_id = $("#record_id").val()
	$.ajax({
		type: 'POST',
		url: WS_PATH + "insert_location_using_zip",
		data: $('#formproquotes').serialize(),
		success: function (response) {
		}
	});
}
if($("#sharing_id").val()){
	var id = $("#sharing_id").val()
	nextsteps(12);
	$.ajax({
		type: "POST",
		url: WS_PATH + "get_location_value",
		data: { id : id},
		// dataType: "dataType",
		success: function (response) {
			console.log(response)
			$("#v_zip1").val(response[0][0][8])
			$("#cityinput").val(response[0][0][20])
			$('#states_drop').val(response[0][0][21]).trigger('change');
		}
	});
	$("#prev").hide()
	autoinquirybid(2);
	setTimeout(function(){
		get_offer_id();
	}, 2000)

}


function clickToCopy(){
	var textToCopy = $('.copy-text').text().trim();
	var tempInput = $('<input>');
	tempInput.val(textToCopy);
	$('body').append(tempInput);
	tempInput.select();
	document.execCommand('copy');
	tempInput.remove();
	
	 //$(".offerid-btn .tooltip-text").text("Copied!");
	 $(".offerid-btn .tooltip-text").show();
	 
	// Reset tooltip text after a short delay
	 setTimeout(function() {
		//$(".offerid-btn .tooltip-text").text("Copy to Clipboard");
		$(".offerid-btn .tooltip-text").hide();
	 }, 1000);
}

//added by pallavi
function user_send_mail(){
	$.ajax({
		url: WS_maillib+'/usermail.php',
		data: $('#formproquotes').serialize(),
		type: 'POST', 
		success: function (response) {
			console.log(response);
		}
	});
}
//end code
