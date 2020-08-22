(function ($, document, window) {

    $(document).ready(function () {

        // Cloning main navigation for mobile menu
        $(".mobile-navigation").append($(".main-navigation .menu").clone());

        // Mobile menu toggle
        $(".menu-toggle").click(function () {
            $(".mobile-navigation").slideToggle();
        });

        $(".find-location").submit(function (e) {
            e.preventDefault();
            let city_id = $("#id_city_value").val();
            let language = $("#id_request_language").val();
            $.ajax({
                type: "GET",
                url: "/api/v1/weather/" + city_id + "/",
                data: {
                    language: language
                },
                success: function (response) {
                    $("#id_location").text(response.city);
                    $("#id_degree").text(response.temperature.average);
                    $("#weather_description .weather_description_title").text(response.description);
                    $("#weather_description .weather_description_min_temp span").text(response.temperature.min);
                    $("#weather_description .weather_description_max_temp span").text(response.temperature.max);
                    $("#id_humidity").text(response.humidity);
                    $("#id_wind_speed").text(response.wind.speed);
                    $("#id_wind_direction").text(response.wind.direction);
                    $("#id_pressure").text(response.pressure);
                    $(".weather-placeholder-text").hide();
                    $(".weather-data").show();
                },
                error: function (response) {
                    $("#id_error").text(response.responseJSON.error).show();
                }
            });
        });

        $('#id_language').on('change', function () {
            var url = $(this).val(); // get selected value
            if (url) { // require a URL
                window.location = url; // redirect
            }
            return false;
        });

        $("#id_city").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/api/v1/cities/",
                    dataType: "json",
                    data: {
                        query: $('#id_city').val()
                    },
                    success: function (data) {
                        let formattedData = $.map(data, function (objet) {
                            return {
                                label: objet.name,
                                value: objet.id
                            };
                        });
                        response(formattedData);
                    },
                    error: function (message) {
                        response([]);
                    }
                });
            },
            appendTo: $(".auto-complete"),
            minLength: 3,
            delay: 500,
            select: function (event, ui) {
                $(' #id_city ').val(ui.item.label);
                $(' #id_city_value ').val(ui.item.value);
                return false;
            },
            messages: {
                noResults: '',
                results: function () {
                }
            }
        }).data( "autocomplete" )._renderItem = function( ul, item ) {
            return $("<li></li>")
                .data("item.autocomplete", item)
                .append('<a href="'+ item.link +'">'+ item.value +'</a>')
                .appendTo($('.auto-complete'));
            };

    });

    $(window).load(function () {
    });

})(jQuery, document, window);