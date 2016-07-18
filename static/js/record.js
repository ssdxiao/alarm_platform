/**
 * Created by lenovo on 2016/6/4.
 */
function get_record_list_refresh(index) {

    get_record_list(index, function (data) {
        var result = JSON.parse(data);
        console.log(result);
        if (result.result == "error") {
            console.log("获取日志列表失败")
        }
        else {
            //显示表信息
            $("#record_table tbody").empty();
            for (var i = 0; i < result.data.length; i++) {
                $("#record_table tbody").append("<tr class='default'> <td>" + result.data[i].id +
                    "</td> <td>" + result.data[i].user + "</td> <td>" + result.data[i].object +
                     "</td> <td>" + result.data[i].context+"</td> <td>" + result.data[i].time + "</td> </tr>")
            }

           

            //显示分页条
           split_page("record", result, get_record_list_refresh);
        }

    })

}


