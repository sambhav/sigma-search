$(function ()
{
    $('#upload-file-btn').click(function ()
    {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax(
        {
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function (response)
            {
                $('#Output').html("");
                var resp = $.parseJSON(response);
                var arr = resp['search'];
                console.log(response)
                for (var i = 0; i < arr.length; i++)
                {
                    var result = "<div class='result'>"
                    result += "<div class='resultTitle'>" + arr[i][0] + "</div>";
                    result += "<div class='resultLink'>" + "<a href='" + arr[i][1] + "'>" + arr[i][1] + "</a></div>";
                    result += "<div class='resultImage'>" + "<img src='" + arr[i][2] + "'>" + "</div>";
                    result += "</div>"
                    $('#Output').append("<div>" + result + "</div>");
                }
                if (arr.length == 0)
                    $('#Output').html("No Result Found.")
            },
            error: function (error)
            {
                console.log(error);
            }
        });
    });
});