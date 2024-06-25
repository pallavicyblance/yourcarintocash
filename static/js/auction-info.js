
$(document).ready(function(){

    var socket = io();

    socket.on('update', function(data) {
        console.log(data);
        if(data !== undefined) {
            data.forEach(function(auction) {
                console.log(auction);
            });
        }
    });

    var windowHeight = $(window).height();
    var topSpace = $("#tab1").offset();
    var topOffset = topSpace.top +50;
    var tableHeight = windowHeight - topOffset;
        
    windowHeight = function windowHeight(){
        var windowHeight = $(window).height();
        var topSpace = $("#tab1").offset();
        var topOffset = topSpace.top +50;
        var tableHeight = windowHeight - topOffset;
        $('div.tab-content-scroll div.dataTables_scrollBody').css('height', tableHeight+ 'px');
    };

    windowHeight();

    $(window).resize(function(){
        windowHeight();
    });

    var loader_call = true;

    auctiondata();

    $(document).on('dblclick', '.dblclick_td', function() {
        selectedAuctionId = $(this).find('span').data('proxy-auction-id');
        $('#proxy_bid').modal('show');
    });

    $('#close-popup').click(function() {
        $('#bid_amount').val(''); 
    });

    $('#place_bid_btn').on('click', function() {
        var bidAmount = $('#bid_amount').val(); 
        if (selectedAuctionId) {
            placeProxyBid(selectedAuctionId, bidAmount);
            $('#proxy_bid').modal('hide');
            $('#bid_amount').val('');
        } else {
            alert('Please select an auction.');
        }
    });

    function placeProxyBid(auctionId, bidAmount) {
        url = WS_PATH + '/place-proxy-bid/';    
        params = {'auctionId':auctionId,'proxyBidAmount': bidAmount};
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(params),
            contentType: 'application/json',
            success: function(response) {
                if (response.error){
                    var errorResponse = JSON.parse(response.error);
                    var errorMessage = errorResponse.error;
                    if (errorResponse.errorDescription) {
                        errorMessage = errorResponse.errorDescription;
                        if(errorMessage == 'Run list proxy amount is less than the acceptable minimum bid.'){
                            errorMessage = 'you can add only higher amount than current bid'
                        }
                    }
                    $('#inquiry_msg_error').show(); 
                    $('#inquiry_msg_error').html(errorMessage); 
                    setTimeout(function() { 
                        $('#inquiry_msg_error').hide(); 
                    }, 3000);
                }else{ 
                    upcomingauction();
                    $('#inquiry_msg_proxy').show();
                    $('#inquiry_msg_proxy').html('Proxy bid was successfully added.');
                    setTimeout(function() { 
                        $('#inquiry_msg_proxy').hide(); 
                    }, 3000);    
                }  
            },
        });
    }


    function startIntervals() {
        auctionIntervalId = setInterval(auctiondata, 9000);
        upcomingIntervalId = setInterval(upcomingauction, 9000);
        missedIntervalId = setInterval(missedauction, 9000);
    }

    function stopIntervals() {
        clearInterval(auctionIntervalId);
        clearInterval(upcomingIntervalId);
        clearInterval(missedIntervalId);
    }

    $('#searchauction').on('input', function() {
        if ($(this).val() == '') {
            console.log("Search cleared. Starting intervals.");
            startIntervals();
        } else {
            console.log('User is searching. Stopping intervals.');
            stopIntervals();
        }
    });
    
    if ($('#searchauction').val() == '') {
        startIntervals();
    } else {
        console.log('User is searching. Intervals not started initially.');
    }
    
    $(document).on('click', '#add_bid', function(e) {
        var auctionId = $('#auction_id').val();
        var bidAmount = $('#place_bid_amount').text();
        console.log(auctionId,bidAmount);
        url = WS_PATH + '/place-bid/';
        params = {'auctionId':auctionId,'bidamount': bidAmount};
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(params),
            contentType: 'application/json',
            success: function(response) {
                if (response.error){
                    let errors = jQuery.parseJSON(response.error);
                    console.log(errors);
                    $('#inquiry_msg_error').show(); 
                    $('#inquiry_msg_error').html(errors.errorDescription);
                    setTimeout(function() { 
                        $('#inquiry_msg_error').hide(); 
                    }, 3000);
                }else{ 
                    fetchData('');
                    
                    $('#inquiry_msg').show();
                    $('#inquiry_msg').html('Success! Your bid has been successfully placed on ACV platform.');
                    setTimeout(function() { 
                        $('#inquiry_msg').hide(); 
                    }, 3000);
                    
                } 
            },
        });
        $('#place_bid').modal('hide'); 
    });

    $('#tab_nav_top a').click(upcomingMissedAuction);

    $('#searchauction').keyup(function() {
        var searchval = $("#searchauction").val();
        var status = $('#status').val();
        $.ajax({
            url: WS_PATH + '/search-auction/',
            type: 'POST',
            data: { searchval: searchval, status: status},
            success: function(response) {
                var data = response;
                var str = '';
                if (data.length == 0) {
                    str += '<tr>';
                        str += '<td colspan="10" align="center">No data found</td>';
                    str += '</tr>';
                }else if(data == 1){
                    if ($('#condition_filter').val() == ''){
                        $('#select_condition_rules').val('');
                        if(status == 'upcoming'){
                            upcomingauction();
                        }else if(status == 'missed'){
                            missedauction();
                        }
                        auctiondata();
                    }else{
                        fetchData($('#condition_filter').val());
                    }
                }
                else{
                    data.forEach(auction => {
                        if(status == 'active'){
                            if (auction[27] == 1){
                                str += '<tr class="cell_green">';
                            }else if(auction[10] == 0){
                                str += '<tr>';
                            }else if(auction[27] == 0){
                                str += '<tr class="cell_red">';
                            }
                        }else{
                            str += '<tr>';
                        }
                        
                        str += '<td><div class="vehicle-img"><a href="'+ auction[42]+'" rel="prettyPhoto[gallery]"><img src="'+ auction[42]+'"></a></td>'
                        
                        str += '<td><b>' + auction[23] + ' VIN:</b>'+ auction[11] + '</td>';

                        str += '<td>' + number_formatchanger(auction[6],1) + '</td>';

                        str += '<td>' + auction[5] + ', ' +auction[8] + '</td>';

                        str += '<td>' + number_formatchanger(auction[9]) + '<button class="btn btn-xs btn-primary ml-2 place_bid" data-auction-id="' + auction[4] + '" data-bid-amount="' + auction[25] + '" onclick="placebid(\'' + auction[9] + '\', \'' + auction[25] + '\',\'' + auction[4] + '\')">Bid + $100</button></td>';

                        str += '<td>' + number_formatchanger(auction[35]) + '</td>';

                        str += '<td class="dblclick_td">';

                        str += '<span data-proxy-auction-id="' + auction[4] + '" > ' + number_formatchanger(auction[36]) +'</span>';

                        str += '</td>';
                
                        str += '<td>' + auction[38] + '</td>';

                        time_left(auction[37],auction[0])
                        
                        str += '<td></span><span class="hours_'+ auction[0]+ '"></span><span class="minutes_'+ auction[0]+ '"></span><span class="seconds_'+ auction[0]+ '"></span></td>';

                        if (auction[41]) {
                            var colorsData = JSON.parse(auction[41]);
                            var htmlString = '<td><div class="lights-btn">';
                        
                            for (var color in colorsData) {
                                if (colorsData.hasOwnProperty(color)) {
                                    var count = colorsData[color];
                                    htmlString += '<span class="' + color + '">' + count + '</span> ';
                                }
                            }
                        
                            htmlString += '</div></td>';
                            str += htmlString;
                        }
                        
                        str += '<td><a class="btn-link" href="#" onclick="condition_popup_open(' + auction[4] + ')">View Conditional Report</a></td>';
                        str += '</tr>';
                    });
                }
                if(status == 'active'){
                    $('#dataConditional tbody').html(str);
                }else if(status == 'won'){
                    $('#dataConditionalwon tbody').html(str);
                }else if(status == 'lost'){
                    $('#dataConditionallost tbody').html(str);
                }else if(status == 'upcoming'){
                    $('#dataConditionalupcoming tbody').html(str);
                }else if(status == 'missed'){
                    $('#dataConditionalmissed tbody').html(str);
                }
                $("a[rel^='prettyPhoto']").prettyPhoto({
                    overlay_gallery: false,
                    social_tools: '',
                    deeplinking: false
                });
            },
            error: function(xhr, status, error) {
                
                console.error(error);
            }
        }); 
    });

    $('#select_condition_rules').change(function() {
        $('#searchauction').val('');
        // loader_call = true;
        var selectedConditionReportId = $(this).val();
        $('#condition_filter').val(selectedConditionReportId);
        $('#report').val(selectedConditionReportId);
        if(selectedConditionReportId ==''){
            jQuery('#all_condition_rules').hide();
        } else{
            jQuery('#all_condition_rules').show();
        }
        fetchData(selectedConditionReportId);
        
    });
    
    function auctiondata() {
        if ($('#report').val() != ''){
            var selectedConditionReportId = $('#report').val();
        }else{
            var selectedConditionReportId = '';
        }
        fetchData(selectedConditionReportId);
    }

    function fetchData(selectedConditionReportId) {

        if (loader_call) {
            $('#loadingdieditvvehicle').show();
        }

        $.ajax({
            url: WS_PATH + '/condition-report-details/',
            type: 'POST',
            data: { id: selectedConditionReportId },
            success: function(response) {
                loader_call = false;
                var data = response.auctions;
                var won_auction = response.won_auction;
                var lost_auction = response.lost_auction;

                var str = '';
                if (data.length == 0) {
                    str += '<tr>';
                        str += '<td colspan="11" align="center">No data found</td>';
                    str += '</tr>';
                } else {
                    data.forEach(auction => {
                        if (auction[27] == 1) {
                            str += '<tr class="cell_green" id="auctionTr-'+auction[4]+'">';
                        } else if(auction[10] == 0) {
                            str += '<tr id="auctionTr-'+auction[4]+'">';
                        } else if(auction[27] == 0) {
                            str += '<tr class="cell_red" id="auctionTr-'+auction[4]+'">';
                        }

                        str += '<td><div class="vehicle-img"><a href="'+ auction[42]+'" rel="prettyPhoto[gallery]"><img src="'+ auction[42]+'"></a></td>'
                        
                        str += '<td><b>' + auction[23] + ' VIN:</b>'+ auction[11] + '</td>';

                        str += '<td>' + number_formatchanger(auction[6],1) + '</td>';

                        str += '<td>' + auction[5] + ', ' +auction[8] + '</td>';

                        str += '<td id=currentBid_'+auction[4]+'>' + number_formatchanger(auction[9]) + '<br><button class="btn btn-xs btn-primary place_bid" data-auction-id="' + auction[4] + '" data-bid-amount="' + auction[25] + '" onclick="placebid(\'' + auction[9] + '\', \'' + auction[25] + '\',\'' + auction[4] + '\')">Bid + $100</button></td>';

                        str += '<td id=ourMaxBid_'+auction[4]+'>' + number_formatchanger(auction[35]) + '</td>';

                        str += '<td class="dblclick_td" id=proqouteAmount_'+auction[4]+'>';

                        str += '<span data-proxy-auction-id="' + auction[4] + '" > ' + number_formatchanger(auction[36]) +'</span>';

                        str += '</td>';
                
                        str += '<td>' + auction[38] + '</td>';

                        time_left(auction[7],auction[0])
                        
                        str += '<td></span><span class="hours_'+ auction[0]+ '"></span><span class="minutes_'+ auction[0]+ '"></span><span class="seconds_'+ auction[0]+ '"></span></td>';


                        if (auction[41]) {
                            var colorsData = JSON.parse(auction[41]);
                            var htmlString = '<td><div class="lights-btn">';
                        
                            for (var color in colorsData) {
                                if (colorsData.hasOwnProperty(color)) {
                                    var count = colorsData[color];
                                    htmlString += '<span class="' + color + '">' + count + '</span> ';
                                }
                            }
                        
                            htmlString += '</div></td>';
                            str += htmlString;
                        }

                        str += '<td><a class="btn-link" href="#" onclick="condition_popup_open(' + auction[4] + ')">View Conditional Report</a></td>';
                        str += '</tr>';
                        
                    });
                }

                $('#dataConditional tbody').html(str);

                var str1 = '';
                if (won_auction.length == 0) {
                    str1 += '<tr>';
                        str1 += '<td colspan="11" align="center">No data found</td>';
                    str1 += '</tr>';
                }else{
                    won_auction.forEach(auction => {
                        str1 += '<tr id="auctionTr-'+auction[4]+'">';

                        str1 += '<td><div class="vehicle-img"><a href="'+ auction[42]+'" rel="prettyPhoto[gallery]"><img src="'+ auction[42]+'"></a></td>'
                        
                        str1 += '<td><b>' + auction[23] + ' VIN:</b>'+ auction[11] + '</td>';

                        str1 += '<td>' + number_formatchanger(auction[6],1) + '</td>';

                        str1 += '<td>' + auction[5] + ', ' +auction[8] + '</td>';
                        
                        str1 += '<td>' + number_formatchanger(auction[9]) + '</td>';

                        str1 += '<td>' + number_formatchanger(auction[35]) + '</td>';

                        str1 += '<td>' + number_formatchanger(auction[36]) + '</td>';
                                                
                        str1 += '<td>' + auction[38] + '</td>';

                        time_left(auction[7],auction[0])
                        
                        str1 += '<td></span><span class="hours_'+ auction[0]+ '"></span><span class="minutes_'+ auction[0]+ '"></span><span class="seconds_'+ auction[0]+ '"></span></td>';

                        if (auction[41]) {
                            var colorsData = JSON.parse(auction[41]);
                            var htmlString = '<td><div class="lights-btn">';
                        
                            for (var color in colorsData) {
                                if (colorsData.hasOwnProperty(color)) {
                                    var count = colorsData[color];
                                    htmlString += '<span class="' + color + '">' + count + '</span> ';
                                }
                            }
                        
                            htmlString += '</div></td>';
                            str1 += htmlString;
                        }

                        str1 += '<td><a class="btn-link" href="#" onclick="condition_popup_open(' + auction[4] + ')">View Conditional Report</a></td>';
                        str1 += '</tr>';
                    });
                }
                $('#dataConditionalwon tbody').html(str1);

                var str2 = '';
                if (lost_auction.length == 0) {
                    str2 += '<tr>';
                        str2 += '<td colspan="11" align="center">No data found</td>';
                    str2 += '</tr>';
                }else{
                    lost_auction.forEach(auction => {
                        str2 += '<tr id="auctionTr-'+auction[4]+'">';

                        str2 += '<td><div class="vehicle-img"><a href="'+ auction[42]+'" rel="prettyPhoto[gallery]"><img src="'+ auction[42]+'"></a></td>'
                        
                        str2 += '<td><b>' + auction[23] + ' VIN:</b>'+ auction[11] + '</td>';

                        str2 += '<td>' + number_formatchanger(auction[6],1) + '</td>';

                        str2 += '<td>' + auction[5] + ', ' +auction[8] + '</td>';
                        
                        str2 += '<td>' + number_formatchanger(auction[9]) + '</td>';

                        str2 += '<td>' + number_formatchanger(auction[35]) + '</td>';

                        str2 += '<td>' + number_formatchanger(auction[36]) + '</td>';
                                                
                        str2 += '<td>' + auction[38] + '</td>';

                        time_left(auction[7],auction[0])
                        
                        str2 += '<td></span><span class="hours_'+ auction[0]+ '"></span><span class="minutes_'+ auction[0]+ '"></span><span class="seconds_'+ auction[0]+ '"></span></td>';

                        if (auction[41]) {
                            var colorsData = JSON.parse(auction[41]);
                            var htmlString = '<td><div class="lights-btn">';
                        
                            for (var color in colorsData) {
                                if (colorsData.hasOwnProperty(color)) {
                                    var count = colorsData[color];
                                    htmlString += '<span class="' + color + '">' + count + '</span> ';
                                }
                            }
                        
                            htmlString += '</div></td>';
                            str2 += htmlString;
                        }

                        str2 += '<td><a class="btn-link" href="#" onclick="condition_popup_open(' + auction[4] + ')">View Conditional Report</a></td>';
                        str2 += '</tr>';
                    });
                }
                $('#dataConditionallost tbody').html(str2);

                $("a[rel^='prettyPhoto']").prettyPhoto({
                    overlay_gallery: false,
                    social_tools: '',
                    deeplinking: false
                });

                if (response.reports.length > 1) {
                    console.log('111');
                }else{
                    var reports = response.reports[0];
                    $('#make_p_43').html(reports[26] + ' ' + reports[27]);
                    $('#year_label_txt').html(':' + reports[5] + ' to ' + reports[6]);
                    $('#mileage_label_txt').html(':' + reports[9] + ' to ' + reports[10]);
    
                    var dataziplist = JSON.parse(reports[31]);
                    var zipLabelTxt = $('#zip_label_txt');
    
    
                    if (dataziplist.length === 0) {
                        zipLabelTxt.html('');
                    } else {
                        var zipInfoText = '';
                        for (var i = 0; i < dataziplist.length; i++) {
                            var data = dataziplist[i];
                            zipInfoText += '<b>ZIP:</b>' + data['distance'] + ' miles from ' + data['range_zip'] + ' ' ;
                        }
                        zipLabelTxt.html(zipInfoText);
                    }                
    
                    $('#country_label_txt').html(reports[50]);
                    $('#state_label_txt').html(reports[49]);
    
                    var body_damage = '';
                    if (reports[33] == "MN,Yes," || reports[33] == "Yes,MN,"){
                        var body_damage = "No, my vehicle is in good shape!, Yes, my vehicle has some damage or rust";
                    }else if(reports[33] == "Yes," || reports[33] == "Yes"){
                        var body_damage = "Yes, my vehicle has some damage or rust";
                    }else if(reports[33] == "MN," || reports[33] == "MN"){
                        var body_damage = "No, my vehicle is in good shape!";
                    }
    
                    if (reports[34] == "Y,N," || reports[34] == "N,Y," ){
                        var airbag_value = " Yes, the airbags are deployed, No, the airbags are not deployed";
                    }else if(reports[34] == "Y," || reports[34] == "Y"){
                        var airbag_value = " Yes, the airbags are deployed"
                    }else if(reports[34] == "N," || reports[34] == "N"){
                        var airbag_value = " No, the airbags are not deployed"
                    }else{
                        var airbag_value = ""
                    }
    
                    if(reports[35] == "D,S,N," || reports[35] == "S,N,D," || reports[35] == "N,D,S,"){
                        var start_and_drive = "Yes, it starts and drives, No, it starts but does not drive, No, it does not start";
                    }else if(reports[35] == "D,S,"){
                        var start_and_drive = "Yes, it starts and drives, No, it starts but does not drive";
                    }else if(reports[35] == "S,N,"){
                        var start_and_drive = "No, it starts but does not drive, No, it does not start";
                    }else if(reports[35] == "D,N,"){
                        var start_and_drive = "Yes, it starts and drives, No, it does not start";
                    }else if(reports[35] == "D," || reports[35] == "D"){
                        var start_and_drive = "Yes, it starts and drives";
                    }else if(reports[35] == "N," || reports[35] == "N"){
                        var start_and_drive = "No, it does not start";
                    }else if(reports[35] == "S," || reports[35] == "S"){
                        var start_and_drive = "No, it starts but does not drive";
                    }else{
                        var start_and_drive = ""
                    }
    
                    if (reports[37] == "Y,N," || reports[37] == "N,Y,"){
                        var key_value = "Yes, I have the key, No, I do not have a key";
                    }else if(reports[37] == "Y," || reports[37] == "Y"){
                        var key_value = "Yes, I have the key";
                    }else if(reports[37] == "N," || reports[37] == "N"){
                        var key_value = "No, I do not have a key";
                    }else{
                        var key_value = "";
                    }
    
                    if(reports[38] == "clean title,Salvage Rebuilt,Unknown," || reports[38] == "Salvage Rebuilt,Unknown,clean title," || reports[38] == ",Unknown,clean title,Salvage Rebuilt,"){
                        var title_type = "Yes, I have a clean title, No, my title is branded (Salvage, rebuilt, lemon law, etc.), No, I don’t have a title";
                    }else if (reports[38] == "clean title,Salvage Rebuilt,"){
                        var title_type = "Yes, I have a clean title, No, my title is branded (Salvage, rebuilt, lemon law, etc.)";
                    }else if (reports[38] == "Salvage Rebuilt,Unknown,"){
                        var title_type = "No, my title is branded (Salvage, rebuilt, lemon law, etc.), No, I don’t have a title";
                    }else if(reports[38] == "clean title,Unknown,"){
                        var title_type = "Yes, I have a clean title, No, I don’t have a title";
                    }else if(reports[38] == "clean title" || reports[38] == "clean title,"){
                        var title_type = "Yes, I have a clean title";
                    }else if(reports[38] == "Salvage Rebuilt" || reports[38] == "Salvage Rebuilt,"){
                        var title_type = "No, my title is branded (Salvage, rebuilt, lemon law, etc.)";
                    }else if(reports[38] == "Unknown," || reports[38] == "Unknown"){
                        var title_type = "No, I don’t have a title"; 
                    }else{
                        var title_type = "";
                    }
                    
                    if (reports[39] == "no,W," || reports[39] == "W,no,"){
                        var water_and_fire_value = "No, it has never had any fire or water damage, Yes, it had fire or water damage";
                    }else if(reports[39] == "W," || reports[39] == "W"){
                        var water_and_fire_value = "Yes, it had fire or water damage";
                    }else if(reports[39] == "no," || reports[39] == "no"){
                        var water_and_fire_value = "No, it has never had any fire or water damage,";
                    }else{
                        var water_and_fire_value = "";
                    }
    
                    $('#bodydamage_label_txt').html(body_damage);
                    $('#airbag_label_txt').html(airbag_value);
                    $('#drive_label_txt').html(start_and_drive);
                    $('#mechanical_label_txt').html(reports[36]);
                    $('#key_label_txt').html(key_value);
                    $('#titletype_label_txt').html(title_type);
                    $('#firedamage_label_txt').html(water_and_fire_value);
                    $('.notification_pubnub').html(response.count);
    
                    if(reports[20] == "plus"){
                        var buyingruletype = "+";
                    }else{
                        var buyingruletype = "-";
                    }
                    $('#buyingruletype_label_txt').html(buyingruletype + ' %'+ reports[22] );
                    $('#nottoexceed_label_txt').html(reports[23]);
                }
                $("#loadingdieditvvehicle").hide();
                // auctiondata(selectedConditionReportId);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }

    function upcomingMissedAuction(e){
        var status = $(this).parent().data('status');
        $('#status').val(status);
        e.preventDefault();

        $('#searchauction').val('');
        $('#select_condition_rules').val('');
        jQuery('#all_condition_rules').hide();
        $('#tab_nav_top li').removeClass('active');
        $('.auction-show, .auction-upcoming-show, .auction-missed-show, .auction-lost-show, .auction-won-show').hide();
        
        if(status == "missed" || status == "upcoming" ){
            $('.condition-filter').hide();   
        }else{
            $('.condition-filter').show();   
        }
        $(this).parent('li').addClass('active');

        if (status == 'upcoming') {
            upcomingauction();
            
        }else if(status == 'missed'){
            missedauction();
        }else if(status == 'lost'){
            $('.auction-lost-show').show();
        }else if(status == 'won'){
            $('.auction-won-show').show();
        }else {
            $('.auction-show').show();
        }

        auctiondata();
    }

    function upcomingauction(){
        if($('#status').val() === 'upcoming'){
            $('.auction-upcoming-show').show();
        }
        $.ajax({
            url:  WS_PATH + '/upcoming-auction-data/',
            type: 'GET',
            success: function(response) {
                var data = response;                    
                var str = '';
                    if (data.length == 0) {
                        str += '<tr>';
                            str += '<td colspan="11" align="center">No data found</td>';
                        str += '</tr>';
                    }else{
                        data.forEach(auction => {
                            str += '<tr>';

                            str += '<td><div class="vehicle-img"><a href="'+ auction[42]+'" rel="prettyPhoto[gallery]"><img src="'+ auction[42]+'"></a></td>'
                        
                            str += '<td><b>' + auction[23] + ' VIN:</b>'+ auction[11] + '</td>';

                            str += '<td>' + number_formatchanger(auction[6],1) + '</td>';

                            str += '<td>' + auction[5] + ', ' +auction[8] + '</td>';
                           
                            str += '<td>' + number_formatchanger(auction[9]) + '</td>';

							str += '<td>' + number_formatchanger(auction[35]) + '</td>';
							
							str += '<td class="dblclick_td">';

							str += '<span data-proxy-auction-id="' + auction[4] + '" > ' + number_formatchanger(auction[36]) +'</span>';

							str += '</td>';
							
							str += '<td>' + auction[38] + '</td>';

                            time_left(auction[37],auction[0])
                            str += '<td></span><span class="hours_'+ auction[0]+ '"></span><span class="minutes_'+ auction[0]+ '"></span><span class="seconds_'+ auction[0]+ '"></span></td>';


                            if (auction[41]) {
                                var colorsData = JSON.parse(auction[41]);
                                var htmlString = '<td><div class="lights-btn">';
                            
                                for (var color in colorsData) {
                                    if (colorsData.hasOwnProperty(color)) {
                                        var count = colorsData[color];
                                        htmlString += '<span class="' + color + '">' + count + '</span> ';
                                    }
                                }
                            
                                htmlString += '</div></td>';
                                str += htmlString;
                            }
                        
                            str += '<td><a class="btn-link" href="#" onclick="condition_popup_open(' + auction[4] + ')">View Conditional Report</a></td>';
                            str += '</tr>';
                        });
                    }

                    
                    $('#dataConditionalupcoming tbody').html(str);

                    $("a[rel^='prettyPhoto']").prettyPhoto({
                        overlay_gallery: false,
                        social_tools: '',
                        deeplinking: false
                    });
                },
            error: function(xhr, status, error) {
            }
        });
    }

    function missedauction(){
        if($('#status').val() === 'missed'){
            $('.auction-missed-show').show();
        }
        $.ajax({
            url: WS_PATH + '/missed-auction/',
            type: 'POST',
            data: { id: "" },
            success: function(response) {
                var data = response;                    
                var str = '';
                if (data.length == 0) {
                    str += '<tr>';
                        str += '<td colspan="11" align="center">No data found</td>';
                    str += '</tr>';
                } else {
                    data.forEach(auction => {
                        str += '<tr>';

                        str += '<td><div class="vehicle-img"><a href="'+ auction[42]+'" rel="prettyPhoto[gallery]"><img src="'+ auction[42]+'"></a></td>'
                        
                        str += '<td><b>' + auction[23] + ' VIN:</b>'+ auction[11] + '</td>';

                        str += '<td>' + number_formatchanger(auction[6],1) + '</td>';

                        str += '<td>' + auction[5] + ', ' +auction[8] + '</td>';
                        
                        str += '<td>' + number_formatchanger(auction[9]) + '</td>';

                        str += '<td>' + number_formatchanger(auction[35]) + '</td>';

                        str += '<td>' + number_formatchanger(auction[36]) + '</td>';
                                                
                        str += '<td>' + auction[38] + '</td>';

                        time_left(auction[7],auction[0])
                        
                        str += '<td></span><span class="hours_'+ auction[0]+ '"></span><span class="minutes_'+ auction[0]+ '"></span><span class="seconds_'+ auction[0]+ '"></span></td>';

                        if (auction[41]) {
                            var colorsData = JSON.parse(auction[41]);
                            var htmlString = '<td><div class="lights-btn">';
                        
                            for (var color in colorsData) {
                                if (colorsData.hasOwnProperty(color)) {
                                    var count = colorsData[color];
                                    htmlString += '<span class="' + color + '">' + count + '</span> ';
                                }
                            }
                        
                            htmlString += '</div></td>';
                            str += htmlString;
                        }

                        str += '<td><a class="btn-link" href="#" onclick="condition_popup_open(' + auction[4] + ')">View Conditional Report</a></td>';
                        str += '</tr>';
                    });
                }
                $('#dataConditionalmissed tbody').html(str);
                $("a[rel^='prettyPhoto']").prettyPhoto({
                    overlay_gallery: false,
                    social_tools: '',
                    deeplinking: false
                });
                },
            error: function(xhr, status, error) {
            }
        });   
    }
});


function time_left(date, id) {

    var targetDateUTC = new Date(new Date(date).toUTCString());
    
    var timerInterval = setInterval(function() {
        // Get the current time in UTC
        var currentDateUTC = new Date(new Date().toUTCString());

        // Calculate the difference in seconds between the target date and the current date
        var timeDifference = Math.floor((targetDateUTC - currentDateUTC) / 1000);
       
        if (timeDifference <= 0) {
            clearInterval(timerInterval);
            $(".hours_" + id).html('Auction Ended');
            $("#auctionTr-" + id).fadeOut();
        } else {
            // console.log('else timeDifference',timeDifference);
            var days = Math.floor(timeDifference / (24 * 60 * 60));
            var hours = Math.floor((timeDifference % (24 * 60 * 60)) / (60 * 60));
            var minutes = Math.floor((timeDifference % (60 * 60)) / 60);
            var seconds = timeDifference % 60;
            $(".days_" + id).html(days + "<span>:</span>");
            $(".hours_" + id).html(hours + "<span>:</span>");
            $(".minutes_" + id).html(minutes + "<span>:</span>");
            $(".seconds_" + id).html(seconds + "<span></span>");
        }
    }, 1000); // Update every second
}

function number_formatchanger(inputValue, id){
    if (inputValue !== null && inputValue !== undefined) {
        var inputValues = inputValue.toString();
        if(id == 1){
            inputValue = inputValues.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
            return inputValue;
        }else{
            inputValue = '$'+inputValues.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
            if (inputValue.indexOf(".") >= 0) {
              myArray = inputValue.split(".");
              if(myArray[1].length == 0){
                inputValue = inputValue+"00"
              }else if(myArray[1].length == 1){
                inputValue = inputValue+0
              }else{
                inputValue = inputValue
              }
            }else{
              inputValue += ".00";
            }
            return  inputValue;
        }
    }else {
        console.error("Input value is null or undefined.");
    }
    
}

function condition_popup_open(id){
    $('#flipFlop').modal({show:true});
    $('.loader').show();
    $.ajax({
        url: WS_PATH + '/get-auction-condition/',
        data:  {auction_id:id},
        type: 'POST',
        success: function (response) {
            if (response.length != null) {
                var conditionresponse = response[0];
                var airbagData = JSON.parse(conditionresponse[2]);
                var vehicleData = JSON.parse(conditionresponse[3]);
                var vehicleStay = JSON.parse(conditionresponse[4]);
                var vehicleCrank = JSON.parse(conditionresponse[5]);
                var penetratingRust = JSON.parse(conditionresponse[6]);
                var unbodyDamage = JSON.parse(conditionresponse[7]);
                var engineNoice = JSON.parse(conditionresponse[8]);
                var engineHesitation = JSON.parse(conditionresponse[9]);
                var timingchainIssue = JSON.parse(conditionresponse[10]);
                var abnormalexhaustSmoke = JSON.parse(conditionresponse[11]);
                var headgasketIssue = JSON.parse(conditionresponse[12]);
                var drivetrainIssue = JSON.parse(conditionresponse[13]);
                var transmissionIssue = JSON.parse(conditionresponse[14]);
                var minor_body_damage = JSON.parse(conditionresponse[15]);
                var modrate_body_damage = JSON.parse(conditionresponse[16]);
                var major_body_damage = JSON.parse(conditionresponse[17]);
                var glass_damage = JSON.parse(conditionresponse[18]);
                var light_damage = JSON.parse(conditionresponse[19]);
                var aftermarket_parts = JSON.parse(conditionresponse[20]);
                var poor_quality_repair = JSON.parse(conditionresponse[21]);
                var surface_rust =  JSON.parse(conditionresponse[22]);
                var heavy_rust = JSON.parse(conditionresponse[23]);
                var OBDIICodes = JSON.parse(conditionresponse[24]);
                var incomplete_monitors = JSON.parse(conditionresponse[25]);
                var seatDamage = JSON.parse(conditionresponse[26]);
                var dashboardDamage = JSON.parse(conditionresponse[27]);
                var interiorTrimDamage = JSON.parse(conditionresponse[28]);
                var electricalIssue = JSON.parse(conditionresponse[29]);
                var breakIssue = JSON.parse(conditionresponse[30]);
                var suspensionIssue = JSON.parse(conditionresponse[31]);
                var steeringIssue = JSON.parse(conditionresponse[32]);
                var aftermarket_wheels = JSON.parse(conditionresponse[33]);
                var damaged_wheels = JSON.parse(conditionresponse[34]);
                var damaged_tiles = JSON.parse(conditionresponse[35]);
                var tire_measurements = JSON.parse(conditionresponse[36]);
                var aftermarket_mechanical = JSON.parse(conditionresponse[37]);
                var engine_accessory_issue = JSON.parse(conditionresponse[38]);
                var title_absent = JSON.parse(conditionresponse[39]);
                var title_branded = JSON.parse(conditionresponse[40]);
                var modrate_body_rust = JSON.parse(conditionresponse[41]);
                var flood_damage = JSON.parse(conditionresponse[42]);
                var scratches = JSON.parse(conditionresponse[43]);
                var minor_body_rust = JSON.parse(conditionresponse[44]);
                var major_body_rust = JSON.parse(conditionresponse[45]);
                var hail_damage = JSON.parse(conditionresponse[46]);
                var mismatched_paint = JSON.parse(conditionresponse[47]);
                var paint_meter_readings = JSON.parse(conditionresponse[48]);
                var previous_paint_work = JSON.parse(conditionresponse[49]);
                var jump_start_required = JSON.parse(conditionresponse[50]);
                var oil_intermix_dipstick_v2 = JSON.parse(conditionresponse[51]);
                var fluid_leaks = JSON.parse(conditionresponse[52]);
                var emissions_modifications = JSON.parse(conditionresponse[53]);
                var catalytic_converters_missing = JSON.parse(conditionresponse[54]);
                var exhaust_modifications = JSON.parse(conditionresponse[55]);
                var exhaust_noise = JSON.parse(conditionresponse[56]);
                var suspension_modifications = JSON.parse(conditionresponse[57]);
                var engine_does_not_stay_running = JSON.parse(conditionresponse[58]); 
                var check_engine_light = JSON.parse(conditionresponse[59]);
                var airbag_light = JSON.parse(conditionresponse[60]);
                var brake_light = JSON.parse(conditionresponse[61]);
                var traction_control_light = JSON.parse(conditionresponse[62]);
                var tpms_light = JSON.parse(conditionresponse[63]);
                var battery_light = JSON.parse(conditionresponse[64]);
                var other_warning_light = JSON.parse(conditionresponse[65]);
                var oversized_tires = JSON.parse(conditionresponse[66]);
                var uneven_tread_wear = JSON.parse(conditionresponse[67]);
                var mismatched_tires = JSON.parse(conditionresponse[68]);
                var missing_spare_tire = JSON.parse(conditionresponse[69]);
                var carpet_damage = JSON.parse(conditionresponse[70]);
                var headliner_damage = JSON.parse(conditionresponse[71]);
                var interior_order = JSON.parse(conditionresponse[72]);
                var crank_windows = JSON.parse(conditionresponse[73]);
                var no_factory_ac = JSON.parse(conditionresponse[74]);
                var five_digit_odometer = JSON.parse(conditionresponse[75]);
                var sunroof = JSON.parse(conditionresponse[76]);
                var navigation = JSON.parse(conditionresponse[77]);
                var aftermarket_stereo = JSON.parse(conditionresponse[78]);
                var hvac_not_working = JSON.parse(conditionresponse[79]);
                var leather_seats = JSON.parse(conditionresponse[80]); 
                var true_mileage_unknown = JSON.parse(conditionresponse[81]);
                var off_lease_vehicle = JSON.parse(conditionresponse[82]);
                var repair_order_attached = JSON.parse(conditionresponse[83]);
                var repossession = JSON.parse(conditionresponse[84]);
                var repossession_papers_wo_title = JSON.parse(conditionresponse[85]);
                var mobility = JSON.parse(conditionresponse[86]);
                var transferrable_registration = JSON.parse(conditionresponse[87]);
                var sold_on_bill_of_sale = JSON.parse(conditionresponse[88]);
                var aftermarket_sunroof = JSON.parse(conditionresponse[89]);
                var backup_camera = JSON.parse(conditionresponse[90]);
                var charging_cable = JSON.parse(conditionresponse[91]);
                var engine_overheats = JSON.parse(conditionresponse[92]);
                var supercharger_issue = JSON.parse(conditionresponse[93]);
                var emissions_issue = JSON.parse(conditionresponse[94]);
                var oil_level_issue = JSON.parse(conditionresponse[95]);
                var oil_condition_issue = JSON.parse(conditionresponse[96]);
                var coolant_level_issue = JSON.parse(conditionresponse[97]);

                if (check_engine_light['selected'] == true){
                    var checkEngineLightHtml = '<div class="col-lg-6"><div> <b>' + check_engine_light['questionTitle'] + ': </b>'+ check_engine_light['answer'][0]['value']+ '</div></div>';

                    $('#lights_report').empty().append('<div class="col-lg-6"><div> <b>' + check_engine_light['questionTitle'] + ': </b> ' + check_engine_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{

                    $('#lights_report').empty().append('<div class="col-lg-6"><div> <b>' + check_engine_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (airbag_light['selected'] == true){
                    var airbagLightHtml = '<div class="col-lg-6"><div> <b>' + airbag_light['questionTitle'] + ': </b>'+ airbag_light['answer'][0]['value']+ '</div></div>';
                
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + airbag_light['questionTitle'] + ': </b> ' + airbag_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + airbag_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (brake_light['selected'] == true){
                    var brakeLightHtml = '<div class="col-lg-6"><div> <b>' + brake_light['questionTitle'] + ': </b>'+ brake_light['answer'][0]['value']+ '</div></div>';
                   
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + brake_light['questionTitle'] + ': </b> ' + brake_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + brake_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (traction_control_light['selected'] == true){
                    var tractionControlLightHtml = '<div class="col-lg-6"><div> <b>' + traction_control_light['questionTitle'] + ': </b>'+ traction_control_light['answer'][0]['value']+ '</div></div>';

                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + traction_control_light['questionTitle'] + ': </b> ' + traction_control_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + traction_control_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (tpms_light['selected'] == true){
                    var tpmsLightHtml = '<div class="col-lg-6"><div> <b>' + tpms_light['questionTitle'] + ': </b>'+ tpms_light['answer'][0]['value']+ '</div></div>';
                    
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + tpms_light['questionTitle'] + ': </b> ' + tpms_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + tpms_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (battery_light['selected'] == true){
                    var batteryLightHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + battery_light['questionTitle'] + ': </b>'+ battery_light['answer'][0]['value']+ '</div></div>'; 

                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + battery_light['questionTitle'] + ': </b> ' + battery_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + battery_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (other_warning_light['selected'] == true){
                    var otherWarningLightHtml = '<div class="col-lg-6"><div> <b>' + other_warning_light['questionTitle'] + ': </b>'+ other_warning_light['answer'][0]['value']+ '</div></div>';

                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + other_warning_light['questionTitle'] + ': </b> ' + other_warning_light['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + other_warning_light['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (OBDIICodes['selected'] == true){
                    var OBDIICodesHtml = '<div class="col-lg-6"><div> <b>' + OBDIICodes['questionTitle'] + ': </b>'+ OBDIICodes['answer'][0]['value']+ '</div></div>';

                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + OBDIICodes['questionTitle'] + ': </b> ' + OBDIICodes['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + OBDIICodes['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (incomplete_monitors['selected'] == true){
                    var incompleteMonitorsHtml = '<div class="col-lg-6"><div><b>' + incomplete_monitors['questionTitle'] + ':</b>';
                    for (var i = 0; i < incomplete_monitors['answer'].length; i++) {
                        var answer = incomplete_monitors['answer'][i];
                        incompleteMonitorsHtml += '<div>' + answer['value'] + ': ' + answer['displayName'] + ',</div>';
                    }

                    incompleteMonitorsHtml += '</div></div>';


                    var newincompleteMonitorsHtml = '<div class="col-lg-6"><div><b>' + incomplete_monitors['questionTitle'] + ':</b>';
                    for (var i = 0; i < incomplete_monitors['answer'].length; i++) {
                        var answer = incomplete_monitors['answer'][i];
                        newincompleteMonitorsHtml += '<div>' + answer['value'] + ': ' + answer['displayName'] + ',</div>';
                    }

                    newincompleteMonitorsHtml += '</div><div class="text-right text-success">Yes</div>';
                    $('#lights_report').append(newincompleteMonitorsHtml)

                }else{
                    $('#lights_report').append('<div class="col-lg-6"><div> <b>' + incomplete_monitors['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (vehicleData['selected'] == true){
                    var vehicleHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + vehicleData['questionTitle'] + ': </b>'+ vehicleData['answer'] + [0]['value']+ '</div></div>';

                    $('#driveability_report').empty().append('<div class="col-lg-6"><div> <b>' + vehicleData['questionTitle'] + ': </b> ' + vehicleData['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#driveability_report').empty().append('<div class="col-lg-6"><div> <b>' + vehicleData['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (drivetrainIssue['selected'] == true){
                    var driveTrainHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + drivetrainIssue['questionTitle'] + ': </b>'+ drivetrainIssue['answer'][0]['value']+ '</div></div>';
                   
                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + drivetrainIssue['questionTitle'] + ': </b> ' + drivetrainIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + drivetrainIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (transmissionIssue['selected'] == true){
                    var transmissionHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + transmissionIssue['questionTitle'] + ': </b>'+ transmissionIssue['answer'][0]['value']+ '</div></div>';

                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + transmissionIssue['questionTitle'] + ': </b> ' + transmissionIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + transmissionIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (breakIssue['selected'] == true){
                    var breakIssueHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + breakIssue['questionTitle'] + ': </b>'+ breakIssue['answer'][0]['value']+ '</div></div>';

                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + breakIssue['questionTitle'] + ': </b> ' + breakIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + breakIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (suspensionIssue['selected'] == true){
                    var suspensionIssueHtml = '<div class="col-lg-6"><div> <b>' + suspensionIssue['questionTitle'] + ': </b>'+ suspensionIssue['answer'][0]['value']+ '</div></div>';

                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + suspensionIssue['questionTitle'] + ': </b> ' + suspensionIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + suspensionIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (steeringIssue['selected'] == true){
                    var steeringIssueHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + steeringIssue['questionTitle'] + ': </b>'+ steeringIssue['answer'][0]['value']+ '</div></div>';
                   
                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + steeringIssue['questionTitle'] + ': </b> ' + steeringIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{

                    $('#driveability_report').append('<div class="col-lg-6"><div> <b>' + steeringIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (vehicleStay['selected'] == true){
                    var vehicleStayHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + vehicleStay['questionTitle'] + ': </b>'+ vehicleStay['answer'][0]['value']+ '</div></div>';
                
                    $('#mechnical_report').empty().append('<div class="col-lg-6"><div> <b>' + vehicleStay['questionTitle'] + ': </b> ' + vehicleStay['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{

                    $('#mechnical_report').empty().append('<div class="col-lg-6"><div> <b>' + vehicleStay['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (vehicleCrank['selected'] == true){
                    var vehicleCrank = '<div class="col-lg-6 bg_orange"><div> <b>' + vehicleCrank['questionTitle'] + ': </b>'+ vehicleCrank['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + vehicleCrank['questionTitle'] + ': </b> ' + vehicleCrank['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + vehicleCrank['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (engine_does_not_stay_running['selected'] == true){
                    var engineDoesNotStayRunningHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + engine_does_not_stay_running['questionTitle'] + ': </b>'+ engine_does_not_stay_running['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engine_does_not_stay_running['questionTitle'] + ': </b> ' + engine_does_not_stay_running['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engine_does_not_stay_running['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (engine_overheats['selected'] == true){
                    var engineOverheatsHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + engine_overheats['questionTitle'] + ': </b>'+ engine_overheats['answer'][0]['value']+ '</div></div>';
                   
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engine_overheats['questionTitle'] + ': </b> ' + engine_overheats['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engine_overheats['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (supercharger_issue['selected'] == true){
                    var superchargerIssueHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + supercharger_issue['questionTitle'] + ': </b>'+ supercharger_issue['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + supercharger_issue['questionTitle'] + ': </b> ' + supercharger_issue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + supercharger_issue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (emissions_issue['selected'] == true){
                    var emissionsIssueHtml = '<div class="col-lg-6"><div> <b>' + emissions_issue['questionTitle'] + ': </b>'+ emissions_issue['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + emissions_issue['questionTitle'] + ': </b> ' + emissions_issue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + emissions_issue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (oil_level_issue['selected'] == true){
                    var oilLevelIssueHtml = '<div class="col-lg-6"><div> <b>' + oil_level_issue['questionTitle'] + ': </b>'+ oil_level_issue['answer'][0]['value']+ '</div></div>';
                   
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + oil_level_issue['questionTitle'] + ': </b> ' + oil_level_issue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + oil_level_issue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');

                }

                if (oil_condition_issue['selected'] == true){
                    var oilConditionIssueHtml = '<div class="col-lg-6"><div> <b>' + oil_condition_issue['questionTitle'] + ': </b>'+ oil_condition_issue['answer'][0]['value']+ '</div></div>';
                
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + oil_condition_issue['questionTitle'] + ': </b> ' + oil_condition_issue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + oil_condition_issue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (coolant_level_issue['selected'] == true){
                    var coolantLevelIssueHtml = '<div class="col-lg-6"><div> <b>' + coolant_level_issue['questionTitle'] + ': </b>'+ coolant_level_issue['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + coolant_level_issue['questionTitle'] + ': </b> ' + oil_condition_issue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + coolant_level_issue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                
                if (engineNoice['selected'] == true){
                    var engineNoiceHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + engineNoice['questionTitle'] + ': </b>'+ engineNoice['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engineNoice['questionTitle'] + ': </b> ' + engineNoice['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engineNoice['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (engineHesitation['selected'] == true){
                    var engineHesitationHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + engineHesitation['questionTitle'] + ': </b>'+ engineHesitation['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engineHesitation['questionTitle'] + ': </b> ' + engineHesitation['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engineHesitation['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (timingchainIssue['selected'] == true){
                    var timingchainIssueHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + timingchainIssue['questionTitle'] + ': </b>'+ timingchainIssue['answer'] [0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + timingchainIssue['questionTitle'] + ': </b> ' + timingchainIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + timingchainIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (abnormalexhaustSmoke['selected'] == true){
                    var abnormalexhaustSmokeHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + abnormalexhaustSmoke['questionTitle'] + ': </b>'+ abnormalexhaustSmoke['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + abnormalexhaustSmoke['questionTitle'] + ': </b> ' + abnormalexhaustSmoke['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + abnormalexhaustSmoke['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (headgasketIssue['selected'] == true){
                    var headgasketIssueHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + headgasketIssue['questionTitle'] + ': </b>'+ headgasketIssue['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + headgasketIssue['questionTitle'] + ': </b> ' + abnormalexhaustSmoke['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + headgasketIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (exhaust_noise['selected'] == true){
                    var exhaustNoiseHtml = '<div class="col-lg-6"><div> <b>' + exhaust_noise['questionTitle'] + ': </b>'+ exhaust_noise['answer'][0]['value']+ '</div></div>';
                   
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + exhaust_noise['questionTitle'] + ': </b> ' + exhaust_noise['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + exhaust_noise['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (exhaust_modifications['selected'] == true){
                    var exhaustModificationsHtml = '<div class="col-lg-6"><div> <b>' + exhaust_modifications['questionTitle'] + ': </b>'+ exhaust_modifications['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + exhaust_modifications['questionTitle'] + ': </b> ' + exhaust_modifications['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + exhaust_modifications['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (suspension_modifications['selected'] == true){
                    var suspensionModificationsHtml = '<div class="col-lg-6"><div> <b>' + suspension_modifications['questionTitle'] + ': </b>'+ suspension_modifications['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + suspension_modifications['questionTitle'] + ': </b> ' + suspension_modifications['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + suspension_modifications['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (emissions_modifications['selected'] == true){
                    var emissionsModificationsHtml = '<div class="col-lg-6"><div> <b>' + emissions_modifications['questionTitle'] + ': </b>'+ emissions_modifications['answer'][0]['value']+ '</div></div>';
                  
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + emissions_modifications['questionTitle'] + ': </b> ' + emissions_modifications['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + emissions_modifications['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (catalytic_converters_missing['selected'] == true){
                    var catalyticConvertersMissingHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + catalytic_converters_missing['questionTitle'] + ': </b>'+ catalytic_converters_missing['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + catalytic_converters_missing['questionTitle'] + ': </b> ' + catalytic_converters_missing['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + catalytic_converters_missing['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (jump_start_required['selected'] == true){
                    var jumpStartRequiredHtml = '<div class="col-lg-6"><div> <b>' + jump_start_required['questionTitle'] + ': </b>'+ jump_start_required['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + jump_start_required['questionTitle'] + ': </b> ' + jump_start_required['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + jump_start_required['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (aftermarket_mechanical['selected'] == true){
                    var aftermarketMechanicalHtml = '<div class="col-lg-6"><div> <b>' + aftermarket_mechanical['questionTitle'] + ': </b>'+ aftermarket_mechanical['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_mechanical['questionTitle'] + ': </b> ' + aftermarket_mechanical['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_mechanical['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (engine_accessory_issue['selected'] == true){
                    var engineAccessoryIssueHtml = '<div class="col-lg-6"><div> <b>' + engine_accessory_issue['questionTitle'] + ': </b>'+ engine_accessory_issue['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engine_accessory_issue['questionTitle'] + ': </b> ' + engine_accessory_issue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + engine_accessory_issue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (fluid_leaks['selected'] == true){
                    var fluidLeaksHtml = '<div class="col-lg-6"><div> <b>' + fluid_leaks['questionTitle'] + ': </b>'+ fluid_leaks['answer'][0]['value']+ '</div></div>';
                    
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + fluid_leaks['questionTitle'] + ': </b> ' + fluid_leaks['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + fluid_leaks['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (oil_intermix_dipstick_v2['selected'] == true){
                    var oilIntermixDipstickV2Html = '<div class="col-lg-6 bg_yellow"><div> <b>' + oil_intermix_dipstick_v2['questionTitle'] + ': </b>'+ oil_intermix_dipstick_v2['answer'][0]['value']+ '</div></div>';

                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + oil_intermix_dipstick_v2['questionTitle'] + ': </b> ' + oil_intermix_dipstick_v2['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#mechnical_report').append('<div class="col-lg-6"><div> <b>' + oil_intermix_dipstick_v2['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (minor_body_damage['selected'] == true){
                    var minorBodyDamageHtml = '<div class="col-lg-6"><div><div> <b>' + minor_body_damage['questionTitle'] + ': </b>'+ minor_body_damage['answer'][0]['value']+'</div> </div>';
                    $('#exterior_report').empty().append('<div class="col-lg-6"><div> <b>' + minor_body_damage['questionTitle'] + ': </b> ' + minor_body_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#exterior_report').empty().append('<div class="col-lg-6"><div> <b>' + minor_body_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (modrate_body_damage['selected'] == true){
                    
                    var modrateBodyDamageHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + modrate_body_damage['questionTitle'] + ': </b>'+ modrate_body_damage['answer'][0]['value']+ '</div></div>';

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + modrate_body_damage['questionTitle'] + ': </b> ' + modrate_body_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + modrate_body_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (major_body_damage['selected'] == true){
                    var majorBodyDamageHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + major_body_damage['questionTitle'] + ': </b>'+ major_body_damage['answer'][0]['value']+ '</div></div>';

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + major_body_damage['questionTitle'] + ': </b> ' + major_body_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');                    
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + major_body_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');

                }

                if (scratches['selected'] == true){
                    var scratchesHtml = '<div class="col-lg-6"><div> <b>' + scratches['questionTitle'] + ': </b>'+ scratches['answer'][0]['value']+ '</div></div>';

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + scratches['questionTitle'] + ': </b> ' + scratches['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');   
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + scratches['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (glass_damage['selected'] == true){
                    var glassDamageHtml = '<div class="col-lg-6"><div> <b>' + glass_damage['questionTitle'] + ': </b>'+ glass_damage['answer'][0]['value']+ '</div></div>';
                    
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + glass_damage['questionTitle'] + ': </b> ' + glass_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');        

                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + glass_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (light_damage['selected'] == true){
                    var lightDamageHtml = '<div class="col-lg-6"><div> <b>' + light_damage['questionTitle'] + ': </b>'+ light_damage['answer'][0]['value']+ '</div></div>';
                

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + light_damage['questionTitle'] + ': </b> ' + light_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');   
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + light_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (minor_body_rust['selected'] == true){
                    var minorBodyRustHtml = '<div class="col-lg-6"><div> <b>' + minor_body_rust['questionTitle'] + ': </b>'+ minor_body_rust['answer'][0]['value']+ '</div></div>';

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + minor_body_rust['questionTitle'] + ': </b> ' + minor_body_rust['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');   
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + minor_body_rust['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (modrate_body_rust['selected'] == true){
                    var modrateBodyRustHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + modrate_body_rust['questionTitle'] + ': </b>'+ modrate_body_rust['answer'][0]['value']+ '</div></div>';

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + modrate_body_rust['questionTitle'] + ': </b> ' + modrate_body_rust['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');   
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + modrate_body_rust['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (major_body_rust['selected'] == true){
                    var majorBodyRustHtml = '<div class="col-lg-6"><div> <b>' + major_body_rust['questionTitle'] + ': </b>'+ major_body_rust['answer'][0]['value']+ '</div></div>';
                    
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + major_body_rust['questionTitle'] + ': </b> ' + major_body_rust['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');   

                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + major_body_rust['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (hail_damage['selected'] == true){
                    var hailDamageHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + hail_damage['questionTitle'] + ': </b>'+ hail_damage['answer'][0]['value']+ '</div></div>';
                   
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + hail_damage['questionTitle'] + ': </b> ' + hail_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + hail_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');                    
                }

                if (aftermarket_parts['selected'] == true){
                    var aftermarketPartsHtml = '<div class="col-lg-6"><div> <b>' + aftermarket_parts['questionTitle'] + ': </b>'+ aftermarket_parts['answer'] [0]['value']+ '</div></div>';
                   
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_parts['questionTitle'] + ': </b> ' + aftermarket_parts['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_parts['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');   

                }

                if (mismatched_paint['selected'] == true){
                    var mismatchedPaintHtml = '<div class="col-lg-6"><div> <b>' + mismatched_paint['questionTitle'] + ': </b>'+ mismatched_paint['answer'][0]['value']+ '</div></div>';
                    
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + mismatched_paint['questionTitle'] + ': </b> ' + mismatched_paint['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + mismatched_paint['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');  
                }

                if (paint_meter_readings['selected'] == true){
                    var paintMeterReadingsHtml = '<div class="col-lg-6"><div> <b>' + paint_meter_readings['questionTitle'] + ': </b>'+ 'minValue : ' +paint_meter_readings['answer'][0]['minValue']+ ',maxValue: '+ paint_meter_readings['answer'][0]['maxValue']  +'</div></div>';
                
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + paint_meter_readings['questionTitle'] + ': </b> minValue : ' + paint_meter_readings['answer'][0]['minValue'] + ', maxValue: '+ paint_meter_readings['answer'][0]['maxValue']  +'</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + paint_meter_readings['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');  
                }
                
                if (poor_quality_repair['selected'] == true){
                    var poorQualityRepairHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + poor_quality_repair['questionTitle'] + ': </b>'+ poor_quality_repair['answer'][0]['value']+ '</div></div>';
                   
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + poor_quality_repair['questionTitle'] + ': </b> ' + poor_quality_repair['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + poor_quality_repair['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');  
                }

                if (previous_paint_work['selected'] == true){
                    var previousPaintWorkHtml = '<div class="col-lg-6"><div> <b>' + previous_paint_work['questionTitle'] + ': </b>'+ previous_paint_work['answer'][0]['value']+ '</div></div>';

                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + previous_paint_work['questionTitle'] + ': </b> ' + previous_paint_work['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#exterior_report').append('<div class="col-lg-6"><div> <b>' + previous_paint_work['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                if (penetratingRust['selected'] == true){
                    var penetratingRustHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + penetratingRust['questionTitle'] + ': </b>'+ penetratingRust['answer'][0]['value']+ '</div></div>';
                    
                    $('#frame_report').empty().append('<div class="col-lg-6"><div> <b>' + penetratingRust['questionTitle'] + ': </b> ' + penetratingRust['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#frame_report').empty().append('<div class="col-lg-6"><div> <b>' + penetratingRust['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (unbodyDamage['selected'] == true){
                    var unbodyDamageHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + unbodyDamage['questionTitle'] + ': </b>'+ unbodyDamage['answer'][0]['value']+ '</div></div>';

                    $('#frame_report').append('<div class="col-lg-6"><div> <b>' + unbodyDamage['questionTitle'] + ': </b> ' + unbodyDamage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#frame_report').append('<div class="col-lg-6"><div> <b>' + unbodyDamage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (surface_rust['selected'] == true){
                    var surfaceRustHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + surface_rust['questionTitle'] + ': </b>'+ surface_rust['answer'][0]['value']+ '</div></div>';

                    $('#frame_report').append('<div class="col-lg-6"><div> <b>' + surface_rust['questionTitle'] + ': </b> ' + surface_rust['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#frame_report').append('<div class="col-lg-6"><div> <b>' + surface_rust['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (heavy_rust['selected'] == true){
                    var heavyRustHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + heavy_rust['questionTitle'] + ': </b>'+ heavy_rust['answer'][0]['value']+ '</div></div>';

                    $('#frame_report').append('<div class="col-lg-6"><div> <b>' + heavy_rust['questionTitle'] + ': </b> ' + heavy_rust['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#frame_report').append('<div class="col-lg-6"><div> <b>' + heavy_rust['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (seatDamage['selected'] == true){
                    var seatDamageHtml = '<div class="col-lg-6"><div> <b>' + seatDamage['questionTitle'] + ': </b>'+ seatDamage['answer'][0]['value']+ '</div></div>';
                   
                    $('#interior_report').empty().append('<div class="col-lg-6"><div> <b>' + seatDamage['questionTitle'] + ': </b> ' + seatDamage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').empty().append('<div class="col-lg-6"><div> <b>' + seatDamage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (carpet_damage['selected'] == true){
                    var carpetDamageHtml = '<div class="col-lg-6"><div> <b>' + carpet_damage['questionTitle'] + ': </b>'+ carpet_damage['answer'][0]['value']+ '</div></div>';

                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + carpet_damage['questionTitle'] + ': </b> ' + carpet_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + carpet_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (dashboardDamage['selected'] == true){
                    var dashboardDamageHtml = '<div class="col-lg-6"><div> <b>' + dashboardDamage['questionTitle'] + ': </b>'+ dashboardDamage['answer'][0]['value']+ '</div></div>';

                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + dashboardDamage['questionTitle'] + ': </b> ' + dashboardDamage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + dashboardDamage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (headliner_damage['selected'] == true){
                    var headlinerDamageHtml = '<div class="col-lg-6"><div> <b>' + headliner_damage['questionTitle'] + ': </b>'+ headliner_damage['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + headliner_damage['questionTitle'] + ': </b> ' + headliner_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + headliner_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (interiorTrimDamage['selected'] == true){
                    var interiorTrimDamageHtml = '<div class="col-lg-6"><div> <b>' + interiorTrimDamage['questionTitle'] + ': </b>'+ interiorTrimDamage['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + interiorTrimDamage['questionTitle'] + ': </b> ' + interiorTrimDamage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + interiorTrimDamage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (interior_order['selected'] == true){
                    var interiorOrderHtml = '<div class="col-lg-6"><div> <b>' + interior_order['questionTitle'] + ': </b>'+ interior_order['answer'][0]['value']+ '</div></div>';
                   
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + interior_order['questionTitle'] + ': </b> ' + interior_order['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + interior_order['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(crank_windows['selected'] == true){
                    var crankWindowsHtml = '<div class="col-lg-6"><div> <b>' + crank_windows['questionTitle'] + ': </b>'+ crank_windows['answer'][0]['value']+ '</div></div>';

                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + crank_windows['questionTitle'] + ': </b> ' + crank_windows['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + crank_windows['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(no_factory_ac['selected'] == true){
                    var noFactoryAcHtml = '<div class="col-lg-6"><div> <b>' + no_factory_ac['questionTitle'] + ': </b>'+ no_factory_ac['answer'][0]['value']+ '</div></div>';
                   
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + no_factory_ac['questionTitle'] + ': </b> ' + no_factory_ac['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + no_factory_ac['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(electricalIssue['selected'] == true){
                    var electricalIssueHtml = '<div class="col-lg-6"><div> <b>' + electricalIssue['questionTitle'] + ': </b>'+ electricalIssue['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + electricalIssue['questionTitle'] + ': </b> ' + electricalIssue['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + electricalIssue['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(five_digit_odometer['selected'] == true){
                    var fiveDigitOdometerHtml = '<div class="col-lg-6"><div> <b>' + five_digit_odometer['questionTitle'] + ': </b>'+ five_digit_odometer['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + five_digit_odometer['questionTitle'] + ': </b> ' + five_digit_odometer['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + five_digit_odometer['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(sunroof['selected'] == true){
                    var sunroofHtml = '<div class="col-lg-6"><div> <b>' + sunroof['questionTitle'] + ': </b>'+ sunroof['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + sunroof['questionTitle'] + ': </b> ' + sunroof['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + sunroof['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(navigation['selected'] == true){
                    var navigationHtml = '<div class="col-lg-6"><div> <b>' + navigation['questionTitle'] + ': </b>'+ navigation['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + navigation['questionTitle'] + ': </b> ' + navigation['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + navigation['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(aftermarket_stereo['selected'] == true){
                    var aftermarketStereoHtml = '<div class="col-lg-6"><div> <b>' + aftermarket_stereo['questionTitle'] + ': </b>'+ aftermarket_stereo['answer'][0]['value']+ '</div></div>';
                   
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_stereo['questionTitle'] + ': </b> ' + aftermarket_stereo['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_stereo['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (airbagData['selected'] == true){
                    var airbagHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + airbagData['questionTitle'] + ': </b>'+ airbagData['answer'][0]['value'] + '</div></div>';
                   
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + airbagData['questionTitle'] + ': </b> ' + airbagData['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + airbagData['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if( hvac_not_working['selected'] == true){
                    var hvacNotWorkingHtml = '<div class="col-lg-6"><div> <b>' + hvac_not_working['questionTitle'] + ': </b>'+ hvac_not_working['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + hvac_not_working['questionTitle'] + ': </b> ' + hvac_not_working['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{

                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + hvac_not_working['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(leather_seats['selected'] == true){
                    var leatherSeatsHtml = '<div class="col-lg-6"><div> <b>' + leather_seats['questionTitle'] + ': </b>'+ leather_seats['answer'][0]['value']+ '</div></div>';
                   
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + leather_seats['questionTitle'] + ': </b> ' + leather_seats['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 

                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + leather_seats['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(aftermarket_sunroof['selected'] == true){
                    var aftermarketSunroofHtml = '<div class="col-lg-6"><div> <b>' + aftermarket_sunroof['questionTitle'] + ': </b>'+ aftermarket_sunroof['answer'][0]['value']+ '</div></div>';
                  
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_sunroof['questionTitle'] + ': </b> ' + aftermarket_sunroof['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + aftermarket_sunroof['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(backup_camera['selected'] == true){
                    var backupCameraHtml = '<div class="col-lg-6"><div> <b>' + backup_camera['questionTitle'] + ': </b>'+ backup_camera['answer'][0]['value']+ '</div></div>';
                    
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + backup_camera['questionTitle'] + ': </b> ' + backup_camera['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>'); 
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + backup_camera['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(charging_cable['selected'] == true){
                    var chargingCableHtml = '<div class="col-lg-6"><div> <b>' + charging_cable['questionTitle'] + ': </b>'+ charging_cable['answer'][0]['value']+ '</div></div>';
                   
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + charging_cable['questionTitle'] + ': </b> ' + charging_cable['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#interior_report').append('<div class="col-lg-6"><div> <b>' + charging_cable['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                    
                if (aftermarket_wheels['selected'] == true){
                    var aftermarketWheelsHtml = '<div class="col-lg-6"><div> <b>' + aftermarket_wheels['questionTitle'] + ': </b>'+ aftermarket_wheels['answer'][0]['value']+ '</div></div>';
                   
                    $('#tires_report').empty().append('<div class="col-lg-6"><div> <b>' + aftermarket_wheels['questionTitle'] + ': </b> ' + aftermarket_wheels['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                    
                }else{
                    $('#tires_report').empty().append('<div class="col-lg-6"><div> <b>' + aftermarket_wheels['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (damaged_wheels['selected'] == true){
                    var damagedWheelsHtml = '<div class="col-lg-6"><div> <b>' + damaged_wheels['questionTitle'] + ': </b>'+ damaged_wheels['answer'][0]['value']+ '</div></div>';
                   
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + damaged_wheels['questionTitle'] + ': </b> ' + damaged_wheels['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + damaged_wheels['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (oversized_tires['selected'] == true){
                    var oversizedTiresHtml = '<div class="col-lg-6"><div> <b>' + oversized_tires['questionTitle'] + ': </b>'+ oversized_tires['answer'][0]['value']+ '</div></div>';
                    
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + oversized_tires['questionTitle'] + ': </b> ' + oversized_tires['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + oversized_tires['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (damaged_tiles['selected'] == true){
                    var damagedTilesHtml = '<div class="col-lg-6"><div> <b>' + damaged_tiles['questionTitle'] + ': </b>'+ damaged_tiles['answer'][0]['value']+ '</div></div>';
                   
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + damaged_tiles['questionTitle'] + ': </b> ' + damaged_tiles['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + damaged_tiles['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (uneven_tread_wear['selected'] == true){
                    var unevenTreadWearHtml = '<div class="col-lg-6"><div> <b>' + uneven_tread_wear['questionTitle'] + ': </b>'+ uneven_tread_wear['answer'][0]['value']+ '</div></div>';
                   
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + uneven_tread_wear['questionTitle'] + ': </b> ' + uneven_tread_wear['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + uneven_tread_wear['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (mismatched_tires['selected'] == true){
                    var mismatchedTiresHtml = '<div class="col-lg-6"><div> <b>' + mismatched_tires['questionTitle'] + ': </b>'+ mismatched_tires['answer'][0]['value']+ '</div></div>';
                   
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + mismatched_tires['questionTitle'] + ': </b> ' + mismatched_tires['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + mismatched_tires['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(missing_spare_tire['selected'] == true){
                    var missingSpareTireHtml = '<div class="col-lg-6"><div> <b>' + missing_spare_tire['questionTitle'] + ': </b>'+ missing_spare_tire['answer'][0]['value']+ '</div></div>';
                    
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + missing_spare_tire['questionTitle'] + ': </b> ' + missing_spare_tire['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + missing_spare_tire['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (tire_measurements['selected'] == true){

                    var tireMeasurementsHtml = '<div class="col-lg-6"><div> <b>' + tire_measurements['questionTitle'] + ': </b>'+ 'Front Right Tire:' + tire_measurements['answer'] [0]['suffix'] + ',Front Left Tire:'+ tire_measurements['answer'] [1]['suffix'] + ',Back Left Tire: ' +  
                    tire_measurements['answer'] [2]['suffix'] + ',Back Right Tire:' + tire_measurements['answer'] [3]['suffix'] + '</div></div>';

         
                    // $('#tires_report').append('<div class="col-lg-6"> <b>' + tire_measurements['questionTitle'] + ': </b> Yes '+ 'Front Right Tire:' + tire_measurements['answer'] [0]['suffix'] + ',Front Left Tire:'+ tire_measurements['answer'] [1]['suffix'] + ',Back Left Tire: ' +  
                    // tire_measurements['answer'] [2]['suffix'] + ',Back Right Tire:' + tire_measurements['answer'] [3]['suffix'] + ' </div>');

                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + tire_measurements['questionTitle'] + ': </b> ' + 'Front Right Tire:' + tire_measurements['answer'] [0]['suffix'] + ',Front Left Tire:'+ tire_measurements['answer'] [1]['suffix'] + ',Back Left Tire: ' +  
                    tire_measurements['answer'] [2]['suffix'] + ',Back Right Tire:' + tire_measurements['answer'] [3]['suffix'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#tires_report').append('<div class="col-lg-6"><div> <b>' + tire_measurements['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (title_absent['selected'] == true){
                    var titleAbsentHtml = '<div class="col-lg-6 bg_blue"><div> <b>' + title_absent['questionTitle'] + ': </b>'+ title_absent['answer'][0]['value']+ '</div></div>';
                  
                    $('#title_report').empty().append('<div class="col-lg-6"><div> <b>' + title_absent['questionTitle'] + ': </b> ' + title_absent['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').empty().append('<div class="col-lg-6"><div> <b>' + title_absent['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }
                
                if (title_branded['selected'] == true){
                    var titleBrandedHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + title_branded['questionTitle'] + ': </b>'+ title_branded['answer'][0]['value']+ '</div></div>';
                    
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + title_branded['questionTitle'] + ': </b> ' + title_branded['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + title_branded['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(true_mileage_unknown['selected'] == true){
                    var trueMileageUnknownHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + true_mileage_unknown['questionTitle'] + ': </b>'+ true_mileage_unknown['answer'][0]['value']+ '</div></div>';
                   
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + true_mileage_unknown['questionTitle'] + ': </b> ' + true_mileage_unknown['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + true_mileage_unknown['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');

                }
                                
                if (flood_damage['selected'] == true){
                    var floodDamageHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + flood_damage['questionTitle'] + ': </b>'+ flood_damage['answer'][0]['value']+ '</div></div>';
                    
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + flood_damage['questionTitle'] + ': </b> ' + flood_damage['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + flood_damage['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(off_lease_vehicle['selected'] == true){
                    var offLeaseVehicleHtml = '<div class="col-lg-6"><div> <b>' + off_lease_vehicle['questionTitle'] + ': </b>'+ off_lease_vehicle['answer'][0]['value']+ '</div></div>';
                    
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + off_lease_vehicle['questionTitle'] + ': </b> ' + off_lease_vehicle['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + off_lease_vehicle['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(repair_order_attached['selected'] == true){
                    var repairOrderAttachedHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + repair_order_attached['questionTitle'] + ': </b>'+ repair_order_attached['answer'][0]['value']+ '</div></div>';
                
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + repair_order_attached['questionTitle'] + ': </b> ' + repair_order_attached['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');

                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + repair_order_attached['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(repossession['selected'] == true){
                    var repossessionHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + repossession['questionTitle'] + ': </b>'+ repossession['answer'][0]['value']+ '</div></div>';
                    
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + repossession['questionTitle'] + ': </b> ' + repossession['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + repossession['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(repossession_papers_wo_title['selected'] == true){
                    var repossessionPapersWoTitleHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + repossession_papers_wo_title['questionTitle'] + ': </b>'+ repossession_papers_wo_title['answer'][0]['value']+ '</div></div>';
                   
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + repossession_papers_wo_title['questionTitle'] + ': </b> ' + repossession_papers_wo_title['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + repossession_papers_wo_title['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(mobility['selected'] == true){
                    var mobilityHtml = '<div class="col-lg-6 bg_yellow"><div> <b>' + mobility['questionTitle'] + ': </b>'+ mobility['answer'][0]['value']+ '</div></div>';
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + mobility['questionTitle'] + ': </b> ' + mobility['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + mobility['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if (transferrable_registration['selected'] == true){
                    var transferrableRegistrationHtml = '<div class="col-lg-6 bg_orange"><div> <b>' + transferrable_registration['questionTitle'] + ': </b>'+ transferrable_registration['answer'][0]['value']+ '</div></div>';
                    
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + transferrable_registration['questionTitle'] + ': </b> ' + transferrable_registration['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + transferrable_registration['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                if(sold_on_bill_of_sale['selected'] == true){
                    var soldOnBillOfSaleHtml = '<div class="col-lg-6 bg_red"><div> <b>' + sold_on_bill_of_sale['questionTitle'] + ': </b>'+ sold_on_bill_of_sale['answer'][0]['value']+ '</div></div>';
                   
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + sold_on_bill_of_sale['questionTitle'] + ': </b> ' + sold_on_bill_of_sale['answer'][0]['value'] + '</div> <div class="text-right text-success">Yes</div> </div>');
                }else{
                    $('#title_report').append('<div class="col-lg-6"><div> <b>' + sold_on_bill_of_sale['questionTitle'] + '</b> </div> <div class="text-right text-danger">  No </div></div>');
                }

                  
                var lights = response[1];
                if (lights[1]) {
                    var colors = lights[1].split(' ');
                    var acvLightHtml = '<div class="col-lg-6"><div class="lights-btn"><b>ACV Lights: <a href="' + lights[2] + '" target="_blank"><button class="btn btn-sm btn-primary" >Go To Auction</button></a></b>';

                    for (var i = 0; i < colors.length; i++) {
                        acvLightHtml += '<span class="' + colors[i] + '">' + colors[i] + '</span> ';
                    }

                    acvLightHtml += '</div></div>';
                }

                var vehicle_details = '<span><b>Vehicle Details</b></span><table data-v-bf22c5b6="" data-v-7769f27a="" class="table table-bordered table-striped"><tbody data-v-bf22c5b6=""><tr data-v-bf22c5b6=""><td data-v-bf22c5b6="" class="left"> Distance </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+lights[3]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-bf22c5b6="" class="left"> City </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[4]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-bf22c5b6="" class="left"> VIN </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[5]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Odometer </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6="">  '+ lights[6]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Transmission </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[7]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Trim </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[8]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Drivetrain </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[9]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Engine </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[10]+'  </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Fuel Type </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[11]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Year </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[12]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Make </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[13]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Model </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[14]+'  </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Color </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[15]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Auction ID </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[0]+' </span><!----></td></tr><tr data-v-bf22c5b6=""><td data-v-7769f27a="" data-v-bf22c5b6="" class="left"> Auction Date </td><td data-v-7769f27a="" data-v-bf22c5b6="" class="right"><span data-v-7769f27a="" data-v-bf22c5b6=""> '+ lights[16] +' </span><!----></td></tr></tbody></table>';
                
                $('#vehicle-detail').empty()
                .append(vehicle_details)
                
                $('#auction-condition').empty()
                .append(acvLightHtml)
                
                //red color
                .append(soldOnBillOfSaleHtml)

                // blue color
                .append(titleAbsentHtml)

                // orange color
                .append(floodDamageHtml)
                .append(transferrableRegistrationHtml)
                .append(vehicleCrank)
                .append(vehicleHtml)
                .append(majorBodyDamageHtml)
                .append(vehicleStayHtml)
                .append(heavyRustHtml)
                .append(modrateBodyDamageHtml)
                .append(airbagHtml)
                .append(titleBrandedHtml)

                // yellow color
                .append(penetratingRustHtml)
                .append(headgasketIssueHtml)
                .append(engineOverheatsHtml)
                .append(timingchainIssueHtml)
                .append(engineNoiceHtml)
                .append(oilIntermixDipstickV2Html)
                .append(superchargerIssueHtml)
                .append(transmissionHtml)
                .append(driveTrainHtml)
                .append(steeringIssueHtml)
                .append(breakIssueHtml)
                .append(abnormalexhaustSmokeHtml)
                .append(engineHesitationHtml)
                .append(engineDoesNotStayRunningHtml)
                .append(modrateBodyRustHtml)
                .append(surfaceRustHtml)
                .append(poorQualityRepairHtml)
                .append(hailDamageHtml)
                .append(catalyticConvertersMissingHtml)
                .append(batteryLightHtml)
                .append(trueMileageUnknownHtml)
                .append(unbodyDamageHtml)
                .append(repossessionHtml)
                .append(repossessionPapersWoTitleHtml)
                .append(repairOrderAttachedHtml)
                .append(mobilityHtml)

                .append(minorBodyDamageHtml)
                .append(glassDamageHtml)
                .append(lightDamageHtml)
                .append(aftermarketPartsHtml)
                .append(OBDIICodesHtml)
                .append(incompleteMonitorsHtml)
                .append(seatDamageHtml)
                .append(dashboardDamageHtml)
                .append(interiorTrimDamageHtml)
                .append(electricalIssueHtml)
                .append(suspensionIssueHtml)
                .append(aftermarketWheelsHtml)
                .append(damagedWheelsHtml)
                .append(damagedTilesHtml)
                .append(tireMeasurementsHtml)
                .append(aftermarketMechanicalHtml)
                .append(engineAccessoryIssueHtml)
                .append(scratchesHtml)
                .append(minorBodyRustHtml)
                .append(majorBodyRustHtml)
                .append(mismatchedPaintHtml)
                .append(paintMeterReadingsHtml)
                .append(previousPaintWorkHtml)
                .append(jumpStartRequiredHtml)
                .append(fluidLeaksHtml)
                .append(oilLevelIssueHtml)
                .append(oilConditionIssueHtml)
                .append(emissionsModificationsHtml)
                .append(emissionsIssueHtml)
                .append(coolantLevelIssueHtml)
                .append(exhaustModificationsHtml)
                .append(exhaustNoiseHtml)
                .append(suspensionModificationsHtml)
                .append(checkEngineLightHtml)
                .append(airbagLightHtml)
                .append(brakeLightHtml)
                .append(otherWarningLightHtml)
                .append(tractionControlLightHtml)
                .append(tpmsLightHtml)
                .append(oversizedTiresHtml)
                .append(unevenTreadWearHtml)
                .append(mismatchedTiresHtml)
                .append(missingSpareTireHtml)
                .append(carpetDamageHtml)
                .append(headlinerDamageHtml)
                .append(interiorOrderHtml)
                .append(crankWindowsHtml)
                .append(noFactoryAcHtml)
                .append(fiveDigitOdometerHtml)
                .append(sunroofHtml)
                .append(navigationHtml)
                .append(aftermarketStereoHtml)
                .append(hvacNotWorkingHtml)
                .append(leatherSeatsHtml)
                .append(aftermarketSunroofHtml)
                .append(backupCameraHtml)
                .append(chargingCableHtml)
                .append(offLeaseVehicleHtml);
            }else{
                $('#auction-condition').empty().append('<div class="col-lg-6"> <b> No Data Found </b></div>');
            }   
        },
        error: function(xhr, status, error) {
            $('#auction-condition').empty().append('<div class="col-lg-6"> <b>Error fetching data</b></div>');
            console.error(error);
        },
        complete: function() {
            $('.loader').hide();
        }
    })
}

function full_condition_report(){
    $('#exterior').modal({show:true});
}

function frame_full_condition_report(){
    $('#frame').modal({show:true});
}

function mechnical_condition_report(){
    $('#mechnical').modal({show:true});
}

function driveability_condition_report(){
    $('#driveability').modal({show:true});
}
  
function lights_condition_report(){
    $('#lights').modal({show:true});
}

function tires_condition_report(){
    $('#tires').modal({show:true});
}

function interior_condition_report(){
    $('#interior').modal({show:true});
}

function title_condition_report(){
    $('#title').modal({show:true});
}

function placebid(currunt_bid, bidAmount, auctionId ){
    $('#place_bid').modal({show:true});
    $('#auction_id').val(auctionId);
    $('#place_bid_amount').text(bidAmount);
    $('#currunt_bid').text(currunt_bid);
}

function notification(){
    $('#notifications').modal({show:true});
    $.ajax({
        url: WS_PATH + '/get-notification-list/',
        type: 'POST',
        success: function (response) {
            var data = response;                    
            var str = '';
            if (data.length == 0) {
                str += '<tr>';
                    str += '<td colspan="1" align="center">No Notification found</td>';
                str += '</tr>';
            }else{
                data.forEach(auction => {
                    var auctionData = JSON.parse(auction[2]);
                    var auctionId = auctionData['data']['id'];
                    var massage = auctionData['data']['message'];
                    str += '<span>'+ auctionId + ' : ' + massage + '</span>';
                });
            }
            $('#notification_list').empty().append(str);
        }
    })

}


