$(document).ready(function () {
    $("#btn-predict").click(function (event) {
        $.ajax({
            type: "POST",
            url: "/home_ajax",
            contentType: 'application/json',
            dataType: "json",
            data: JSON.stringify({
                "content_raw": $("#text-content").val()
            }),
            success: function (resp) {
                $("#content-clean").empty();
                $("#content-clean").append("<b>Content Clean: </b>" + " " + resp.content_clean);

                var text = ""
                for (const [key, value] of Object.entries(resp.result)) {
                    text += "<b>Nhánh:</b> " + String(key) + "<br/>"
                    text += "<b>Xác suất:</b> " + String(value) + "<br/><br/>"
                }
                $("#predict-result").empty();
                $("#predict-result").append(text);

                // output_chart
                var text_image = "<img src=\""
                var path_image = "/static/output_chart/" + resp.image_name
                console.log(path_image)
                text_image += path_image + "\" width=\"480\" height=\"360\">"
                console.log(text_image)
                $("#image-result").empty()
                $("#image-result").append(text_image)
            },
            error: function (err) {
                console.log(err);
            }
        })
    });
})
;
