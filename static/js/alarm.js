/**
 * Created by lenovo on 2016/6/4.
 */

alarm_css = new Array();

alarm_css[0] = "success";
alarm_css[1] = "error";
alarm_css[2] = "warning";
alarm_css[3] = "default";

alarm_string = new Array();

alarm_string[0] = "未分配处理人";
alarm_string[1] = "未处理";
alarm_string[2] = "处理中";
alarm_string[3] = "处理完成";


function get_alarm_list_refresh(index) {

    get_alarm_list(index, function (data) {
        var result = JSON.parse(data);
        console.log(result);
        if (result.result == "error") {
            console.log("获取告警列表失败")
        }
        else {
            //显示表信息
            $("#alarm_table tbody").empty();
            for (var i = 0; i < result.data.length; i++) {

                $("#alarm_table tbody").append("<tr class='" + alarm_css[result.data[i].deal_progress] + "'> <td>" + result.data[i].id +
                    "</td> <td>" + result.data[i].alarm_level + "</td> <td>" + result.data[i].create_time +
                    "</td> <td>" + result.data[i].alarm_obj + "</td> <td>" + result.data[i].alarm_content +
                    "</td> <td>" + result.data[i].alarm_custumer + "</td colspan='6'> </tr>")
            }

            $('#alarm_table tbody tr').each(function () {
                $(this).click(function (e) {
                    console.log("click alarm tr " + ($(this).text()).split(" ")[1]);
                    //用户详情信息写入
                    get_alarm($(this).text().split(" ")[1], function (data) {
                        var result = JSON.parse(data);
                        console.log(result);
                        if (result.result == "error") {
                            console.log("获取告警失败")
                        }
                        else {
                            $("#deal_progress").text("当前状态：" + alarm_string[result.data.deal_progress]);
                            $("#modal_alarm_table tbody").empty();
                            $("#modal_alarm_table tbody").append("<tr class='default'> <td>" + result.data.id +
                                "</td> <td>" + result.data.alarm_level + "</td> <td>" + result.data.create_time +
                                "</td> <td>" + result.data.alarm_obj + "</td> <td>" + result.data.alarm_content +
                                "</td></tr>");
                            get_custumer(result.data.alarm_custumer, function (data) {
                                var result = JSON.parse(data);
                                console.log(result);
                                if (result.result == "error") {
                                    console.log("获取用户失败")
                                }
                                else {
                                    //设置主人电话
                                    $("#custumer_telephone").text(result.data.custumertelephone)
                                    //设置其他相关成员电话
                                    //处理other信息
                                    $("#alarm_table_other tbody").empty();
                                    for (var i = 0; i < result.data.other.length; i++) {
                                        insert_to_alarm_other_table(result.data.other[i])
                                    }
                                }
                            });
                        }
                    });
                    $("#alarm_detail").trigger("click")

                })
            });

            //显示分页条
            split_page("alarm", result, get_alarm_list_refresh);

        }

    })

}

function insert_to_alarm_other_table(data) {
    $("#alarm_table_other tbody").last().append("< class='default'><tr><td><input type='text'class='input-mini' disabled value='" + data.name +
        "'/></td> <td> <input type='text'class='input-mini' disabled value='" + data.token + "'/></td> <td><a href='#' class='btn btn-mini'>" + data.famliyphone +
        "</a></td> <td><a href='#' class='btn btn-mini'>" + data.workphone + "</a></td> <td><a href='#' class='btn btn-mini'>" + data.telphone +
        "</a></td>/tr>")
}

