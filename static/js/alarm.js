/**
 * Created by lenovo on 2016/6/4.
 */

alarm_css = new Array();

alarm_css[3] = "warning"; //他人未处理
alarm_css[0] = "error"; //未处理
alarm_css[1] = "success";//已处理，未完成
alarm_css[2] = "default"; //已完成



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
                if (result.data[i].deal_progress != 2) {
                    if (result.data[i].deal_user == get_userid()) {
                        deal_progress_css = result.data[i].deal_progress
                    }
                    else {
                        deal_progress_css = 3
                    }
                }
                else{
                    deal_progress_css = 2
                }


                $("#alarm_table tbody").append("<tr class='" + alarm_css[deal_progress_css] + "'> <td>" + result.data[i].id +
                    "</td> <td>" + result.data[i].create_time +
                        "</td> <td>" + result.data[i].deal_context +
                    "</td> <td>" + alarm_string[deal_progress_css] +
                    "</td> <td>" + result.data[i].deal_user_name + "</td colspan='4'> </tr>")
            }


            $('#alarm_table tbody tr').each(function () {
                $(this).click(function (e) {
                    console.log("click alarm tr " + ($(this).text()).split(" ")[1]);
                    //用户详情信息写入

                            fresh_alarm_modal($(this).text().split(" ")[1])
                            $("#alarm_detail").trigger("click")

                });


            })

            //显示分页条
            split_page("alarm", result, get_alarm_list_refresh);

        }

    })

}

function fresh_alarm_modal(alarmid){
                    //清理痕迹
                            $("#modal_alarm_table tbody").empty();
                            $("#alarm_deal_progress_table tbody").empty();
                            $("#alarm_table_other tbody").empty();
                                    $("#custumer_telephone").text("")
                                    $("#custumerName").text("")
                                    $("#custumerAddress").text("")
                                    $("#custumerRemark").text("")

                    get_alarm(alarmid, function (data) {
                        var result = JSON.parse(data);
                        console.log(result);
                        if (result.result == "error") {
                            console.log("获取告警失败")
                        }
                        else {
                            $("#deal_progress").text(alarm_string[result.data.deal_progress]);
                            if(result.data.deal_progress == 2)
                            {
                    $("#deal_alarm_ok").attr("class","btn");
                    $("#deal_alarm_ok").attr("disabled", "true");
                            }
                            else
                            {
                    $("#deal_alarm_ok").removeAttr("disabled");
                    $("#deal_alarm_ok").attr("class","btn btn-success");
                            }
                            $("#deal_user").text(result.data.deal_user)
                            $("#td_alarm_id").text(result.data.id)
                            $("#alarm_device").text(result.data.deviceid)

                            $("#modal_alarm_table tbody").empty();
                            get_event_list(result.data.id, function(data) {
                                var result = JSON.parse(data);
                                console.log(result);
                                if (result.result == "error") {
                                    console.log("获取告警失败")
                                } else {

                                for (var i = 0; i < result.data.length; i++) {
                                $("#modal_alarm_table tbody").append("<tr class='default'> <td >" + result.data[i].id +
                                    "</td> <td>" + result.data[i].type + "</td> <td>" + result.data[i].eventtime +
                                    "</td> <td>" + result.data[i].context +
                                    "</td></tr>");
                                }
                            }})
                            get_custumer(result.data.deviceid, function (data) {
                                var result = JSON.parse(data);
                                console.log(result);
                                if (result.result == "error") {
                                    console.log("获取用户失败")
                                }
                                else {
                                    //设置主人电话
                                    $("#custumer_telephone").text(result.data.custumertelephone)
                                    $("#custumerName").text(result.data.custumername)
                                    $("#custumerAddress").text(StateList[result.data.state] + " " + State[result.data.state][result.data.city]+ " "+ result.data.street)
                                    $("#custumerRemark").text(result.data.custumerremark)


                                    //设置其他相关成员电话
                                    //处理other信息
                                    $("#alarm_table_other tbody").empty();
                                    for (var i = 0; i < result.data.other.length; i++) {
                                        insert_to_alarm_other_table(result.data.other[i])
                                    }
                                    } })

                                    $("#alarm_deal_progress_table tbody").empty();
                                    //处理记录
                                    get_audio_list($("#td_alarm_id").text(), function (data) {
                                        var result = JSON.parse(data);
                                        console.log(result);
                                        if (result.result == "error") {
                                            console.log("获取告警处理记录失败")
                                        } else {
                                            var audio_dom
                                            for (var i = 0; i < result.data.length; i++) {
                                                if (result.data[i].has_audio == 1){
                                                    audio_dom ="<div><audio type='audio/wav' src='/static/audio/"+result.data[i].audio+"'>您的浏览器不支持</audio>"+
                                                        "<a href=javascript:void(0); onclick=playAudio(event);return false; class='btn'>Play</a>"+result.data[i].audio+"</div>"
                                                }
                                                else
                                                {
                                                    audio_dom = "<a href=javascript:void(0); onclick=upload_model(event);return false; id= '"+result.data[i].audio+"'class='btn'>"+string_upload+"</a>" + result.data[i].audio
                                                }


                                                $("#alarm_deal_progress_table tbody").append("<tr class='default'> <td>" + result.data[i].deal_user +
                                                    "</td> <td>" + result.data[i].telephone+ "</td> <td>" + result.data[i].deal_time + "</td> <td><p>" + result.data[i].deal_remark + "</p></td> <td>" + audio_dom + "</td> </tr>")
                                            }
                                        }
                                    })


                        }
                    });

}

function insert_to_alarm_other_table(data) {
    $("#alarm_table_other tbody").last().append("< class='default'><tr><td><input type='text'class='btn' disabled value='" + data.name +
        "'/></td> <td> <input type='text'class='btn' disabled value='" + data.token + "'/></td> <td><a href=javascript:void(0); onclick=callup(event);return false; class='btn btn-mini'>" + data.famliyphone +
        "</a></td> <td><a href=avascript:void(0); onclick=callup(event);return false; class='btn btn-mini'>" + data.workphone + "</a></td> <td><a href=avascript:void(0); onclick=callup(event);return false; class='btn btn-mini'>" + data.telphone +
        "</a></td>/tr>")
}

