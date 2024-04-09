<?php include 'header.php';?>


   <div class="body-overlay"></div>
   <!-- offcanvas area end -->

    <main>

	  <!-- breadcrumb area start -->
      <div class="breadcrumb-custom">
         <div class="container">
            <div class="row">
               <div class="col-xxl-12">
                  <div class="breadcrumb__content p-relative z-index-1">
                     <div class="breadcrumb__list">
                        <span><a href="index.php">Home</a></span>
                        <span class="dvdr"><i class="fa-regular fa-angle-right"></i></span>
                        <span>Live Auction</span>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </div>
      <!-- breadcrumb area end -->

    <!-- Banner-Slider -->
    <section class="Detailpage">
        <div class="container container-full">
			
			<div class="row">
				<div class="leftpart4">
					<div class="row"> 
						<div class="col-lg-3">
							<div class="car-details mb-15">
								<div class="product-details-img">
									<div id="aniimated-thumbnials"  class="slider-for" style="height:auto">

										<div class="item">
											<a href="assets/images/car-slide-01.jpeg" data-src="assets/images/car-slide-01.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-01.jpeg" width="100%" alt="">
											</a>
										</div>
										<div class="item">
											<a href="assets/images/car-slide-02.jpeg" data-src="assets/images/car-slide-02.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-02.jpeg"  width="100%" alt="">
											</a>
										</div>
										<div class="item">
											<a class="zoom-box" href="assets/images/car-slide-03.jpeg" data-image="assets/images/car-slide-03.jpeg" data-zoom-image="assets/images/car-slide-03.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-03.jpeg"  width="100%" alt="">
											</a>
										</div>
										<div class="item">
											<a class="zoom-box" href="assets/images/car-slide-01.jpeg" data-image="assets/images/car-slide-01.jpeg" data-zoom-image="assets/images/car-slide-01.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-01.jpeg" width="100%" alt="">
											</a>
										</div>
										<div class="item">
											<a class="zoom-box" href="assets/images/car-slide-02.jpeg" data-image="assets/images/car-slide-02.jpeg" data-zoom-image="assets/images/car-slide-02.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-02.jpeg"  width="100%" alt="">
											</a>
										</div>
										<div class="item">
											<a class="zoom-box" href="assets/images/car-slide-03.jpeg" data-image="assets/images/car-slide-03.jpeg" data-zoom-image="assets/images/car-slide-03.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-03.jpeg"  width="100%" alt="">
											</a>
										</div>
										<div class="item">
											<a class="zoom-box" href="assets/images/car-slide-01.jpeg" data-image="assets/images/car-slide-01.jpeg" data-zoom-image="assets/images/car-slide-01.jpeg" data-fancybox="images">
											  <img src="assets/images/car-slide-01.jpeg" width="100%" alt="">
											</a>
										</div>
									</div>

									<div class="gallry-popup">
										<i class="fa-solid fa-arrow-up-right-and-arrow-down-left-from-center"></i>
									</div>
	                                <div class="vehicle_controls">
	                                    <ul>
	                                        <li>
	                                            <div><a href="#" class="btn waves-effect waves-light btn-sm btn-warning">Video</a></div>
	                                        </li>
	                                       
	                                    </ul>
	                                </div>
									
									<div class="mt-5 product-dec-slider">
										
										<div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-01.jpeg" width="100%" alt="">
											</div>
										</div>
										<div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-02.jpeg" width="100%" alt="">
											</div>
										</div>
										<div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-03.jpeg" width="100%" alt="">
											</div>
										</div>
										<div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-01.jpeg" width="100%" alt="">
											</div>
										</div>
										<div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-02.jpeg" width="100%" alt="">
											</div>
										</div>
										<div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-03.jpeg" width="100%" alt="">
											</div>
										</div>
	                                    <div class="item">
											<div class="s-sliderthumb">
												<img src="assets/images/car-slide-01.jpeg" width="100%" alt="">
											</div>
										</div>
									</div>
								</div>
							</div>

							<aside class="sidebar-right">
							<div class="SLetestnews sidebar-box">
								<h3 class="sidebar-title">Next Vehicle</h3>
								<ul>
									 <?php
										for ($x = 0; $x <= 10; $x++) {?>
										<li>
											<div class="cardImage">
												<a href="javascript:void(0)" data-toggle="modal" data-target="#PreBidModal" class="red" title="Toyota Innova Crysta"><img src="assets/images/ac3.jpg" width="100%" alt="">
													<span> 130 min </span></a>
											</div>
											<div class="sidebar-newstext">
												<a href="javascript:void(0)" data-toggle="modal" data-target="#PreBidModal" class="red" title="Toyota Innova Crysta">2006 AUDI A6 3.2...</a>
												<p><span>Stock#:</span> <b>DCB999912</b></p>
												<p><span>Current Bid:</span> <b class="red">600</b></p>
												<p><span>VIN:</span> <b>WBAUC9C55CVM1</b></p>

											</div>
										</li>

									 <?php }?>

								</ul>
							</div>
							</aside>
							
						</div>
						<div class="col-lg-3">
							<div class="rows">
	                            <h5 class="text-start mb-0 pt-0 pb-5 px-0">1998 Nissan Atlima</h5>
	                            <div class="bidinfo mb-15">
									<h3 class="sidebar-title">Bid Information</h3>
									<div class="detail-info-box box px-0 py-0">
										
										<div role="progressbar"  aria-valuemin="0" aria-valuemax="100" style="--value:65">
											<div class="rounded-bid">
												<p class="mb-2"><img  width="22px" src="assets/images/united-states-flag-icon.png"/></p>
												<span>New jers..</span>
												<h5>$81,500</h5>
												<p>Bid</p>
											</div>
											
										</div>
										<p class="text-center mb-0"><b>All Bids in USD.</b></p>
										<p class="mb-10 text-center">You are not eligible to bid on this lot. </p>
										<table width="100%" class="">
											<!--<tr>
												<td valign="top"><span>Status:</span> </td>
												<td class="current-bid">
													<h5 class="mb-0"><span class="badge btn-warning btn">Going Once</span>  4 <button onclick="startstop();"><i class="fa-sharp fa-solid fa-volume-slash"></i></button><audio id="audio" src="assets/images/audio.mp3"></audio><br></h5>
												</td>
											</tr>-->
											<tr>
												<td><span>Current Bid:</span> </td>
												<td><button onclick="startstop();"><i class="fa-sharp fa-solid fa-volume-slash"></i></button><audio id="audio" src="assets/images/audio.mp3"></audio> <b>$1800.00</b> </td>
											</tr>
											<tr>
												<td><span>Asking Bid:</span> </td>
												<td><b class="text-danger">$1900.00</b></td>
											</tr>
											<tr>
												<td colspan="2">
													<p class="mt-5 bid-btn mb-5">
														<a href="javascript:void(0)" class="btn waves-effect waves-light  btn-sm btn-danger">$1900.00</a>
	                                                </p>
	                                                <p class="mt-5 mb-5 text-start">
	                                                    <label for="maxBidAmount" class="form-label m-0">Max Bid Amount</label>
	                                                    <input type="text" class="form-control ui-autocomplete-input" id="maxBidAmount" autocomplete="off">
	                                                </p>
	                                                <p class="mt-10">
	                                                    <a href="javascript:void(0)" class="theme-btn d-inline-block">Place Max Bid</a>
	                                                </p>
												</td>
											</tr>
										</table>
										
										<div class="prev-bids-list SLetestnews">
											<h5>Previous Bids</h5>
											<ul>			
												<li>
													<!--<div class="bidsImage">
														<img  width="40px" src="assets/images/united-states-flag-icon.png"/>
													</div>-->
													<div class="prevbids-next">
														<!--<a class="red" title="" href="#">New Jersey</a>-->
														<p>$80,500</p>
													</div>
												</li>
												<li>	
													<!--<div class="bidsImage">
														<img  width="40px" src="assets/images/united-states-flag-icon.png"/>
													</div>-->
													<div class="prevbids-next">
														<!--<a class="red" title="" href="#">New Jersey</a>-->
														<p>$30,500</p>
													</div>
												</li>
												<li>	
													<!--<div class="bidsImage">
														<img  width="40px" src="assets/images/united-states-flag-icon.png"/>
													</div>-->
													<div class="prevbids-next">
														<!--<a class="red" title="" href="#">New Jersey</a>-->
														<p>$50,500</p>
													</div>
												</li>
											</ul>
										</div>
									</div>
								</div>
							
							</div>
						</div>
						<div class="col-lg-3">
							<div class="bidinfo mb-15">
									<h3 class="sidebar-title">Vehicle Information</h3>
									<div class="detail-info-box px-0 py-0">
									<table width="100%" class="table table-striped">
											<tr>
											  <td><span>Run#:</span> </td>
												<td><b>156</b></td>
											</tr>
											<tr>
											  <td><span>Stock#:</span> </td>
												<td><b>DCB999912</b></td>
											</tr>
											<tr>
											  <td ><span>VIN:</span> </td>
											  <td><b>JH4CL96856C020398</b></td>
											</tr>
											<tr>
												<td><span>Drive:</span> </td>
												<td><b>2WD</b></td>
											</tr>
											<tr>
												<td><span>Odo:</span> </td>
												<td><b>248745</b> </td>
											</tr>
											<tr>
												<td><span>Engine:</span> </td>
												<td><b>2.4L L4 DOHC 16v</b></td>
											</tr>
											<tr>
												<td><span>Transmission:</span> </td>
												<td><b>Automatic</b></td>
											</tr>
											<tr>
												<td><span>Int Type:</span> </td>
												<td><b>Leather</b></td>
											</tr>
										</table>
									</div>
								</div>
							<div class="bidinfo mb-15 mt-15">
									<h3 class="sidebar-title">Auction Announcements</h3>
									<div class="detail-info-box">
										<p>Vehicle Sold as-is, Charity Donated Vehicle, There Will Be an $95 Surcharge Applied to the Purchase Price, Please Note All Visible Defects in the Photos Are an Extension of Written Condition Report</p>

										<p>Buyer Agrees to Check for Outstanding Recalls on the Sale Vehicle, and to Contact Either Their Local Dealership or Use the National Highway Traffic Safety Administration’s (Nhtsa) Website to Check the Vehicle’s Recall Status.</p>
									</div>
								</div>
						</div>
						<div class="col-lg-3">
								<div class="bidinfo mb-25">
									<h3 class="sidebar-title">Condition Report</h3>
									<div class="detail-info-box px-0 py-0">
										<table width="100%" class="table">
	                                        <tr>
	                                            <th style="--bs-table-accent-bg: #f2f2f2;" colspan="2">Interior</th>
	                                        </tr>
	                                        <tr>
	                                            <td width="20%"><span>Sunroof</span> </td>
	                                            <td><b>Yes, id sunroof is present. Disclose if it is aftermarket </b></td>
	                                        </tr>
	                                        <tr>
	                                            <td><span>Navigation</span> </td>
	                                            <td><b>Yes, is factory navigation without device paired or no subscription</b></td>
	                                        </tr>
	                                        <tr>
	                                            <th style="--bs-table-accent-bg: #f2f2f2;" colspan="2">Exterior</th>
	                                        </tr>
	                                        <tr>
	                                            <td width="20%"><span>Mismatched paint colors</span> </td>
	                                            <td><b>Adjavent panels have noticeable mistint form improper paint matching during</b></td>
	                                        </tr>
	                                        <tr>
	                                            <td width="20%"><span>Paint meter readings</span> </td>
	                                            <td><b>Indicate high and low paint meter readings</b></td>
	                                        </tr>
	                                        <tr>
	                                            <th style="--bs-table-accent-bg: #f2f2f2;" colspan="2">Mechanicals</th>
	                                        </tr>
	                                        <tr>
	                                            <td width="20%"><span>Jump start required</span> </td>
	                                            <td><b>Turns on with application of outside power source</b></td>
	                                        </tr>
	                                    </table>
									</div>
								</div>
						</div>
					</div>
				</div>
				
				<div class="rightpart">		
					
				
				</div>
			</div>
          
			
        </div>
    </section>
		
	 <!-- about section  start -->
	   
	   <div class="popular-section">
	   		<div class="container container-full">
               <div class="row">
				   <div class="tp-section__title-wrapper mb-15 text-left">
					   <h2 class="tp-section__title">View Similar Vehicles</h2>
				   </div>
                   <div class="popular-slider">
				   	   <div class="slider-box">
					   	   <div class="popular-img">
						   		<img src="assets/images/slide-01.jpg" alt="">
							   
						   </div>
						   <div class="popular-text">
						   	   <h3>2014 BMW 535 XI</h3>
							   <p>1,500 kms • Diesel • Automatic</p>
							   <p>Location: IL - CHICAGO SOUTH</p>
							   <div class="usd">$300.00 </div>
							    <a href="#" class="theme-btn">View Details</a>
						   </div>
					   </div>
					   <div class="slider-box">
					   	   <div class="popular-img">
						   		<img src="assets/images/slide-02.jpg" alt="">
							    <div class="button-list">
								  <a href="#" class="theme-btn">Bid</a>
							    </div>
						   </div>
						   <div class="popular-text">
						   	   <h3>2014 JEEP GRAND SRT-8</h3>
							   <p>1,400 kms • Diesel • Automatic</p>
							   <p>Location: IL - WHEELING</p>
							   <div class="usd">$500.00 </div>
							   <a href="#" class="theme-btn">View Details</a>
						   </div>
					   </div>	
					   <div class="slider-box">
					   	   <div class="popular-img">
						   		<img src="assets/images/slide-03.jpg" alt="">
							   
						   </div>
						   <div class="popular-text">
						   	   <h3>2014 TOYOTA PRIUS</h3>
							   <p>1,500 kms • Diesel • Automatic</p>
							   <p>Location: IL - CHICAGO SOUTH</p>
							   <div class="usd">$300.00 </div>
							   <a href="#" class="theme-btn">View Details</a>
						   </div>
					   </div>	
					   <div class="slider-box">
					   	   <div class="popular-img">
						   		<img src="assets/images/slide-01.jpg" alt="">
						   </div>
						   <div class="popular-text">
						   	   <h3>2014 TOYOTA CAMRY L</h3>
							   <p>1,500 kms • Diesel • Automatic</p>
							   <p>Location: IL - CHICAGO SOUTH</p>
							   <div class="usd">$100.00 </div>
							    <a href="#" class="theme-btn">View Details</a>
						   </div>
					   </div>	
					   <div class="slider-box">
					   	   <div class="popular-img">
						   		<img src="assets/images/slide-02.jpg" alt="">
							    
						   </div>
						   <div class="popular-text">
						   	   <h3>2014 BMW 535 XI</h3>
							   <p>1,500 kms • Diesel • Automatic</p>
							   <p>Location: IL - CHICAGO SOUTH</p>
							   <div class="usd">$300.00 </div>
							    <a href="#" class="theme-btn">View Details</a>
						   </div>
					   </div>
					   <div class="slider-box">
					   	   <div class="popular-img">
						   		<img src="assets/images/slide-03.jpg" alt="">
							  
						   </div>
						   <div class="popular-text">
						   	   <h3>2014 JEEP GRAND SRT-8</h3>
							   <p>1,400 kms • Diesel • Automatic</p>
							   <p>Location: IL - WHEELING</p>
							   <div class="usd">$500.00 </div>
							    <a href="#" class="theme-btn">View Details</a>
						   </div>
					   </div>
				   </div>
				</div>
		   </div>
	   </div>
      
      <!-- about section end  -->
