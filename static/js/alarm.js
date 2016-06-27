/**
 * Created by lenovo on 2016/6/4.
 */

alarm_css = new Array();

alarm_css[3] = "success"; //他人未处理
alarm_css[0] = "error"; //未处理
alarm_css[1] = "warning";//已处理，未完成
alarm_css[2] = "default"; //已完成

alarm_string = new Array();

alarm_string[0] = "未处理";
alarm_string[1] = "处理中";
alarm_string[2] = "处理完成";


function get_alarm_list_refresh(index) {

    get_alarm_list(index, function (data) {
        var result = JSON.parse(data);
        console.log(result);
        if (result.result == "error") {
            console.log("获取告警列表失败")
            return
        }
        else {
            //显示表信息
            $("#alarm_table tbody").empty()
            var deal_progress_css;
            for (var i = 0; i < result.data.length; i++) {
                console.log(result.data[i].deal_user)
                if (result.data[i].deal_user == get_userid()  )
                {
                    deal_progress_css = result.data[i].deal_progress
                }
                else
                {
                    deal_progress_css = 3
                }


                $("#alarm_table tbody").append("<tr class='" + alarm_css[deal_progress_css] + "'> <td>" + result.data[i].id +
                    "</td> <td>" + result.data[i].alarm_level + "</td> <td>" + result.data[i].create_time +
                    "</td> <td>" + result.data[i].alarm_obj + "</td> <td>" + result.data[i].alarm_content +
                    "</td> <td>" + result.data[i].deal_user + "</td colspan='6'> </tr>")
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
                                $("#deal_progress").text( alarm_string[result.data.deal_progress] );
                                $("#deal_user").text(result.data.deal_user)

                                $("#modal_alarm_table tbody").empty();
                                $("#modal_alarm_table tbody").append("<tr class='default'> <td id='td_alarm_id'>" + result.data.id +
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
                                            $("#custumerRemark").text(result.data.custumerremark)
                                            //设置其他相关成员电话
                                            //处理other信息
                                            $("#alarm_table_other tbody").empty();
                                            for (var i = 0; i < result.data.other.length; i++) {
                                                insert_to_alarm_other_table(result.data.other[i])
                                            }

                                            //处理记录
                                            get_audio_list($("#td_alarm_id").text(), function (data) {
                                                var result = JSON.parse(data);
                                                console.log(result);
                                                if (result.result == "error") {
                                                    console.log("获取告警处理记录失败")
                                                } else {
                                                    $("#alarm_deal_progress_table tbody").empty()
                                                    for (var i = 0; i < result.data.length; i++) {
                                                        $("#alarm_deal_progress_table tbody").append("<tr class='default'> <td>" + result.data[i][2] +
                                                            "</td> <td>" + result.data[i][3] + "</td> <td>" + result.data[i][4]  + "</td> <td>"+ result.data[i][5]  + "</td> <td>" + result.data[i][6] +"</td> </tr>")
                                                    }
                                                }
                                            })

                                        }
                                    })


                                $("#alarm_detail").trigger("click")
                            }

                        });
                    });


                })

             //显示分页条
            split_page("alarm", result, get_alarm_list_refresh);

        }

    })

}

function insert_to_alarm_other_table(data) {
    $("#alarm_table_other tbody").last().append("< class='default'><tr><td><input type='text'class='input-mini' disabled value='" + data.name +
        "'/></td> <td> <input type='text'class='input-mini' disabled value='" + data.token + "'/></td> <td><a href=javascript:void(0); onclick=callup(event);return false; class='btn btn-mini'>" + data.famliyphone +
        "</a></td> <td><a href=avascript:void(0); onclick=callup(event);return false; class='btn btn-mini'>" + data.workphone + "</a></td> <td><a href=avascript:void(0); onclick=callup(event);return false; class='btn btn-mini'>" + data.telphone +
        "</a></td>/tr>")
}

