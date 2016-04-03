$(function ()
{
    x = 'Search';
    //Setting Default Pill

    //Calling search function on Pill Change
    $('.nav-pills a').on('shown.bs.tab', function (event)
    {
        x = $(event.target).text();
        $('#activeTab').val(x);
        post(x);
    });
    //Calling search function on keyup for instant results
    $('#searchQ').keyup(function ()
    {
        post($('#activeTab').val());
    });
    //Search post Function
    function post(x)
    {	
    	//AJAX post to Flask to return Search queries, run a loop to parse queries and render the Did you mean
        if (x == 'Search' || x == "")
        {
        	//Clearing Suggestions
            $('#Suggestions').html("");
            var search = $('#searchQ').val();
            $.ajax(
            {
                url: '/search',
                data: $('form').serialize(),
                type: 'POST',
                success: function (response)
                {
                    $('#Search').html("");
                    var resp = $.parseJSON(response);
                    var arr = resp['search'];
                    for (var i = 0; i < arr.length - 1; i++)
                    {
                        var result = "<div class='result'>"
                        result += "<div class='resultTitle'>" + arr[i][0] + "</div>";
                        result += "<div class='resultLink'>" + "<a href='" + arr[i][1] + "'>" + arr[i][1] + "</a></div>";
                        result += "<div class='resultContent'>" + arr[i][2] + "</div>";
                        result += "</div>"
                        $('#Search').append("<div>" + result + "</div>");
                    }
                    if (arr[i][0] == 1) $('#Suggestions').html("No results for this. Did You Mean: <b>" + arr[i][1] + "</b>");
                    else $('#Suggestions').html("");
                    //Clearing other results
                    $('#Document').html("");
                    $('#Image').html("");
                },
                error: function (error)
                {
                    console.log(error);
                }
            });
        }
        else if (x == 'Document')
        {
            $('#Suggestions').html("");
            var search = $('#searchQ').val();
            $.ajax(
            {
                url: '/search',
                data: $('form').serialize(),
                type: 'POST',
                success: function (response)
                {
                    $('#Document').html("");
                    var resp = $.parseJSON(response);
                    var arr = resp['search'];
                    for (var i = 0; i < arr.length - 1; i++)
                    {
                        var result = "<div class='result'>"
                        result += "<div class='resultTitle'>" + arr[i][0] + "</div>";
                        result += "<div class='resultLink'>" + "<a href='" + arr[i][1] + "'>" + arr[i][1] + "</a></div>";
                        result += "<div class='resultContent'>" + arr[i][2] + "</div>";
                        result += "</div>"
                        $('#Document').append("<div>" + result + "</div>");
                    }
                    if (arr[i][0] == 1) $('#Suggestions').html("No results for this. Did You Mean: <b>" + arr[i][1] + "</b>");
                    else $('#Suggestions').html("");
                    $('#Search').html("");
                    $('#Image').html("");
                },
                error: function (error)
                {
                    console.log(error);
                }
            });
        }
        else if (x == 'Image')
        {
            $('#Suggestions').html("");
            var search = $('#searchQ').val();
            $.ajax(
            {
                url: '/search',
                data: $('form').serialize(),
                type: 'POST',
                success: function (response)
                {
                    $('#Image').html("");
                    var resp = $.parseJSON(response);
                    var arr = resp['search'];
                    for (var i = 0; i < arr.length; i++)
                    {
                        var result = "<div class='result'>"
                        result += "<div class='resultTitle'>" + arr[i][0] + "</div>";
                        result += "<div class='resultLink'>" + "<a href='" + arr[i][1] + "'>" + arr[i][1] + "</a></div>";
                        result += "<div class='resultImage'>" + "<img src='" + arr[i][2] + "'>" + "</div>";
                        result += "</div>"
                        $('#Image').append("<div>" + result + "</div>");
                    }
                    if (arr.length == 0 && $('#searchQ').val() != "") $('#Suggestions').html("No results found.");
                    else $("#Suggestions").html("");
                    $('#Document').html("");
                    $('#Search').html("");
                },
                error: function (error)
                {
                    console.log(error);
                }
            });
        }
    }
});