<div id="PreBidModal" class="modal fade bs-example-modal-lg PreBidModal" tabindex="-1" role="dialog" aria-labelledby="PreBidModalLabel" aria-hidden="true" style="display: none;">
  <div class="modal-dialog ">
    <div class="modal-content">
		  <div class="modal-header">
			<h5 class="modal-title" id="exampleModalLongTitle">Pre/Max Bid</h5>
			<button type="button" class="btn-close" data-dismiss="modal"></button>
		  </div>
		  <div class="modal-body">
			  <!--<p style="line-height:normal">Enter a bid amount below to get an estimated final cost for this vehicle.</p>-->
                <form class="">
                    <div class="SLetestnews">
                        <ul>	 							
                            <li style="list-style: none;padding: 0;">
                                <div class="cardImage">
                                    <img src="assets/images/ac3.jpg" width="100%" alt="">
                                </div>
                                <div class="sidebar-newstext">
                                    <table style="width: 100%;" cols>
                                        <tbody>
                                            <tr>
                                                <td>Auction Name:</td>
                                                <td><a href="javascript:void(0)" class="red" title="Toyota Innova Crysta">2014 TOYOTA CAMRY</a></td>
                                            </tr>
                                            <tr>
                                                <td>Auction Date:</td>
                                                <td>Tue. Feb 07, 2023 11:30 PM IST</td>
                                            </tr>
                                            <tr>
                                                <td>Stock#:</td>
                                                <td>DCB999912</td>
                                            </tr>
                                            <tr>
                                                <td>VIN:</td>
                                                <td>WBAUC9C55CVM1</td>
                                            </tr>
                                            <tr>
                                                <td>Buy Now Price:</td>
                                                <td>$4,000.00</td>
                                            </tr>
                                            <tr>
                                                <td>Current Bid:</td>
                                                <td>$600.00</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div class="d-flex flex-wrap gap-3 mb-3">
                        <div class="form-check">
                          <input id="checkbox_pre" class="form-check-input" type="radio" name="hidden" value="Individual" checked="">
                          <label class="form-check-label" for="checkbox_pre">
                            Pre Bid Amount
                          </label>
                        </div>
                        <div class="form-check">
                          <input id="checkbox_max" class="form-check-input" type="radio" name="hidden" value="Individual" checked="">
                          <label class="form-check-label" for="checkbox_max">
                            Max Bid Amount
                          </label>
                        </div>
                    </div>
                    
                    <div class="col-md-12 mb-1">
                        <label for="preBidAmount" class="form-label">Bid Amount</label>
                        <input type="text" class="form-control" id="preBidAmount">
                    </div>
                </form>
			  
		  </div>
          <div class="modal-footer">
			  <a href="#" class="theme-btn">Place Bid</a>
		  </div>
	</div>
  </div>
</div>
 
    
 </main>

    <?php include 'footer.php' ?>

<style>

	.tp-header__area .tp-header__main {
		display: none;
	}
	.logo img {
		width: 100px;
		height: auto;
	}
	.tp-header__area{
		padding: 5px 0px;
	}
</style>



<!--<script src="assets/js/jquery.jqZoom.js"></script>
<link rel="stylesheet" href="assets/css/jquery.jqZoom.css">
<script>
    $(window).on('load',function(){
        console.log('in load');
        $(".slider-for .zoom-box img").jqZoom({
            selectorWidth: 30,
            selectorHeight: 30,
            viewerWidth: 500,
            viewerHeight: 400
        });

    })
</script>
<style>
    .slider-for .slick-track .item, .slider-for .slick-list{
        overflow:visible;
    }
    .car-details{
        z-index: 9;
        position: relative;
    }
</style>-->