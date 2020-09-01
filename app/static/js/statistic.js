$(document).ready(function () {
    $("#btn-search-process").click(function (event) {
        $.ajax({
            type: "POST",
            url: "/statistic_ajax",
            contentType: 'application/json',
            dataType: "json",
            //pass input to routes /statistic_ajax
            data: JSON.stringify({
                // "# ==> id
                "hidden_file_name_output": $("#hidden-input").val(),
                "id_user": $("#text-id-user").val()
            }),


            //success --> receive from routes /statistic_ajax
            success: function (resp) {
                // content-clean --> received from routes /statistic_ajax
                var text_status = resp.status
                $("#text-status").empty();
                $("#text-status").append(text_status);

                if (text_status == "success") {
                    var text_image = "<img src=\""
                    var path_image = "/static/output_chart/output_prob_each_user/" + resp.image_name
                    console.log(path_image)
                    text_image += path_image + "\" width=\"480\" height=\"360\">"
                    console.log(text_image)
                    $("#image-each-user").empty()
                    $("#image-each-user").append(text_image)
                }
            },
            error: function (err) {
                console.log(err);
            }
        })
    });
});
