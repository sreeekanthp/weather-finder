(function($, document, window){
	
	$(document).ready(function(){

		// Cloning main navigation for mobile menu
		$(".mobile-navigation").append($(".main-navigation .menu").clone());

		// Mobile menu toggle 
		$(".menu-toggle").click(function(){
			$(".mobile-navigation").slideToggle();
		});

		$(".find-location").submit(function (e) {
			e.preventDefault();
			let city_id = $("#id_city").val();
			$.ajax({
				type: "GET",
				url: "/api/v1/weather/" + city_id + "/",
				success: function (response) {
					$("#id_location").text(response.city);
					$("#id_degree").text(response.temperature.average);
					$("#id_description").text(response.description);
					$("#id_min_temperature").text(response.temperature.min);
					$("#id_max_temperature").text(response.temperature.max);
					$("#id_humidity").text(response.humidity);
					$("#id_wind_speed").text(response.wind.speed);
					$("#id_wind_direction").text(response.wind.direction);
					$("#id_pressure").text(response.pressure);
				},
				error: function (response) {
					$("#id_error").text(response.responseJSON.error);
				}
			});
		});
	});

	$(window).load(function(){
	});

})(jQuery, document, window);